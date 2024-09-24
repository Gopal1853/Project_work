from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import unicodedata

app = Flask(__name__)

# english_to_russian_model
tokenizer_en_ru = AutoTokenizer.from_pretrained("Gopal1853/Gopal-finetuned-custom-en-to-ru")
model_en_ru = AutoModelForSeq2SeqLM.from_pretrained("Gopal1853/Gopal-finetuned-custom-en-to-ru")

# russian_to_English_model
tokenizer_ru_en = AutoTokenizer.from_pretrained("Gopal1853/Gopal-finetuned-custom-ru-to-en")
model_ru_en = AutoModelForSeq2SeqLM.from_pretrained("Gopal1853/Gopal-finetuned-custom-ru-to-en")

# english_to_german_model
tokenizer_en_de = AutoTokenizer.from_pretrained("Gopal1853/Gopal-finetuned-custom-en-de")
model_en_de = AutoModelForSeq2SeqLM.from_pretrained("Gopal1853/Gopal-finetuned-custom-en-de")

# german_to_english_model
tokenizer_de_en = AutoTokenizer.from_pretrained("Gopal1853/Gopal-finetuned-custom-de-en")
model_de_en = AutoModelForSeq2SeqLM.from_pretrained("Gopal1853/Gopal-finetuned-custom-de-en")

# english_to_spanish_model
tokenizer_en_es = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-es")
model_en_es = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-es")

# spanish_to_english_model
tokenizer_es_en = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en")
model_es_en = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-es-en")

# english_to_french_model
tokenizer_en_fr = AutoTokenizer.from_pretrained("Gopal1853/marian-finetuned-kde4-en-to-fr")
model_en_fr = AutoModelForSeq2SeqLM.from_pretrained("Gopal1853/marian-finetuned-kde4-en-to-fr")

# english_to_italian_model
tokenizer_en_it = AutoTokenizer.from_pretrained("Gopal1853/Gopal-finetuned-custom-en-to-it")
model_en_it = AutoModelForSeq2SeqLM.from_pretrained("Gopal1853/Gopal-finetuned-custom-en-to-it")

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()

        if 'text' not in data or 'model' not in data:
            return jsonify({'error': 'Invalid request. Required fields: text, model'}), 400
        
        text = data['text']
        model_code = data['model']

        if model_code == 'EN_RU':
            tokenizer = tokenizer_en_ru
            model = model_en_ru
        elif model_code == 'RU_EN':
            tokenizer = tokenizer_ru_en
            model = model_ru_en
        elif model_code == 'EN_DE':
            tokenizer = tokenizer_en_de
            model = model_en_de
        elif model_code == 'DE_EN':
            tokenizer = tokenizer_de_en
            model = model_de_en
        elif model_code == 'EN_ES':
            tokenizer = tokenizer_en_es
            model = model_en_es
        elif model_code == 'ES_EN':
            tokenizer = tokenizer_es_en
            model = model_es_en
        elif model_code == 'EN_FR':
            tokenizer = tokenizer_en_fr
            model = model_en_fr
        elif model_code == 'EN_IT':
            tokenizer = tokenizer_en_it
            model = model_en_it
        else:
            return jsonify({'error': 'Invalid model code. Use EN_RU, RU_EN, EN_DE, DE_EN, EN_ES, ES_EN, EN_FR, or EN_IT.'}), 400

        # Tokenize input text
        inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)

        # Perform translation
        outputs = model.generate(**inputs)

        # Decode the generated output and replace Unicode characters with plain text
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
        translated_text = unicodedata.normalize('NFKD', translated_text).encode('ascii', 'ignore').decode('utf-8')

        return jsonify({'translation': translated_text}), 200

    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(port=5000)
