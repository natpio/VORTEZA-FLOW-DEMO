import streamlit as st

# --- KONFIGURACJA DANYCH DEMO ---
# Dane zaszyte bezpośrednio w kodzie, aby demo działało bez pliku config.json
DEMO_DATA = {
    "EURO_RATE": 4.3,
    "VEHICLE_TYPES": {
        "FTL (Zestaw)": {"fuel": 0.3, "service": 0.5, "myto_key": "mytoFTL"},
        "Bus (Dostawczy)": {"fuel": 0.14, "service": 0.37, "myto_key": "mytoBus"}
    },
    "ROUTES": {
        "Poznań": {
            "Berlin": {"distPL": 172, "distEU": 101, "mytoFTL": 77.77, "mytoBus": 60.0},
            "Paryż": {"distPL": 172, "distEU": 1144, "mytoFTL": 355.82, "mytoBus": 60.0},
            "Londyn": {"distPL": 171, "distEU": 915, "mytoFTL": 282.0, "mytoBus": 60.0}
        },
        "Warszawa": {
            "Wrocław": {"distPL": 363, "distEU": 0, "mytoFTL": 24.0, "mytoBus": 90.0},
            "Praga": {"distPL": 470, "distEU": 153, "mytoFTL": 59.57, "mytoBus": 150.0}
        }
    },
    "PRICES": {
        "fuelPLN": 6.4,
        "fuelEUR": 1.65
    }
}

# --- LOGIKA OBLICZENIOWA ---
def calculate_demo_costs(vehicle_name, route_name, origin, rate_pln):
    v = DEMO_DATA["VEHICLE_TYPES"][vehicle_name]
    r = DEMO_DATA["ROUTES"][origin][route_name]
    
    # Koszty paliwa
    cost_fuel = (r["distPL"] * v["fuel"] * DEMO_DATA["PRICES"]["fuelPLN"]) + \
                (r["distEU"] * v["fuel"] * DEMO_DATA["PRICES"]["fuelEUR"] * DEMO_DATA["EURO_RATE"])
    
    # Myto i serwis
    cost_myto = r[v["myto_key"]] * DEMO_DATA["EURO_RATE"]
    cost_service = (r["distPL"] + r["distEU"]) * v["service"]
    
    total = cost_fuel + cost_myto + cost_service
    return round(total, 2)

# --- INTERFEJS ---
st.set_page_config(page_title="VORTEZA FLOW DEMO", page_icon="🚛")

st.title("🚛 VORTEZA FLOW - Demo Logistyczne")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    start = st.selectbox("Miejsce załadunku", list(DEMO_DATA["ROUTES"].keys()))
    vehicle = st.selectbox("Typ pojazdu", list(DEMO_DATA["VEHICLE_TYPES"].keys()))

with col2:
    end = st.selectbox("Miejsce rozładunku", list(DEMO_DATA["ROUTES"][start].keys()))
    price = st.number_input("Stawka frachtu (PLN)", value=4500)

if st.button("Analizuj rentowność transportu"):
    total_cost = calculate_demo_costs(vehicle, end, start, price)
    margin = price - total_cost
    
    st.subheader(f"Wynik analizy dla: {start} ➡️ {end}")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Koszty całkowite", f"{total_cost} PLN")
    m2.metric("Marża", f"{round(margin, 2)} PLN", delta=f"{round(margin, 2)} PLN")
    m3.metric("Rentowność", f"{round((margin/price)*100, 1)}%")

    if margin > 500:
        st.success("Transport wysoce opłacalny.")
    elif margin > 0:
        st.warning("Niska marża - sprawdź dodatkowe koszty (sloty, rozładunki).")
    else:
        st.error("Transport generuje straty!")

st.sidebar.markdown("### O VORTEZA FLOW")
st.sidebar.info("To jest wersja demonstracyjna systemu do zarządzania logistyką targową SQM.")
