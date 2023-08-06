import sqlite3, firebasePort, json, os, sys, requests, uuid, string, random, hashlib

class Login(object):
    def __init__(self, type_, config = None, firebasePath = None):
        self.type_ = type_.lower()
        self.config = config
        self.serverDomain = config['authDomain']
        self.firebasePath = firebasePath


    def login(self, user, password):
        if self.checkUser(user) is not None:
            cryptPassword, stPassword = self.getCryptPsw(user, password)
            
            if cryptPassword != stPassword:
                return 'psw_error'
            else:
                return True

        else:
            return 'user_error'
            
            

    def register(self, user, password, passwordConfirm):
        if password != passwordConfirm:
            return 'psw_error'
        if self.checkUser(user) is None:
            userID = uuid.uuid4().hex
            hpassword = self.hash_password(password, userID)
            self.firebase.writeData(f'{self.firebasePath}/{user}/password', hpassword)
            self.firebase.writeData(f'{self.firebasePath}/{user}/uuid', userID)
        else:
            return 'user_error'

    def checkUser(self, user):
        if self.type_ == 'firebase':
            if not self.internet_connection(self.serverDomain):
                return 'timed_out'

            self.firebase = firebasePort.Database(self.config)

            return self.firebase.getData(f'{self.firebasePath}/{user}')

                
    def getCryptPsw(self, user, password):
        if self.type_ == 'firebase':
            return self.hash_password(password, self.firebase.getData(f'{self.firebasePath}/{user}/uuid')), self.firebase.getData(f'{self.firebasePath}/{user}/password')

    def hash_password(self, password, salt):
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest()

    def internet_connection(self, domain):
        try:
            requests.get(f'https://{domain}', timeout=5)
            return True
        except requests.ConnectionError: 
            return False


config = {
    "apiKey": "AIzaSyDehw4NuNihPM1Lezc1GbPGWE272yHOE1s",
    "authDomain": "rgb-led-control.firebaseapp.com",
    "databaseURL": "https://rgb-led-control.firebaseio.com",
    "storageBucket": "rgb-led-control.appspot.com",
    "tls": {
        "rejectUnauthorized": False
        }
    }

login = Login('firebase',config,'/users')
#login.register('Teddy', '12345', '12345')
login.login('Teddy', '12345')
