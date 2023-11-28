import speech_recognition as sr
import time
from colorama import Fore, Style
import multiprocessing
import argparse
import sys

mp_context = multiprocessing.get_context('spawn')
r = sr.Recognizer()
r.energy_threshold = 0
r.dynamic_energy_threshold = False


def print_col(text, color):
    color_constant = getattr(Fore, color.upper(), None)
    if color_constant:
        print(color_constant + text + Style.RESET_ALL)
    else:
        print(text)

def print_wpm(words):
    wpm = len(words) / 3 * 60
    sys.stdout.write("\rWords per minute: {0}".format(wpm))
    sys.stdout.flush()

def process_speech(process_num, output_mode=False):
    # if output_mode:
    print_col(f"Started process_speech() function number {process_num}", "red")
    time.sleep(3)
    words = {}
    with sr.Microphone() as source:
        try:
            #Nagryawnie jest 2 procesy przed procesem rozpoznawania mowy
            process = mp_context.Process(target=process_speech, args=(process_num+1,output_mode,))
            process.start()
            audio_text = r.listen(source, phrase_time_limit=3)
            words = r.recognize_google(audio_text, language='pl-PL').split()
        except sr.UnknownValueError:
            try:
                words = r.recognize_google(audio_text, language='en-US').split()
            except:
                pass
        except sr.WaitTimeoutError:
            pass
        except KeyboardInterrupt:
            process.terminate()
            return print_col(f"Interrupted process_speech() function number {process_num}", "red")
        except Exception as e:
            print(Fore.RED + "An error occurred: {0}".format(e) + Style.RESET_ALL)
    # if len(words) != 0 and output_mode:
    print_col(f"Process {process_num} recognized: {words}", "green")
    print_col(f"Words per minute: {len(words) / 3 * 60}", "green")
    






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', action='store_true', help='Enable output mode')
    args = parser.parse_args()

    process_speech(0,args.output)