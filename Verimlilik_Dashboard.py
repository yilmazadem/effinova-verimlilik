...
    # Haftalık Ortalama
    st.subheader("🕒 Haftalık Ortalama Verimlilik Skoru")
    df["Hafta"] = df["Tarih"].dt.isocalendar().week
    haftalik = df.groupby("Hafta")["Skor"].mean().reset_index()
    st.line_chart(haftalik.set_index("Hafta"))

    # Yapay Zekâ destekli özet yorum
    st.subheader("🧠 AI Destekli Rapor Özeti")
    if ort > 0.75:
        yorum = "Genel performans çok iyi seviyede. Takım motivasyonu yüksek ve süreçler verimli işliyor."
    elif ort > 0.50:
        yorum = "Performans ortalamanın biraz üstünde. Geliştirme alanları belirlenerek küçük dokunuşlarla iyileşme sağlanabilir."
    elif ort > 0.30:
        yorum = "Performans zayıf. Belirli ekiplerdeki verimlilik sorunları detaylı analiz edilerek aksiyon alınmalı."
    else:
        yorum = "Kritik düzeyde düşük performans. Yönetim düzeyinde müdahale ve kapsamlı yeniden yapılandırma önerilir."
    st.info(yorum)

    # CSV İndirme
    ...
