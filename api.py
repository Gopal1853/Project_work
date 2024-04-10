from flask import Flask, request
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# Load EN to RU model
tokenizer_en_ru = AutoTokenizer.from_pretrained("Bradpitt1234/Gopal-finetuned-custom-en-to-ru")
model_en_ru = AutoModelForSeq2SeqLM.from_pretrained("Bradpitt1234/Gopal-finetuned-custom-en-to-ru")

# Load RU to EN model
tokenizer_ru_en = AutoTokenizer.from_pretrained("Bradpitt1234/Gopal-finetuned-custom-ru-to-en")
model_ru_en = AutoModelForSeq2SeqLM.from_pretrained("Bradpitt1234/Gopal-finetuned-custom-ru-to-en")

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()

        if 'text' not in data or 'model' not in data:
            return 'Invalid request. Required fields: text, model', 400
        
        text = data['text']
        model_code = data['model']

        if model_code == 'EN_RU':
            tokenizer = tokenizer_en_ru
            model = model_en_ru
        elif model_code == 'RU_EN':
            tokenizer = tokenizer_ru_en
            model = model_ru_en
        else:
            return 'Invalid model code. Use EN_RU or RU_EN.', 400

        max_length = model.config.max_length  # Get maximum input size from model configuration

        inputs = tokenizer(text, return_tensors="pt", max_length=max_length, truncation=True)

        outputs = model.generate(**inputs)

        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return translated_text, 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Internal Server Error', 500

if __name__ == '__main__':
    app.run(port=5000)
