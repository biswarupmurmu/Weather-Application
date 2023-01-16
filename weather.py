from tkinter import *
import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

api_key = ""

root = Tk()
root.title("Weather Application")
img = PhotoImage(file='assets/weather.png')
root.tk.call('wm', 'iconphoto', root._w, img)

# App window size and position it in the center of screen
app_width = 500
app_height = 500

# Know the scrren size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Determine (x,y) for the app
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)

root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
root.minsize(500,500)

welcome_text = Label(root,
    text = "Welcome to weather application!",
    font=('Arial',20),
    pady=50)
welcome_text.pack()

enter_a_city = Label(root,
    text = "Please enter a city name:",
    font=('Arial',12))
enter_a_city.pack()

enter_city_name = Entry(root,
    bg='white',
    bd=0.5)
enter_city_name.pack(pady=5,
    padx=5)


i = 0

def main_function():
    if i > 0:
        delete_previous_output()
    check_the_input()

def delete_previous_output():
    for widget in output_frame.winfo_children():
        widget.destroy()

def check_the_input():

    global i
    i = 1

    global city
    city = enter_city_name.get()
    if len(city)==0:
        nocity_entered = Label(output_frame,
            text="You have not entered any city.",
            fg='brown')
        nocity_entered.pack()

    else:
        check_internet_connection()


def check_internet_connection():
    global url
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    timeout = 10
    try:
        request = requests.get(url,timeout=timeout)

    except (requests.ConnectionError,requests.Timeout) as exception:
        print("no internet")
        no_internet = Label(output_frame,
            text="Please check your internet connection.",
            fg='red')
        no_internet.pack()
    else:
        make_api_call()

# API call
def make_api_call():
    global response
    response = requests.get(url)
    check_status_of_api_call()

# Check status of API call
def check_status_of_api_call():
    
    if response.status_code == 200:
        print("call successful")
        make_weathere_report()
    else:
        error_occured = Label(output_frame,
            text = "Please enter city name correctly",
            fg='red')
        error_occured.pack()

def make_weathere_report():
    data = response.json()
    print(data)
    global cityname
    cityname = data['name']
    global countryname
    countryname = data['sys']['country']
    global weathertoday
    weathertoday = data['weather'][0]['main']
    global temperature
    k=273.15
    temperature = data['main']['temp'] - k
    temperature = round(temperature,2)
    global feelslike
    feelslike = data['main']['feels_like'] - k
    feelslike = round(feelslike, 2)
    global humidity
    humidity = data['main']['humidity']
    global windspeed
    windspeed = data['wind']['speed']
    global visibility
    m = 1000
    visibility = data['visibility'] / m
    global date_time
    date_time = datetime.fromtimestamp(data['dt'])


    # Frame for showing weather result beautifully // this frame is inside output_frame

    weather_output = LabelFrame(output_frame,
        padx=10,
        pady=10)
    weather_output.pack()

    cityname_result = Label(weather_output,
        text=f"{cityname}({countryname}):",
        font=('Arial',15))
    cityname_result.grid(row=0,
        column=0,
        columnspan=2,
        pady=(0,10),
        sticky=W)

    weathertoday_result = Label(weather_output,
        text =  weathertoday,
        font=('Arial',30))
    weathertoday_result.grid(row=1,
        column=0,
        rowspan=2,
        sticky=E,
        padx=(0,10))

    temperature_result = Label(weather_output,
        text = f"{temperature}°C",
        font=('Arial',30))
    temperature_result.grid(row=3,
        column=0,
        rowspan=2,
        sticky=E,
        padx=(0,10))

    feelslike_result = Label(weather_output,
        text = f"Feels like: {feelslike}°C")
    feelslike_result.grid(row=1,
        column=1,
        sticky=W)

    humidity_result = Label(weather_output,
        text = f"Humidity: {humidity}%")
    humidity_result.grid(row=2,
        column=1,
        sticky=W)

    windspeed_result = Label(weather_output,
        text = f"Wind speed: {windspeed} m/sec")
    windspeed_result.grid(row=3,
        column=1,
        sticky=W)

    visibility_result = Label(weather_output,
        text = f"Visibility: {visibility} km")
    visibility_result.grid(row=4,
        column=1,
        sticky=W)

    # Show the save button
    global save_result_button
    save_result_button = Button(output_frame,
        text="Save",
        command=save_button_functions)
    save_result_button.pack()

def save_button_functions():
    save_result()
    disable_save_button()

def disable_save_button():
    save_result_button["state"] = DISABLED

def save_result():
    # Creating the image
    W, H = (1000,1000)
    img = Image.new('RGB', (W,H),color='white')
    draw_result = ImageDraw.Draw(img)

    # Font size of Weather description & Temperature
    big_font_size = 50
    medium_font_size = 40
    # Gap between WeatherDescription-Temperature and other four parameters
    gap_between = 20
    # Font size for other parameters
    small_font_size = 25
    font_url='assets/Roboto_Mono/RobotoMono-VariableFont_wght.ttf'
    small_font = ImageFont.truetype(font_url,small_font_size)
    big_font = ImageFont.truetype(font_url,big_font_size)
    medium_font = ImageFont.truetype(font_url,medium_font_size)

    # Adding date time on left top corner
    date_msg = f"{date_time}"
    draw_result.text((20,20),date_msg, fill='black',font=small_font)

    # Adding city name on the image
    city_msg=f"Weather in {cityname}({countryname}):"
    w, h = draw_result.textsize(city_msg,font=medium_font)
    draw_result.text(((W-w)/2,350), city_msg,fill='black',font=medium_font)

    # Weather description
    description_msg = f"{weathertoday}"
    w, h = draw_result.textsize(description_msg,font=big_font)
    draw_result.text(((W/2)-w-gap_between,(H/2)-h),description_msg,fill='black',font=big_font)

    # Temperature
    temperature_msg = f"{temperature}°C"
    w, h =draw_result.textsize(temperature_msg,font=big_font)
    draw_result.text(((W/2)-w-gap_between,H/2),temperature_msg,fill='black',font=big_font)

    # Humidity
    humidity_msg = f"Humidity: {humidity}%"
    w, h =draw_result.textsize(temperature_msg,font=small_font)
    draw_result.text(((W/2)+gap_between,(H/2)-h),humidity_msg,fill='black',font=small_font)

    # Feels like
    feels_like_msg = f"Feels like: {feelslike}°C"
    w, h =draw_result.textsize(feels_like_msg,font=small_font)
    draw_result.text(((W/2)+gap_between,(H/2)-h-h),feels_like_msg,fill='black',font=small_font)

    # Wind speed
    wind_speed_msg = f"Wind speed: {windspeed}m/s"
    w, h =draw_result.textsize(temperature_msg,font=small_font)
    draw_result.text(((W/2)+gap_between,(H/2)),wind_speed_msg,fill='black',font=small_font)

    # Visibility
    visibility_msg = f"Visibility: {visibility}km"
    w, h =draw_result.textsize(visibility_msg,font=small_font)
    draw_result.text(((W/2)+gap_between,(H/2)+h),visibility_msg,fill='black',font=small_font)

    # Save the image
    image_name = f"weather-{cityname}-{date_time}"
    img.save(f'{image_name}.png')

    image_saved_message = Label(output_frame,text="Weather report is saved.",fg='green')
    image_saved_message.pack()

    img.show()

        
# OK and Exit buttons
button_frame = LabelFrame(root,bd=0)
button_frame.pack(pady=(3,30))

okButton = Button(button_frame, text="OK",command=main_function, fg='blue')
okButton.grid(row=0,column=0,padx=25)

button_quit = Button(button_frame, text="Exit", command=root.destroy,fg='red')
button_quit.grid(row=0,column=1,padx=25)


# Place for showing output
output_frame = LabelFrame(root,bd=0)
output_frame.pack()


# Version
version = Label(root, text = "Version 1.0.0")
version.place(rely=1.0, relx=1.0, x=-5, y=-5, anchor=SE)

root.mainloop()