import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import musicLibrary
import requests
#pip install pocketsphinx


recognizer=sr.Recognizer()
engine= pyttsx3.init()
newsapi="4cd5829204fa4c0ca83d0f34774ae296"



def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open explorer" in c.lower():
        os.system("explorer")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles=data.get('articles',[])
            for article in articles:
                speak(article['title'])




                

if __name__=="__main__":
    speak("Initializing AI")
    while True:
        #Listen for the wake word "Doc"
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        print("recognizing...")
    # recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Listening....!")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            word=r.recognize_google(audio)
            #word=word.lower()
            print(word)
            if "nova" in word.lower().strip():
                speak("At your service...")
                with sr.Microphone() as source:
                    print("Nova Active....!")
                    audio = r.listen(source)
                    command=r.recognize_google(audio)

                    processCommand(command)
                
                


            elif "stop" in word.lower().strip():
                speak("Closing AI")
                break
                
        except Exception as e:
            print("I think i ran through some error; {0}".format(e))