mechanize <- function(city="Rimini", startdate="01-01-2008", enddate="01-01-2009") {
  
  # Set the dates that we want to look for and the output filename
  date_diff <- enddate - startdate
  year <- 
  ndays <- days(date_diff) + 1
  out_filename <- paste0("./", city, "_weather_", year, ".csv")
  
}

