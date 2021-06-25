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
            
            
@app.route("/login", methods=["GET", "POST"])
def login():
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        if user:
            if bcrypt.check_password_hash(user.Password, form.Password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("bull.reports"))
    return render_template("login.html", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")
    
@app.route('/ImamWebView')
def ImamWebView():
    pass # Kabir

@app.route('/Whatsappenpoint')
def Whatsappenpoint():
    pass # Ismail
    
if __name__ == '__main__':
    database.create_all()
    application.run()