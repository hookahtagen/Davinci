#
# Imports
#

import os, sys, openai, platform, time

import pyaudio, wave
from playsound import playsound

import pyChatGPT

from dotenv import load_dotenv
from gtts import gTTS
#
#   Globale Variablen
#

_temperature = 0.9
_max_length = 150
_top_p = 1
_frequency_penalty = 0.65
_presence_penalty = 0.34
_best_of = 1
_stop_sequence ="\n"

_name = 'Davinci'

RATE = 44100
session_token = '-'

load_dotenv()
openai.api_key = os.environ.get('OPENAI_KEY')
completion = openai.Completion()

def ask(prompt):
    response = completion.create(
        prompt=prompt, engine="text-davinci-003", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0.65, presence_penalty=0.34, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    
    return answer

def cls():
    if platform.system() == 'Windows': os.system('cls')
    else: os.system('clear')

def sleep(delay):
    time.sleep(delay)

def boot_up():
    answer=ask('Create a message for a system while it\'s booting up')
    print(answer)
    tts = gTTS(answer, lang='en')
    tts.save('prompt.mp3')
    playsound('%s' % "prompt.mp3")
    

def run_chat():
    session_api = pyChatGPT.ChatGPT(session_token=session_token)

    run = True
    
    while run:
        u_in = input('Hendrik: ')
        if "!esc" in u_in:
            run = False
            break
        if "!cls" in u_in:
            cls()
        else:    
            response = "".join(session_api.send_message(u_in).get('message'))
            response = response.replace('```\n','**********\n')

        print('Jarvis: '+response)

def main():
    boot_up()
    run_chat()
    

if __name__ == "__main__":
    session_token = input('API-Key: ')
    cls()
    main()