# KlawaServer
# by Kostek001
# Version: 1.1

min = 95 # Minimal typing delay (in ms)
max = 185 # Maximal typing delay (in ms)
error_chance = 0.005 # Error chance
redemption_chance = 0.7 # Fix error chance

import time
import random
from pynput.keyboard import Key, Controller, Listener
import threading
from flask import Flask, request
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

keyboard = Controller()
letters = 'abcdefghijklmnopqrstuvwxyz'

class Thread:
    stop = False
threads = []

globalText = ""

def typeText(thread, text):
    print("Writing text.")
    for letter in text:
        if thread.stop:
            break
        if random.random() < error_chance:
            keyboard.tap(random.choice(letters))
            if random.random() < redemption_chance:
                time.sleep(random.randint(min, max) / 1000)
                keyboard.tap(Key.backspace)
                time.sleep(random.randint(min, max) / 1000)
                keyboard.tap(letter)
        else:
            keyboard.tap(letter)
        time.sleep(random.randint(min, max) / 1000)
    if thread.stop:
        print("Writing stopped!")
    else:
        print("Writing done!")
    threads.remove(thread)

def on_press(key):
    if key == Key.f8:
        thread = Thread()
        threads.append(thread)
        global globalText
        threading.Thread(target=typeText, args=(thread, globalText,), name='typeText', daemon=True).start()
    if key == Key.f9:
        for thread in threads:
            thread.stop = True

Listener(on_press=on_press).start()
  
app = Flask(__name__)

@app.route('/text', methods=['POST']) 
def process():
    print("Received text from browser!")
    global globalText
    globalText = request.form.get('data')
    return "ok"

if __name__ == '__main__':
    app.run(debug=False)
