import zoneinfo #convert UST into IST
from astral import LocationInfo #to get the sunset and sunrise time of any location
from astral.sun import sun
from datetime import date, timedelta, datetime #use to perform calculation on time
import geopy # give the logitude and latitude of the given city

#list of planet in definate order
planetNames = ['Moon','Saturn','Jupiter','Mars','Sun','Venus','Mercury']

horaChart = {"day": [], "night": []} #empty list for hora chart

#converting weekdays number into planetNames index
planetNamesIndex = {
    0:0, 1:3, 2:6, 3:2, 4:5, 5:1, 6:4
} 

def genrateHoraChart(dateStr, locationStr):
    try:
        loc = geopy.Nominatim(user_agent='hora calculater').geocode(locationStr) #show error for invalid city name

        #specifing location
        city = LocationInfo(
            timezone="Asia/Kolkata",
            latitude=loc.latitude,
            longitude=loc.longitude,
        )
        #converting UTC timezone to local timezone
        timezone = zoneinfo.ZoneInfo("Asia/Kolkata")
        currentDate = date.fromisoformat(dateStr) #show error if the date is not in correct format
        nextDate = currentDate + timedelta(1)
        
        # Get the sunrise and sunset times
        firstDay = sun(city.observer, date=date(currentDate.year, currentDate.month, currentDate.day), tzinfo=timezone)
        nextDay = sun(city.observer, date=date(nextDate.year, nextDate.month, nextDate.day), tzinfo=timezone)

        # converting sunrise and sunset times into datetime object
        firstSunRise = datetime.fromisoformat(str(firstDay['sunrise'].strftime('%Y-%m-%d %H:%M:%S')))
        firstSunSet = datetime.fromisoformat(str(firstDay['sunset'].strftime('%Y-%m-%d %H:%M:%S')))
        nextSunRise = datetime.fromisoformat(str(nextDay['sunrise'].strftime('%Y-%m-%d %H:%M:%S')))

        #defining duration of a hora 
        dayHoraPeriod = (firstSunSet - firstSunRise)/12
        nightHoraPeriod = (nextSunRise - firstSunSet)/12
        horaPeriod = {"day":dayHoraPeriod, "night":nightHoraPeriod}

        #defining index of the planets
        index = planetNamesIndex[currentDate.weekday()]

        #create a hora chart
        initialTime = firstSunRise
        for key in horaChart.keys():
            horaDuration = horaPeriod[key]
            for j in range(0,12):
                horaChart[key].append([planetNames[index],initialTime.time().isoformat(timespec='seconds'),(initialTime+horaDuration).time().isoformat(timespec='seconds')])
                initialTime = horaDuration + initialTime
                index += 1
                if(index == 7):
                    index = 0

        return {"horaChart": horaChart, "sunRise": firstSunRise, "sunSet": firstSunSet, "nextSunRise": nextSunRise, "error": False}
    except Exception as e:
        return {"error": e}


