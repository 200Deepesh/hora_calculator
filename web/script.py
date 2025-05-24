from pyscript import display # type: ignore
from pyscript import document # type: ignore

# install astral and geopy 

# import tkinter as tk #use to make gui of the app
# from tkinter import messagebox, ttk
import zoneinfo #convert UST into IST
from astral import LocationInfo #to get the sunset and sunrise time of any location
from astral.sun import sun
from datetime import date, timedelta, datetime #use to perform calculation on time
import geopy # give the logitude and latitude of the given city

import pyodide_http # type: ignore
pyodide_http.patch_all()  # Patch urllib3 and requests



#list of planet in definate order
planetNames = [['Moon'],['Saturn'],['Jupiter'],['Mars'],['Sun'],['Venus'],['Mercury']]

hc = [] #empty list for hora chart

horaChart = document.getElementById('hora-chart')
# messagebox = document.getElementById('message-box')

#converting weekdays number into planetNames index
planetNamesIndex = {
    0:0, 1:3, 2:6, 3:2, 4:5, 5:1, 6:4
}


#verifing input data
def validate_inputdata(date_text, city):
    try:
        date.fromisoformat(date_text) #show error if the date is not in correct format
        try:
            loc = geopy.Nominatim(user_agent='hora calculater', scheme='https').geocode(city) #show error for invalid city name
            return True 
        except: 
            # messagebox.showerror("Invalid Date", "Please enter the valid city name or check your internet connection.")
            print("Invalid Date", "Please enter the valid city name or check your internet connection.")
            return False        
    except:
        # messagebox.showerror("Invalid Date", "Please enter the valid city name or date in YYYY-MM-DD format.")
        print("Invalid Date", "Please enter the valid city name or date in YYYY-MM-DD format.")
        return False

def submit_date(event):
    input_date = document.getElementById('date').value
    city = document.getElementById('city').value

    print(input_date, city)

    if validate_inputdata(input_date, city):
        loc = geopy.Nominatim(user_agent='hora calculater', scheme='https').geocode(city)

        #specifing location
        city = LocationInfo(
            timezone="Asia/Kolkata",
            latitude=loc.latitude,
            longitude=loc.longitude,
        )
        #converting UTC timezone to local timezone
        timezone = zoneinfo.ZoneInfo("Asia/Kolkata")
        currentDate = date.fromisoformat(input_date)
        nextDate = currentDate + timedelta(1)
        
        # Get the sunrise and sunset times
        firstDay = sun(city.observer, date=date(currentDate.year, currentDate.month, currentDate.day), tzinfo=timezone)
        nextDay = sun(city.observer, date=date(nextDate.year, nextDate.month, nextDate.day), tzinfo=timezone)

        # converting sunrise and sunset times into datetime object
        firstSR = datetime.fromisoformat(str(firstDay['sunrise'].strftime('%Y-%m-%d %H:%M:%S')))
        firstSS = datetime.fromisoformat(str(firstDay['sunset'].strftime('%Y-%m-%d %H:%M:%S')))
        nextSR = datetime.fromisoformat(str(nextDay['sunrise'].strftime('%Y-%m-%d %H:%M:%S')))

        #defining duration of a hora 
        dayHoraPeriod = (firstSS - firstSR)/12
        nightHoreaPeriod = (nextSR - firstSS)/12
        td = [dayHoraPeriod, nightHoreaPeriod]

        #defining index of the planets
        index = planetNamesIndex[currentDate.weekday()]

        clear() 

        #create a hora chart
        tt = firstSR
        for i in range(0,2):
            for j in range(0,12):
                hc.append([j+1,planetNames[index],tt.time().isoformat(timespec='seconds'),(tt+td[i]).time().isoformat(timespec='seconds')])
                tt = td[i] + tt
                index += 1
                if(index == 7):
                    index = 0

        

        #print the hora chart
        tbody = '<tbody>'
        for index, i in enumerate(hc):
            tr = f'''<tr>
                <td>{i[0]}</td>
                <td>{i[1][0]}</td>
                <td>{i[2]}</td>
                <td>{i[3]}</td>
                </tr>
            '''
            tbody += tr
        tbody += '</tbody>'
        horaChart.insertAdjacentHTML( 'beforeend', tbody )

#clear the data of previous table
def clear():
    hc.clear()
    horaChart.removeChild(document.querySelector('#hora-chart > tbody'))
