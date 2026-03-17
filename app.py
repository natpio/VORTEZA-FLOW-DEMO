import streamlit as st
import base64
from PIL import Image

# =========================================================
# DANE DEMO (ZAMIAST CONFIG.JSON I GITHUB API)
# =========================================================
DEMO_CONFIG = {
    "EURO_RATE": 4.3,
    "PRICE": {
        "fuelPLN": 6.4, "fuelEUR": 1.65,
        "adBluePLN": 3.8, "adBlueEUR": 1.4
    },
    "VEHICLE_DATA": {
        "FTL": {"fuelUsage": 0.3, "adBlueUsage": 0.02, "serviceCostPLN": 0.5, "serviceCostEUR": 0.075, "tankCapacity": 900},
        "Solo": {"fuelUsage": 0.2, "adBlueUsage": 0.02, "serviceCostPLN": 0.5, "serviceCostEUR": 0.075, "tankCapacity": 600},
        "Bus": {"fuelUsage": 0.14, "adBlueUsage": 0.013, "serviceCostPLN": 0.37, "serviceCostEUR": 0.09, "tankCapacity": 85}
    },
    "DISTANCES_AND_MYTO": {
        "Poznań": {
            "Berlin": {"distPL": 172, "distEU": 101, "mytoFTL": 77.77, "mytoSolo": 120.0, "mytoBus": 60.0},
            "Paryż": {"distPL": 172, "distEU": 1144, "mytoFTL": 355.82, "mytoSolo": 450.0, "mytoBus": 120.0}
        },
        "Warszawa": {
            "Poznań": {"distPL": 354, "distEU": 0, "mytoFTL": 21.85, "mytoSolo": 45.0, "mytoBus": 15.0}
        }
    }
}

# =========================================================
# IDENTYCZNA STYLIZACJA VORTEZA SYSTEMS
# =========================================================
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

def apply_vorteza_theme():
    bin_str = get_base64_of_bin_file('bg_vorteza.png')
    if bin_str:
        bg_style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(bg_style, unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');
            :root {
                --v-copper: #B58863;
                --v-dark: #0E0E0E;
                --v-panel: rgba(20, 20, 20, 0.9);
                --v-text: #E0E0E0;
            }
            .stApp { color: var(--v-text); font-family: 'Montserrat', sans-serif; }
            h1, h2, h3 {
                color: var(--v-copper) !important;
                font-weight: 700 !important;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            label[data-testid="stWidgetLabel"] {
                color: var(--v-copper) !important;
                font-weight: 700 !important;
                text-transform: uppercase;
                font-size: 0.85rem !important;
            }
            div[data-baseweb="select"] > div, input {
                background-color: rgba(15, 15, 15, 0.9) !important;
                color: white !important;
                border: 1px solid #444 !important;
            }
            .vorteza-card {
                background-color: var(--v-panel);
                padding: 30px;
                border-radius: 5px;
                border-left: 5px solid var(--v-copper);
                box-shadow: 0 10px 40px rgba(0,0,0,0.8);
                backdrop-filter: blur(15px);
            }
            .route-preview {
                background-color: rgba(181, 136, 99, 0.1);
                border: 1px solid var(--v-copper);
                padding: 15px;
                margin-top: 15px;
                border-radius: 4px;
            }
            [data-testid="stMetricValue"] {
                color: var(--v-copper) !important;
                font-size: 2.2rem !important;
                font-weight: 700 !important;
            }
            .stButton > button {
                background-color: rgba(0, 0, 0, 0.7);
                color: var(--v-copper);
                border: 1px solid var(--v-copper);
                width: 100%;
                font-weight: 700;
                text-transform: uppercase;
            }
            .stButton > button:hover { background-color: var(--v-copper); color: black; }
            .cost-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
            .cost-table th { text-align: left; color: var(--v-copper); border-bottom: 1px solid #444; padding: 8px; }
            .cost-table td { padding: 10px 8px; border-bottom: 1px solid #222; }
        </style>
    """, unsafe_allow_html=True)

# =========================================================
# INTERFEJS GŁÓWNY (IDENTYCZNY UKŁAD)
# =========================================================
st.set_page_config(page_title="VORTEZA FLOW | DEMO", layout="wide")
apply_vorteza_theme()

# Header
col_logo, col_title = st.columns([1, 5])
with col_logo:
    try:
        st.image('logo_vorteza.png', use_container_width=True)
    except:
        st.title("VORTEZA")
with col_title:
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("VORTEZA FLOW - DEMO VERSION")

st.markdown("---")

# Layout Kalkulatora
col_cfg, col_res = st.columns([1, 1], gap="large")

with col_cfg:
    st.subheader("Transport Configuration")
    v_type = st.selectbox("Vehicle Unit Type", list(DEMO_CONFIG["VEHICLE_DATA"].keys()))
    start_p = st.selectbox("Starting Point", list(DEMO_CONFIG["DISTANCES_AND_MYTO"].keys()))
    
    available_dests = list(DEMO_CONFIG["DISTANCES_AND_MYTO"][start_p].keys())
    route = st.selectbox("Target Destination", available_dests)
    extra_km = st.number_input("Additional Distance (KM)", value=0, step=10)
    
    r_info = DEMO_CONFIG["DISTANCES_AND_MYTO"][start_p][route]
    st.markdown(f"""
        <div class="route-preview">
            <b style="color:#B58863;">BASE DISTANCE DATA:</b><br>
            🇵🇱 Poland: <b>{r_info['distPL']} km</b><br>
            🇪🇺 EU / Other: <b>{r_info['distEU']} km</b><br>
            ➕ Additional: <b>{extra_km} km</b><br>
            <hr style="border:0; border-top:1px solid #444; margin:5px 0;">
            📏 Total Calculation: <b>{r_info['distPL'] + r_info['distEU'] + extra_km} km</b>
        </div>
    """, unsafe_allow_html=True)

with col_res:
    st.markdown('<div class="vorteza-card">', unsafe_allow_html=True)
    st.subheader("Technical Margin Analysis")
    
    v_info = DEMO_CONFIG["VEHICLE_DATA"][v_type]
    prices = DEMO_CONFIG["PRICE"]
    euro_rate = DEMO_CONFIG["EURO_RATE"]
    total_km = r_info["distPL"] + r_info["distEU"] + extra_km

    # Logika obliczeń (Bliźniacza do oryginału)
    total_fuel_l = total_km * v_info["fuelUsage"]
    pl_l = min(total_fuel_l, v_info["tankCapacity"])
    eu_l = max(0, total_fuel_l - pl_l)
    
    c_fuel_pln = (pl_l * prices["fuelPLN"]) + (eu_l * prices["fuelEUR"] * euro_rate)
    c_adblue_pln = (total_km * v_info["adBlueUsage"]) * prices["adBluePLN"]
    c_service_pln = (r_info["distPL"] * v_info["serviceCostPLN"]) + ((r_info["distEU"] + extra_km) * v_info["serviceCostEUR"] * euro_rate)
    
    myto_key = f"myto{v_type}"
    c_myto_eur = r_info.get(myto_key, 0)
    c_myto_pln = c_myto_eur * euro_rate
    
    total_pln = c_fuel_pln + c_adblue_pln + c_service_pln + c_myto_pln
    total_eur = total_pln / euro_rate

    m1, m2 = st.columns(2)
    m1.metric("TOTAL COST (PLN)", f"{round(total_pln, 2)} zł")
    m2.metric("TOTAL COST (EUR)", f"€ {round(total_eur, 2)}")

    st.markdown(f"""
        <table class="cost-table">
            <tr><th>Category</th><th>PLN Value</th><th>EUR Value</th></tr>
            <tr><td>Fuel & Energy</td><td>{round(c_fuel_pln, 2)} zł</td><td>€ {round(c_fuel_pln/euro_rate, 2)}</td></tr>
            <tr><td>AdBlue Fluids</td><td>{round(c_adblue_pln, 2)} zł</td><td>€ {round(c_adblue_pln/euro_rate, 2)}</td></tr>
            <tr><td>Technical Service</td><td>{round(c_service_pln, 2)} zł</td><td>€ {round(c_service_pln/euro_rate, 2)}</td></tr>
            <tr><td>Road Tolls (Myto)</td><td>{round(c_myto_pln, 2)} zł</td><td>€ {round(c_myto_eur, 2)}</td></tr>
        </table>
        <div style="margin-top:15px; font-size:0.75rem; color:#666; text-transform: uppercase;">
            EX RATE: 1 EUR = {euro_rate} PLN | UNIT: {v_type} | {start_p} - {route}
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("RUN FULL SIMULATION"):
    st.toast("Calculating logistics data...", icon="🚛")
