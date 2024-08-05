// Overlay gösterim işlevi
function showAbout() {
    document.getElementById("about-overlay").style.display = "flex";
}

// Overlay kapama işlevi
function closeAbout() {
    document.getElementById("about-overlay").style.display = "none";
}

// Koyu mod / açık mod geçiş işlevi
function toggleMode() {
    document.body.classList.toggle('dark-mode');
}

// Bölümleri soluklaştırma ve aktif bölüm vurgulama işlevi
function dimSections(activeSection) {
    const sections = document.querySelectorAll('.section');
    sections.forEach((section, index) => {
        if (index + 1 === activeSection) {
            section.classList.remove('dimmed');
            section.classList.add('active-section'); // Aktif bölümü vurgulama
        } else {
            section.classList.add('dimmed');
            section.classList.remove('active-section'); // Diğer bölümleri soluklaştırma
        }
    });
}

// Metin analizi işlevi
function analyzeText() {
    const text = document.getElementById('text-analysis').value;
    if (text.trim() === "") {
        alert("Lütfen metin giriniz.");
        return;
    }
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text, type: 'text_analysis' })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.result);
    });
}


// Metin sınıflandırma işlevi
function classifyText() {
    const text = document.getElementById('text-classification').value;
    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, type: 'text_classification' })
    }).then(response => response.json())
      .then(data => {
        let result = "Metin sınıflandırması:\n";
        for (let entity in data.result) {
            result += `${entity}: ${data.result[entity]}\n`;
        }
        alert(result);
      })
      .catch(error => console.error('Hata:', error));
}



// duygu analizi
function analyzeSentiment() {
    const text = document.getElementById('sentiment-analysis').value;
    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, type: 'sentiment_analysis' })
    }).then(response => response.json())
      .then(data => alert(data.result))
      .catch(error => console.error('Hata:', error));
}

// Soru-cevap işlevi
function answerQuestion() {
    const text = document.getElementById('qa-context').value;
    const question = document.getElementById('qa-question').value;
    fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, type: 'question_answering', question: question })
    }).then(response => response.json())
      .then(data => alert(data.result))
      .catch(error => console.error('Hata:', error));
}

// Metin okuma işlevi
function readText() {
    const text = document.getElementById('text-to-read').value;
    if (text.trim() === "") {
        alert("Metin boş. Lütfen bir metin girin.");
        return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
}

// Ürün arama işlevi
function searchProducts() {
    const products = document.getElementById('product-search').value.split(',').map(p => p.trim().toLowerCase());
    if (products.length === 0 || products[0] === "") {
        alert("Lütfen ürün giriniz.");
        return;
    }

    fetch('/search_products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ products: products })
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('search-results');
        resultsDiv.innerHTML = ''; // Önceki sonuçları temizle
        if (data.results && Array.isArray(data.results) && data.results.length > 0) {
            data.results.forEach(result => {
                // Her bir ürün ve mağaza sonucunu bir HTML elemanı olarak ekleyin
                const resultElement = document.createElement('div');
                resultElement.classList.add('result-item');
                resultElement.textContent = `Ürünler mevcut: ${result.store}`;
                resultsDiv.appendChild(resultElement);
            });
        } else {
            resultsDiv.innerHTML = "<p>Ürün bulunamadı.</p>";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const resultsDiv = document.getElementById('search-results');
        resultsDiv.innerHTML = "<p>Bir hata oluştu. Lütfen tekrar deneyin.</p>";
    });
}

function readText() {
    const text = document.getElementById('text-to-read').value;
    if (text.trim() === "") {
        alert("Metin boş. Lütfen bir metin girin.");
        return;
    }

    fetch('/speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `text=${encodeURIComponent(text)}`
    }).then(response => response.text())
      .then(result => alert(result))
      .catch(error => console.error('Hata:', error));
}

// Diğer işlem işlevleri
function processText() {
    const text = document.getElementById('text-input').value;
    console.log("İlk bölüm metni: ", text);
}

function anotherProcess() {
    const text = document.getElementById('another-text-input').value;
    console.log("İkinci bölüm metni: ", text);
}

function moreProcess() {
    const text = document.getElementById('more-text-input').value;
    console.log("Üçüncü bölüm metni: ", text);
}

function evenMoreProcess() {
    const text = document.getElementById('even-more-text-input').value;
    console.log("Dördüncü bölüm metni: ", text);
}
