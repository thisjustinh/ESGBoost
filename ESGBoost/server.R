library(shiny)

# Define server logic required to draw a histogram
function(input, output) {

    # dataviz choice
    dataset <- reactive({
        switch(input$option,
               "Clustering" = preprocessed,
               "ESG Analysis" = master,
               "XGBoost" = esgdata)
    })
    
    output$plot <- renderPlot({
        if (input$option == "Clustering") {
            if (input$clusterData == 1) {
                p <- clusterDataset(input$clusterX, input$clusterY, k=input$k)
            } else if (input$clusterData == 2) {
                p <- clusterPCA(k=input$k)
            }
        } else if (input$option == "ESG Analysis") {
            p <- esg.compare(input$stock, input$esgMetric)
        } else if (input$option == "XGBoost") {
            p <- bst_train(input$ratio, input$nrounds, input$lambda, input$alpha)
        }
        return(p)
    }, height=600)

}
