import speech_recognition as sr
import webbrowser
import musiclibrary
import pyttsx3
import requests
from playsound import playsound
import time
import cv2
import threading

recognizer = sr.Recognizer()

def speak(text):
    engine = pyttsx3.init()  # NEW ENGINE EVERY TIME
    engine.say(text)
    engine.runAndWait()
    news_api = "bcd161e06ae44f628f4dcf387c3c16bd"
    del engine   # release the engine so it works next time

def play_video():
    cap = cv2.VideoCapture("interface.mp4")

    cv2.namedWindow("JARVIS INTERFACE", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("JARVIS INTERFACE", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_MSEC, 3000)  # restart from 3 seconds
            continue

        screen_w = cv2.getWindowImageRect("JARVIS INTERFACE")[2]
        screen_h = cv2.getWindowImageRect("JARVIS INTERFACE")[3]

        if screen_w > 0 and screen_h > 0:
            frame = cv2.resize(frame, (screen_w, screen_h))

        cv2.imshow("JARVIS INTERFACE", frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def processcommand(c):
    c_lower = c.lower().replace("'", "").strip()  # normalize input

    if "open youtube" in c_lower:
        playsound("task.mp3.mp3")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in c_lower:
        playsound("task.mp3.mp3")
        webbrowser.open("https://www.google.com")
    elif "open whatsapp" in c_lower:
        webbrowser.open("https://web.whatsapp.com/")
        playsound("task.mp3.mp3")
    elif "what is your name" in c_lower:
        speak("My name is Jarvis and you designed me boss , i am at your service")
    elif "how are you" in c_lower:
        speak("I am fine, thank you")
    elif "instagram" in c_lower:
        webbrowser.open("https://www.instagram.com")
        playsound("task.mp3.mp3")
    elif c_lower.startswith("play"):
        song = c_lower.split(" ")[1]
        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song} boss")
        else:
            speak("Song not found boss")
    elif "news" in c_lower:
        try:
            r = requests.get(
                "https://newsapi.org/v2/top-headlines?country=pk&apiKey=bcd161e06ae44f628f4dcf387c3c16bd"
            )
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])[:5]
                if articles:
                    for i, article in enumerate(articles, 1):
                        speak(f"News {i}: {article['title']}")
                else:
                    speak("No news available right now.")
            else:
                speak("Sorry, could not fetch news.")
        except:
            speak("There was an error fetching news.")
    elif "daddys home" in c_lower or "boss home" in c_lower:
        speak("Welcome back boss")
    elif "who designed you" in c_lower:
        speak("You designed me boss..")


if __name__ == "__main__":

    video_thread = threading.Thread(target=play_video, daemon=True)
    video_thread.start()

    playsound("alert.mp3.wav")
    time.sleep(0.0001)
    playsound("jarvis.mp3")

    print("NOW IM FULLY ACTIVATED!")
    playsound("active.mp3")
    while True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("listening....")
                audio = r.listen(source)

            heard = r.recognize_google(audio)
            print("Heard:", heard)

            processcommand(heard)

            if "jarvis" in heard.lower():
                playsound("wakeword.mp3")

            with sr.Microphone() as source:
                print("jarvis active....")
                audio = r.listen(source)
                command = r.recognize_google(audio)
                processcommand(command)

        except Exception as e:
            print("Error {0}".format(e))
            playsound("eror.mp3")
