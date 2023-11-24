import speech_recognition as sr
import time
import keyboard
from colorama import Fore, Style
import threading

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Create an Event object
recording_finished = threading.Event()


while True:
    with sr.Microphone() as source:
        # print(Fore.YELLOW + "Speak Anything :" + Style.RESET_ALL)
        try:
            start_time = time.time()
            audio_text = r.listen(source, timeout=0.5)
            end_time = time.time()
            # print(Fore.RED + "Stop." + Style.RESET_ALL)
            print(Fore.CYAN + "Powiedziałeś: " + r.recognize_google(audio_text, language='pl-PL') + Style.RESET_ALL)
            duration = end_time - start_time - 1
            print(Fore.MAGENTA + "Time: " + str(duration) + Style.RESET_ALL)
        except sr.UnknownValueError:
            try:
                print(Fore.BLUE + "You said: " + r.recognize_google(audio_text, language='en-US') + Style.RESET_ALL)
                print(Fore.MAGENTA + "Time: " + str(duration) + Style.RESET_ALL)
            except:
                # print(Fore.RED + "Google Speech Recognition could not understand audio" + Style.RESET_ALL)
                pass
        except sr.WaitTimeoutError:
            pass
        except Exception as e:
            print(Fore.RED + "An error occurred: {0}".format(e) + Style.RESET_ALL)