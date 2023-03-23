import os, json
import hashlib

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict

from views.assetview import Alert

Builder.load_file('views/signin/signin.kv')
class Signin(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.alert = Alert()

    def signin(self):
        uname = self.ids.username.text.strip()
        passw = self.ids.password.text.strip()

        self.ids.username.text = ""
        self.ids.password.text = ""

        if len(uname) < 3:
            self.alert.text = "Invalid username"
            self.alert.open()
            return
        
        if len(passw) < 5:
            self.alert.text = "Invalid password"
            self.alert.open()
            return

        passw = hashlib.sha256(bytes(passw, encoding="utf-8")).hexdigest()
        
        users = {}

        upath = App.get_running_app().user_data_dir
        save_path = os.path.join(upath, "users.json")
        if os.path.exists(save_path):
            with open(save_path, "r") as f:
                users = json.load(f)
        
        if uname in list(users.keys()):
            upass = users[uname]['password']

            if upass != passw:
                self.alert.text = "Password is incorrect"
                self.alert.open()
                return
            else:
                App.get_running_app().root.ids.scrn_mngr.current = 'scrn_home'
        else:
            self.alert.text = "User not found"
            self.alert.open()
            return
