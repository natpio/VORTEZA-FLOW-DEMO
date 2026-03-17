import streamlit as st
import json
import random
import os

# Konfiguracja strony
st.set_page_config(page_title="VORTEZA FLOW - DEMO", layout="wide")

def load_config():
    """Ładuje dane z pliku config.json znajdującego się w tym samym folderze."""
    file_path = 'config.json'
    if not os.path.exists(file_path):
        st.error(f"BŁĄD: Nie znaleziono pliku '{file_path}' w folderze z aplikacją!")
        st.info("Utwórz plik config.json i wklej do niego dane konfiguracyjne.")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Błąd podczas odczytu pliku: {e}")
        return None

def get_random_routes(config, count=5):
    all_possible_routes = []
    distances = config.get("DISTANCES_AND_MYTO", {})
    for start_city, destinations in distances.items():
        for end_city, data in destinations.items():
            all_possible_routes.append({"from": start_city, "to": end_city, "data": data})
    
    # Losowanie dokładnie 5 tras (lub mniej, jeśli w pliku jest ich mniej)
    return random.sample(all_possible_routes, min(count, len(all_possible_routes)))

def calculate_margin(vehicle_type, route_data, config):
    v_data = config["VEHICLE_DATA"][vehicle_type]
    prices = config["PRICE"]
    euro_rate = config["EURO_RATE"]
    
    dist_pl = route_data["distPL"]
    dist_eu = route_data["distEU"]
    
    fuel_cost_pln = (dist_pl * v_data["fuelUsage"]) * prices["fuelPLN"]
    fuel_cost_eur = (dist_eu * v_data["fuelUsage"]) * prices["fuelEUR"]
    adblue_cost_pln = (dist_pl * v_data["adBlueUsage"]) * prices["adBluePLN"]
    adblue_cost_eur = (dist_eu * v_data["adBlueUsage"]) * prices["adBlueEUR"]
    service_cost_pln = dist_pl * v_data["serviceCostPLN"]
    service_cost_eur = dist_eu * v_data["serviceCostEUR"]
    
    myto_key = f"myto{vehicle_type}"
    total_myto_eur = route_data.get(myto_key, 0.0)
    
    total_pln = fuel_cost_pln + adblue_cost_pln + service_cost_pln
    total_eur = fuel_cost_eur + adblue_cost_eur + total_myto_eur
    grand_total_pln = total_pln + (total_eur * euro_rate)
    
    return {
        "grand_total_pln": grand_total_pln,
        "grand_total_eur": grand_total_pln / euro_rate,
        "breakdown": {
            "Fuel & Energy": (fuel_cost_pln, fuel_cost_eur),
            "AdBlue Fluids": (adblue_cost_pln, adblue_cost_eur),
            "Technical Service": (service_cost_pln, service_cost_eur),
            "Road Tolls (Myto)": (0.0, total_myto_eur)
        }
    }

def main():
    config = load_config()
    if config is None:
        st.stop() # Zatrzymaj aplikację, jeśli nie ma pliku

    if 'demo_routes' not in st.session_state:
        st.session_state.demo_routes = get_random_routes(config, 5)

    st.title("VORTEZA FLOW - Analiza Rentowności (DEMO)")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("KONFIGURACJA")
        route_options = [f"{r['from']} -> {r['to']}" for r in st.session_state.demo_routes]
        selected_idx = st.selectbox("Wybierz trasę", range(len(route_options)), format_func=lambda x: route_options[x])
        selected_route = st.session_state.demo_routes[selected_idx]
        vehicle_type = st.selectbox("Typ pojazdu", ["FTL", "Solo", "Bus"])
        
        st.write(f"**Dystans PL:** {selected_route['data']['distPL']} km")
        st.write(f"**Dystans EU:** {selected_route['data']['distEU']} km")
        st.caption(f"Kurs EUR: {config['EURO_RATE']}")

    with col2:
        st.subheader("WYNIKI ANALIZY")
        res = calculate_margin(vehicle_type, selected_route['data'], config)
        
        c1, c2 = st.columns(2)
        c1.metric("KOSZT (PLN)", f"{res['grand_total_pln']:,.2f} zł")
        c2.metric("KOSZT (EUR)", f"€ {res['grand_total_eur']:,.2f}")

        st.markdown("### Rozbicie kosztów")
        rows = [{"Kategoria": k, "PLN": f"{v[0]:,.2f}", "EUR": f"{v[1]:,.2f}"} for k, v in res['breakdown'].items()]
        st.table(rows)

if __name__ == "__main__":
    main()
