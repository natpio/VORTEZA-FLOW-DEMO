import streamlit as st
import base64

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="VORTEZA FLOW - Logistics Management System",
    page_icon="🚛",
    layout="wide"
)

# --- FUNKCJA DO ŁADOWANIA TŁA ---
def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64_encoded}");
        background-attachment: fixed;
        background-size: cover;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Próba załadowania tła - upewnij się, że plik jest w repozytorium
try:
    set_background("bg_vorteza.png")
except Exception:
    pass

# --- DANE DEMO (IDENTYCZNA STRUKTURA JAK W CONFIG.JSON) ---
DEMO_CONFIG = {
    "EURO_RATE": 4.3,
    "PRICE": {"fuelPLN": 6.4, "fuelEUR": 1.65},
    "VEHICLE_DATA": {
        "FTL": {"fuelUsage": 0.3, "serviceCostPLN": 0.5, "myto_key": "mytoFTL"},
        "Bus": {"fuelUsage": 0.14, "serviceCostPLN": 0.37, "myto_key": "mytoBus"}
    },
    "ROUTES": {
        "Poznań": {
            "Berlin": {"distPL": 172, "distEU": 101, "mytoFTL": 77.77, "mytoBus": 60.0},
            "Paryż": {"distPL": 172, "distEU": 1144, "mytoFTL": 355.82, "mytoBus": 60.0}
        },
        "Warszawa": {
            "Wrocław": {"distPL": 363, "distEU": 0, "mytoFTL": 24.0, "mytoBus": 90.0},
            "Praga": {"distPL": 470, "distEU": 153, "mytoFTL": 59.57, "mytoBus": 150.0}
        }
    }
}

# --- PASEK BOCZNY (BRANDING) ---
with st.sidebar:
    try:
        st.image("logo_vorteza.png", use_container_width=True)
    except Exception:
        st.title("VORTEZA FLOW")
    
    st.markdown("---")
    st.info("Wersja demonstracyjna systemu rentowności.")
    st.write(f"Aktualny kurs EUR: **{DEMO_CONFIG['EURO_RATE']}**")

# --- GŁÓWNY INTERFEJS ---
st.title("Analiza Rentowności Transportu")

with st.container():
    c1, c2, c3 = st.columns(3)
    
    with c1:
        origin = st.selectbox("Punkt startowy", list(DEMO_CONFIG["ROUTES"].keys()))
    with c2:
        destination = st.selectbox("Cel podróży", list(DEMO_CONFIG["ROUTES"][origin].keys()))
    with c3:
        vehicle_type = st.selectbox("Typ pojazdu", list(DEMO_CONFIG["VEHICLE_DATA"].keys()))

    rate_pln = st.number_input("Stawka frachtu (PLN)", min_value=0, value=5000)

if st.button("OBLICZ RENTOWNOŚĆ", use_container_width=True):
    # Logika obliczeń
    v = DEMO_CONFIG["VEHICLE_DATA"][vehicle_type]
    r = DEMO_CONFIG["ROUTES"][origin][destination]
    
    cost_fuel = (r["distPL"] * v["fuelUsage"] * DEMO_CONFIG["PRICE"]["fuelPLN"]) + \
                (r["distEU"] * v["fuelUsage"] * DEMO_CONFIG["PRICE"]["fuelEUR"] * DEMO_CONFIG["EURO_RATE"])
    
    cost_myto = r[v["myto_key"]] * DEMO_CONFIG["EURO_RATE"]
    cost_service = (r["distPL"] + r["distEU"]) * v["serviceCostPLN"]
    
    total_cost = round(cost_fuel + cost_myto + cost_service, 2)
    margin = round(rate_pln - total_cost, 2)
    roi = round((margin / rate_pln) * 100, 1) if rate_pln > 0 else 0

    # Prezentacja wyników (identycznie jak w pełnej wersji)
    st.markdown("---")
    res1, res2, res3 = st.columns(3)
    
    res1.metric("Koszty całkowite", f"{total_cost} PLN")
    res2.metric("Marża (Zysk)", f"{margin} PLN", delta=f"{margin} PLN")
    res3.metric("Rentowność (ROI)", f"{roi}%")

    if margin > 0:
        st.success("Zlecenie rentowne.")
    else:
        st.error("Zlecenie nierentowne!")

# --- STOPKA ---
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0,0,0,0.5);
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 12px;
    }
    </style>
    <div class="footer">
        VORTEZA FLOW DEMO - SQM Multimedia Solutions System
    </div>
    """,
    unsafe_allow_html=True
)
