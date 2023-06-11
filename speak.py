import pyttsx3
import datetime
import speech_recognition as speechrec
import wikipedia
import webbrowser
import os
import smtplib
import subprocess
import wolframalpha
import time
import winshell
import random
import pyjokes
import requests
from requests import get
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from math import log10
import threading
import psutil
from tkinter import messagebox
from tkinter import PhotoImage, Text
import pywhatkit
import pyautogui
from tkinter import *
from PIL import ImageTk, Image
from intent_classifier import IntentClassifier

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio,output):
    output.after(0, lambda: output.insert(END, f"Assistant: {audio}\n"))
    engine.say(audio)
    engine.runAndWait()
    

def set_songvolume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    if volume_level == "loud":
        volume.SetMasterVolumeLevel(0.0, None)  
    elif volume_level == "quiet":
        volume.SetMasterVolumeLevel(-30.0, None)    


def tellMe(output):
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour<12:
        speak("Good Morning!",output)
        
    elif hour>=12 and hour<18:
        speak("Good Afternoon!",output)

    else:
        speak("Good Evening!",output)
        
    speak("Hello I am your Assistant. Please tell me how may I help you?",output)    

def speechCommand(output):
    take = speechrec.Recognizer()
    with speechrec.Microphone() as source:
        print("Listening User...")
        take.pause_threshold = 0.5
        take.adjust_for_ambient_noise(source, duration=2)
        take.dynamic_energy_threshold = True
        audio = take.listen(source)
        
    try:
        print("Recognizing...")
        query = take.recognize_google(audio, language='en-us') 
        print(f"User said: {query}\n")
        output.after(0, lambda: output.insert(END, f"User: {query}\n"))
        
    except Exception as e:               
        print("Please say that again...")
        return "None"
    
    return query 

def set_volume(level):
    speaker = AudioUtilities.GetSpeakers()
    use = speaker.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(use, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(level, None)
    

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login("iders810@gmail.com", "ddsjtydhbsdtcpvh")
    server.sendmail("iders810@gmail.com", to, content)  
    server.close()


def battery_status(percentage):
    if percentage >= 75:
        return "Power level is strong. We can continue our tasks without worries."
    elif 40 <= percentage < 75:
        return "Power level is sufficient, but consider charging soon for uninterrupted work."
    elif 15 <= percentage < 40:
        return "Power is dwindling. It's time to connect the charger."
    else:
        return "Warning! Battery level critical. Connect to power immediately to avoid shutdown."
        
def open_website(website_name, website_url, output):
    speak(f"Are you sure you want to open {website_name}?",output)
    confirm = speechCommand(output)

    if 'yes' in confirm.lower():
        speak(f'Opening {website_name}.',output)
        webbrowser.open(website_url)
        speak(f"{website_name} is now open. Is there anything else you need?",output)
        next_task = speechCommand(output)

        if 'yes' in next_task.lower():
            speak("What do you want me to do next?",output)
        else:
            speak("Okay, let me know if you need something.",output)
    else:
        speak(f"Okay, I won't open {website_name}. What can I assist you with next?",output)   
    
def clear_output(output):
    output.delete(1.0, END)  

def gui():
    master = Tk() 
    master.geometry("1000x500")
    master.title("VAS")

    master.configure(background='#123456')


    output = Text(master, height=13, width=90, bg="light blue", fg="black", font=("Times New Roman", 12))
    output.pack(padx=10, pady=10)

    def start_recognition():
        classifier = IntentClassifier()
        classifier.train()
        try:
            tellMe(output)
            while True:
                start_time = time.perf_counter()
                clear_output(output)
                query = speechCommand(output).lower()
                intent = classifier.predict(query)

                if intent == 'search_wikipedia':
                    speak('Search Wikipedia...',output)
                    query = query.replace("wikipedia", "")
                    try:
                        results = wikipedia.summary(query, sentences=3)
                        speak("According to Wikipedia",output)
                        print(results)
                        speak(results,output)
                    except wikipedia.exceptions.DisambiguationError as e:
                        speak("There are multiple entries that match your search. Could you please be more specific?",output)
                        print("Disambiguation Error: ", e.options)
                    except wikipedia.exceptions.PageError:
                        speak("Sorry, I couldn't find a page that matches your search.",output)
                    except Exception as e:
                        speak("Sorry, an error occurred while searching on Wikipedia.",output)
                        print("Error: ", str(e))    
                        
                elif intent == 'play_music':
                    if "loudly" in query:
                        set_songvolume("loud")
                    elif "quietly" in query:
                        set_songvolume("quiet")
                        
                    speak('Playing Music.',output)
                    time.sleep(2)
                    music_directory = 'C:\\Music\\2010s\\Classical Music' 
                    songs = os.listdir(music_directory)
                    os.startfile(os.path.join(music_directory, songs[0]))
                          
                            
                elif intent == 'play_music_random':
                    if "loudly" in query:
                        set_songvolume("loud")
                    elif "quietly" in query:
                        set_songvolume("quiet")
                        
                    speak('Playing Music Random.',output)
                    time.sleep(2)
                    music_directory = 'C:\\Music\\2010s\\Classical Music' 
                    songs = os.listdir(music_directory)
                    r = random.choice(songs)
                    os.startfile(os.path.join(music_directory, r))            
                    
                elif intent == 'open_youtube':
                    open_website('Youtube', 'https://youtube.com/',output)
                    
                elif intent == 'open_whatsapp':
                    open_website('Whatsapp', 'https://web.whatsapp.com/',output)

                elif intent == 'open_google':
                    open_website('Google', 'https://google.com/',output)

                elif intent == 'open_twitter':
                    open_website('Twitter', 'https://twitter.com/',output)

                elif intent == 'open_yandex':
                    open_website('Yandex', 'https://yandex.com/',output)

                elif intent == 'open_opera':
                    open_website('Opera', 'https://opera.com/',output)

                elif intent == 'open_stackoverflow':
                    open_website('Stackoverflow', 'https://stackoverflow.com/',output)

                elif intent == 'open_facebook':
                    open_website('Facebook', 'https://facebook.com/',output)

                elif intent == 'open_instagram':
                    open_website('Instagram', 'https://instagram.com/',output)

                elif intent == 'open_gmail':
                    open_website('Gmail', 'https://mail.google.com/mail/',output)

                elif intent == 'open_maps':
                    open_website('Google Maps', 'https://www.google.co.in/maps/',output)

                elif intent == 'open_googlenews':
                    open_website('Google News', 'https://news.google.com/',output)

                elif intent == 'open_calendar':
                    open_website('Google Calendar', 'https://calendar.google.com/calendar/',output)

                elif intent == 'open_documents':
                    open_website('Google Documents', 'https://docs.google.com/document/',output)

                elif intent == 'open_amazon':
                    open_website('Amazon', 'https://www.amazon.com/',output)     
                                                                                    

                elif intent == 'get_time':
                    Timetostring = datetime.datetime.now().strftime("%H:%M:%S") 
                    speak(f"The time is {Timetostring}.",output)
                    
                elif intent == 'get_day':
                    day = datetime.datetime.today().weekday() + 1  
                    week_Days = {1: 'monday', 2: 'tuesday', 3: 'wednesday',4: 'thursday', 5: 'friday', 6: 'saturday',7: 'sunday'}  
                    if day in week_Days.keys():
                        current_day = week_Days[day]
                        speak(current_day,output)
                        print(current_day)
                 
                elif intent == 'get_date':
                    def suffix(d):
                        return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

                    today = datetime.date.today()
                    day_with_suffix = str(today.day) + suffix(today.day)

                    speak(f"Today is {today.strftime('%B')} {day_with_suffix}, {today.strftime('%Y')}.",output) 
                                                         
                                            
                elif intent == 'get_joke':
                    speak("Let me tell you a joke!",output)
                    time.sleep(2)
                    speak(pyjokes.get_joke(),output) 
                    print(pyjokes.get_joke()) 
                
                    
                elif intent == 'battery':
                    cpu_usage = psutil.cpu_percent()
                    speak(f"Current CPU usage is {cpu_usage}%",output)
                    
                    battery_info = psutil.sensors_battery()
                    battery_percentage = battery_info.percent
                    speak(f"The system currently has {battery_percentage}% battery power",output)
                    
                    speak(battery_status(battery_percentage),output)
                 
                elif intent == 'volume_medium':
                    set_volume(-8.0)
                    speak(f'Volume has been set to {-8.0} decibels.',output)
                    speak('Is there anything else you need?',output)

                elif intent == 'volume_high':
                    set_volume(-2.0)
                    speak(f'Volume has been set to {-2.0} decibels.',output)
                    speak('Is there anything else you need?',output)

                elif intent == 'volume_low':
                    set_volume(-30.0)
                    speak(f'Volume has been set to {-30.0} decibels.',output)
                    speak('Is there anything else you need?',output)

                elif intent == 'volume_minimum':
                    set_volume(-60.0)  
                    speak(f'Volume has been set to {-60.0} decibels.',output)
                    speak('Is there anything else you need?',output) 
                 
                elif intent == 'open_code':
                    speak('Opening Vscode',output)
                    vscodepath = "C:\\Users\\cagri\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                    os.startfile(vscodepath)
                
                elif intent == 'close_code':  
                    speak('Closing  Vscode.',output)           
                    os.system("taskkill /f /im Code.exe")       
                
                elif intent == 'open_eclipse':
                    speak('Opening Eclipse',output)
                    eclipsepath = "C:\\Users\\cagri\\eclipse\\java-2022-09\\eclipse\\eclipse.exe"   
                    os.startfile(eclipsepath)
                    
                elif intent == 'close_eclipse':  
                    speak('Closing Eclipse.',output)           
                    os.system("taskkill /f /im eclipse.exe")      
                    
                    
                elif intent == 'open_excel':
                    speak('Opening Excel',output)
                    excelpath = '"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"' 
                    os.startfile(excelpath)  
                    
                elif intent == 'close_excel':  
                    speak('Closing Excel.',output)           
                    os.system("taskkill /f /im EXCEL.EXE")      
                    
                elif intent == 'open_discord':  
                    speak('Opening Discord.',output)
                    discordpath = "C:\\Users\\cagri\\AppData\\Local\\Discord\\app-1.0.9013\\Discord.exe"
                    os.startfile(discordpath)
                    
                elif intent == 'open_steam':  
                    speak('Opening Steam.',output)
                    steampath = "C:\\Program Files (x86)\\Steam\\steam.exe"
                    os.startfile(steampath)     
            
                elif intent == 'close_steam':
                    speak('Closing Steam.',output)           
                    os.system("taskkill /f /im steam.exe")  
                            
                    
                elif intent == 'close_discord':  
                    speak('Closing Discord.',output)           
                    os.system("taskkill /f /im Discord.exe")  
                    
                    
                elif intent == 'open_word':  
                    speak('Opening Word.',output)
                    wordpath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
                    os.startfile(wordpath)   
                    
                elif intent == 'close_word':  
                    speak('Closing Word.',output)           
                    os.system("taskkill /f /im WINWORD.EXE")      
                    
                elif intent == 'open_notepad++':  
                    speak('Opening Notepad++.',output)
                    code_notepad = "C:\\Program Files (x86)\\Notepad++\\notepad++.exe"
                    os.startfile(code_notepad)   
                    
                elif intent == 'close_notepad++':  
                    speak('Closing Notepad++.',output)           
                    os.system("taskkill /f /im notepad++.exe")          
                
                elif intent == 'open_powerpoint':  
                    speak('Opening PowerPoint.',output)
                    powerpoint_path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
                    os.startfile(powerpoint_path)
                    
                elif intent == 'close_powerpoint':  
                    speak('Closing PowerPoint.',output)           
                    os.system("taskkill /f /im POWERPNT.EXE")        
                            
                    
                elif intent == 'open_paint':
                    speak('Opening paint.',output)
                    subprocess.Popen('C:\\Windows\\System32\\mspaint.exe')
                    
                elif intent == 'close_paint':  
                    speak('Closing Paint.',output)           
                    os.system("taskkill /f /im mspaint.exe")            
                
                elif intent == 'open_calculator':
                    speak('Opening calculator.',output)
                    subprocess.Popen('C:\\Windows\\System32\\calc.exe')
                    
                elif intent == 'close_calculator':  
                    speak('Closing Calculator.',output)           
                    os.system("taskkill /f /im calc.exe")     
                    
                elif intent == 'open_notepad':
                    speak('Opening notepad.',output)
                    subprocess.Popen('C:\\Windows\\System32\\notepad.exe')
                    
                elif intent == 'close_notepad':  
                    speak('Closing Notepad.',output)           
                    os.system("taskkill /f /im notepad.exe")         
                    
                elif intent == 'open_tool':
                    speak('Opening SnippingTool.',output)
                    subprocess.Popen('C:\\Windows\\System32\\SnippingTool.exe')    
                
                elif intent == 'close_tool':  
                    speak('Closing SnippingTool.',output)           
                    os.system("taskkill /f /im SnippingTool.exe")   
                
                elif intent == 'email_that': 
                    try:
                        speak("What would you to like me write?",output)
                        content = speechCommand(output)                
                        to = "berat.oztelli@gmail.com"
                        sendEmail(to, content)
                        speak("Email has been sent!",output)
                    except Exception as e:
                        print(e)
                        speak("Error.I cant send this mail.",output)
                        
                elif intent == 'take_note':
                    speak("What would you like to note down?",output)
                    note_content = speechCommand(output)

                    with open('reminder.txt', 'w') as file:        
                        current_time = datetime.datetime.now().strftime("%H:%M:%S")
                        file.write(f'{current_time} :- {note_content}\n')
                            
                elif intent == 'show_note':
                    speak("Showing Notes",output)
                    with open("reminder.txt", "r") as file:
                        content = file.read()
                        print(content)
                        speak(content,output) 
                
                elif intent == 'screenshot':
                    try:
                        speak("What would you like to name the screenshot?",output)
                        name = speechCommand(output).replace(' ', '_')

                        if os.path.isfile(f"{name}.png"):
                            speak(f"A file with the name {name} already exists. Would you like to overwrite it?",output)
                            response = speechCommand(output)
                            if 'yes' in response.lower():
                                speak("Please hold on, I will take the screenshot in 3 seconds.",output)
                                time.sleep(3)
                                img = pyautogui.screenshot()
                                img.save(f"{name}.png")
                                speak("Screenshot saved in the main directory.",output)
                            else:
                                speak("Please provide a new name for the screenshot.",output)
                        else:
                            speak("Please hold on, I will take the screenshot in 3 seconds.",output)
                            time.sleep(3)
                            img = pyautogui.screenshot()
                            img.save(f"{name}.png")
                            speak("Screenshot saved in the main directory.",output)
                            
                    except Exception as e:
                        print(e)
                        speak("I'm sorry, I couldn't take the screenshot. Please try again.",output)      
                                            
                elif intent == 'how_are_you':
                    speak("I am fine, Thank you",output)
                    speak("How are you?",output)
                
                elif intent == 'good':
                    speak("I am delighted about this news.",output)
                    
                elif intent == 'not_good':
                    speak("I am sorry, How can I help you?",output)
                    
                elif intent == 'what_are_you':
                    speak("I am helpful virtual assistant.",output)  
                    
                elif intent == 'who_are_you':
                    speak("My name is VAS.",output) 
                    
                elif intent == 'are_you_okay':       
                    speak("Yes I am.",output)

                elif intent == 'how_old_are_you':
                    speak("I am 1 years old.",output)
                    
                elif intent == 'are_you_tired':
                    speak("No I am not.I am always at your service.",output)

                elif intent == 'do_you_like_music':
                    speak("Yes i like music.",output)
                
                elif intent == 'most_asked_topics':
                    speak("First is Music Second is News then third is How to instructions.",output)
                    
                elif intent == 'do_you_know_who_am_i':
                    speak("Yes you are the user.",output)
                                
                elif intent == 'can_you_hear_me':
                    speak('Yes, I can hear you',output)
                    
                elif intent == 'greet':
                    speak("Hi",output)                        
                 
                elif intent == 'stop_listening':
                    speak("For how long do you want me to stop listening to commands?",output)
                    duration = speechCommand(output)
                    try:
                        if duration.isdigit():
                            duration = int(duration)
                            if duration < 1:
                                speak("Sorry, I didn't get that. Please specify a valid duration in minutes.",output)
                            elif duration == 1:
                                speak(f"Alright, I will stop listening for {duration} minute. Call me if you need anything.",output)
                                time.sleep(duration * 60)
                                print(f"Stopped listening for {duration} minute.")
                            else:
                                speak(f"Alright, I will stop listening for {duration} minutes. Call me if you need anything.",output)
                                time.sleep(duration * 60)
                                print(f"Stopped listening for {duration} minutes.")
                        else:
                            speak("Sorry, I couldn't understand the duration you specified. Please try again.",output)
                                
                    except Exception as e:
                        print(e)
                        speak("I'm sorry, I couldn't process your request. Please try again.",output) 
                 
                 
                elif intent == 'search':
                    
                    query = query.replace("search", "")      
                    webbrowser.open(query)
                                
                                
                elif intent == 'play_song':
                    speak("What do you want me to play?",output)
                    song = speechCommand(output)
                    
                    if 'play' in song:
                        song = song.replace("play", "").strip()

                    speak("Preparing to play " + song,output)
                    print(f'Playing {song}')
                    pywhatkit.playonyt(song)             
                                                
                elif intent == 'sign_out':
                    speak("Are you sure you want to sign out? All running applications will be closed.",output)
                    confirm = speechCommand(output)
                    if 'yes' in confirm.lower():
                        speak("Signing out in 5 seconds. Save all your work.",output)
                        time.sleep(5)
                        subprocess.call(["shutdown", "/l"])
                    else:
                        speak("Sign out cancelled.",output)

                elif intent == 'restart':
                    speak("Are you sure you want to restart the system? All running applications will be closed.",output)
                    confirm = speechCommand(output)
                    if 'yes' in confirm.lower():
                        speak("System will restart in 5 seconds. Save all your work.",output)
                        time.sleep(5)
                        subprocess.call(["shutdown", "/r"])
                    else:
                        speak("System restart cancelled.",output)

                elif intent == 'sleep':
                    speak("Are you sure you want to put the system to sleep?",output)
                    confirm = speechCommand(output)
                    if 'yes' in confirm.lower():
                        speak("Putting the system to sleep in 5 seconds. Save all your work.",output)
                        time.sleep(5)
                        os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")
                    else:
                        speak("Sleep mode cancelled.",output) 
                 
                elif intent == 'empty_recycle':
                    speak("Are you sure you want to empty the recycle bin?",output)
                    confirm = speechCommand(output)
                    if 'yes' in confirm.lower():
                        winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
                        speak("Recycle Bin has been emptied.",output)
                    else:
                        speak("Recycle bin emptying cancelled.",output)
                            
                elif intent == 'shutdown':
                    speak("Are you sure you want to shut down the system? All running applications will be closed.",output)
                    confirm = speechCommand(output)
                    if 'yes' in confirm.lower():
                        speak("System will shut down in 5 seconds. Save all your work.",output)
                        time.sleep(5)
                        subprocess.call("shutdown /s /t 1")
                    else:
                        speak("System shutdown cancelled.",output)  
                    
                elif intent == 'what_is':
                    
                    question = wolframalpha.Client("EXGL48-GLQU3K37KP")
                    
                    try:
                        result = question.query(query)

                        if result.success:
                            answer_text = next(result.results).text

                            print(answer_text)
                            speak(answer_text,output)

                        else:
                            print("No results found for your query.")
                            speak("No results found for your query.",output)

                    except StopIteration:
                            print("No results found for your query.")
                            speak("No results found for your query.",output)

                    except Exception as e:
                            print(f"An error occurred: {e}")
                            speak(f"An error occurred: {e}",output)
                                                
                    
                elif intent == 'calculate':
                    app_id = "EXGL48-GLQU3K37KP"
                    client = wolframalpha.Client(app_id)
                    
                    try:
                        indx = query.lower().split().index('calculate')
                        query = query.split()[indx + 1:]
                        calculation_query = ' '.join(query)

                        if calculation_query:
                            print(f"Processing the calculation: {calculation_query}")
                            speak(f"Processing the calculation: {calculation_query}",output)
                            res = client.query(calculation_query)

                            if res.results:
                                answer = next(res.results).text
                                print(f"The answer is {answer}")
                                speak(f"The answer is {answer}",output)
                            else:
                                print("Sorry, I couldn't find an answer to that calculation.")
                                speak("Sorry, I couldn't find an answer to that calculation.",output)
                        else:
                            print("You asked for a calculation but did not provide one.")
                            speak("You asked for a calculation but did not provide one.",output)

                    except Exception as e:
                        print(f"An error occurred while processing the calculation: {e}")
                        speak(f"An error occurred while processing the calculation: {e}",output)  
                
                elif intent == 'where_is':
                    query = query.replace("where is", "").strip()
                    
                    if not query:  
                        print("You've asked for a location but haven't specified one.")
                        speak("You've asked for a location but haven't specified one.",output)
                        

                    area = query.replace("+", " ").title()

                    print(f"User asked to locate: {area}")
                    speak(f"User asked to locate: {area}",output)
                    
                    try:
                        url = f"https://www.google.nl/maps/place/{query}"
                        webbrowser.open(url)
                        print(f"Opening Google Maps for: {area}")
                        speak(f"Opening Google Maps for: {area}",output)
                    except webbrowser.Error as e:
                        print(f"An error occurred while trying to open the location on Google Maps: {str(e)}")
                        speak(f"An error occurred while trying to open the location on Google Maps: {str(e)}",output)    
            
                elif intent == 'tell_me_the_news':
                        url = "https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=75449f74c8ed4e549d20f8bb3f5d36c5"

                        response = get(url)
                        
                        if response.status_code == 200:
                            www_url = response.json()
                            articles = www_url.get("articles", [])

                            if articles:
                                speak("Here are the top news:",output)
                                
                                ordinal_numbers = ['first', 'second', 'third', 'fourth', 'fifth']
                                headlines = [article.get('title', '') for article in articles]

                                for i, ordinal in enumerate(ordinal_numbers):
                                    if i < len(headlines):
                                        print(f"Today's {ordinal} news is: {headlines[i]}")
                                        speak(f"Today's {ordinal} news is: {headlines[i]}",output)
                                    else:
                                        break

                                speak("That's all the news I have right now.",output)
                            else:
                                print("I'm sorry, but I couldn't find any news at this time.")
                                speak("I'm sorry, but I couldn't find any news at this time.",output)
                        else:
                            print("I'm sorry, but I'm unable to access the news at this time.")
                            speak("I'm sorry, but I'm unable to access the news at this time.",output)
                            
                            
                
                elif intent == 'weather':
                    api_key = "b68571ee7ad85dac819bd12033e3dfb1"
                    ip_address = requests.get('https://api.ipify.org').text
                    geo_url = f'https://get.geojs.io/v1/ip/geo/{ip_address}.json'
                    geo_response = requests.get(geo_url)

                    if geo_response.status_code == 200:
                        geo_data = geo_response.json()
                        city = geo_data.get('city', '')

                        if city:
                            weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
                            weather_response = requests.get(weather_url)

                            if weather_response.status_code == 200:
                                weather_data = weather_response.json()
                                main_weather = weather_data.get('weather', [{}])[0].get('main', '')
                                description = weather_data.get('weather', [{}])[0].get('description', '')
                                temperature = weather_data.get('main', {}).get('temp', '')
                                temperature = round(temperature - 273.15, 2) 

                                speak(f"The current weather in {city} is {main_weather} with {description}. The temperature is {temperature}°C.",output)
                            else:
                                speak("I'm sorry, I couldn't access the weather data.",output)
                        else:
                            speak("I'm sorry, I couldn't determine your city based on your IP address.",output)
                    else:
                        speak("I'm sorry, I couldn't get your geographical data.",output)                                       
                    
                elif intent == 'exit':
                    speak("Are you sure you want to exit the program?",output)
                    confirm = speechCommand(output)
                    
                    if 'yes' in confirm.lower():
                        speak("Understood. Before I go, is there anything else you need?",output)
                        last_request = speechCommand(output)

                        if 'no' in last_request.lower():
                            speak("Alright, thank you for using me. Goodbye!",output)
                            time.sleep(2)
                            print("Exited the program.")
                            master.destroy()
                            exit()
                            
                        else:
                            speak("I'm sorry, I didn't understand that. Please repeat or say 'no' if you don't need anything else.",output)
                    else:
                        speak("Okay, I'm here if you need any assistance.",output)
                    
                    
                elif intent == 'thank_you':
                    speak("You're welcome.",output)    
                    
                        
                end_time = time.perf_counter() 
                response_time = end_time - start_time
                print(f"Response time: {response_time} seconds") 
        except Exception as e:
            messagebox.showerror("Error", "An error occurred.\n"+str(e))
            
    microphone_img= 'mic.png'        
    microphone_img = Image.open('mic.png')
    microphone_img_resized = microphone_img.resize((100, 100), Image.ANTIALIAS)
    microphone_image = ImageTk.PhotoImage(microphone_img_resized)          
        
    recognize_button = Button(master, image=microphone_image, command=lambda: threading.Thread(target=start_recognition).start(), bd=0, bg="#123456", activebackground="#123456")
    recognize_button.image = microphone_image
    recognize_button.pack(pady=20)

    mainloop()

if __name__ == "__main__":
    gui()
