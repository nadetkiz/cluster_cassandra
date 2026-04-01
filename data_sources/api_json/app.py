from flask import Flask, Response, jsonify
import json
import os
import logging
import xml.etree.ElementTree as ET

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Utiliser des chemins relatifs au dossier du script
BASE_DIR = os.path.dirname(__file__)
JSON_FILE_PATH = os.path.join(BASE_DIR, "paiements.json")
XML_OUTPUT_PATH = os.path.join(BASE_DIR, "paiements.xml")


def write_xml_file():
    with open(JSON_FILE_PATH, 'r', encoding="utf-8") as f:
        data = json.load(f)

    root = ET.Element('paiements')

    # data is expected to be a list of paiement objects
    for entry in data:
        item = ET.SubElement(root, 'item')
        for key in ('id_paiement', 'date_paiement', 'matricule', 'type_paiement', 'montant'):
            value = entry.get(key)
            if value is not None:
                child = ET.SubElement(item, key)
                child.text = str(value)

    tree = ET.ElementTree(root)
    # write with XML declaration and UTF-8 encoding
    tree.write(XML_OUTPUT_PATH, encoding='utf-8', xml_declaration=True)

    logging.info('--- [AUTO] Fichier actualisé avec succes ---')
    with open(XML_OUTPUT_PATH, 'rb') as f:
        return f.read()


@app.route("/paiements", methods=['GET'])
def generate_xml():
    """Route qui renvoie le contenu JSON des paiements."""
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        logging.exception('Erreur lors de la lecture du JSON')
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # tenter une génération initiale sans planter le serveur
    try:
        write_xml_file()
    except Exception:
        logging.exception('Erreur lors de la generation initiale')

    app.run(debug=True, port=5001)