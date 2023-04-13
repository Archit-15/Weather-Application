#This project will only work in WeatherProject Environment, always activate it first as geopy, pytz
#timezonefinder are only present here

from tkinter import *
from PIL import ImageTk,Image
from geopy.geocoders import Nominatim
from tkinter import ttk,messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import requests

#Creating the window
root = Tk()
root.title('Weather Application')
root.geometry('850x450+245+90')     #+230+75 will move the window by 250 units in the x axis(right) and 75
#units in the y axis(down) from where it would have normally appeared (helps in placing the window in the
# middle of our screen at start)

icon = ImageTk.PhotoImage(Image.open('l.png'))
root.iconphoto(True,icon)
root.resizable(False,False)     #This wont let the user resize the window on his own

#FUNCTIONS
def getweather():
    try:
        city = textfield.get()
        geolocator = Nominatim(user_agent='geoapiExercises')    #Nomitaing is used for geocoding services
        #converting physical addresses into coordinates and vice versa.Here a Nomainatim geocoder object is
        #initialized and user_agent is used to identify the user of geocoding services(here we have set
        # 'geoapiExercises')
        location = geolocator.geocode(city) #Here the coordinates of the city variable are found out by using
        #geocode method of Nomainatim object
        obj = TimezoneFinder()  #Creating an instance of TimezoneFinder class which can find timezeone of 
        #given coordinate(it finds the timezone and not the time)
        result = obj.timezone_at(lng=location.longitude,lat=location.latitude) #We can get timezone using 
        #method and obtain latitude and longitude using geocode method
        print(result) #COMMENT this later
        # print(location.longitude)
        # print(location.latitude)

        home = pytz.timezone(result)    #Here we create a timezone object that represents the timezone present
        #in result and initialize it to home now we can perform various timezone related operations
        local_time = datetime.now(home)  #Here we create a datetime object which contains the current date and
        #time of the timezone present in home
        current_time = local_time.strftime("%I:%M %p")     #The strftime function takes the time part of datetime 
        #object and converts into a string format %I is for hours and %M is for minutes, %p for am/pm
        
        clock.config(text=current_time)     #Labels have already been made and placed but they dont have text
        name.config(text='CURRENT WEATHER') #in them, so when this function is called they get text in them

        #Weather
        api = 'https://api.openweathermap.org/data/2.5/weather?lat='+str(location.latitude)+'&lon='+str(location.longitude)+'&appid=1c91042d371a2d1b28bee1fde1aa95c8'
        json_data = requests.get(api).json()        #Get request is sent to OpenWeatherMap API and the 
        #repsonse is converted in json using json() and stored in json_data variable
        # ALL the other valriables are extrated from json_data using their keys
        condition = json_data['weather'][0]['main'] 
        description  = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp']-273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        t.config(text = (temp,'°'))
        c.config(text = (condition,'|','FEELS','LIKE',temp,'°'))

        w.config(text=wind)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)
    
    except Exception as e:
        messagebox.showerror("Weather Application","Invalid Entry!!")

#SEARCH BOX
Search_image = ImageTk.PhotoImage(Image.open('Search.png'))
myimage = Label(root,image =Search_image)
myimage.place(x=20,y=20)

textfield = Entry(root,justify='center',width=17,font=('poppins',25,'bold'),bg='#404040',border=0,fg='white')
#Since the textfield doesn't cover the whole search box we make the border 0 to make it look like it does
textfield.place(x=50,y=40)
textfield.focus()       #Setting focus will make the cursor automatiacally appear here

Search_icon = ImageTk.PhotoImage(Image.open('search_i.png'))
myimage_icon = Button(root,image = Search_icon,borderwidth=0,cursor = 'hand2',bg='#404040',command=getweather) 
#The cursor attribute will change the cursor wehnever we hover over this mouse 
myimage_icon.place(x=400,y=34)

#LOGO
logo_image = ImageTk.PhotoImage(Image.open('Logo.png'))
logo = Label(root,image = logo_image)
logo.place(x=150,y=100)

#BOTTOM BOX
Frame_image = ImageTk.PhotoImage(Image.open('Box.png'))     
frame_myimage = Label(root,image = Frame_image)
frame_myimage.pack(padx=5,pady=5,side=BOTTOM)   #Side determines at which side the widget gets packed

#TIME
name = Label(root,font=('arial',15,'bold'))
name.place(x=30,y=100)
clock = Label(root,font=('Helvetica',20))
clock.place(x=30,y=130)

#LABEL IN BOTTOM BOX
label1 = Label(root,text='WIND',font=('Helvetica',15,'bold'),fg='white',bg='#1ab5ef')
label1.place(x=120,y=350)

label2 = Label(root,text='HUMIDITY',font=('Helvetica',15,'bold'),fg='white',bg='#1ab5ef')
label2.place(x=250,y=350)

label3 = Label(root,text='DESCRIPTION',font=('Helvetica',15,'bold'),fg='white',bg='#1ab5ef')
label3.place(x=430,y=350)

label4 = Label(root,text='PRESSURE',font=('Helvetica',15,'bold'),fg='white',bg='#1ab5ef')
label4.place(x=650,y=350)

t = Label(font=('arial',70,'bold'),fg='#ee666d')
t.place(x=400,y=150)
c = Label(font=('arial',15,'bold'))
c.place(x=400,y=250)

w = Label(root,text='...',font=('arial',20,'bold'),bg='#1ab5ef')
w.place(x=120,y=380)
h = Label(root,text='...',font=('arial',20,'bold'),bg='#1ab5ef')
h.place(x=280,y=380)
d = Label(root,text='...',font=('arial',20,'bold'),bg='#1ab5ef')
d.place(x=440,y=380)
p = Label(root,text='...',font=('arial',20,'bold'),bg='#1ab5ef')
p.place(x=670,y=380)


root.mainloop()