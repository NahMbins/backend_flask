from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuration de la base de données MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stock"
)

cursor = db.cursor()

def produit_dict(produit):
    return{
        'numProduit':produit[0],
        'design':produit[1],
        'stock':produit[2],
    }
def fournisseur_dict(fournisseur):
    return{
        'numFrs':fournisseur[0],
        'nom':fournisseur[1],
    }


def approvisonnement_dict(approvisonnement):
    return{
        'id_approvisonnement':approvisonnement[0],
        'numProduit':approvisonnement[1],
        'numFrs':approvisonnement[2],
        'id_login':approvisonnement[3],
        'qteEntree':approvisonnement[4],
    }

def audit_approvisonnement_dict(audit_approvisonnement):
    return{
        'type_action':audit_approvisonnement[0],
        'date':audit_approvisonnement[1],
        'nom':audit_approvisonnement[2],
        'design':audit_approvisonnement[3],
        'qteEntree_ancien':audit_approvisonnement[4],
        'qteEntree_nouv':audit_approvisonnement[5],
    }

def count_audit_approvisonnement_dict(count_audit_approvisonnement):
    return{
        'type_action':count_audit_approvisonnement[0],
        'Nombre':count_audit_approvisonnement[1],
    }
# Endpoint pour récupérer tous les elements de a table produits
@app.route('/api/produit', methods=['GET'])
def get_produit():
    cursor.execute("SELECT * FROM produit")
    produits = cursor.fetchall()
    data = {
        'produits':[produit_dict(produit) for produit in produits]
    }
    return jsonify(data)

# Endpoint pour récupérer tous les elements de a table fournisseurs
@app.route('/api/fournisseur', methods=['GET'])
def get_fournisseur():
    cursor.execute("SELECT * FROM fournisseur")
    fournisseurs = cursor.fetchall()
    data = {
        'fournisseur':[fournisseur_dict(fournisseur) for fournisseur in fournisseurs]
    }
    return jsonify(data)

# Endpoint pour récupérer tous les elements de a table approvisonnement
@app.route('/api/approvisonnement', methods=['GET'])
def get_approvisonnement():
    cursor.execute("SELECT * FROM approvisonnement")
    approvisonnements = cursor.fetchall()
    data = {
        'approvisonnement':[approvisonnement_dict(approvisonnement) for approvisonnement in approvisonnements]
    }
    return jsonify(data)

# Endpoint pour récupérer tous les elements de a table approvisonnement
@app.route('/api/audit_approvisonnement', methods=['GET'])
def get_AuditApprovisonnement():
    cursor.execute("SELECT * FROM audit_approvisonnement")
    audit_approvisonnements = cursor.fetchall()
    data = {
        'audit_approvisonnement':[audit_approvisonnement_dict(audit_approvisonnement) for audit_approvisonnement in audit_approvisonnements]
    }
    return jsonify(data)

# Endpoint pour récupérer tous les elements de a table approvisonnement
@app.route('/api/audit_approvisonnement/count', methods=['GET'])
def get_CountAuditApprovisonnement():
    cursor.execute("SELECT type_action,COUNT(type_action) as Nombre FROM audit_approvisonnement GROUP BY type_action")
    count_audit_approvisonnements = cursor.fetchall()
    data = {
        'audit_approvisonnement':[count_audit_approvisonnement_dict(count_audit_approvisonnement) for count_audit_approvisonnement in count_audit_approvisonnements]
    }
    return jsonify(data)

# Endpoint pour créer un nouvel élément produit
@app.route('/api/produit', methods=['POST'])
def create_produit():
    data = request.get_json()
    design = data['design']
    stock = data['stock']

    cursor.execute("INSERT INTO produit (design, stock) VALUES (%s, %s)", (design, stock))
    db.commit()

    return jsonify({"message": "L'élément a été créé avec succès"})

# Endpoint pour créer un nouvel élément fournisseur
@app.route('/api/fournisseur', methods=['POST'])
def create_fournisseur():
    data = request.get_json()
    nom = data['nom']
   
    cursor.execute("INSERT INTO fournisseur (nom) VALUES (%s)", (nom,))
    db.commit()

    return jsonify({"message": "L'élément a été créé avec succès"})

# Endpoint pour créer un nouvel élément approvisonnement
@app.route('/api/approvisonnement', methods=['POST'])
def create_approvisonnement():
    data = request.get_json()
    numProduit = data['numProduit']
    numFrs = data['numFrs']
    id_login = data['id_login']
    qteEntree = data['qteEntree']
   
    cursor.execute("INSERT INTO approvisonnement (numProduit,numFrs,id_login,qteEntree) VALUES (%s, %s,%s, %s)", (numProduit,numFrs,id_login,qteEntree))
    db.commit()

    return jsonify({"message": "L'élément a été créé avec succès"})

# Endpoint pour mettre à jour un élément produit par son ID
@app.route('/api/produit/<int:numProduit>', methods=['PUT'])
def update_produit(numProduit):
    data = request.get_json()
    design = data['design']
    stock = data['stock']
    cursor.execute("UPDATE produit SET design = %s, stock = %s WHERE numProduit = %s", (design, stock, numProduit))
    db.commit()

    return jsonify({"message": "L'élément a été mis à jour avec succès"})

# Endpoint pour mettre à jour un élément fournisseur par son ID
@app.route('/api/fournisseur/<int:numFrs>', methods=['PUT'])
def update_fournisseur(numFrs):
    data = request.get_json()
    nom = data['nom']
    cursor.execute("UPDATE fournisseur SET nom = %s WHERE numFrs = %s", (nom, numFrs))
    db.commit()

    return jsonify({"message": "L'élément a été mis à jour avec succès"})

# Endpoint pour mettre à jour un élément approvisonnement par son ID
@app.route('/api/approvisonnement/<int:id_approvisonnement>', methods=['PUT'])
def update_approvisonnement(id_approvisonnement):
    data = request.get_json()
    numProduit = data['numProduit']
    numFrs = data['numFrs']
    id_login = data['id_login']
    qteEntree = data['qteEntree']
    cursor.execute("UPDATE approvisonnement SET numProduit = %s,numFrs = %s,id_login = %s,qteEntree = %s WHERE id_approvisonnement = %s", (numProduit, numFrs,id_login,qteEntree,id_approvisonnement))
    db.commit()

    return jsonify({"message": "L'élément a été mis à jour avec succès"})

# Endpoint pour supprimer un élément produit par son ID
@app.route('/api/produit/<int:numProduit>', methods=['DELETE'])
def delete_produit(numProduit):
    cursor.execute("DELETE FROM produit WHERE numProduit = %s", (numProduit,))
    db.commit()

    return jsonify({"message": "L'élément a été supprimé avec succès"})

# Endpoint pour supprimer un élément fournisseur par son ID
@app.route('/api/fournisseur/<int:numFrs>', methods=['DELETE'])
def delete_fournisseur(numFrs):
    cursor.execute("DELETE FROM fournisseur WHERE numFrs = %s", (numFrs,))
    db.commit()

    return jsonify({"message": "L'élément a été supprimé avec succès"})

# Endpoint pour supprimer un élément approvisonnement par son ID
@app.route('/api/approvisonnement/<int:id_approvisonnement>', methods=['DELETE'])
def delete_approvisonnement(id_approvisonnement):
    cursor.execute("DELETE FROM approvisonnement WHERE id_approvisonnement = %s", (id_approvisonnement,))
    db.commit()

    return jsonify({"message": "L'élément a été supprimé avec succès"})

if __name__ == '__main__':
    app.run(debug=True)
