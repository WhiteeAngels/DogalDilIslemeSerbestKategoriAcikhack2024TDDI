from flask import Flask, render_template, request, jsonify
from transformers import pipeline
from gtts import gTTS
import os
import playsound

app = Flask(__name__)

# Transformer model pipeline'ları
classifier = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")
sentiment_analyzer = pipeline("sentiment-analysis")
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Örnek mağaza ve ürün verileri
stores_products = {
    "Nike": ["top", "ayakkabı", "çanta", "forma", "racket", "toka"],
    "Ikea": ["sandalye", "tornavida", "matkap", "çadır"],
    "Mediamarkt": ["cep telefonu", "laptop", "mouse", "kulaklık", "tablet bilgisayar"]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    tts = gTTS(text, lang='tr')
    tts.save("output.mp3")
    playsound.playsound("output.mp3")
    os.remove("output.mp3")
    return 'Metin seslendirildi!'

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text')
    analysis_type = data.get('type')

    if analysis_type == 'text_analysis':
        word_count = len(text.split())
        return jsonify(result=f'Metin {word_count} kelime içeriyor.')

    elif analysis_type == 'text_classification':
        categories = classify_text(text)
        return jsonify(result=f'Metin sınıfı: {categories}')

    elif analysis_type == 'sentiment_analysis':
        sentiment = analyze_sentiment(text)
        return jsonify(result=f'Duygu analizi sonucu: {sentiment}')

    elif analysis_type == 'question_answering':
        question = data.get('question')
        if question:
            answer = answer_question(text, question)
            return jsonify(result=f'Soru-Cevap: {answer}')
        return jsonify(result='Soru belirtilmedi.')

    return jsonify(result='Geçersiz analiz türü.')

def classify_text(text):
    results = classifier(text)
    return results[0]['label']

def analyze_sentiment(text):
    results = sentiment_analyzer(text)
    return results[0]['label']

def answer_question(text, question):
    result = qa_pipeline({'context': text, 'question': question})
    return result['answer']

@app.route('/search_products', methods=['POST'])
def search_products():
    data = request.json
    requested_products = data.get('products', '')
    requested_products = [p.strip() for p in requested_products.split(',')]

    results = []
    for store, products in stores_products.items():
        if all(product in products for product in requested_products):
            results.append({'store': store, 'products': requested_products})

    if results:
        return jsonify({'results': results})
    else:
        return jsonify({'results': 'İstediğiniz ürünlerin hepsini tek bir mağazada bulamadık.'})

if __name__ == '__main__':
    app.run(debug=True)
