import time
from datetime import datetime
from pynput.keyboard import Key, Controller
import pyperclip
import pytz
import tweepy


UTC = pytz.utc
datetime_utc = datetime.now(UTC)                             #sets the time of start
time_object = datetime_utc.strftime("%Y-%m-%dT%H:%M:%SZ")    #converts the time of start into the right format
api = tweepy.Client(
    "")

if __name__ == '__main__':
    print("code is now running...")


def new_time():
    UTC = pytz.utc
    datetime_utc = datetime.now(UTC)                             #sets the time of start
    global time_object
    time_object = datetime_utc.strftime("%Y-%m-%dT%H:%M:%SZ")    #converts the time of start into the right format
    print(f'The account has posted, no promotion code found. New time: {time_object}')
    new_tweet()

def new_tweet():    #checks if there is any new tweet since starting the program
    time.sleep(1)
    twt = api.get_users_tweets(id=1234567899123456789, max_results=5, start_time=time_object) # getting tweet data posted
    try:                                                                                      # after the time_object
        twt.meta.pop('newest_id')           #removing useless keys from data dict
        twt.meta.pop('oldest_id')
        twt.meta.pop('next_token')
    except:
        pass
    for key,value in twt.meta.items(): #if the value is 0 - meaning no new tweet reapeat the function
        if value == 0:
            new_tweet()
        else:                           #if the value does not equal 0 start splitting the text into words
            spliting(twt)

def spliting(twt):                      #cleans the text from dict data and splits the text of the tweet into words
        y = str(twt.data)
        y = y[37:-3]                    #getting rid of the [<Tweet id=1234567899123456789 (...) '>] part in the data string
        y = y.replace("\n", " ")        #the text has \n as new line indicators, so it needs to be removed
        y = y.replace("\\n", " ")
        global words
        words = y.split(" ")            #splitting the clear tweet text into words
        global code
        code = promo_codes(words)


def promo_codes(words):                 #finding which word from the list(words) is the code
    global c,c1
    c = -1
    c1 = 0
    promo_code = words[c:]            #last word
    while len(str(promo_code)) != 24: #checks the lenght of every word, the code has a length of 24 characters
        promo_code = words[c:c1]
        d = len(words)
        if (c*-1)>=d:                   #run the program only the ammount of times equal to ammount of words in the tweet
            if (len(str(promo_code))) != 24:
                return 1
        c -= 1
        c1 -= 1
    return promo_code

def enter_code(code):
    keyboard = Controller()
    code = code[0]
    pyperclip.copy(code)
    with keyboard.pressed(Key.cmd):
        keyboard.press('v')
        keyboard.release('v')
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


if __name__ == '__main__':
    new_tweet()
    while code ==1:
        new_time()
    print(f'the code is: {code}')
    enter_code(code)
