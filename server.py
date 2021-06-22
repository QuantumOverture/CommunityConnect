from flask import Flask,redirect,render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MainData.sqlite3'

SQLALCHEMY_BINDS = {
    'ImamData': 'sqlite:///ImamData.sqlite3',
    'Annoucements': 'sqlite:///Annoucements.sqlite3',
    'QuestionDatabase': 'sqlite///Questions.sqlite3'
}

database = SQLAlchemy(app)
class MainImamData(database.Model):
    __bind_key__ = 'ImamData'
    DataID = database.Column(database.Integer, primary_key = True)
    UserName = database.Column(database.String(100))
    Password = database.Column(database.String(100))
    MasjidLocation = database.Column(database.String(100))
    
    def __init__(self, Username, Password, MasjidLocation):
        self.UserName = Username
        self.Password = generate_password_hash(Password)
        self.MasjidLocation = MasjidLocation

class Annoucements(database.Model):
    __bind_key__ = 'Annoucements'
    DataID = database.Column(database.Integer, primary_key = True)
    ImamOwnership = database.Column(database.String(100))
    AnnouncementText = database.Column(database.String(500))
    InactiveOrActive = database.Column(database.Boolean)
    
    def __init__(self, ImamOwnership, AnnouncementText):
            self.ImamOwnership = ImamOwnership
            self.AnnouncementText = AnnouncementText
            self.InactiveOrActive = True # True -> active False -> inactive

class QuestionDatabase(database.Model):
    __bind_key__ = 'QuestionDatabase'
    DataID = database.Column(database.Integer, primary_key = True)
    QuestionText = database.Column(database.String(200))
    SenderNumber = database.Column(database.String(100))
    ImamUsername = database.Column(database.String(100))
    AnsweredOrUnAnswered = database.Column(database.Boolean)
    def __init__(self, QuestionText,SenderNumber, ImamUsername):
            self.QuestionText = QuestionText
            self.SenderNumber = SenderNumber # In this format: "+1 4078763333"
            self.ImamUsername = ImamUsername
            self.AnsweredOrUnAnswered = False # False -> Unanswered True -> Answered
            
            
@app.route('/')
def LoginLandingPage(): # Kabir
    return render_template() # Returning the html file we got from the front end team
    
@app.route('/ImamWebView')
def ImamWebView():
    pass # Kabir

@app.route('/Whatsappenpoint')
def Whatsappenpoint():
    pass # Ismail
    
if __name__ == '__main__':
    database.create_all()
    application.run()