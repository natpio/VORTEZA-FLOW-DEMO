import streamlit as st
import base64

# =========================================================
# KONFIGURACJA STRONY
# =========================================================
st.set_page_config(page_title="VORTEZA FLOW | DEMO", layout="wide")

# =========================================================
# DANE DEMO I DOSTĘPU
# =========================================================
DEMO_PASSWORD = "Quietpanther294"  # <--- TUTAJ USTAW HASŁO DLA KLIENTA

DEMO_DATA = {
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
    "ROUTES": [
        {"from": "Poznań", "to": "Berlin", "distPL": 172, "distEU": 101, "mytoFTL": 77.77, "mytoSolo": 120.0, "mytoBus": 60.0},
        {"from": "Poznań", "to": "Paryż", "distPL": 172, "distEU": 1144, "mytoFTL": 355.82, "mytoSolo": 450.0, "mytoBus": 120.0},
        {"from": "Warszawa", "to": "Londyn", "distPL": 470, "distEU": 914, "mytoFTL": 355.43, "mytoSolo": 350.0, "mytoBus": 175.0},
        {"from": "Gdańsk", "to": "Wrocław", "distPL": 455, "distEU": 0, "mytoFTL": 32.52, "mytoSolo": 220.0, "mytoBus": 110.0},
        {"from": "Gorzów Wielkopolski", "to": "Hannover", "distPL": 80, "distEU": 300, "mytoFTL": 45.0, "mytoSolo": 60.0, "mytoBus": 30.0}
    ]
}

# =========================================================
# STYLIZACJA VORTEZA SYSTEMS
# =========================================================
def apply_style():
    bg_base64 = ""
    try:
        with open("bg_vorteza.png", "rb") as f:
            bg_base64 = base64.b64encode(f.read()).decode()
    except:
        pass

    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');
            
            :root {{
                --v-copper: #B58863;
                --v-dark: #0E0E0E;
                --v-panel: rgba(20, 20, 20, 0.9);
                --v-text: #E0E0E0;
            }}

            .stApp {{
                background-image: url("data:image/png;base64,{bg_base64}");
                background-size: cover;
                background-attachment: fixed;
                color: var(--v-text);
                font-family: 'Montserrat', sans-serif;
            }}

            h1, h2, h3 {{
                color: var(--v-copper) !important;
                font-weight: 700 !important;
                text-transform: uppercase;
                letter-spacing: 2px;
            }}

            label {{
                color: var(--v-copper) !important;
                font-weight: 700 !important;
                text-transform: uppercase;
                font-size: 0.85rem !important;
            }}

            div[data-baseweb="select"] > div, input {{
                background-color: rgba(15, 15, 15, 0.9) !important;
                color: white !important;
                border: 1px solid #444 !important;
            }}

            .vorteza-card {{
                background-color: var(--v-panel);
                padding: 30px;
                border-radius: 5px;
                border-left: 5px solid var(--v-copper);
                box-shadow: 0 10px 40px rgba(0,0,0,0.8);
                backdrop-filter: blur(15px);
                margin-bottom: 20px;
            }}

            .route-preview {{
                background-color: rgba(181, 136, 99, 0.1);
                border: 1px solid var(--v-copper);
                padding: 15px;
                margin-top: 15px;
                border-radius: 4px;
            }}

            [data-testid="stMetricValue"] {{
                color: var(--v-copper) !important;
                font-size: 2.2rem !important;
                font-weight: 700 !important;
            }}

            .cost-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}
            .cost-table th {{
                text-align: left;
                color: var(--v-copper);
                border-bottom: 1px solid #444;
                padding: 8px;
            }}
            .cost-table td {{
                padding: 10px 8px;
                border-bottom: 1px solid #222;
            }}
            
            /* Stylizacja formularza logowania */
            .stForm {{
                background-color: var(--v-panel);
                border: 1px solid var(--v-copper);
                padding: 20px;
                border-radius: 10px;
            }}
        </style>
    """, unsafe_allow_html=True)

# =========================================================
# SYSTEM LOGOWANIA
# =========================================================
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            with st.form("Login"):
                st.subheader("VORTEZA | SECURE ACCESS")
                password = st.text_input("Hasło dostępu", type="password")
                submit = st.form_submit_button("WEJDŹ DO SYSTEMU")
                if submit:
                    if password == DEMO_PASSWORD:
                        st.session_state["authenticated"] = True
                        st.rerun()
                    else:
                        st.error("Nieprawidłowe hasło.")
        return False
    return True

# =========================================================
# GŁÓWNA APLIKACJA
# =========================================================
apply_style()

if check_password():
    # Nagłówek i przycisk wylogowania
    col_l, col_r, col_out = st.columns([1, 4, 1])
    with col_l:
        try:
            st.image("logo_vorteza.png", use_container_width=True)
        except:
            st.title("VORTEZA")
    with col_r:
        st.markdown("<br>", unsafe_allow_html=True)
        st.title("VORTEZA FLOW — DEMO")
    with col_out:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("WYLOGUJ"):
            st.session_state["authenticated"] = False
            st.rerun()

    st.markdown("---")

    # Layout Kalkulatora
    c_left, c_right = st.columns([1, 1], gap="large")

    with c_left:
        st.subheader("Transport Configuration")
        vehicle = st.selectbox("VEHICLE UNIT TYPE", list(DEMO_DATA["VEHICLE_DATA"].keys()))
        route_names = [f"{r['from']} ➔ {r['to']}" for r in DEMO_DATA["ROUTES"]]
        route_idx = st.selectbox("SELECT ROUTE", range(len(route_names)), format_func=lambda x: route_names[x])
        selected_route = DEMO_DATA["ROUTES"][route_idx]
        extra = st.number_input("ADDITIONAL DISTANCE (KM)", value=0, step=10)
        
        st.markdown(f"""
            <div class="route-preview">
                <b style="color:#B58863;">BASE DISTANCE DATA:</b><br>
                🇵🇱 Poland: <b>{selected_route['distPL']} km</b><br>
                🇪🇺 EU / Other: <b>{selected_route['distEU']} km</b><br>
                ➕ Additional: <b>{extra} km</b><br>
                <hr style="border:0; border-top:1px solid #444; margin:5px 0;">
                📏 Total Calculation: <b>{selected_route['distPL'] + selected_route['distEU'] + extra} km</b>
            </div>
        """, unsafe_allow_html=True)

    with c_right:
        st.markdown('<div class="vorteza-card">', unsafe_allow_html=True)
        st.subheader("Technical Margin Analysis")
        
        # Logika obliczeń
        v = DEMO_DATA["VEHICLE_DATA"][vehicle]
        er = DEMO_DATA["EURO_RATE"]
        km_pl = selected_route["distPL"]
        km_eu = selected_route["distEU"] + extra
        
        c_fuel = (km_pl * v["fuelUsage"] * DEMO_DATA["PRICE"]["fuelPLN"]) + (km_eu * v["fuelUsage"] * DEMO_DATA["PRICE"]["fuelEUR"] * er)
        c_adblue = ((km_pl + km_eu) * v["adBlueUsage"]) * DEMO_DATA["PRICE"]["adBluePLN"]
        c_service = (km_pl * v["serviceCostPLN"]) + (km_eu * v["serviceCostEUR"] * er)
        myto_eur = selected_route.get(f"myto{vehicle}", 0)
        c_myto = myto_eur * er
        
        total_pln = c_fuel + c_adblue + c_service + c_myto

        m1, m2 = st.columns(2)
        m1.metric("TOTAL COST (PLN)", f"{total_pln:,.2f} zł")
        m2.metric("TOTAL COST (EUR)", f"€ {total_pln/er:,.2f}")

        st.markdown(f"""
            <table class="cost-table">
                <tr><th>Category</th><th>PLN Value</th><th>EUR Value</th></tr>
                <tr><td>Fuel & Energy</td><td>{c_fuel:,.2f} zł</td><td>€ {c_fuel/er:,.2f}</td></tr>
                <tr><td>AdBlue Fluids</td><td>{c_adblue:,.2f} zł</td><td>€ {c_adblue/er:,.2f}</td></tr>
                <tr><td>Technical Service</td><td>{c_service:,.2f} zł</td><td>€ {c_service/er:,.2f}</td></tr>
                <tr><td>Road Tolls (Myto)</td><td>{c_myto:,.2f} zł</td><td>€ {myto_eur:,.2f}</td></tr>
            </table>
            <div style="margin-top:15px; font-size:0.75rem; color:#666; text-transform: uppercase;">
                EX RATE: 1 EUR = {er} PLN | UNIT: {vehicle} | DEMO MODE
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
