from flask import Flask, render_template, request, jsonify
from transformers import pipeline,AutoModelForTokenClassification, AutoModelForSequenceClassification, AutoTokenizer,AutoModelForQuestionAnswering
from gtts import gTTS
import os
import playsound
import re
import pandas as pd
from datasets import load_dataset

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

# Veri setini yükle ve işleme
dataset = load_dataset("WhiteAngelss/magaza-urun-listesi-with-links", split='train')
df = pd.DataFrame(dataset)
df = df['Mağaza;Ürün;Link'].str.split(';', expand=True)
df.columns = ['Mağaza', 'Ürün', 'Link']

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
        return jsonify(result=categories)

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
    results = classifier(text)
    categories = {}
    entity_types = {
        'PER': 'Kişi',
        'LOC': 'Yer',
        'ORG': 'Organizasyon'
    }

    for entity in results:
        entity_type = entity['entity'].split('-')[-1]  # Eğer entity tipleri 'B-LOC', 'I-LOC' şeklindeyse son kısmı al
        entity_text = entity['word']
        entity_type_turkish = entity_types.get(entity_type, 'Bilinmeyen')  # Türkçeye çevir

        if entity_type_turkish not in categories:
            categories[entity_type_turkish] = []
        categories[entity_type_turkish].append(entity_text)

    return categories

def analyze_sentiment(text):
    results = sentiment_analyzer(text)
    sentiment = results[0]['label']
    return sentiment


def answer_question(text, question):
    result = qa_pipeline({'context': text, 'question': question})
    return result['answer']


def find_stores_with_products(products, df):
    # Mağaza bazında ürünleri ve linkleri gruplandır
    store_products_links = df.groupby('Mağaza').agg(
        {'Ürün': lambda x: list(x), 'Link': lambda x: list(x)}
    ).reset_index()

    # Mağaza-Ürün-Link şeklinde bir sözlük oluştur
    store_products_dict = store_products_links.set_index('Mağaza').to_dict('index')

    # Girilen ürünleri barındıran mağazaları bul
    matching_stores = {}
    for store, details in store_products_dict.items():
        store_products = details['Ürün']
        store_links = details['Link']

        # Ürünlerin hepsi mağazada var mı?
        if all(prod in store_products for prod in products):
            matching_products = []
            matching_links = []
            for product in products:
                idx = store_products.index(product)
                matching_products.append(store_products[idx])
                matching_links.append(store_links[idx])
            matching_stores[store] = {'products': matching_products, 'links': matching_links}

    return matching_stores




@app.route('/search_products', methods=['POST'])
def search_products():
    data = request.json
    products = [product.strip() for product in data.get('products', '').split(',')]
    matching_stores = find_stores_with_products(products, df)

    if matching_stores:
        results = [{'store': store, 'products': details['products'], 'links': details['links']} for store, details in
                   matching_stores.items()]
        return jsonify({'results': results})
    else:
        return jsonify({'results': []})

if __name__ == '__main__':
    app.run(debug=True)
