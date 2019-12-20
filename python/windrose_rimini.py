import numpy
import pylab as lab
#from mpl_toolkits.basemap import *
import string
import datetime as dt
#import utils
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import copy
import random
import matplotlib.cm as cm
import math
import calendar

months2   = mdates.MonthLocator(interval=1) 
months3   = mdates.MonthLocator(interval=1,bymonthday=15) 
monthFmt2 = mdates.DateFormatter('')
monthFmt3 = mdates.DateFormatter('%b')

# Read wind speed data from Rouen airport

file_ta = open('./rimini_weather_2012.csv','r')
ta_data = file_ta.readlines()
file_ta.close()
n_data_ta=len(ta_data)

ta_date = []
ta_wspd = []
ta_dir = []
ta_month= []

for yind in range(1,n_data_ta):
  line_split = string.split(ta_data[yind],',')
  metar = line_split[13][:5]
  if metar=="METAR":
    date_split = string.split(line_split[15])
    date = date_split[0]
    time = date_split[1]
    date_split = string.split(date,'-')
    year = int(date_split[0])
    month = int(date_split[1])
    day = int(date_split[2])
    time_split = string.split(time,':')
    hr = int(time_split[0])
    mn = int(time_split[1])

    wspd = line_split[8]
    dirstr = line_split[7]
    if wspd == "Calm":
      wspd2 = 0.0
      dir2 = 0.0
    elif wspd == "N/A" or wspd == "-9999":
      wspd2 = -99.0
      dir2 = -99.0
    else:
      wspd2 = float(line_split[8])
      dir2 = float(line_split[14])
      if wspd2 < 3.9*1.852:
        wspd2 = 0.0
        dir2 = 0.0

    if dirstr == "Variable" and wspd2 > 0.0:
      dir2 = random.randint(0,35)*10.0 
  
    if wspd2 >= 0.0 and dir2 >= 0.0 and dir2 <=360 :
      ta_date.append(dt.datetime(year,month,day,hr,mn,0))
      ta_wspd.append(wspd2/1.852)
      if dir2 > 348.75:
       dir2 = dir2 - 360.0
      ta_dir.append(dir2)
      ta_month.append(month)

ta_wspd = numpy.array(ta_wspd)
ta_dir = numpy.array(ta_dir)
ta_month = numpy.array(ta_month)

lab.plot(ta_date,ta_wspd,'x')
lab.show()

print numpy.average(ta_wspd)

# Calculate histogram for windroses

for pl_num in range(2):

  fig1 = lab.figure(figsize=(7,10.5))

  for month in range(1,7):
    month2 = month + (pl_num*6)
    mtext = calendar.month_name[month2]+'\n'
    if month == 1:
      parea1 = [0.05,0.68,0.3,0.3]
      parea2 = [0.42,0.73,0.02,0.2]
    elif month == 2:
      parea1 = [0.57,0.68,0.3,0.3]
      parea2 = [0.94,0.73,0.02,0.2]
    elif month == 3:
      parea1 = [0.05,0.39,0.3,0.3]
      parea2 = [0.42,0.44,0.02,0.2]
    elif month == 4:
      parea1 = [0.57,0.39,0.3,0.3]
      parea2 = [0.94,0.44,0.02,0.2]
    elif month == 5:
      parea1 = [0.05,0.10,0.3,0.3]
      parea2 = [0.42,0.15,0.02,0.2]
    elif month == 6:
      parea1 = [0.57,0.10,0.3,0.3]
      parea2 = [0.94,0.15,0.02,0.2]
    ind = numpy.nonzero(ta_month == month2)
    ind = ind[0]
    wspd_hist = numpy.array(ta_wspd[ind])
    dir_hist = numpy.array(ta_dir[ind])
    bins1=numpy.array([-1.0,3.9,6.9,10.9,16.9,21.9,26.9,200,400])
    bins2=11.25*numpy.array([-1,1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31])
  
    in_hist = numpy.vstack((wspd_hist,dir_hist)).T
    H, edges = numpy.histogramdd(in_hist, bins=[bins1,bins2])
  
    H = H*100.0/numpy.sum(H)

# Plot the windrose

    lab.rc('xtick',labelsize=8)
    lab.rc('ytick',labelsize=7)

    ax1 = fig1.add_axes(parea1, polar=True)

    theta = (90.0-22.5*numpy.arange(0,16)-7.5) % 360
    theta = theta*2*numpy.pi/360.0
    mywidth = 15.0*2*numpy.pi/360.0

    radii1=sum(H[0,:])/16
    bar_all = {}
    bar_all['0'] = ax1.bar(0, radii1, width=3*numpy.pi, bottom = 0.0, edgecolor='b')
    radii2=H[1,:]
    for ind in range(1,7):
      bar_all[str(ind)] = ax1.bar(theta, radii2, width=mywidth, bottom = radii1)
      radii1 = radii2 + radii1
      radii2=H[ind+1,:]
  
    ax1.set_xticklabels(['E','NE','N','NW','W','SW','S','SE'])
    ax1.set_ylim([0,30.0])
    ax1.set_yticks([10,20,30])
    ax1.set_yticklabels(['10%','20%',''])
    ax1.set_title(mtext,fontsize=12)

    for ind in range(0,7):
      for bar_tmp in bar_all[str(ind)]:
        bar_tmp.set_facecolor(cm.jet(ind/7.))
        bar_tmp.set_edgecolor(cm.jet(ind/7.))
        bar_tmp.set_linewidth(0)

    sumH = numpy.sum(H,axis=1) 

    lab.rc('ytick',labelsize=7)

    ax2 = fig1.add_axes(parea2,frame_on=False)

    bar_all2={}
    hgt2 = 0
    for ind in range(0,8):
      hgt1 = sumH[ind]
      bar_all[str(ind)] = ax2.bar(0.1, hgt1, width=0.8, bottom = hgt2)
      hgt2 = hgt1 + hgt2

    for ind in range(0,8):
      for bar_tmp in bar_all[str(ind)]:
        bar_tmp.set_facecolor(cm.jet(ind/7.))
        bar_tmp.set_edgecolor(cm.jet(ind/7.))
        bar_tmp.set_linewidth(0)

    ax2.set_xlim([0.1,0.9])
    ax2.set_ylim([0,100])
    ax2.set_xticks([])
    ax2.tick_params(direction='out')
    ax2.set_yticks([0,10,20,30,40,50,60,70,80,90,100])
    ax2.set_yticklabels(['0%','','','','','50%','','','','','100%'])
    ax2.get_yaxis().tick_left()

# Plot the legend

  ax3 = fig1.add_axes([0.025,0.017,0.95,0.06],frame_on=False,aspect='equal')
  ax3.set_xticks([])
  ax3.set_yticks([])
  ax3.set_title('Wind speed\n(Beaufort scale)',fontsize=10)
  
  ax3.set_xlim([0,18.5])
  ax3.set_ylim([0,1.4])
  
  labs = ['Force 1','Force 2','Force 3','Force 4','Force 5','Force 6','Force 7\nand above']

  for ind in range(0,7):

    offset = (ind)*2.6+0.1
    ax3.fill(numpy.array([0.1,0.1,0.9,0.9,0.1])+offset,numpy.array([0.1,0.9,0.9,0.1,0.1]),facecolor=cm.jet(ind/7.),linewidth=0)
    ax3.text(1.05+offset,0.5,labs[ind],fontsize=9,va='center',ha='left')

  if pl_num == 0:
    fig1.savefig('./rimini_airport_rose2012_1.png',dpi=300)
  if pl_num == 1:
    fig1.savefig('./rimini_airport_rose2012_2.png',dpi=300)
