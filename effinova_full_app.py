
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="EFFINOVA Panel", layout="wide")
st.title("🕊️ EFFINOVA | Verimlilik + İnovasyon Skoru Paneli")
st.markdown("Her kurum kendi Anka’sına uçar.")

# Oturum verisi
if "veriler" not in st.session_state:
    st.session_state.veriler = []

# Giriş Formu
with st.form("verimlilik_formu"):
    col1, col2 = st.columns(2)
    with col1:
        ad = st.text_input("Ad Soyad")
        departman = st.selectbox("Departman", ["İK", "Satış", "Kabin Hizmetleri", "Kargo", "Ar-Ge", "Hukuk"])
        cikti = st.number_input("Üretilen Çıktı", min_value=1)
        kalite = st.slider("Kalite Katsayısı", 0.0, 1.0, 0.90)
    with col2:
        katkı = st.select_slider("Katkı Katsayısı", options=[0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5])
        inovasyon = st.slider("İnovasyon Katsayısı", 0.0, 1.0, 0.2)
        zaman = st.number_input("Harcanan Zaman (saat)", min_value=1)
    gönder = st.form_submit_button("Hesapla ve Listeye Ekle")

# Skor Hesaplama
def hesapla_skor(cikti, kalite, katkı, inovasyon, zaman):
    return round((cikti * kalite * katkı * (1 + inovasyon)) / zaman, 2)

def aksiyon(skor):
    if skor > 3.5:
        return "🎖️ Ödüllendirme", "🟢"
    elif skor >= 2.0:
        return "📈 Gelişim Planı", "🟡"
    elif skor >= 1.0:
        return "👥 Mentorluk", "🟡"
    elif skor >= 0.5:
        return "🔁 Görev Değişikliği", "🔴"
    else:
        return "⚠️ Akit Gözden Geçirilsin", "🔴"

# Listeye Ekleme
if gönder:
    skor = hesapla_skor(cikti, kalite, katkı, inovasyon, zaman)
    aks, durum = aksiyon(skor)
    st.session_state.veriler.append({
        "Ad Soyad": ad,
        "Departman": departman,
        "Çıktı": cikti,
        "Kalite": kalite,
        "Katkı": katkı,
        "İnovasyon": inovasyon,
        "Zaman": zaman,
        "Skor": skor,
        "Durum": durum,
        "Aksiyon": aks,
        "Tarih": datetime.today().strftime('%Y-%m-%d')
    })

# Skor Tablosu
if st.session_state.veriler:
    st.subheader("📋 Çalışan Skorları")
    df = pd.DataFrame(st.session_state.veriler)
    st.dataframe(df, use_container_width=True)

    ortalama = df["Skor"].mean()
    st.metric("📊 Ortalama Verimlilik Skoru", f"{ortalama:.2f}")
    st.progress(min(ortalama / 5, 1.0))  # Maksimum 5'e normalize bar

    # Aksiyon Grafiği
    st.subheader("🧭 Aksiyon Dağılımı")
    aksiyonlar = df["Aksiyon"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(aksiyonlar, labels=aksiyonlar.index, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

    # Skor Zaman Serisi
    st.subheader("📅 Tarihe Göre Skor Eğilimi")
    fig2, ax2 = plt.subplots()
    df_sorted = df.sort_values("Tarih")
    df_sorted["Tarih"] = pd.to_datetime(df_sorted["Tarih"])
    df_grouped = df_sorted.groupby("Tarih")["Skor"].mean()
    df_grouped.plot(kind="line", marker="o", ax=ax2)
    ax2.set_ylabel("Ortalama Skor")
    st.pyplot(fig2)

    # İndirilebilir CSV
    st.download_button(
        label="📥 Verileri CSV olarak indir",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="effinova_skorlari.csv",
        mime="text/csv"
    )
