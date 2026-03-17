import streamlit as st
import json

# Funkcja ładująca konfigurację (w demo używamy uproszczonego zestawu danych)
def load_demo_config():
    # W wersji demo ograniczamy miasta i pojazdy, by pokazać mechanikę działania
    return {
        "EURO_RATE": 4.3,
        "PRICE": {
            "fuelPLN": 6.4,
            "fuelEUR": 1.65
        },
        "VEHICLE_DATA": {
            "FTL": {"fuelUsage": 0.3, "serviceCostPLN": 0.5},
            "Bus": {"fuelUsage": 0.14, "serviceCostPLN": 0.37}
        },
        "ROUTES_DEMO": {
            "Poznań": {
                "Berlin": {"distPL": 172, "distEU": 101, "mytoFTL": 77.77, "mytoBus": 60.0},
                "Paryż": {"distPL": 172, "distEU": 1144, "mytoFTL": 355.82, "mytoBus": 60.0}
            },
            "Warszawa": {
                "Poznań": {"distPL": 352, "distEU": 0, "mytoFTL": 21.85, "mytoBus": 110.0},
                "Londyn": {"distPL": 470, "distEU": 914, "mytoFTL": 355.43, "mytoBus": 175.0}
            }
        }
    }

def calculate_costs(vehicle_type, route_data, config):
    v_data = config["VEHICLE_DATA"][vehicle_type]
    
    # Obliczenia paliwa
    total_dist = route_data["distPL"] + route_data["distEU"]
    fuel_needed = total_dist * v_data["fuelUsage"]
    
    # Koszt paliwa (uproszczone: PL w PLN, EU w EUR)
    fuel_cost_pln = route_data["distPL"] * v_data["fuelUsage"] * config["PRICE"]["fuelPLN"]
    fuel_cost_eur = route_data["distEU"] * v_data["fuelUsage"] * config["PRICE"]["fuelEUR"]
    
    # Myto i serwis
    myto_key = f"myto{vehicle_type}"
    myto_cost = route_data.get(myto_key, 0)
    service_cost = total_dist * v_data["serviceCostPLN"]
    
    total_cost_pln = fuel_cost_pln + (fuel_cost_eur * config["EURO_RATE"]) + (myto_cost * config["EURO_RATE"]) + service_cost
    return round(total_cost_pln, 2)

# Interfejs Streamlit
st.set_page_config(page_title="VORTEZA FLOW - DEMO", layout="centered")
st.title("🚢 VORTEZA FLOW - Wersja Demonstracyjna")
st.info("To jest wersja DEMO. Pełna wersja obsługuje wszystkie trasy europejskie i pojazdy typu Solo.")

cfg = load_demo_config()

col1, col2 = st.columns(2)

with col1:
    origin = st.selectbox("Punkt startowy", list(cfg["ROUTES_DEMO"].keys()))
    vehicle = st.selectbox("Typ pojazdu", list(cfg["VEHICLE_DATA"].keys()))

with col2:
    destination = st.selectbox("Cel podróży", list(cfg["ROUTES_DEMO"][origin].keys()))
    rate_pln = st.number_input("Twoja stawka za fracht (PLN)", value=5000)

if st.button("Oblicz rentowność"):
    route = cfg["ROUTES_DEMO"][origin][destination]
    total_cost = calculate_costs(vehicle, route, cfg)
    margin = rate_pln - total_cost
    
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Całkowity koszt", f"{total_cost} PLN")
    c2.metric("Zysk/Marża", f"{round(margin, 2)} PLN", delta=f"{round(margin, 2)} PLN")
    c3.metric("Dystans", f"{route['distPL'] + route['distEU']} km")

    if margin > 0:
        st.success("Transport opłacalny!")
    else:
        st.error("Transport poniżej progu rentowności!")

st.sidebar.image("logo_vorteza.png", width=200) # Jeśli masz plik w repo
st.sidebar.write(f"Kurs EUR: {cfg['EURO_RATE']}")
