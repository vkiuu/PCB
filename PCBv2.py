import wget
import time
from datetime import datetime
from pynput.keyboard import Key, Controller
import pyperclip
import pytz
import tweepy
import platform
from PIL import Image
import pytesseract

try:
    from config import id, token, code_len
except ImportError:
    print("Error ~ Please remember to first run the setup.py file before running this program.")
api = tweepy.Client(token)



def start():
    utc = pytz.utc
    datetime_utc = datetime.now(utc)  #sets the time of start
    global time_object
    time_object = datetime_utc.strftime("%Y-%m-%dT%H:%M:%SZ")  #converts the time of start into the right format


def new_time():
    UTC = pytz.utc
    datetime_utc = datetime.now(UTC)                             #sets the time of start
    global time_object
    time_object = datetime_utc.strftime("%Y-%m-%dT%H:%M:%SZ")    #converts the time of start into the right format
    new_tweet()

def new_tweet():    #checks if there is any new tweet since starting the program
    time.sleep(1)
    twt = api.get_users_tweets(id=id, max_results=5, start_time=time_object) # getting tweet data posted ->
    tid = twt.meta.get('newest_id')
    try:                                                                     # after the time_object
        twt.meta.pop('newest_id')        #removing useless keys from data dictionary
        twt.meta.pop('oldest_id')
        twt.meta.pop('next_token')
    except:
        pass
    for key, value in twt.meta.items():  #if the value is 0 - meaning no new tweet repeat the function
        if value == 0:
            new_tweet()
        else:                            #if the value does not equal 0 check if there is some image that might have ->
            check_for_image_reply(twt,tid)   #the desired code

def check_for_image_reply(twt,tweet_id):
    tweet = api.get_tweet(id=tweet_id, expansions="attachments.media_keys", media_fields="url")
    if "media" in tweet.includes:
        media_entities = tweet.includes["media"]
        media = media_entities[0]
        media_url = media.url
        filename = wget.download(media_url)
        retrive_text_from_image(filename)
    else:
        splitting(twt)

def retrive_text_from_image(filename):
    image = Image.open(filename)
    text = pytesseract.image_to_string(image)
    with open('output.txt', 'w') as file:
        y = text
        y = y.replace("\n", " ")
        y = y.replace("\\n", " ")
        words = y.split(" ")
        global code
        code = promo_codes(words)

def splitting(twt):                      #cleans the text from dict data and splits the text of the tweet into words
    y = str(twt.data)
    y = y[37:-3]                    #getting rid of the [<Tweet id=1234567899123456789 (...) '>] part in the data string
    y = y.replace("\n", " ")        #the text has \n as new line indicators, so it needs to be removed
    y = y.replace("\\n", " ")
    words = y.split(" ")            #splitting the clear tweet text into words
    global code
    code = promo_codes(words)


def promo_codes(words):                 #finding which word from the list(words) is the code
    global c, c1
    c = -1
    c1 = 0
    promo_code = words[c:]                  #last word
    while len(str(promo_code)) != code_len: #checks the length of every word, the code has a length of 24 characters
        promo_code = words[c:c1]
        d = len(words)
        if (c*-1) >= d:                #run the program only the amount of times equal to amount of words in the tweet
            if (len(str(promo_code))) != code_len:
                return 1
        c -= 1
        c1 -= 1
    return promo_code


def enter_code(code):
    keyboard = Controller()
    code = code[0]
    pyperclip.copy(code)
    if platform.system() == 'Windows':
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
    elif platform.system() == 'Darwin':
        with keyboard.pressed(Key.cmd):
            keyboard.press('v')
            keyboard.release('v')
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


print("code is now running...")
start()
new_tweet()
while code == 1:
    new_time()
print(f'Promotion Code: {code}')
enter_code(code)
