
import datetime
import time
from random import randint
from flask import Flask, render_template, request, url_for, flash, redirect
from data_access import USER_CURRENT
from data_access.data_access_autorization import get_all_autorizations, DATA_FOLDER_AUTORIZATION
from data_access.data_access_troc import get_all_trocs, get_troc_by_id_fichier
from models.autorisation import Autorisation
from models.coordonnees import Coordonnees
from models.demandeautorisation import DemandeAutorisation
from models.message import Message
from models.objetechanger import ObjetExchange
from models.troc import Troc
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_manager, login_required, logout_user, current_user, LoginManager
from flask_wtf import  FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt



PREFIX_FOLDER_TROC_SENT="data/troc_sent"
PREFIX_FOLDER_TROC_RECEIVED="data/troc_received"
PREFIX_FOLDER_AUTH="data/autorisations"


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username= StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.date).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one.")

class LoginForm(FlaskForm):
     username = StringField(validators=[InputRequired(), Length(
            min=4, max=20)], render_kw={"placeholder": "Username"})
     password = PasswordField(validators=[InputRequired(), Length(
            min=4, max=20)], render_kw={"placeholder": "Password"})
     submit = SubmitField("Login")



@app.route("/")
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template(login.html, form=form)


app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect (url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template(register.html, form=form)



if __name__=='__main__':
    app.run(debug=True)


@app.route("/trocsent")
def index_troc_sent():
    trocs,noms_des_fichiers_pas_bons=get_all_trocs(PREFIX_FOLDER_TROC_SENT)
    return render_template("indextrocsent.html",trocs=trocs,noms_des_fichiers_pas_bons=noms_des_fichiers_pas_bons)

@app.route("/trocreceived")
def index_troc_received():
    trocs,noms_des_fichiers_pas_bons=get_all_trocs(PREFIX_FOLDER_TROC_RECEIVED)
    print(f"********************************{len(trocs)}*****************")
    return render_template("indextrocreceived.html",trocs=trocs,noms_des_fichiers_pas_bons=noms_des_fichiers_pas_bons)

@app.route("/autorisation")
def index_autorisation():
    autorizations=get_all_autorizations(folder_path=DATA_FOLDER_AUTORIZATION)
    print(autorizations)
    return render_template("indexautorisation.html",autorizations=autorizations)


@app.route("/create",methods=("GET", "POST"))
def create():
    if request.method=="GET":
        return render_template("createtroc.html")
    if request.method=="POST":
        # get the name of file to create
        file_name = generate_unique_name_file_troc()
        objects = ObjetExchange(titre=request.form[f"titre"],
                                                        description=request.form[f"description"],
                                                        qualite=int(request.form[f"qualite"]),
                                                        quantite=int(request.form[f"quantite"])
                                                        )
        messages = Message(id_message=str(randint(0, 10000000)),
                                                date_message=request.form["date_message"],
                                                 statut= request.form["statut"],
                                                objets=[objects])

        troc = Troc(id_troqueur=request.form["id_troqueur"],
                             id_destinataire=request.form["id_destinataire"],
                             id_fichier=file_name,
                             date_fichier=request.form["date_fichier"],
                             messages=[messages])
        troc.save(f"{PREFIX_FOLDER_TROC_SENT}/{file_name}")
        return redirect(url_for('index_troc_sent'))

@app.route("/createdemandeautorisation/id_message=<id_message>&id_fichier=<id_fichier>", methods=("GET", "POST"))
def create_demande_autorisation(id_message, id_fichier):
    if request.method=="GET":
        print(f"*******************{id_message}****************")
        return render_template("createdemandeautorisation.html",id_message=id_message,id_fichier=id_fichier)
    if request.method=="POST":
        troc = get_troc_by_id_fichier(f"{PREFIX_FOLDER_TROC_SENT}/{id_fichier}")
        coord = Coordonnees(mail=request.form["mail"],
                                                telephone=request.form["telephone"])
        demande_authorization = DemandeAutorisation(statut_autorisation=request.form["statut_autorisation"],
                                                                        date=get_current_date(),
                                                                        id_message=id_message,
                                                                        coord=coord)
        autorisation = Autorisation(id_troqueur=troc.id_troqueur,
                                        id_destinataire=USER_CURRENT,
                                        id_fichier=troc.id_fichier,
                                        date_fichier=get_current_date(),
                                        demande_autorisation=demande_authorization)
        file_name = generate_unique_name_file_for_authorization()

        autorisation.save(f"{PREFIX_FOLDER_AUTH}/{file_name}")
        return redirect(url_for('index_autorisation'))


def generate_unique_name_file_troc():
    ts = time.time()
    string_date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
    return f'troc_{string_date}.json'



def generate_unique_name_file_for_authorization():
    ts = time.time()
    string_date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
    return f'autorization_{string_date}.json'


def get_current_date():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')