import webbrowser
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window


class Setup(App):
    #---------------- build function ----------------#

    def build(self):
        self.window = GridLayout(cols=1, rows=9, row_force_default=True, rows_minimum={0: 40, 1: 100})
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        self.window2 = GridLayout(cols=2, rows=3, row_default_height=100, row_force_default=True,
                                  cols_minimum={0:10, 1: 1})
        self.window2.size_hint = (0.6, 0.7)
        self.window2.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.window.add_widget(self.window2)
        self.title = "PCB Setup"
        self.label = Label(
            text='1. Enter the User ID of the account',
            font_size=40,
        )
        self.window.add_widget(self.label)
        self.label2 = Label(
            text="[color=#808080][i]for more information about [b]User ID[/b] click" \
                 " [u][ref=<str>]here[/ref][/u][/i][/color]",
            italic=True,
            font_size=35,
            color='#FF0000',
            opacity=0.6,
            markup=True,
        )
        self.label2.bind(on_ref_press=self.warning)
        self.window.add_widget(self.label2)

        class Input(TextInput):
            max_length = 128

            def insert_text(self, substring, from_undo=False):
                s = substring.strip()
                if len(self.text) <= self.max_length:
                    return super(Input, self).insert_text(s, from_undo=from_undo)

        self.pholder1a = Label()
        self.pholder2a = Label()
        self.pholder3a = Label()
        self.pholder4a = Label()
        self.window2.add_widget(self.pholder1a)
        self.window2.add_widget(self.pholder2a)
        self.window2.add_widget(self.pholder3a)
        self.window2.add_widget(self.pholder4a)

        self.pholder1b = Label()
        self.pholder2b = Label()
        self.window.add_widget(self.pholder1b)
        self.window.add_widget(self.pholder2b)

        self.user = Input(
            multiline=False,
            hint_text='User ID',
            padding_y=(30, 10),
            halign="center",
            size_hint=(1, 0.23)
        )
        self.window2.add_widget(self.user)

        self.button1 = Button(text="NEXT",
                              bold=True,
                              size=(10, 10),
                              border=(30, 27, 30, 27)
                              )
        self.window2.add_widget(self.button1)
        Clock.schedule_interval(self.checkempty, 0.25)
        global event, event2, x
        event = Clock.schedule_interval(self.check, 0.25)
        event2 = Clock.schedule_interval(self.check2, 0.25)
        x = None

        return self.window

    #---------------- checks ----------------#

    def check(self, ab):
        self.button1.bind(on_press=self.callback)
        if x == 1:
            event.cancel()
            self.window2.remove_widget(widget=self.button1)
            Clock.schedule_once(self.api, 1)
            self.button2 = Button(text="NEXT",
                                  size_hint=(1, 0.3),
                                  bold=True,
                                  )
            self.window2.add_widget(self.button2)
            self.button2.bind(on_press=self.api_callback)

    def check2(self, ba):
        if x == 2:
            event2.cancel()
            self.window2.remove_widget(widget=self.button2)
            Clock.schedule_once(self.code, 1)
            self.button3 = Button(text="NEXT",
                                  size_hint=(1, 0.3),
                                  bold=True,
                                  )
            self.window2.add_widget(self.button3)
            self.button3.bind(on_press=self.code_callback)

    def checkempty(self, dt):
        input = self.user.text
        if input == "":
            self.button1.disabled = True
        elif input != "":
            self.button1.disabled = False

    #---------------- callbacks ----------------#

    def callback(self, instance):
        inp = self.user.text
        try:
            inp = int(inp)
        except:
            pass
        if type(inp) != int:
            self.label2.text = "'" + self.user.text + "' is not a proper ID, please try again"
        else:
            self.label.text = "The ID has been set to '" + self.user.text + "'"
            self.user.disabled = True
            self.label2.text = ""
            global id, x
            id = inp
            x = 1
            return
        Clock.schedule_once(self.removeinfo, 10)

    def api_callback(self, dt):
        inp = self.user.text
        if len(inp) < 112:
            self.label2.text = "Please enter a proper Bearer Token"
        else:
            self.label.text = "The Bearer Token has been successfully entered"
            self.label2.text = ""
            self.user.text = ""
            self.user.disabled = True
            global token, x
            token = inp
            x = 2
            return

    def code_callback(self, dt):
        inp = self.user.text
        try:
            inp = int(inp)
        except:
            self.label2.text = "Please enter the length as a number not a word"
            return
        self.label.text = "The length of the code has been successfully entered"
        self.label2.text = ""
        self.user.text = ""
        self.user.disabled = True
        self.window.remove_widget(widget=self.label)
        self.window.remove_widget(widget=self.label2)
        self.window2.remove_widget(widget=self.user)
        self.window2.remove_widget(widget=self.button3)
        self.pholder2b.text = "The setup has been completed. Thank You"
        self.window2.rows = 6
        self.window2.cols = 1
        self.end_button = Button(text="CLOSE & SAVE",
                                 size_hint=(1, 0.3),
                                 bold=True,
                                 )
        self.window2.add_widget(self.end_button)
        self.end_button.bind(on_press=self.close_window)
        global code_len
        code_len = inp+4

    #---------------- popup ----------------#

    def warning(self, pp, bx):
        self.box = FloatLayout()

        self.info = (Label(text="You are about to be redirected\n                   to a website.", font_size=30,
                           markup=True, size_hint=(None, None), pos_hint={'x': 0.4, 'y': .6}))
        self.box.add_widget(self.info)

        self.cancel = (Button(text="Cancel", size_hint=(None, None),
                              height=70, pos_hint={'x': 0, 'y': 0}))
        self.box.add_widget(self.cancel)

        self.proceed = (Button(text="Open", size_hint=(None, None),
                               height=70, pos_hint={'right': 1, 'y': 0}))
        self.box.add_widget(self.proceed)

        self.main_pop = Popup(title="Redirect", content=self.box, title_align='center',
                              size=(550, 400), size_hint=(None, None), auto_dismiss=False, title_size=25)

        self.cancel.bind(on_release=self.main_pop.dismiss)
        if x == 1:
            self.proceed.bind(on_release=self.webbrowser1)
        else:
            self.proceed.bind(on_release=self.webbrowser2)
        self.main_pop.open()

    def webbrowser1(self, wb):
        webbrowser.open('https://developer.twitter.com/en/docs/twitter-api')
        self.main_pop.dismiss()

    def webbrowser2(self, wb):
        webbrowser.open('https://tweeterid.com')
        self.main_pop.dismiss()

    #---------------- window layouts ----------------#

    def api(self, dt):
        self.user.disabled = False
        self.label.text = "2. Enter the Twitter API Bearer Token"
        self.label2.text = "[color=#808080][i]for more information about [b]API Tokens[/b] click" \
                           " [u][ref=<str>]here[/ref][/u][/i][/color]"
        self.user.text = ""
        self.user.hint_text = "Bearer Token"

    def code(self, dt):
        self.user.disabled = False
        self.label.text = "3. Enter the length of desired promotion code"
        self.label2.text = ""
        self.user.text = ""
        self.user.hint_text = "Promotion Code"

    def removeinfo(self, dt):
        self.label2.text = ""

    def close_window(self, dt):
        with open("config.py", 'r+') as file:
            file.truncate(0)
        text = f'id={id} \ntoken="{token}" \ncode_len={code_len}'
        with open('config.py', 'a') as file:
            file.write("")
            file.write(text)
            Window.close()


#---------------- main ----------------#


if __name__ == "__main__":
    Setup().run()
