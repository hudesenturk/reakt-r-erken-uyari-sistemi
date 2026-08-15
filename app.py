import streamlit as st
import pandas as pd
import numpy as np
import time
from sklearn.ensemble import IsolationForest
import plotly.express as px

# 1. SAYFA AYARLARI
st.set_page_config(page_title="AI Erken Uyarı Sistemi", page_icon="🏭", layout="wide")

st.title("🏭 Reaktör Kestirimci Bakım ve Erken Uyarı Paneli")
st.markdown("""
Bu canlı panel, ekzotermik bir proses reaktöründeki **soğutma suyu vanası arızasını** (termal kaçak riski), 
proses fiziği ve **Isolation Forest** yapay zeka modeli kullanarak önceden tespit etmek için tasarlanmıştır.
""")

# 2. VERİ ÜRETİMİ VE YAPAY ZEKA MODELİ (Arka Plan İşlemleri)
@st.cache_data
def run_model():
    np.random.seed(42) 
    # Normal Veri
    df_normal = pd.DataFrame({
        'Reaktor_Basinci': np.random.normal(2700, 15, 500), 
        'Reaktor_Sicakligi': np.random.normal(120, 1.5, 500), 
        'Sogutma_Suyu_Debisi': np.random.normal(3500, 50, 500)
    })
    # Arızalı Veri
    df_fault = pd.DataFrame({
        'Reaktor_Basinci': np.concatenate([np.random.normal(2700, 15, 200), np.linspace(2700, 3200, 300) + np.random.normal(0, 20, 300)]),
        'Reaktor_Sicakligi': np.concatenate([np.random.normal(120, 1.5, 200), np.linspace(120, 145, 300) + np.random.normal(0, 2, 300)]),
        'Sogutma_Suyu_Debisi': np.concatenate([np.random.normal(3500, 50, 200), np.linspace(3500, 1500, 300) + np.random.normal(0, 40, 300)])
    })

    # Özellik Türetme
    for df in [df_normal, df_fault]:
        df['P_T_Orani'] = df['Reaktor_Basinci'] / (df['Reaktor_Sicakligi'] + 273.15)
        
    # Model Eğitimi
    ozellikler = ['Reaktor_Basinci', 'Reaktor_Sicakligi', 'P_T_Orani']
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(df_normal[ozellikler])
    
    # Tahmin
    df_fault['Anomali_Skoru'] = model.predict(df_fault[ozellikler])
    df_fault['Durum'] = df_fault['Anomali_Skoru'].map({1: 'Normal', -1: 'Anomali (Tehlike)'})
    
    return df_fault

df_sonuc = run_model()

# 3. CANLI AKIŞ (SCADA SİMÜLASYONU) EKRANI 
st.title("🏭 Reaktör Erken Uyarı Sistemi (Canlı Akış)")
st.write("Bu panel, reaktördeki basınç ve sıcaklık verilerini saniye saniye okuyarak anomali tespiti yapar.")

# Ekranı canlı güncellemek için boş bir kutu (placeholder) oluşturuyoruz
placeholder = st.empty()

# Veriyi sanki saniye saniye okuyormuşuz gibi bir döngüye sokuyoruz
for saniye in range(10, len(df_sonuc), 5): # 5'er 5'er atlayarak hızlı bir animasyon yapar
    
    # O anki saniyeye kadar olan veriyi kesip alıyoruz
    df_anlik = df_sonuc.iloc[:saniye]
    son_durum = df_anlik.iloc[-1]
    
    # Tüm ekranı 'placeholder' içine çizdiriyoruz ki sürekli yenilensin
    with placeholder.container():
        st.subheader("Anlık Sistem Durumu")
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Son Basınç", f"{son_durum['Reaktor_Basinci']:.0f} kPa", delta_color="inverse")
        col2.metric("Son Sıcaklık", f"{son_durum['Reaktor_Sicakligi']:.1f} °C", delta_color="inverse")
        
        if son_durum['Durum'] == 'Normal':
            col3.success("Sistem Durumu: NORMAL")
        else:
            col3.error("Sistem Durumu: ANOMALİ TESPİT EDİLDİ!")
            
        # Canlı güncellenen grafik
        fig = px.scatter(
            df_anlik, x=df_anlik.index, y='Reaktor_Basinci', color='Durum',
            color_discrete_map={'Normal': '#00b4d8', 'Anomali (Tehlike)': '#d00000'},
            labels={'index': 'Zaman (Dakika)', 'Reaktor_Basinci': 'Basınç (kPa)'},
            range_x=[0, 500], range_y=[2650, 3250] # Eksenleri sabitliyoruz ki grafik titremesin
        )
        fig.add_vline(x=200, line_dash="dash", line_color="green", annotation_text="Arıza Başlangıcı")
        st.plotly_chart(fig, use_container_width=True)
        
    # Her güncelemeden sonra 0.1 saniye bekle (Gerçek zamanlı animasyon hissi)
    time.sleep(0.1)