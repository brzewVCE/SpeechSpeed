import speech_recognition as sr
import time
from colorama import Fore, Style
import multiprocessing
mp_context = multiprocessing.get_context('spawn')
r = sr.Recognizer()

def process_speech():
    with sr.Microphone() as source:
        # print(Fore.YELLOW + "Speak Anything :" + Style.RESET_ALL)
        try:
            audio_text = r.listen(source, timeout=0.5, phrase_time_limit=3)
            process = mp_context.Process(target=process_speech)
            process.start()
            # print(Fore.RED + "Stop." + Style.RESET_ALL)
            print(Fore.CYAN + "Powiedziałeś: " + r.recognize_google(audio_text, language='pl-PL') + Style.RESET_ALL)
        except sr.UnknownValueError:
            try:
                print(Fore.BLUE + "You said: " + r.recognize_google(audio_text, language='en-US') + Style.RESET_ALL)
            except:
                # print(Fore.RED + "Google Speech Recognition could not understand audio" + Style.RESET_ALL)
                pass
        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(Fore.RED + "An error occurred: {0}".format(e) + Style.RESET_ALL)







if __name__ == '__main__':
    while True:
        process_speech()