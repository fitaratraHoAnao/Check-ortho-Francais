from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL de l'API LanguageTool
LANGUAGETOOL_API_URL = "https://languagetool.org/api/v2/check"

# Route principale qui affiche un message lorsque le serveur est en ligne
@app.route('/')
def home():
    return "Votre API Flask correction orthographe français est en cours d'exécution...."

# Route pour vérifier l'orthographe
@app.route('/check', methods=['POST'])
def check_text():
    # Récupérer le texte et la langue depuis la requête POST
    text = request.json.get('text', '')
    language = request.json.get('language', 'fr')  # Par défaut, on met 'fr' pour le français

    if not text:
        return jsonify({'error': 'Le texte est requis'}), 400

    # Préparer les données à envoyer à l'API LanguageTool
    data = {
        'text': text,
        'language': language
    }

    # Envoyer la requête à l'API LanguageTool
    response = requests.post(LANGUAGETOOL_API_URL, data=data)

    if response.status_code != 200:
        return jsonify({'error': 'Erreur lors de l\'appel à LanguageTool'}), 500

    # Récupérer la réponse JSON
    lt_data = response.json()

    # Extraire les informations essentielles (message et suggestions)
    corrections = []
    for match in lt_data.get('matches', []):
        corrections.append({
            'message': match.get('message'),
            'suggestions': [suggestion['value'] for suggestion in match.get('replacements', [])]
        })

    # Renvoyer la réponse simplifiée sous forme de JSON
    return jsonify({
        'corrections': corrections
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
