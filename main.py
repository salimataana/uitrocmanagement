import datetime
import time
from random import randint

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from constant import GROUP_NUMBER
from data_access import USER_CURRENT
from data_access.data_access_autorization import DATA_FOLDER_AUTORIZATION, get_all_autorizations, \
    get_autorization_with_idFichier
from data_access.data_access_troc import get_all_trocs, get_troc_by_id_fichier, get_all_trocs_sent_by_current_user, \
    get_all_trocs_received_by_current_user
from models.autorisation import Autorisation
from models.coordonnees import Coordonnees
from models.demandeautorisation import MessageDemandeAutorisation
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
@main.route("/autorisation_envoye")
def index_autorisation_envoye():
    autorizations=get_all_autorizations(folder_path="data/demandeauthorizationenvoye")
    print(autorizations)
    return render_template("indexautorisationenvoye.html",autorizations=autorizations)



@main.route("/createdemandeautorizationaccepted/idFichier=<idFichier>", methods=("GET", "POST"))
def create_demande_autorization_accepted(idFichier):
    autorization = get_autorization_with_idFichier(idFichier)
    if request.method=="GET":
        return render_template("creationdemandeautorizationaccepted.html", autorization=autorization )
    if request.method=="POST":
        autorization.messageDemandeAutorisation["statutAutorisation"] = request.form["statut_autorisation"]
        #autorization.messageDemandeAutorisation = MessageDemandeAutorisation(**autorization.messageDemandeAutorisation)

        if request.form["statut_autorisation"] == "accepte":
            autorization.save(f"data/demandeautorisationaccepted/{generate_unique_name_file_for_authorization()}")
            autorizations = get_all_autorizations(folder_path="data/demandeautorisationaccepted/")
        else:
            autorization.save(f"data/demandeautorisationrefused/{generate_unique_name_file_for_authorization()}")
            autorizations = get_all_autorizations(folder_path="data/demandeautorisationrefused")
        return render_template("indexautorisationaccepted.html", autorizations=autorizations)


def get_destinataires_acceptes():
    folder_path = "data/demandeautorisationaccepted/"
    autorisations = get_all_autorizations(folder_path=folder_path)
    destinataires = [
        {"id": autorisation.idDestinataire}
        for autorisation in autorisations
    ]
    return destinataires





@login_required
@main.route("/create",methods=("GET", "POST"))
def create_troc():
    if request.method=="GET":
        destinataires_acceptes = get_destinataires_acceptes()
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
                             id_destinataire=request.form["id_destinataire"],
                             id_fichier=file_name,
                             date_fichier=request.form["date_fichier"],
                             messages=[messages])
        troc.save(f"{PREFIX_FOLDER_TROC_SENT}/{file_name}")
        return redirect(url_for('main.index_troc_sent'))

@login_required
@main.route("/createdemandeautorisation/", methods=("GET", "POST"))
def create_demande_autorisation():

    if request.method=="GET":
        return render_template("createdemandeautorisation.html",groupe_id=GROUP_NUMBER,
                        )
    print("*****************************POST***************************")
    if request.method=="POST":
        print(request.form)
        coord = Coordonnees(mail=request.form["mail"],
                                                telephone=request.form["telephone"])
        messageDemandeAutorisation = MessageDemandeAutorisation(
                                                                        statutAutorisation=request.form["statut_autorisation"],
                                                                        date=get_current_date(),
                                                                        idMessage=request.form["idMessage"],
                                                                        coordonnees=coord)
        autorisation = Autorisation(idTroqueur=request.form["idTroqueur"],
                                                            idDestinataire=request.form["idDestinataire"],
                                                            idFichier=request.form["idFichier"],
                                                            dateFichier=get_current_date(),
                                                            messageDemandeAutorisation=messageDemandeAutorisation)
        file_name = generate_unique_name_file_for_authorization()

        autorisation.save(f"data/demandeauthorizationenvoye/{file_name}")
        return redirect(url_for('main.index_autorisation_envoye'))



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

