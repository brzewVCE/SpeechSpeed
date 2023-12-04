import speech_recognition as sr
import time
from colorama import Fore, Style
import multiprocessing
import argparse
from multiprocessing import shared_memory
import customtkinter as ctk
import numpy as np

#multiprocessing settings
mp_context = multiprocessing.get_context('spawn')

#speech recognition settings
r = sr.Recognizer()
r.energy_threshold = 0
r.dynamic_energy_threshold = False

#window settings
ctk.set_appearance_mode("system")
root = ctk.CTk()
root.geometry("500x350")

#global variables
rec_time=4
offset=1.2
previous_sentence = []
WPM = 0




def print_col(text, color):
    color_constant = getattr(Fore, color.upper(), None)
    if color_constant:
        print(color_constant + text + Style.RESET_ALL)
    else:
        print(text)


#naprawić globalne zmienne
def process_speech(process_num, shared_data, rec_time=rec_time, offset=offset):
    time.sleep(rec_time-offset)
    print_col(f"Started process_speech() function number {process_num}", "yellow")
    buffer = shared_data.buf
    if buffer[0] == 0:
        buffer[0] = process_num
    print_col(f"buffer: {buffer}", "yellow")
    words = {}
    with sr.Microphone() as source:
        try:
            process = mp_context.Process(target=process_speech, args=(process_num+1, shared_data,))
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
    #for testing purposes
    words = [word.lower() for word in words]
    #print words
    
    print_col(f"words: {words}", "red")
    print_col(f"previous_sentence: {previous_sentence}", "red")
    #compare if last two words is the same as first word in new sentence
    
    if len(previous_sentence) != 0:
        #scan the last two words of previous sentences for all sentences
        for sentence in previous_sentence:
            if len(sentence) >= 2:
                if sentence[-2:] == words[0]:
                    words = words[2:]
                    print_col(f"words: {words}", "red")
                    break
                if sentence[-1] == words[0]:
                    words = words[1:]
                    print_col(f"words: {words}", "red")
                    break
    previous_sentence = words
    print_col(f"corrected words: {words}", "red")
    WPM = len(words) / rec_time * 60
    print_col(f"Process {process_num} recognized: {words}", "green")
    print_col(f"Words per minute: {WPM}", "green")
    shared_data.unlink()

    
    




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', action='store_true', help='Enable output mode')
    args = parser.parse_args()

    #shared memory, last 3 sentences and last WPM
    sentences = shared_memory.SharedMemory(create=True, size=3)
    buffer = sentences.buf
    buffer[0] = 0



    process = mp_context.Process(target=process_speech, args=(0, sentences,))
    process.start()

    

    frame = ctk.CTkFrame(root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    label = ctk.CTkLabel(frame, text="Words Per Minute:")
    label.pack(padx=10, pady=10)
    label = ctk.CTkLabel(frame, text=WPM)
    label.pack(padx=10, pady=10)

    root.mainloop()

    #wyłączenie procesu