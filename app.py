import streamlit as st
import base64

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="VORTEZA FLOW", layout="wide")

# --- CUSTOM CSS (Klucz do wyglądu pełnej wersji) ---
def local_css():
    st.markdown("""
        <style>
        /* Tło główne */
        .stApp {
            background-color: #0e1117;
            color: #d4af37;
        }
        
        /* Stylizacja kontenerów wejściowych */
        .stSelectbox div[data-baseweb="select"], .stNumberInput div[data-baseweb="input"] {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid #d4af37 !important;
            color: white !important;
        }
        
        /* Kolor czcionek etykiet */
        label {
            color: #d4af37 !important;
            font-weight: bold;
            text-transform: uppercase;
        }

        /* Przyciski */
        .stButton>button {
            background-color: rgba(0,0,0,0);
            color: #d4af37;
            border: 1px solid #d4af37;
            border-radius: 0px;
            width: 100%;
            height: 3em;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #d4af37;
            color: black;
        }

        /* Sekcja wyników (Technical Margin Analysis) */
        .result-box {
            background-color: rgba(0, 0, 0, 0.6);
            border-left: 3px solid #d4af37;
            padding: 20px;
            margin-top: 20px;
        }
        
        /* Pasek boczny */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.8);
            border-right: 1px solid #d4af37;
        }
        </style>
    """, unsafe_allow_html=True)

# --- ŁADOWANIE TŁA OBRAZKOWEGO ---
def set_bg():
    try:
        with open("bg_vorteza.png", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{b64}");
                background-size: cover;
                background-attachment: fixed;
            }}
            </style>
            """, unsafe_allow_html=True)
    except:
        pass

local_css()
set_bg()

# --- DANE DEMO ---
CONFIG = {
    "EURO": 4.3,
    "VEHICLES": ["FTL", "Solo", "Bus"],
    "CITIES": ["Poznań", "Warszawa", "Gdańsk", "Gorzów Wielkopolski"]
}

# --- UI (UKŁAD Z OBRAZKA 1f020a.jpg) ---
with st.sidebar:
    try:
        st.image("logo_vorteza.png")
    except:
        st.header("VORTEZA")
    st.markdown("---")
    st.write("TRANSPORT CONFIGURATION")

# Główny layout
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.write("### TRANSPORT CONFIGURATION")
    v_type = st.selectbox("VEHICLE UNIT TYPE", CONFIG["VEHICLES"])
    origin = st.selectbox("STARTING POINT", CONFIG["CITIES"])
    dest = st.selectbox("TARGET DESTINATION", ["Berlin", "Paryż", "Londyn", "Warszawa"])
    add_dist = st.number_input("ADDITIONAL DISTANCE (KM)", value=0)
    
    st.markdown(f"""
    <div style='background: rgba(0,0,0,0.4); padding: 10px; border: 1px solid #444;'>
        <small>BASE DISTANCE DATA:</small><br>
        🇵🇱 Poland: 254 km<br>
        🇪🇺 EU / Other: 100 km<br>
        <b>Total Calculation: 354 km</b>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.write("### TECHNICAL MARGIN ANALYSIS")
    
    # Przykładowe wartości jak na screenie
    c1, c2 = st.columns(2)
    c1.metric("TOTAL COST (PLN)", "982.79 zł")
    c2.metric("TOTAL COST (EUR)", "€ 228.55")
    
    st.markdown("""
    <table style='width:100%; color:white; border-collapse: collapse;'>
        <tr style='border-bottom: 1px solid #444;'>
            <th style='text-align:left; padding: 10px;'>Category</th>
            <th style='text-align:right;'>PLN Value</th>
            <th style='text-align:right;'>EUR Value</th>
        </tr>
        <tr><td>Fuel & Energy</td><td style='text-align:right;'>679.58 zł</td><td style='text-align:right;'>€ 158.07</td></tr>
        <tr><td>AdBlue Fluids</td><td style='text-align:right;'>26.9 zł</td><td style='text-align:right;'>€ 6.26</td></tr>
        <tr><td>Technical Service</td><td style='text-align:right;'>177.0 zł</td><td style='text-align:right;'>€ 41.16</td></tr>
        <tr><td>Road Tolls (Myto)</td><td style='text-align:right;'>99.3 zł</td><td style='text-align:right;'>€ 23.07</td></tr>
    </table>
    """, unsafe_allow_html=True)

st.button("OBLICZ RENTOWNOŚĆ")
