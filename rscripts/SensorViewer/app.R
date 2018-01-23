#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(RMariaDB)
library(dplyr)
library(ggplot2)

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Sensor Viewer"),
   
   # Sidebar with tuneable options
   sidebarLayout(
      sidebarPanel(
         dateRangeInput("dateRange", h3("Date Range")),
         selectInput("valTypeSelect", h3("Y1 Axis"),
                     choices = list("TEMPERATURE",
                                    "HUMIDITY"),
                     selected = "TEMPERATURE"
         ),
         h3("Aestethics"), #placeholder
         checkboxInput("showPoints", "Show Points", value = TRUE)
           
      ),
      
      #the body of the page
      mainPanel(
        #the main plot
        plotOutput("mainPlot")
      )
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  #connect to the server and get some data
  con <- dbConnect(RMariaDB::MariaDB(), host='localhost', username='brandon', password='LLacey2015', dbname='sensdb')
  res <- dbSendQuery(con, "SELECT * FROM generic_sensor_data ORDER BY date ASC")
  dat <- dbFetch(res)
  dbClearResult(res)
  dbDisconnect(con)
  
  filt_dat <- reactive({
    return <- filter(dat,
           as.Date(date) >= input$dateRange[1],
           as.Date(date) <= input$dateRange[2],
           value_type == input$valTypeSelect
    )
  })
  
  output$mainPlot <- renderPlot({
    # plot the graph
    mydat <- filt_dat()
    #plot using base graphics
    #plot(mydat$value ~ mydat$date, type='line', ylim=c(0, 40), ylab = input$valTypeSelect)
    #set the ylim high to eaither twice the mean (mean is centered) or to the max value, whichever is greatest
    ylimhigh <- max(2 * mean(mydat$value), max(mydat$value))
    #set the plot aestethics
    plt <- ggplot(mydat, aes(x=date, y=value, color=sensor_id)) + geom_line() + ylim(0,ylimhigh) + ylab(input$valTypeSelect)
    #set the theme for the plot
    plt <- plt + theme_bw() + theme(panel.border = element_blank(), panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))
    #if the 'showPoint' checkbox is pressed, show the individual datapoints
    if(input$showPoints == TRUE){
      plt <- plt + geom_point()
    }
    #show the plot
    plt
  })
}

# Run the application 
shinyApp(ui = ui, server = server)

