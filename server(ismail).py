from flask import Flask,redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Whatsapp libraries
import os
from twilio.rest import Client


app = Flask(__name__)

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MainData.sqlite3'

app.config['SQLALCHEMY_BINDS'] = {
    'ImamData': 'sqlite:///ImamData.sqlite3',
    'Annoucements':'sqlite:///Annoucements.sqlite3',
    'QuestionDatabase': 'sqlite:///Questions.sqlite3'
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
    ImamAnswer = database.Column(database.String(500))
    def __init__(self, QuestionText,SenderNumber, ImamUsername):
            self.QuestionText = QuestionText
            self.SenderNumber = SenderNumber # In this format: "+14078763333"
            self.ImamUsername = ImamUsername
            self.AnsweredOrUnAnswered = False # False -> Unanswered True -> Answered
            self.ImamAnswer = ""
            
            
@app.route('/')
def LoginLandingPage(): # Kabir
    return render_template() # Returning the html file we got from the front end team
    
@app.route('/ImamWebView')
def ImamWebView():
    pass # Kabir




@app.route('/Whatsappenpoint',methods=["GET","POST"])
def Whatsappenpoint():
    
    # Creditentials for API
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    if request.method == "POST":
        UserMessage = request.form
        Body = UserMessage.get('Body').split(" ")
        print(Body)
        UserNumber = UserMessage.get('From')[UserMessage.get('From').index(":")+1:]
        print(UserNumber)
        if Body[0] == "list":
            MainData = MainImamData.query.filter_by(MasjidLocation = " ".join(Body[1:])).all()
            if len(MainData) == 0:
                message = client.messages.create(
                              body="No masjids in this area :( ",
                              from_='whatsapp:+14155238886',
                              to='whatsapp:{}'.format(UserNumber)
                          )
                          
            ListData = ""
            ItemList = 1
            for Item in MainData:
                ListData += "{}. ImamUserName:{} MasjidLocation:{}".format(ItemList,Item.UserName,Item.MasjidLocation)
                ItemList += 1
            print(ListData)   
            message = client.messages.create(
                              body=ListData,
                              from_='whatsapp:+14155238886',
                              to='whatsapp:{}'.format(UserNumber)
                          )
        elif Body[0] == "announcements":
            MainData = MainImamData.query.filter_by(MasjidLocation = " ".join(Body[1:-1])).all()
            if len(MainData) == 0:
                message = client.messages.create(
                              body="No masjids in this area :( ",
                              from_='whatsapp:+14155238886',
                              to='whatsapp:{}'.format(UserNumber)
                          )
            ResultData = ""
            for Item in Annoucements.query.filter_by(ImamOwnership = MainData[int(Body[-1])-1].UserName).all():
                ResultData += Item.AnnouncementText+"\n"
            if ResultData == "":
                message = client.messages.create(
                              body="No annoucements for this Imam",
                              from_='whatsapp:+14155238886',
                              to='whatsapp:{}'.format(UserNumber)
                          )
            else:
                message = client.messages.create(
                              body=ResultData,
                              from_='whatsapp:+14155238886',
                              to='whatsapp:{}'.format(UserNumber)
                          )
        elif Body[0] == "ask":
            ListNumIndex = 0
            for item in Body:
                if item.isnumeric():
                    break
                ListNumIndex += 1
            print(ListNumIndex)
            MainData = MainImamData.query.filter_by(MasjidLocation = " ".join(Body[1:ListNumIndex])).all()
            if len(MainData) == 0:
                message = client.messages.create(
                              body="No masjids in this area :( ",
                              from_='whatsapp:+14155238886',
                              to='whatsapp:{}'.format(UserNumber)
                          )
            
            database.session.add(QuestionDatabase(" ".join(Body[ListNumIndex+1:]),UserNumber, MainData[int(Body[ListNumIndex])-1].UserName))
            database.session.commit()
            print(QuestionDatabase.query.all())
        elif Body[0] == "inbox":
            AllQuestions = QuestionDatabase.query.all()
            MainData = MainImamData.query.filter_by(MasjidLocation = " ".join(Body[1:-1])).all()
            if len(MainData) == 0:
                message = client.messages.create(
                              body="No masjids in this area :( ",
                              from_='whatsapp:+14155238886',
                              to='whatsapp:{}'.format(UserNumber)
                          )
            
            ResultData = ""
            for item in AllQuestions:
                if item.SenderNumber == UserNumber and item.ImamUsername == MainData[int(Body[-1]) -1].UserName:
                    ResultData += "Question:{}  Answer:{} \n".format(item.QuestionText,item.ImamAnswer)
            
            if ResultData == "":
                message = client.messages.create(
                              body="Inbox empty",
                              from_='whatsapp:+14155238886',
                              to='whatsapp:{}'.format(UserNumber)
                          )
            else:
                message = client.messages.create(
                              body=ResultData,
                              from_='whatsapp:+14155238886',
                              to='whatsapp:{}'.format(UserNumber)
                          )
        else:
            message = client.messages.create(
                              body="Invalid command[valid commands: list,ask,inbox,announcements]",
                              from_='whatsapp:+14155238886',
                              to='whatsapp:{}'.format(UserNumber)
                          )
            return "Failure - POST"

        return "Success - POST"
    else:
        database.session.add(MainImamData("Dr.Ali","securepassword","San Jose"))
        database.session.add(Annoucements("Dr.Ali","Zuhr is at 1:30 Today."))
        database.session.commit()
        return "Success - GET"

if __name__ == '__main__':
    database.create_all()
    app.run(port=8080)

