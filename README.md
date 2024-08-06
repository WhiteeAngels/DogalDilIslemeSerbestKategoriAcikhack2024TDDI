# Türkçe Doğal Dil İşleme Projesi - Açıkhack 2024 - Acikhack2024TDDI
### Bu proje Teknofest Dogal Dil İşleme için yapılmıştır. 
(https://www.teknofest.org/tr/yarismalar/turkce-dogal-dil-isleme-yarismasi/)py
## Takım Bilgileri

**Takım Adı:** White Angels

**Hugging Face:** [White Angels](https://huggingface.co/WhiteAngelss)

**Github:** [White Angels](https://github.com/WhiteeAngels)

### Takım Üyeleri:

- **Ali Emre (Kaptan):** [GitHub](https://github.com/Aliemree)
- **İhsan Yörük:** [GitHub](https://github.com/yorukihsan1)
- **Can Ahmedi Yaşar Parlak:** [GitHub](https://github.com/canahmed)
- **Uğur Çoruh (Danışman):** [GitHub](https://github.com/ucoruh)

# Proje Hakkında

Bu proje, Türkçe metinlerin otomatik olarak ve entitylerin sınıflandırılması, duygu analizi yapılması, metinlerin anlamının anlaşılması, soru-cevap işlemleri, metin okuma ve ürün almak için geliştirilmiştir.
# Model Açıklaması
Kullandığımız modeller: 'dbmdz/bert-base-turkish-cased', 'yunusemreemik/logo-qna-model', 'gurkan08/turkish-product-comment-sentiment-classification', 'akdeniz27/convbert-base-turkish-cased-ner' veri setleri üzerinde eğitilmiştir.

# DataSet Açıklaması
Kendi Hugging Face'imizde oluşturduğumuz dataset kullanılmıştır. 'WhiteAngelss/magaza-urun-listesi-with-links'
### Gereksinimler

transformers
tf-keras
torch
torchvision
torchaudio
flask
gunicorn
rankit
datasets
pandass

Gerekli kütüphaneleri yüklemek için:
pip install -r requirements.txt
# Kullanım Amacı
Model; metin sınıflandırma, analizleri, soru-cevap ve okuma işlemlerini yapmaktadır. Ayrıca kullanıcının istediği ürünleri tek bir mağazada almasını sağlayacak model de içermektedir.  
# Proje Mimarisi
Bu proje beş ana bileşenden oluşmaktadır:
Metin Analizi: Girilen metinin kaç kelime olduğunu analiz eder.
Metin Sınıflandırma: Girilen metini entitylerine ayırarak entity sınıflandırması yapar.
Metin Soru-Cevap: Girilen metinle ilgili soru sorarak cevap verdirmesi yapılır.
Metin Okuma: Girilen metinin sesli bir şekilde okunması sağlanır.
Ürün Alma: Girilen ürünlerin hepsini içeren mağaza listelenir.
## Kullanım

Flask uygulamasını çalıştırmak için:
python app.py
## Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Daha fazla bilgi için [LICENSE](./LICENSE) dosyasına bakınız.

Bu proje **WhiteAngels** tarafından yapılmıştır.
