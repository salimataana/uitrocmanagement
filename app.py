
import json
import datetime
import time
from flask import Flask, render_template, request, url_for, flash, redirect
from pyexpat.errors import messages

from data_access import get_all_trocs

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/index")
def index():
    trocs,noms_des_fichiers_pas_bons=get_all_trocs()
    return render_template("indextroc.html",trocs=trocs,noms_des_fichiers_pas_bons=noms_des_fichiers_pas_bons)

@app.route("/create",methods=("GET", "POST"))
def create():
    if request.method=="GET":
        return render_template("createtroc.html")
    if request.method=="POST":


        id_troqueur=request.form["id_troqueur"]
        id_destinataire = request.form["id_destinataire"]
        id_fichier = request.form["id_fichier"]
        date_fichier = request.form["date_fichier"]
        date_message = request.form["date_message"]
        statut= request.form["statut"]
        titre = request.form[f"titre"]
        description = request.form[f"description"]
        qualite = int(request.form[f"qualite"])
        quantite = int(request.form[f"quantite"])
        objets = [{"titre":titre,
          "description":description,
          "qualite": qualite,
          "quantite": quantite}]
        messages = [{"date_message":date_message, "statut":statut, "objets":objets}]



        """messages = []
        nombre_messages = int(request.form["message_count"])
        for i in range(nombre_messages):
            date_message = request.form[f"date_message_{i}"]
            statut = request.form[f"statut_{i}"]
            objets = []
            nombre_objets = int(request.form[f"objet_count_{i}"])
            for j in range(nombre_objets):
                titre = request.form[f"titre_{i}_{j}"]
                description = request.form[f"description_{i}_{j}"]
                qualite = int(request.form[f"qualite_{i}_{j}"])
                quantite = int(request.form[f"quantite_{i}_{j}"])
                objets.append({
                    "titre": titre,
                    "description": description,
                    "qualite": qualite,
                    "quantite": quantite
                })
            messages.append({
                "date_message": date_message,
                "statut": statut,
                "objets": objets
            })
        """

        my_json={"id_troqueur":id_troqueur,"id_destinataire":id_destinataire, "id_fichier":id_fichier,
                 "date_fichier":date_fichier,"messages":messages, "checksum":"toto"}




        ts=time.time()
        string_date=datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
        with open(f'data/example_{string_date}.json', 'w') as fp:
            json.dump(my_json, fp)
        return redirect(url_for('index'))