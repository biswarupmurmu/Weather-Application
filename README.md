# A very simple and stupid weather application with a GUI

This python program can take input(a city name) from the user and show the current weather report of that city.

### Requirements

  #### Modules
- The modules required to run this python program are listed in the "*requirements.txt*" file. You can install those modules manually or you can open the terminal and go to this project's root directory and simply run
`pip install -r requirements.txt`.
  #### API key
 - This program uses a third party weather API (https://openweathermap.org/api) to get the weather report. To get a new API key from https://openweathermap.org/api for free all you need to do is to sign up in the website using your email. When you complete the sign up process you will get an API key. Now open the 'weather.py' file in your favourite text editor ang go to line 6 where you will find a variable named `api_key` and assign the API key to that variable like `api_key = "api-key-from-openweather.org"`.

### How to run
After installing the required modules you can run the program `weather.py` in the terminal(yes, you have to be in this project's root directory) using the command:
`python3 wether.py`.


### Feature(s):
- Save the weather report
