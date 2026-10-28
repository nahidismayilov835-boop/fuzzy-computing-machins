import streamlit as st
import pandas as pd
import numpy as np

# Səhifənin tənzimlənməsi
st.set_page_config(page_title="SOCAR Hackathon - Quyu Analizi", page_icon="🛢️", layout="wide")

st.title("🛢️ Quyu Performansının İntellektual Təhlili (Prototip)")
st.markdown("SOCAR Hackathon 2026 üçün ilkin süni intellekt/analitika modelinin idarəetmə paneli.")

# Yan panel (Parametrlərin daxil edilməsi)
st.sidebar.header("📊 Quyu Parametrləri")
tezyiq = st.sidebar.slider("Bunker/Boru Təzyiqi (bar)", 50, 350, 180)
temperatur = st.sidebar.slider("Quyu Dibi Temperaturu (°C)", 30, 120, 65)
derinlik = st.sidebar.number_input("Quyunun Dərinliyi (metr)", min_value=500, max_value=5000, value=2500)
su_faizi = st.sidebar.slider("Su Qarışığı Faizi (%)", 0, 90, 15)

# Hesablama və Alqoritm
# Hasilatın hesablanması (Sadələşdirilmiş riyazi model)
ham_hasilat = (tezyiq * 0.7) + (derinlik / 80) - (temperatur * 0.3)
su_faktor = 1 - (su_faizi / 100)
real_hasilat = max(10, ham_hasilat * su_faktor)

# Risk və Status təyini
risk_status = "Optimal"
status_rengi = "green"
tovsiye = "Quyu normal rejimdə işləyir. Heç bir müdaxiləyə ehtiyac yoxdur."

if tezyiq > 280 or temperatur > 100:
    risk_status = "Kritik Risk (Yüksək Təzyiq/Temperatur)"
    status_rengi = "red"
    tovsiye = "Təcili olaraq təzyiq tənzimlənməli və klapanlar yoxlanılmalıdır!"
elif su_faizi > 60:
    risk_status = "Yüksək Su Təhlükəsi"
    status_rengi = "orange"
    tovsiye = "Quyuda su basması (water breakthrough) ehtiyacı var. İzolə işləri aparılmalıdır."

# Əsas Ekran - Nəticələr
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Gündəlik Təxmini Hasilat", value=f"{round(real_hasilat, 2)} ton/gün")

with col2:
    st.metric(label="Quyu Sağlamlıq İndeksi", value=f"{max(0, 100 - su_faizi)}%")

with col3:
    st.markdown(f"**Status:**")
    if status_rengi == "green":
        st.success(risk_status)
    elif status_rengi == "orange":
        st.warning(risk_status)
    else:
        st.error(risk_status)

st.info(f"💡 **Süni İntellekt Tövsiyəsi:** {tovsiye}")

st.markdown("---")

# Qrafik Hissəsi: Son 7 günün təzyiq dəyişimi simulyasiyası
st.subheader("📈 Quyu Təzyiqinin Son Günlər Üzrə Dinamikası")
gunler = [f"Gün - {i}" for i in range(7, 0, -1)]
simulyasiya_tezyiq = [tezyiq + np.random.randint(-15, 15) for _ in range(7)]

df_chart = pd.DataFrame({
    'Gün': gunler,
    'Təzyiq (bar)': simulyasiya_tezyiq
})

st.line_chart(df_chart.set_index('Gün'))