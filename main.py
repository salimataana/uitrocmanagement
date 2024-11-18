import datetime
import time
from random import randint

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from data_access import USER_CURRENT
from data_access.data_access_autorization import DATA_FOLDER_AUTORIZATION, get_all_autorizations
from data_access.data_access_troc import get_all_trocs, get_troc_by_id_fichier, get_all_trocs_sent_by_current_user, \
    get_all_trocs_received_by_current_user
from models.autorisation import Autorisation
from models.coordonnees import Coordonnees
from models.demandeautorisation import DemandeAutorisation
from models.message import Message
from models.objetechanger import ObjetExchange
from models.troc import Troc

PREFIX_FOLDER_TROC_SENT="data/trocs"
PREFIX_FOLDER_TROC_RECEIVED="data/trocs"
PREFIX_FOLDER_AUTH="data/autorisations"

main = Blueprint('main', __name__)


####################### logic authen ############################

#@main.route('/')
#def index():
#    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)



########################## logic application #############################
@main.route("/")
def home():
    return render_template("home.html")


@login_required
@main.route("/trocsent")
def index_troc_sent():
    trocs,noms_des_fichiers_pas_bons=get_all_trocs_sent_by_current_user(PREFIX_FOLDER_TROC_SENT, id_troqueur=current_user.id)
    return render_template("indextrocsent.html",trocs=trocs,noms_des_fichiers_pas_bons=noms_des_fichiers_pas_bons)

@login_required
@main.route("/trocreceived")
def index_troc_received():
    trocs,noms_des_fichiers_pas_bons=get_all_trocs_received_by_current_user(PREFIX_FOLDER_TROC_RECEIVED, id_troqueur=current_user.id)
    print(f"********************************{len(trocs)}*****************")
    return render_template("indextrocreceived.html",trocs=trocs,noms_des_fichiers_pas_bons=noms_des_fichiers_pas_bons)

@login_required
@main.route("/autorisation")
def index_autorisation():
    autorizations=get_all_autorizations(folder_path=DATA_FOLDER_AUTORIZATION)
    print(autorizations)
    return render_template("indexautorisation.html",autorizations=autorizations)


@login_required
@main.route("/create",methods=("GET", "POST"))
def create_troc():
    if request.method=="GET":
        return render_template("createtroc.html", user_id=current_user.id, current_date=get_current_date())
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
                             id_destinataire=None, # NOT CONNU#request.form["id_destinataire"],
                             id_fichier=file_name,
                             date_fichier=request.form["date_fichier"],
                             messages=[messages])
        troc.save(f"{PREFIX_FOLDER_TROC_SENT}/{file_name}")
        return redirect(url_for('main.index_troc_sent'))

@login_required
@main.route("/createdemandeautorisation/id_message=<id_message>&id_fichier=<id_fichier>", methods=("GET", "POST"))
def create_demande_autorisation(id_message, id_fichier):
    if request.method=="GET":
        print(f"*******************{id_message}****************")
        return render_template("createdemandeautorisation.html",id_message=id_message,
                               id_fichier=id_fichier, email=current_user.email)
    if request.method=="POST":
        troc = get_troc_by_id_fichier(f"{PREFIX_FOLDER_TROC_SENT}/{id_fichier}")
        coord = Coordonnees(mail=request.form["mail"],
                                                telephone=request.form["telephone"])
        demande_authorization = DemandeAutorisation(statut_autorisation=request.form["statut_autorisation"],
                                                                        date=get_current_date(),
                                                                        id_message=id_message,
                                                                        coord=coord)
        autorisation = Autorisation(id_troqueur=troc.id_troqueur,
                                        id_destinataire=current_user.id,
                                        id_fichier=troc.id_fichier,
                                        date_fichier=get_current_date(),
                                        demande_autorisation=demande_authorization)
        file_name = generate_unique_name_file_for_authorization()

        autorisation.save(f"{PREFIX_FOLDER_AUTH}/{file_name}")
        return redirect(url_for('main.index_autorisation'))


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