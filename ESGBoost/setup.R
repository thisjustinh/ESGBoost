library(shiny)
library(xgboost)
library(caret)
library(e1071)
library(tidyverse)


### Data CSVs & Vars ###

esgdata <- read.csv("https://raw.githubusercontent.com/xinging-birds/EchoSG/main/src/data/esgmodel.csv")
preprocessed <- read.csv("https://raw.githubusercontent.com/xinging-birds/EchoSG/main/src/data/preprocessed.csv")
master <- read.csv("https://raw.githubusercontent.com/xinging-birds/EchoSG/main/src/data/master.csv")
returns <- read.csv("https://raw.githubusercontent.com/xinging-birds/EchoSG/main/src/data/returns.csv")
# only used because I need tickers for clusters generated in R
cluster_tickers <- read.csv('https://raw.githubusercontent.com/xinging-birds/EchoSG/main/src/data/clusters.csv')

### k-means clustering ###

# optimal number of clusters
# sse = numeric()
# for (i in c(6:16)){
#   km.out <- kmeans(preprocessed, centers=i)
#   sse = c(sse, km.out$tot.withinss)
# }
# plot(sse)

### ESG Analysis Summary ###

# Averages
average.esg <- master %>%
  summarize(environmental=mean(environmental), 
            social=mean(social), 
            governance=mean(governance), 
            controversy=mean(controversy)) %>%
  pivot_longer(everything(), names_to="avg_key", values_to="avg_value")
average.education <- master %>%
  summarize(primary_school=mean(primary_school),
            high_school=mean(high_school),
            hs_diploma=mean(hs_diploma),
            some_college=mean(some_college),
            bsba=mean(bsba)) %>%
  pivot_longer(everything(), names_to="avg_key", values_to="avg_value")
average.income <- master %>%
  summarize(l15=mean(income_l15),
            b15_25=mean(income_15_25),
            b25_50=mean(income_25_50),
            b50_75=mean(income_50_75),
            p75=mean(income_p75)) %>%
  pivot_longer(everything(), names_to="avg_key", values_to="avg_value")
average.ejs <- master %>%
  summarize(pm25=mean(pm25),
            ozone=mean(ozone),
            nata_dieselpm=mean(nata_dieselpm),
            nata_cancerrisk=mean(nata_cancerrisk),
            traffic_prox=mean(traffic_prox),
            lead_paint=mean(lead_paint),
            rmp_prox=mean(rmp_prox),
            superfund_prox=mean(superfund_prox),
            hazardwaste_prox=mean(hazardwaste_prox),
            waterdischarge_prox=mean(waterdischarge_prox)) %>%
  pivot_longer(everything(), names_to="avg_key", values_to="avg_value")

# Gathered DFs
esg <- master %>%
  select(c(longName, environmental, social, governance, controversy)) %>%
  pivot_longer(c(environmental, social, governance, controversy), names_to="key", values_to="value")
education <- master %>%
  select(longName, primary_school, high_school, hs_diploma, some_college, bsba) %>%
  pivot_longer(!longName, names_to="key", values_to="value")
income <- master %>%
  select(longName, starts_with("income")) %>%
  pivot_longer(starts_with("income"), names_to="key", values_to="value")
ejs <- master %>%
  select(longName, pm25, ozone, nata_dieselpm, nata_cancerrisk, traffic_prox, lead_paint, rmp_prox, superfund_prox, hazardwaste_prox, waterdischarge_prox) %>%
  pivot_longer(!longName, names_to="key", values_to="value")


### Plot functions ###

# Clustering
clusterDataset <- function(x, y, k=16) {
  if (x == y) {
    return("x and y must be different.")
  }
  
  set.seed(1)
  km.out <- kmeans(preprocessed, centers=k)
  p <-preprocessed %>%
    # cbind(clusters$ticker) %>%
    ggplot(aes_string(x=x, y=y, color="as.factor(km.out$cluster)", size="total")) +
    geom_point() +
    geom_text(aes(label=cluster_tickers$ticker), hjust=0.5, vjust=-1) +
    theme(legend.position="none") +
    ggtitle(paste("K-Means Clustering (k=", k, ") with ", x, " and ", y, sep=""))
  
  return(p)
}

clusterPCA <- function(k=16) {
  pr.out <- prcomp(preprocessed)
  set.seed(1)
  scores <- pr.out$x[, 1:3]
  km.out <- kmeans(scores, centers=k)
  p <- as.data.frame(scores) %>%
    ggplot(aes(x=PC1, y=PC2, color=as.factor(km.out$cluster), size=PC3)) +
    geom_point() +
    geom_smooth(aes(col=as.factor(km.out$cluster)), method="lm", se=F) +
    theme(legend.position="none") +
    ggtitle(paste("K-Means Cluster (k=",k,") with PC1 and PC2", sep=""))
            
  return(p)
}

# ESG Analysis
esg.compare <- function(stock, metric) {
  df <- switch(metric,
               'esg' = esg,
               'edu' = education,
               'income' = income,
               'ejs' = ejs)
  avg <- switch(metric,
                'esg' = average.esg,
                'edu' = average.education,
                'income' = average.income,
                'ejs' = average.ejs)
  
  p <- df %>%
    filter(longName == stock) %>%
    cbind(avg) %>%
    select(!c(longName, avg_key)) %>%
    pivot_longer(c(value, avg_value), names_to="type", values_to="var")

  p <- p %>%
    ggplot(aes(x=key, y=var, fill=type)) +
      geom_col(position="dodge") +
      xlab("Data") +
      ylab("Percentage") +
      theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))
  
  return(p)
}

### XGBoost ###

# confusionMatrix from https://newbedev.com/plot-confusion-matrix-in-r-using-ggplot
bst_train <- function(ratio, nrounds, lambda, alpha) {
  train.index <- createDataPartition(esgdata$beat0, p=ratio, list=FALSE)
  train <- esgdata[train.index,]
  xtrain <- train %>% select(!beat0)
  ytrain <- train$beat0
  test <- esgdata[-train.index,]
  xtest <- test %>% select(!beat0)
  ytest <- test$beat0
  
  bst <- xgboost(as.matrix(xtrain), 
                 label=as.matrix(ytrain), 
                 nrounds=nrounds, 
                 objective="binary:logistic",
                 params=list(lambda=lambda, alpha=alpha))
  pred <- predict(bst, as.matrix(xtest))
  predictions = as.numeric(pred > 0.5)
  acc <- mean(predictions == ytest)

  confusionMatrix(as.factor(predictions), as.factor(ytest))$table
  table <- data.frame(confusionMatrix(as.factor(predictions), as.factor(ytest))$table)
  
  plotTable <- table %>%
    mutate(goodbad = ifelse(table$Prediction == table$Reference, "good", "bad")) %>%
    group_by(Reference) %>%
    mutate(prop = Freq/sum(Freq))
  
  # fill alpha relative to sensitivity/specificity by proportional outcomes within reference groups (see dplyr code above as well as original confusion matrix for comparison)
  p <- ggplot(data = plotTable, mapping = aes(x = Reference, y = Prediction, fill = goodbad, alpha = prop)) +
    geom_tile() +
    geom_text(aes(label = Freq), vjust = .5, fontface  = "bold", alpha = 1) +
    scale_fill_manual(values = c(good = "green", bad = "red")) +
    theme_bw() +
    theme(legend.position="none") +
    xlim(rev(levels(table$Reference)))
  
  return(p)
}
