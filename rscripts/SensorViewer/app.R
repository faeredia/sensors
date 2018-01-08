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

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Sensor Viewer"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
         dateRangeInput("dateRange", h3("Date Range")),
         selectInput("valTypeSelect", h3("Y1 Axis"),
                     choices = list("TEMPERATURE",
                                    "HUMIDITY"),
                     selected = "TEMPERATURE"
         )
          
      ),
      
      # Show a plot of the generated distribution
      mainPanel(
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
    #plot using ggplot
    plt <- ggplot(mydat, aes(x=date, y=value, color=sensor_id)) + geom_line() + ylim(0,ylimhigh) + ylab(input$valTypeSelect)
    plt <- plt + theme_bw() + theme(panel.border = element_blank(), panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))
    plt
  })
}

# Run the application 
shinyApp(ui = ui, server = server)

