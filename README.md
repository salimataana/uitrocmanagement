<option value="accepte">Accepté</option>
            <option value="valide">Validé</option>
            <option value="annule">Annulé</option>
            <option value="refuse">Refusé</option>






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