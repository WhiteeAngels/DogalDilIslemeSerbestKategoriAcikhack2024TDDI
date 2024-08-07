# Türkçe Doğal Dil İşleme Projesi - Açıkhack 2024 - Acikhack2024TDDI

### [Bu proje Teknofest Doğal Dil İşleme Yarışması için yapılmıştır](https://www.teknofest.org/tr/yarismalar/turkce-dogal-dil-isleme-yarismasi/).

## Takım Bilgileri

**Takım Adı:** White Angels

**Hugging Face:** [White Angels](https://huggingface.co/WhiteAngelss)

**Github:** [White Angels](https://github.com/WhiteeAngels)

### Takım Üyeleri

- **Ali EMRE (Kaptan):** [GitHub](https://github.com/Aliemree)
- **İhsan YÖRÜK:** [GitHub](https://github.com/yorukihsan1)
- **Can Ahmedi Yaşar PARLAK:** [GitHub](https://github.com/canahmed)
- **Dr. Öğr. Üyesi Uğur CORUH (Danışman):** [GitHub](https://github.com/ucoruh)

# Proje Hakkında

Bu proje, Türkçe metinlerin otomatik olarak sınıflandırılması, entitylerin belirlenmesi, duygu analizinin yapılması, metinlerin anlamının anlaşılması, soru-cevap işlemleri ve metin okuma gibi amaçlarla geliştirilmiştir.

## Model Açıklaması

Kullandığımız modeller:

- dbmdz/bert-base-turkish-cased
- yunusemreemik/logo-qna-model
- gurkan08/turkish-product-comment-sentiment-classification
- akdeniz27/convbert-base-turkish-cased-ner

## Veri Seti Açıklaması

Kendi Hugging Face hesabımızda oluşturduğumuz `WhiteAngelss/magaza-urun-listesi-with-links` veri seti kullanılmıştır.

## Gereksinimler

Gerekli kütüphaneleri yüklemek için:

```bash
pip install -r requirements.txt
```

Gereken Kütüphaneler:

- transformers
- tf-keras
- torch
- torchvision
- torchaudio
- flask
- gunicorn
- rankit
- datasets
- pandas

## Kullanım Amacı

Model, metin sınıflandırma, analizleri, soru-cevap ve okuma işlemlerini yapmaktadır. Ayrıca, kullanıcının istediği ürünleri tek bir mağazada almasını sağlayacak bir modeli de içermektedir.

## Proje Mimarisi

Bu proje beş ana bileşenden oluşmaktadır:

1. **Metin Analizi**: Girilen metnin kaç kelime olduğunu analiz eder.
2. **Metin Sınıflandırma**: Girilen metni entitylerine ayırarak sınıflandırma yapar.
3. **Soru-Cevap**: Girilen metinle ilgili soruları yanıtlar.
4. **Metin Okuma**: Girilen metni sesli olarak okur.
5. **Ürün Alma**: Girilen ürünlerin hepsini içeren mağaza listeler.

## Kullanım

Flask uygulamasını çalıştırmak için:

```bash
python app.py
```

## Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Daha fazla bilgi için [LICENSE](./LICENSE) dosyasına bakınız.



Bu proje **WhiteAngels** tarafından yapılmıştır.
