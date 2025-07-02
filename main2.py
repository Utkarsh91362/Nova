import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import musicLibrary
import requests

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "4cd5829204fa4c0ca83d0f34774ae296"  # Replace if needed

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    c = c.lower().strip()
    print("Command received:", c)

    if "open google" in c:
        speak("Opening Google.")
        webbrowser.open("https://google.com")

    elif "open explorer" in c:
        speak("Opening File Explorer.")
        os.system("explorer")

    elif c.startswith("play"):
        try:
            song = c.split(" ", 1)[1]
            link = musicLibrary.music.get(song)
            if link:
                speak(f"Playing {song}")
                webbrowser.open(link)
            else:
                speak(f"Sorry, I couldn't find the song {song}.")
        except Exception as e:
            speak("Something went wrong while trying to play the song.")
            print("Music Error:", e)

    elif any(keyword in c for keyword in ["news", "tell me the news", "latest news", "headlines"]):
        speak("Fetching top news .")
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
            r = requests.get(url)
            print("Status Code:", r.status_code)

            if r.status_code == 200:
                data = r.json()
                print("Raw API Response:", data)
                articles = data.get('articles', [])
                print("Number of articles found:", len(articles))

                if not articles:
                    speak("Sorry, no news found.")
                else:
                    for i, article in enumerate(articles[:3], 1):  # Limit to 6 articles
                        title = article.get('title', 'No title available')
                        print(f"{i}. {title}")
                        speak(title)
            else:
                speak("Failed to fetch news. Status code: " + str(r.status_code))
        except Exception as e:
            speak("Something went wrong while fetching the news.")
            print("News Error:", e)

    else:
        speak("Sorry, I didn’t understand that command.")

# Main program loop
if __name__ == "__main__":
    speak("Initializing Nova AI")
    while True:
        try:
            with sr.Microphone() as source:
                print("\n🎤 Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            word = recognizer.recognize_google(audio).lower().strip()
            print("You said:", word)

            if "nova" in word:
                speak("At your service...")
                with sr.Microphone() as source:
                    print("🎤 Nova Active... Listening for command.")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                    command = recognizer.recognize_google(audio)
                    print("Recognized Command:", command)
                    processCommand(command)

            elif "stop" in word:
                speak("Closing Nova. Goodbye.")
                break

        except Exception as e:
            print("⚠️ Error:", e)
