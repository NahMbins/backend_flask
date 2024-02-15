from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuration de la base de données MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vente"
)

cursor = db.cursor()


def vente_dict(vente):
    return{
    
        'numProduit':vente[0],
        'design':vente[1],
        'prix':vente[2],
        'qte':vente[3],
        'montant':vente[4]

    }

def minmax_dict(vente):
    return{
        'design':vente[0],
        'prix':vente[1],
        

    }


# Endpoint pour récupérer tous les elements de a table vente
@app.route('/api/vente', methods=['GET'])
def get_vente():
    cursor.execute("SELECT numProduit,design,prix,qte,SUM(prix*qte)AS montant FROM vente GROUP BY numProduit ")
    ventes = cursor.fetchall()
    data = {
        'ventes':[vente_dict(vente) for vente in ventes]
    }
    return jsonify(data)

# Endpoint pour récupérer tous les elements de a table vente
@app.route('/api/vente/min', methods=['GET'])
def get_min():
    cursor.execute("SELECT design,MIN(prix) as prix FROM vente")
    ventes = cursor.fetchall()
    data = {
        'min':[minmax_dict(vente) for vente in ventes]
    }
    return jsonify(data)

# Endpoint pour récupérer tous les elements de a table vente
@app.route('/api/vente/max', methods=['GET'])
def get_max():
    cursor.execute("SELECT design,MAX(prix) as prix FROM vente")
    ventes = cursor.fetchall()
    data = {
        'min':[minmax_dict(vente) for vente in ventes]
    }
    return jsonify(data)

# Endpoint pour récupérer tous les elements de a table vente
@app.route('/api/vente/montantTotal', methods=['GET'])
def get_montantTotal():
    cursor.execute("SELECT SUM(qte*prix) AS MontantTotal FROM vente")
    vente = cursor.fetchall()
    data={
        'Total':vente[0][0],
    }
    return jsonify(data)


# Endpoint pour créer un nouvel élément approvisonnement
@app.route('/api/vente', methods=['POST'])
def create_vente():
    data = request.get_json()
    design = data['design']
    prix = data['prix']
    qte = data['qte']
   
    cursor.execute("INSERT INTO vente (design,prix,qte) VALUES (%s,%s, %s)", (design,prix,qte))
    db.commit()

    return jsonify({"message": "L'élément a été créé avec succès"})

# Endpoint pour mettre à jour un élément produit par son ID
@app.route('/api/vente/<int:numProduit>', methods=['PUT'])
def update_vente(numProduit):
    data = request.get_json()
    design = data['design']
    prix = data['prix']
    qte = data['qte']
    cursor.execute("UPDATE vente SET design = %s,prix = %s,qte = %s WHERE numProduit = %s", (design, prix,qte, numProduit))
    db.commit()
    return jsonify({"message": "L'élément a été mis à jour avec succès"})



# Endpoint pour supprimer un élément produit par son ID
@app.route('/api/vente/<int:numProduit>', methods=['DELETE'])
def delete_vente(numProduit):
    cursor.execute("DELETE FROM vente WHERE numProduit = %s", (numProduit,))
    db.commit()

    return jsonify({"message": "L'élément a été supprimé avec succès"})


if __name__ == '__main__':
    app.run(debug=True)
