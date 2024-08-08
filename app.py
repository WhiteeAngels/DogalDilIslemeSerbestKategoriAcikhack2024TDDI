from flask import Flask, render_template, request, jsonify
from transformers import pipeline,AutoModelForTokenClassification, AutoModelForSequenceClassification, AutoTokenizer,AutoModelForQuestionAnswering
from gtts import gTTS
import os
import playsound
import re

app = Flask(__name__)

 # Transformer model pipeline'ları
classifier = pipeline("ner", model="akdeniz27/convbert-base-turkish-cased-ner")
text_analysis_pipeline = pipeline("feature-extraction", model="dbmdz/bert-base-turkish-cased")

# Yeni Duygu Analizi Modeli
model_name = "gurkan08/turkish-product-comment-sentiment-classification"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Yeni Soru-Cevap Modeli
qa_model_name = "yunusemreemik/logo-qna-model"
qa_tokenizer = AutoTokenizer.from_pretrained(qa_model_name)
qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model_name)
qa_pipeline = pipeline("question-answering", model=qa_model, tokenizer=qa_tokenizer)

# Örnek mağaza ve ürün verileri
stores_products = {
    "Nike": ["top", "ayakkabı", "çanta", "forma", "racket", "toka"],
    "Ikea": ["sandalye", "tornavida", "matkap", "çadır"],
    "Mediamarkt": ["cep telefonu", "laptop", "mouse", "kulaklık", "tablet bilgisayar"]
}

# Yeni Metin Sınıflandırma Modeli
text_classification_model_name = "dbmdz/bert-base-turkish-cased"
text_classification_tokenizer = AutoTokenizer.from_pretrained(text_classification_model_name)
text_classification_model = AutoModelForSequenceClassification.from_pretrained(text_classification_model_name)
text_classifier = pipeline("text-classification", model=text_classification_model, tokenizer=text_classification_tokenizer)

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
        analysis_result = analyze_text(text)
        return jsonify(result=analysis_result)

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

def analyze_text(text):
    # Kelime ve karakter sayısı analizi
    words = text.split()
    word_count = len(words)
    character_count = len(text)

    # Cümle sayısı analizi
    sentences = re.split(r'[.!?]', text)
    sentence_count = len([s for s in sentences if s.strip() != ""])

    # Ortalama kelime uzunluğu
    if word_count > 0:
        average_word_length = sum(len(word) for word in words) / word_count
    else:
        average_word_length = 0

    analysis_result = (
        f"Kelime Sayısı: {word_count}\n"
        f"Karakter Sayısı: {character_count}\n"
        f"Cümle Sayısı: {sentence_count}\n"
        f"Ortalama Kelime Uzunluğu: {average_word_length:.2f}"
    )
    return analysis_result


def classify_text(text):
    # Text classification using a transformer model
    results = classifier(text)
    return results[0]['label']


def analyze_sentiment(text):
    results = sentiment_analyzer(text)
    sentiment = results[0]['label']
    return sentiment


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
