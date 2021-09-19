library(shiny)

# Define UI for application that draws a histogram
fluidPage(

    # Application title
    titlePanel("ESGBoost"),

    # Sidebar with a slider input for number of bins
    sidebarLayout(
        sidebarPanel(
            helpText("Analyze environmental, social, and governance risk within
                     the S&P 500."),
            h2("Responsible Investing!"),
            selectInput("option",
                        label="Action:",
                        choices=list("Clustering",
                                     "ESG Analysis",
                                     "XGBoost"),
                        selected="Clustering"),
            conditionalPanel(
                condition="input.option == 'Clustering'",
                radioButtons("clusterData",
                             label="Variable Choice",
                             choices=list("Original"=1,
                                          "Principal Components"=2),
                             selected=2),
                conditionalPanel(
                    condition="input.clusterData == 1",
                    selectInput("clusterX:",
                                label="x-axis:",
                                choices=colnames(preprocessed),
                                selected=colnames(preprocessed)[1]),
                    selectInput("clusterY:",
                                label="y-axis:",
                                choices=colnames(preprocessed),
                                selected=colnames(preprocessed)[2]),
                ),
                sliderInput("k",
                            "Number of Clusters:",
                            min = 5,
                            max = 15,
                            value = 10)
            ),
            conditionalPanel(
                condition="input.option == 'ESG Analysis'",
                selectInput("stock",
                            label="Stock:",
                            choices=master$longName,
                            selected=master$longName[1]),
                selectInput("esgMetric",
                            label="Factor:",
                            choices=list("ESG",
                                         "Highest Education",
                                         "Income Distribution",
                                         "Environmental Justice Screen Indexes"),
                            selected="ESG")
            ),
            conditionalPanel(
                condition="input.option == 'XGBoost'",
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
                            step=0.01)
            )
        ),

        # Show a plot of the generated distribution
        mainPanel(
            plotOutput("plot")
        )
    )
)
