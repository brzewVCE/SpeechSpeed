import speech_recognition as sr
import time
from colorama import Fore, Style
import multiprocessing
import argparse
import sys
import customtkinter as ctk

mp_context = multiprocessing.get_context('spawn')
r = sr.Recognizer()
r.energy_threshold = 0
r.dynamic_energy_threshold = False

ctk.set_appearance_mode("system")

root = ctk.CTk()
root.geometry("500x350")

rec_time=4
offset=2
previous_sentence = []
WPM = 0

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

#zdesignować GUI
def process_speech(process_num, output_mode=False, rec_time=rec_time, offset=offset, previous_sentence=previous_sentence, WPM=WPM):
    time.sleep(rec_time-offset)
    print_col(f"Started process_speech() function number {process_num}", "red")
    words = {}
    with sr.Microphone() as source:
        try:
            process = mp_context.Process(target=process_speech, args=(process_num+1,output_mode,))
            process.start()
            audio_text = r.listen(source, phrase_time_limit=rec_time)
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
            process.join()
        except Exception as e:
            print(Fore.RED + "An error occurred: {0}".format(e) + Style.RESET_ALL)
    # if len(words) != 0 and output_mode:
    #for testing purposes
    words = [word.lower() for word in words]
    #compare if last two words is the same as first word in new sentence
    
    if len(previous_sentence) != 0:
        while previous_sentence[-1] == words[0] or previous_sentence[-2] == words[0]:
            words = words[1:]
    
    previous_sentence = words
    WPM = len(words) / rec_time * 60
    print_col(f"Process {process_num} recognized: {words}", "green")
    print_col(f"Words per minute: {WPM}", "green")

    return previous_sentence, WPM
    
    




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', action='store_true', help='Enable output mode')
    args = parser.parse_args()

    process = mp_context.Process(target=process_speech, args=(0,args.output,rec_time,rec_time))
    process.start()
    frame = ctk.CTkFrame(root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    label = ctk.CTkLabel(frame, text="Words Per Minute:")
    label.pack(padx=10, pady=10)

    label = ctk.CTkLabel(frame, text=WPM)
    label.pack(padx=10, pady=10)

    # root.mainloop()