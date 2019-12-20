getWeather <- function(x){
  
  # Load riem package
  library(riem)
  
  #' Alternatively, there is also the `weatherData` package, 
  #' which fetches weather data from WeatherUnderground
  
  #' ## Get networks and corresponding stations
  
  # Get available networks
  #+r, warning = FALSE, message = FALSE
  networks <- riem_networks() 
  
  # Get available stations for one network
  german_stations <- riem_stations(network = "DE__ASOS")
  austrian_stations <- riem_stations(network = "AT__ASOS")
  uk_stations <- riem_stations(network = "GB__ASOS")
  
  #' ## Station measures
  
  #' Possible variables are (copied from (https://mesonet.agron.iastate.edu/request/download.phtml), 
  #' see also the [ASOS user guide](http://www.nws.noaa.gov/asos/pdfs/aum-toc.pdf))
  
  #' * station: three or four character site identifier
  #' * valid: timestamp of the observation (UTC)
  #' * tmpf: Air Temperature in Fahrenheit, typically @ 2 meters
  #' * dwpf: Dew Point Temperature in Fahrenheit, typically @ 2 meters
  #' * relh: Relative Humidity in \%
  #' * drct: Wind Direction in degrees from north
  #' * sknt: Wind Speed in knots
  #' * p01i: One hour precipitation for the period from the observation time to the time of the previous hourly precipitation reset. This varies slightly by site. Values are in inches. This value may or may not contain frozen precipitation melted by some device on the sensor or estimated by some other means. Unfortunately, we do not know of an authoritative database denoting which station has which sensor.
  #' * alti: Pressure altimeter in inches
  #' * mslp: Sea Level Pressure in millibar
  #' * vsby: Visibility in miles
  #' * gust: Wind Gust in knots
  #' * skyc1: Sky Level 1 Coverage
  #' * skyc2: Sky Level 2 Coverage
  #' * skyc3: Sky Level 3 Coverage
  #' * skyc4: Sky Level 4 Coverage
  #' * skyl1: Sky Level 1 Altitude in feet
  #' * skyl2: Sky Level 2 Altitude in feet
  #' * skyl3: Sky Level 3 Altitude in feet
  #' * skyl4: Sky Level 4 Altitude in feet
  #' * presentwx: Present Weather Codes (space seperated), see e.g. [this manual](http://www.ofcm.gov/fmh-1/pdf/H-CH8.pdf) for further explanations.
  #' * metar: unprocessed reported observation in METAR format
  
  # Get measures for one station, can start from 1928
  munich_data <- riem_measures(station = "EDDM", date_start = "2000-01-01", date_end = "2016-12-31") 
  munich2_data <- riem_measures(station = "EDPN", date_start = "2000-01-01", date_end = "2016-12-31") 
  leipzig_data <-  riem_measures(station = "EDDP", date_start = "2000-01-01", date_end = "2016-12-31") 
  bayreuth_data <- riem_measures(station = "EDQD", date_start = "2000-01-01", date_end = "2016-12-31")
  ffm_data <- riem_measures(station = "EDDF", date_start = "2000-01-01", date_end = "2016-12-31") 
  krems_data <- riem_measures(station = "LOAG", date_start = "2000-01-01", date_end = "2016-12-31") 
  anglesey_data <-  riem_measures(station = "EGOF", date_start = "2000-01-01", date_end = "2016-12-31")
  texel_data <- riem_measures(station = "EHTX", date_start = "2000-01-01", date_end = "2016-12-31")
  loughneagh_data <- riem_measures(station = "EGAA", date_start = "2000-01-01", date_end = "2016-12-31")
  
  # Save data to file
  write.csv(munich_data, file="E:/Data/ASOS/munich_2000_2016.csv")
  write.csv(munich2_data, file="E:/Data/ASOS/munich2_2000_2016.csv")
  write.csv(bayreuth_data, file="E:/Data/ASOS/bayreuth_2000_2016.csv")
  write.csv(leipzig_data, file="E:/Data/ASOS/leipzig_2000_2016.csv")
  write.csv(ffm_data, file="E:/Data/ASOS/ffm_2000_2016.csv")
  write.csv(krems_data, file="E:/Data/ASOS/krems_2000_2016.csv")
  
  # Table of first few data entries
  knitr::kable(head(munich_data))
  
  # Change time into correct format
  munich_data$valid <- as.POSIXct(munich_data$valid)
  
  # Convert temperature into degree Celsius
  library(weathermetrics)
  munich_data$temp <- fahrenheit.to.celsius(munich_data$tmpf, round = 2)
  
  # Plot temperature data over time
  library(ggplot2)
  ggplot() + geom_line(data=munich_data, aes(x=valid,y=temp)) + 
    labs(x="Time", y="Temperature (F)")
  
  ggplot() + geom_line(data=munich_data, aes(x=valid,y=tmpf)) + 
    labs(x="Time", y="Temperature (F)") + 
    geom_line(data=leipzig_data, aes(x=valid,y=tmpf), color="blue") + 
    geom_line(data=ffm_data, aes(x=valid,y=tmpf), color="red")
  
  #For conversion of wind speed or temperature into other units, 
  #see [this package](https://github.com/geanders/weathermetrics/).
  
}