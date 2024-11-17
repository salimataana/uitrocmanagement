
import datetime
import time
from flask import Flask, render_template, request, url_for, flash, redirect
from data_access import get_all_trocs
from models.message import Message
from models.objetechanger import ObjetExchange
from models.troc import Troc

PREFIX_FOLDER_TROC_SENT="data/troc_sent"
PREFIX_FOLDER_TROC_RECEIVED="data/troc_received"

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/trocsent")
def index_troc_sent():
    trocs,noms_des_fichiers_pas_bons=get_all_trocs(PREFIX_FOLDER_TROC_SENT)
    return render_template("indextroc.html",trocs=trocs,noms_des_fichiers_pas_bons=noms_des_fichiers_pas_bons)

@app.route("/trocreceived")
def index_troc_received():
    trocs,noms_des_fichiers_pas_bons=get_all_trocs(PREFIX_FOLDER_TROC_RECEIVED)
    print(f"********************************{len(trocs)}*****************")
    return render_template("indextroc.html",trocs=trocs,noms_des_fichiers_pas_bons=noms_des_fichiers_pas_bons)


@app.route("/create",methods=("GET", "POST"))
def create():
    if request.method=="GET":
        return render_template("createtroc.html")
    if request.method=="POST":
        # get the name of file to create
        id_fichier = generate_unique_name_file()
        objects = ObjetExchange(titre=request.form[f"titre"],
                                                        description=request.form[f"description"],
                                                        qualite=int(request.form[f"qualite"]),
                                                        quantite=int(request.form[f"quantite"])
                                                        )
        messages = Message(date_message=request.form["date_message"],
                                                 statut= request.form["statut"],
                                                objets=[objects])

        troc = Troc(id_troqueur=request.form["id_troqueur"],
                             id_destinataire=request.form["id_destinataire"],
                             id_fichier=id_fichier,
                             date_fichier=request.form["date_fichier"],
                             messages=[messages])
        troc.save()
        return redirect(url_for('index_troc_sent'))

def generate_unique_name_file():
    ts = time.time()
    string_date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
    return f'{PREFIX_FOLDER_TROC_SENT}/troc_{string_date}.json'


