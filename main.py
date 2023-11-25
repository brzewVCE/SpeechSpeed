import speech_recognition as sr
import time
from colorama import Fore, Style
import multiprocessing
mp_context = multiprocessing.get_context('spawn')
r = sr.Recognizer()

def process_speech():
    words = {}
    with sr.Microphone() as source:
        try:
            #Jakoś mądrzej te 3 sekundy zrobić
            #Czasem dwa razy ten sam tekst (?)
            audio_text = r.listen(source, phrase_time_limit=3)
            process = mp_context.Process(target=process_speech)
            process.start()
            words = r.recognize_google(audio_text, language='pl-PL').split()
            print(Fore.CYAN + "Powiedziałeś: " + r.recognize_google(audio_text, language='pl-PL') + Style.RESET_ALL)
        except sr.UnknownValueError:
            try:
                words = r.recognize_google(audio_text, language='en-US').split()
                print(Fore.BLUE + "You said: " + r.recognize_google(audio_text, language='en-US') + Style.RESET_ALL)
            except:
                pass
        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(Fore.RED + "An error occurred: {0}".format(e) + Style.RESET_ALL)
    # if len(words) != 0:
    #     print(len(words))
    print(words)






if __name__ == '__main__':
    while True:
        process_speech()