# To use this code, both mechanize and ClientForm need to be installed
import mechanize
import datetime as dt
import string

# Set the web page preferences so the returned data will show the full METARS
request = mechanize.Request("http://www.wunderground.com/cgi-bin/findweather/getForecast?setpref=SHOWMETAR&value=1")
response = mechanize.urlopen(request)

# Set the dates that we want to look for and the output filename
start_date = dt.date(2008, 1, 1)
end_date = dt.date(2009, 1, 1)
date_diff = end_date - start_date
ndays = date_diff.days + 1
out_filename='./rimini_weather_2007.csv'

# Open the output file
file_out = open(out_filename,'w')
header = 'Date,LocalTime,TemperatureC,Dew PointC,Humidity,Sea Level PressurehPa,VisibilityKm,Wind Direction,Wind SpeedKm/h,Gust SpeedKm/h,PrecipitationCm,Events,Conditions,FullMetar,WindDirDegrees,DateUTC\n'
file_out.write(header)

# Loop through number of days to look for
for i in range(ndays):

  delta_days = dt.timedelta(days = i)
  cday = start_date + delta_days

  date_string=str(cday.year)+'/'+str(cday.month)+'/'+str(cday.day)
  print date_string

# Fetch the data from the web page for the particular day
  request2 = mechanize.Request("http://www.wunderground.com/history/airport/LIPR/"+date_string+"/DailyHistory.html?req_city=NA&req_state=NA&req_statename=NA&&theprefset=SHOWMETAR&theprefvalue=1&format=1")
  response2 = mechanize.urlopen(request2)

  web_data = response2.readlines() 

# Tidy up the output and send it to a file

  for line in web_data:
    line_split = string.split(line,",")
    if ((len(line_split) == 15) and (line_split[0][0:4] != "Time")):
      line_split = string.split(line,"<")
      line_trim = str(cday.day)+'/'+str(cday.month)+'/'+str(cday.year)+','+line_split[0]+'\n'
      file_out.write(line_trim)

# Close the output file

file_out.close()

