# Kestirimci Bakım: Reaktör Erken Uyarı Sistemi (Digital Twin & AI)

Bu proje, kimya ve petrokimya endüstrisinde sıkça karşılaşılan ekzotermik reaktör arızalarını (özellikle soğutma suyu kesintisi kaynaklı termal kaçak risklerini) önceden tespit etmek amacıyla geliştirilmiş bir **Kestirimci Bakım (Predictive Maintenance)** ve **Makine Öğrenmesi** uygulamasıdır.

**Canlı Uygulamayı Test Etmek İçin Tıklayın** * [(https://reaktor-erken-uyari-sistemi.streamlit.app)] *

## Projenin Amacı ve Çözdüğü Problem
Endüstriyel tesislerde (örneğin polimerizasyon reaktörleri), soğutma sistemlerindeki bir arıza, reaktör içinde **Termal Kaçak (Thermal Runaway)** adı verilen sapmalara ve yüksek basınç patlamalarına yol açabilir. Klasik sistemler, sadece sıcaklık veya basınç kritik seviyeye ulaştığında alarm verir; bu da müdahale için çoğu zaman çok geçtir.

Bu proje, sadece ham sensör verilerine değil, termodinamik kurallara (İdeal Gaz Yasası - P/T Oranı) odaklanarak; sistemdeki anormal sapmaları **Isolation Forest (İzolasyon Ormanı)** algoritması ile saatler öncesinden yakalar ve "Erken Uyarı" verir.

## Teknik Altyapı ve Metodoloji
Proje üç ana aşamadan oluşmaktadır:

1. **Dijital İkiz (Sentetik Veri Üretimi):** Sürekli Karıştırmalı Tank Reaktörünün (CSTR) 500 dakikalık normal çalışma (steady-state) ve soğutma vanası arıza senaryosu fiziksel kurallara uygun olarak simüle edilmiştir.
2. **Özellik Mühendisliği (Feature Engineering):** Sensör verilerindeki gürültü hareketli ortalama (rolling mean) ile filtrelenmiş ve fiziksel bir anomali belirteci olarak `Basınç/Sıcaklık Oranı` modele tanıtılmıştır.
3. **Yapay Zeka (Denetimsiz Öğrenme):** Sadece "normal" çalışma verileri kullanılarak eğitilen Isolation Forest algoritması, arıza senaryosundaki sapmaları henüz kritik seviyeye ulaşmadan önce başarıyla izole edip tespit etmiştir.

## Kullanılan Teknolojiler
* **Python** (Temel Programlama Dili)
* **Pandas & NumPy** (Veri manipülasyonu ve matematiksel simülasyon)
* **Scikit-Learn** (Isolation Forest Makine Öğrenmesi Modeli)
* **Plotly** (İnteraktif Veri Görselleştirme)
* **Streamlit** (Web Dashboard / Arayüz Geliştirme)

## Kendi Bilgisayarında Çalıştırmak İçin
Projeyi kendi ortamınızda test etmek isterseniz şu adımları izleyebilirsiniz:
1. Bu depoyu bilgisayarınıza klonlayın (veya ZIP dosyası olarak indirin):
   `git clone https://github.com/hudesenturk/reaktor-erken-uyari.git`
2. Projenin çalışması için gerekli kütüphaneleri kurun: 
   `pip install -r requirements.txt`
3. Web uygulamasını başlatın: 
   `streamlit run app.py`
