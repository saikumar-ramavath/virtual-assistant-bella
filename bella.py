import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import smtplib
import pyjokes


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# choosing voices, print(voices[0].id)
engine.setProperty(voices, voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 0.8
        r.energy_threshold = 450
        audio = r.listen(source)

    try:
        print('Recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said : {query}\n")

    except Exception as exp:
        # print(exp)
        if Active == 1:
            print('say that again please')
            speak('say that again please')
        return 'None'
    return query

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good Morning')
    elif hour >= 12 and hour < 18:
        speak('Good Afternoon')
    else:
        speak('Good Evening')    

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # Intialize mail id and mail password here
    server.login('mailid@gmail.com', 'mailpassword')
    server.sendmail('mailid@gmail.com', to, content)
    server.close()

def exists(commands, query):
    for command in commands:
        if command in query:
            return True

class user:
    name = ''
    def set_username(self, name):
        self.name = name
    
Active = 0
username = user()


if __name__ == "__main__":
    if username.name:
        speak(f"Hi, Im bella, a virtual assistant of {username.name}")
    else:
        speak('Hi, Im bella, a virtual assistant')

    while True:
        query = takecommand().lower()

        if  exists(['active', 'activate', 'activate bella'], query) and 'deactivate' not in query:
            Active = 1
            wishme()
            speak('how can i help you')
            continue

        if Active == 0:
            continue

        if 'wikipedia' in query:
            speak('Searching Wikipedia')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=1)
            print('According to wikipedia', results)
            speak(f'According to wikipedia, {results}')

        #close program terminates the program
        elif exists(['close program', 'terminate program', 'deactivate', 'shutdown'], query):
            speak('program as been terminated, you have to manually start it nexttime to awake bella, take care bye')
            exit()

        elif exists(['who are you', "what's your name", "your name"], query):
            if username.name:
                speak(f"Im bella, a virtual assistant of {username.name}")
            else:
                speak(f"Im bella, a virtual assistant, what's your name?")

        elif exists(['my name is'], query):
            if "not" in query:
                speak("ok, what's your name?")
            else:
                name = query.split("is")[-1].strip()
                speak(f"okay, I will remember that {name}")
                username.set_username(name)

        elif exists(["latest news", "news"], query):
            speak("here's the latest news for you")
            url = "https://news.google.com/topstories?gl=IN&hl=en-IN&ceid=IN:en"
            webbrowser.get().open(url)

        elif exists(["joke"], query):
            speak(pyjokes.get_joke())

        elif "close" and "browser" in query:
            speak("closing browser")
            os.system("taskkill /im chrome.exe /f")

        elif 'open youtube' in query or 'in youtube' in query:
            speak('opening youtube')
            if 'open youtube' in query:
                url = 'https://www.youtube.com/'
                webbrowser.get().open(url)
            else:
                result = query.split("in")[0].strip()
                url = f"https://www.youtube.com/results?search_query={result}"
                webbrowser.get().open(url)

        elif exists(["who made you", "who created you"], query) or "your developer" in query and "email" not in query:
            speak("I was created by sai kumar, as a virtual assistant, to make people life easier")

        elif exists(['search', 'search for', 'who is'], query):
            speak('here what i found')

            if exists(["who is"], query):
                result = query.split("is")[-1].strip()
                speak(f'Here is what I found about {result} on google')
                url = f"https://google.com/search?q={result}"
                webbrowser.get().open(url)
                continue

            result = query.split('search')[-1].strip()
            url = f"https://google.com/search?q={result}"
            webbrowser.get().open(url)

        elif 'open google' in query:
            speak('opening google')
            webbrowser.get().open('https://www.google.com')

        elif 'play music' in query:
            speak('playing music')
            pass

        elif 'the time' in query or "what's the time" in query:
            strtime = datetime.datetime.now().strftime('%H:%M:%S')
            print(strtime)
            if strtime[0:2] == '00':
                speak(f"sir, it's midnight {strtime}")
            elif int(strtime[0:2]) >=0 and int(strtime[0:2]) < 12:
                speak(f"sir, it's morning {strtime}")
            elif int(strtime[0:2]) >= 12 and int(strtime[0:2]) < 6:
                speak(f"sir, it's afternoon {strtime}")
            else:
                speak(f"sir, it's evening {strtime}")    

        elif 'open chrome' in query:
            chrome = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            speak('opening chrome')
            os.startfile(chrome)        

        elif exists(["how are you", "how are you doing"], query):
            speak(f"I'm doing good, thanks for asking {username.name}")

        elif exists(["what are you doing"], query):
            replies = ["watching beautifull sky", "Exploring beautifull World", "nothing, just chilling"]
            reply = replies[random.randint(0, len(replies)-1)]
            speak(reply)

        elif exists(["location of"], query):
            result = query.split("of")[-1].strip()
            speak(f"Getting, location of {result}")
            url = f"https://www.google.com/maps/place/{result}"
            webbrowser.get().open(url)
        
        elif 'email' in query and 'developer' in query:
            try:
                speak('what should i say?')
                content = takecommand()
                # Developer mail id here
                to = 'developermail@gmail.com'
                sendEmail(to, content)
                speak('email has been sent!')

            except Exception as e:
                speak('failed to send email')

        elif 'send email' in query or 'open mail' in query:
            if 'open mail' in query:
                speak("opening mail")
                url = "https://mail.google.com/mail/u/0/#inbox"
                webbrowser.get().open(url)
                continue

            speak("Do you want to open in web?")
            judge = takecommand().lower()

            if 'yes' in judge or 'yep' in judge:
                speak(f"opening mail")
                url = "https://mail.google.com/mail/u/0/#inbox"
                webbrowser.get().open(url)
                continue

            try:
                speak('email address of receiver')
                to = takecommand().lower()
                to = to.replace(' ', '')
                to_temp = to
                print('email of receiver:', to)
                speak(f'email address of receiver is {to}, is it correct?')
                judge = takecommand().lower()

                if 'no' in judge and 'no idea' not in judge and "don't know" not in judge:
                    speak('sorry, failed to send it')
                    continue

                elif "don't know" in judge or "no idea" in judge:
                    speak('do you want me to spell it?')
                    spell = takecommand().lower()
                    if 'yes' in spell:
                        for i in range(len(to_temp)):
                            speak(to_temp[i])
                    speak('do you want to send it?')
                    correctness = takecommand().lower()
                    if 'no' in correctness:
                        speak('okay, email has not sent')
                        continue

                to = to + '@gmail.com'
                speak('what should i say?')
                content = takecommand()
                sendEmail(to, content)
                speak('email has been sent!')

            except Exception as e:
                speak('failed to send email')

        elif exists(['goodbye', 'bye', 'bella sleep' ,'exit', 'quit', 'bella exit', 'bella quit'], query):
            speak('bye take care, going to sleep')
            Active = 0

        elif exists(['on google', 'in google'], query):
            speak('here what i found')
            result = query.split('google')[0]
            url = f"https://google.com/search?q={result}"
            webbrowser.get().open(url)


            