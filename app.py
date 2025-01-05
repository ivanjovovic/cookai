from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv
import os
# Postavi OpenAI API ključ
load_dotenv()

# Get OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
# Inicijalizacija Flask aplikacije
app = Flask(__name__, template_folder="templates", static_folder="static")

# Endpoint za generisanje recepta
@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    data = request.json
    ingredients = data.get('ingredients', [])
    equipment = data.get('equipment', [])
    servings = data.get('servings', 1)

    if not ingredients:
        return jsonify({"error": "Niste uneli sastojke"}), 400

    prompt = (
        f"Generiši detaljan recept na crnogorskom jeziku koristeći sledeće sastojke: {', '.join(ingredients)}. "
        f"Korisnik poseduje sledeću opremu: {', '.join(equipment)}. "
        f"Recept treba da bude za {servings} osoba. "
        f"Na kraju prikaži nutritivne vrijednosti jela."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Odgovaraj isključivo na crnogorskom jeziku. Ti si stručnjak za kulinarstvo."},
                {"role": "user", "content": prompt}
            ]
        )
        recipe = response['choices'][0]['message']['content']
        return jsonify({"recipe": recipe}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint za prikaz početne stranice
@app.route('/')
def home():
    return render_template('index.html')

# Pokretanje aplikacije
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port, debug=True)

