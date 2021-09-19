library(shiny)

function(input, output) {
    
    output$originalClusterPlot <- renderPlot({
        p <- clusterDataset(input$clusterX, input$clusterY, k=input$datak)
        return(p)
    }, height=600)
    
    output$pcClusterPlot <- renderPlot({
        p <- clusterPCA(k=input$pck)
        return(p)
    }, height=600)
    
    output$esgPlot <- renderPlot({
        p <- esg.compare(input$stock, 'esg')
        return(p)
    }, height=600)
    
    output$educationPlot <- renderPlot({
        p <- esg.compare(input$stock, 'edu')
        return(p)
    }, height=600)
    
    output$incomePlot <- renderPlot({
        p <- esg.compare(input$stock, 'income')
        return(p)
    }, height=600)
    
    output$ejsPlot <- renderPlot({
        p <- esg.compare(input$stock, 'ejs')
        return(p)
    }, height=600)
    
    output$confusionMatrix <- renderPlot({
        p <- bst_train(input$ratio, input$nrounds, input$lambda, input$alpha)
        return(p)
    }, height=600)
}
