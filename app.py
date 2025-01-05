from flask import Flask, request, jsonify, render_template
import openai

# Postavi OpenAI API ključ
openai.api_key = "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"

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
    app.run(debug=True)
