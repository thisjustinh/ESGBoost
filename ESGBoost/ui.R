library(shiny)

navbarPage(
    title = "ESGBoost", 
    tabPanel("ESG Analysis",
        sidebarLayout(
            sidebarPanel(
                h2("Responsible Investing!"),
                helpText("Analyze environmental, social, and governance risk within
                         the S&P 500 by looking at individual companies."),
                selectInput("stock",
                            label="Stock:",
                            choices=master$longName,
                            selected=master$longName[1]),
            ),
            mainPanel(
                tabsetPanel(
                    tabPanel("ESG", plotOutput("esgPlot")),
                    tabPanel("Highest Education Level", plotOutput("educationPlot")),
                    tabPanel("Income Distribution", plotOutput("incomePlot")),
                    tabPanel("Environmental Justice Screen Indexes", plotOutput("ejsPlot"))
                )
            )
        )
    ), 
    tabPanel("Clustering",
        sidebarLayout(
            sidebarPanel(
                h2("K-Means Clustering"),
                helpText("See what clustering can do visually, either applied on the original data or the principal components from PCA."),
                h4("Original Dataset"),
                selectInput("clusterX:",
                            label="x-axis:",
                            choices=colnames(preprocessed),
                            selected=colnames(preprocessed)[1]),
                selectInput("clusterY:",
                            label="y-axis:",
                            choices=colnames(preprocessed),
                            selected=colnames(preprocessed)[2]),
                sliderInput("datak",
                            "Number of Clusters for Original:",
                            min = 5,
                            max = 15,
                            value = 10),
                h4("Principal Components"),
                sliderInput("pck",
                            "Number of Clusters for PCs:",
                            min = 5,
                            max = 15,
                            value = 10)
            ),
            mainPanel(
                tabsetPanel(
                    tabPanel("Original Dataset", plotOutput("originalClusterPlot")),
                    tabPanel("Principal Components", plotOutput("pcClusterPlot"))
                )
            )
        )
    ),
    tabPanel("XGBoost",
        sidebarLayout(
            sidebarPanel(
                h2("XGBoost: Beat SPY with ESG"),
                helpText("Play around with parameters to try to best fit a model."),
                sliderInput("ratio",
                            label="Train-to-Test Split:",
                            min=0.1,
                            max=0.9,
                            value=0.7,
                            step=0.1),
                sliderInput("nrounds",
                            label="Number of Rounds:",
                            min=1,
                            max=100,
                            value=10),
                sliderInput("lambda",
                            label="L2 Weight Penalty:",
                            min=0.01,
                            max=5,
                            value=0.1,
                            step=0.01),
                sliderInput("alpha",
                            label="L1 Weight Penalty",
                            min=0.01,
                            max=5,
                            value=0.1,
                            step=0.01),
            ),
            mainPanel(
                plotOutput("confusionMatrix")
            )
        )
    ),
    navbarMenu("More", tabPanel(a("GitHub", href="https://github.com/xinging-birds/ESGBoost", target="_blank"))
    )
)
