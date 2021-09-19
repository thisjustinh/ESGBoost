# ESGBoost

[R Shiny](https://superbia-vice.shinyapps.io/ESGBoost/) ESG and ECHO-based information hub for accessible, long-term growth investing! Made at HackMIT 2021, the app provides sustainability information about certain companies in the S&P 500.

## Introduction

ESGBoost is a sustainability information hub for the curious investor gazing beyond the quarterly financial statements and Reddit posts. If you're going beyond the traditional fundamentals, we welcome you to explore the statistics behind a company's (possibly poor) environmental impact, social demographic, and compliance (I bet you thought I would say governance!) history&mdash;at least, in my sales pitch (:

The R Shiny application is divided into three categories. Click below to learn more, or keep reading!

- [ESG Analysis](#ESG-Analysis)
- [Clustering](#Clustering)
- [XGBoost](#XGBoost)

## Data

Data are collected from two sources: ESG ratings from Yahoo Finance sourced by Sustainalytics, and the Enforcement and Compliance History Online (ECHO) by the Environmental Protection Agency. 

The ESG ratings from Yahoo Finance were scraped using BeautifulSoup4 (largely inspired by [this](https://curt-beck1254.medium.com/scrapping-financial-esg-data-with-python-99d171a12c51) Medium article), and the ECHO information was accessed via the EPA's RESTful API.

ESG ratings are comprised of three factors: environmental risk, social risk, and governance risk, for a specific company. These ratings are also accompanied by an aggregate score (the sum of all three ratings) and a controversy level ranging from 0 to 5. 

ECHO provides information about health risks (officially, the Environmental Justice Screen Indexes) and demographics about the employees and households working in a company. Health risks can include cancer risks, hazardous waste proximity, ozone and PM25 levels. Demographics are mostly split into two categories: highest level of education attained by employees as a percentage, and income distribution in the <15k, 15-25k, 25-50k, 50-75k, and >75k brackets, as a percentage.

Yahoo finance also provided quarterly returns for stocks and SPY in the past year, which we used in k-means clustering and XGBoost.

## Methodology

### ESG Analysis

With each individual stock comes information on its ESG sustainability ratings, highest levels of education among employees, income distribution, and health risks. There are accompanying charts that compare the stock's individual performance in one of the four categories to the average of all the stocks included in our analysis. The analysis for these were written in R, although the data itself was obtained through API calls and some data pruning in Python.

### Clustering

Perhaps it'd be interesting to know which companies are most similar to one another based on their ESG risk. We can group companies together using k-means clustering, which is exactly what was done in R (and briefly in Python's `scikit-learn`). One chart shows k-means clustering performed on the original dataset involving all companies analyzed. Another performs k-means clustering on the first three principal components obtained via principal component analysis, which may offer insight to variables whose affect on the variance in the dataset are similar.

The R Shiny database offers different variable combinations and a slider to control the number of clusters created, which will reperform k-means clustering in real time when changed.

### XGBoost

Finally, XGBoost. Here, we were curious if ESG data would be able to help classify a specific stock's quarterly returns versus the S&P 500 average (in this case, we substitute with SPY quarterly returns). Using the ESG factors, including the controversy level, and a binary variable indicating whether or not the stock beat SPY in the last quarter, we aim to perform binary classification. In the R Shiny app, there are sliders that allow control over certain hyperparameters: how many times the model passes through, the L2-penalty on the weights, and the L1-penalty on the weights.

XGBoost was performed in R using the `xgboost` library, although we experimented with Tangram's CLI experience.
