import speech_recognition as sr 
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import time

MASTER = "Pai"
AI_NAME = "kibo"

mendengarkan = sr.Recognizer()
engine = pyttsx3.init("sapi5")

#kecepatan baca
rate = engine.getProperty('rate')
engine.setProperty('rate', 125)

#jenis suara [0] male [1] female
voices = engine.getProperty('voices')
engine.setProperty ('voice', voices[0].id)

def talk(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.3)
      
def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
         talk(f"Hello {MASTER}, Good Morning, I'am {AI_NAME}, your privat AI ")
    elif hour >= 12 and hour < 18:
         talk(f"Hello {MASTER}, Good Afternoon, I'am {AI_NAME}, your privat AI ")
    else:
         talk(f"Hello {MASTER}, Good Evening, I'am {AI_NAME}, your privat AI ")


def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            mendengarkan.adjust_for_ambient_noise(source)
            print("listening...")
            voice = mendengarkan.listen(source, timeout=2, phrase_time_limit=2)
            command = mendengarkan.recognize_google(voice)
            command = command.lower().strip()

        if AI_NAME.lower() in command:
            command = command.replace(AI_NAME.lower(), "").strip()

    except sr.WaitTimeoutError:
        print("no speech detected.")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except Exception as e:
        print("Terjadi Eror:", e)

    return command

def run_kibo():
    command = take_command()
    print("Command received:", command)
    if command == "":
        talk("i didn't get that, please say again")
        return

    if 'play' in command:
        song = command.replace("play", "").strip()
        talk("playing"+ song)
        pywhatkit.playonyt(song)

    elif "time" in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        talk("now is "+ time_now)
        
    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        talk("Searching Wikipedia...")
        try:
            info = wikipedia.summary(topic, sentences=1)
            talk(info)
        except Exception as e:
            talk("Sorry, i could not find that topic.")
            print("Wikipedia error:", e)

    elif "hello" in command or "hi" in command:
        talk(f"Hello {MASTER}, how are you?")
        
    else:
        talk("I didn't get that, please say again")
    
    
wishMe()
time.sleep(0.5)

while True:
    
    time.sleep(0.5)
    run_kibo()
    