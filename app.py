import streamlit as st
import json
import random

# Konfiguracja strony
st.set_page_config(page_title="VORTEZA FLOW - DEMO", layout="wide")

def load_config():
    """Ładuje dane z pliku config.json."""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Nie znaleziono pliku config.json!")
        return None

def get_random_routes(config, count=5):
    """Wybiera losowo określoną liczbę tras z pliku konfiguracyjnego."""
    all_possible_routes = []
    distances = config.get("DISTANCES_AND_MYTO", {})
    
    for start_city, destinations in distances.items():
        for end_city, data in destinations.items():
            all_possible_routes.append({
                "from": start_city,
                "to": end_city,
                "data": data
            })
    
    return random.sample(all_possible_routes, min(count, len(all_possible_routes)))

def calculate_margin(vehicle_type, route_data, config):
    """Oblicza koszty techniczne dla danej trasy i pojazdu."""
    v_data = config["VEHICLE_DATA"][vehicle_type]
    prices = config["PRICE"]
    euro_rate = config["EURO_RATE"]
    
    dist_pl = route_data["distPL"]
    dist_eu = route_data["distEU"]
    
    # Koszty Paliwa
    fuel_usage_total = (dist_pl + dist_eu) * v_data["fuelUsage"]
    # Przyjmujemy proporcjonalne tankowanie lub model mieszany - tutaj dla uproszczenia:
    # paliwo w PL za PLN, paliwo w EU za EUR
    fuel_cost_pln = (dist_pl * v_data["fuelUsage"]) * prices["fuelPLN"]
    fuel_cost_eur = (dist_eu * v_data["fuelUsage"]) * prices["fuelEUR"]
    
    # Koszty AdBlue
    adblue_cost_pln = (dist_pl * v_data["adBlueUsage"]) * prices["adBluePLN"]
    adblue_cost_eur = (dist_eu * v_data["adBlueUsage"]) * prices["adBlueEUR"]
    
    # Koszty Serwisowe
    service_cost_pln = dist_pl * v_data["serviceCostPLN"]
    service_cost_eur = dist_eu * v_data["serviceCostEUR"]
    
    # Myto (pobierane bezpośrednio z tabeli dla danego typu pojazdu)
    myto_key = f"myto{vehicle_type}"
    total_myto_eur = route_data.get(myto_key, 0.0)
    
    # Sumowanie
    total_pln = fuel_cost_pln + adblue_cost_pln + service_cost_pln
    total_eur = fuel_cost_eur + adblue_cost_eur + service_cost_eur + total_myto_eur
    
    # Całość przeliczona na PLN dla wyniku głównego
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
    if not config:
        return

    # Inicjalizacja sesji dla losowych tras, aby nie zmieniały się przy każdym kliknięciu
    if 'demo_routes' not in st.session_state:
        st.session_state.demo_routes = get_random_routes(config, 5)

    st.title("VORTEZA FLOW - Analiza Rentowności Transportu")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("KONFIGURACJA TRANSPORTU")
        
        # Wybór jednej z 5 wylosowanych tras
        route_options = [f"{r['from']} -> {r['to']}" for r in st.session_state.demo_routes]
        selected_route_idx = st.selectbox("Wybierz trasę (Demo: 5 losowych)", range(len(route_options)), format_func=lambda x: route_options[x])
        
        selected_route = st.session_state.demo_routes[selected_route_idx]
        
        vehicle_type = st.selectbox("Typ pojazdu", ["FTL", "Solo", "Bus"])
        
        st.info(f"**Dane trasy:**\n\n- Dystans PL: {selected_route['data']['distPL']} km\n- Dystans EU: {selected_route['data']['distEU']} km")
        st.caption(f"Aktualny kurs EUR: {config['EURO_RATE']}")

    with col2:
        st.subheader("TECHNICZNA ANALIZA MARŻY")
        
        results = calculate_margin(vehicle_type, selected_route['data'], config)
        
        res_col1, res_col2 = st.columns(2)
        res_col1.metric("KOSZT CAŁKOWITY (PLN)", f"{results['grand_total_pln']:,.2f} zł")
        res_col2.metric("KOSZT CAŁKOWITY (EUR)", f"€ {results['grand_total_eur']:,.2f}")

        # Tabela szczegółowa
        st.markdown("### Szczegóły kosztów")
        data_rows = []
        for cat, values in results['breakdown'].items():
            data_rows.append({
                "Kategoria": cat,
                "Wartość PLN": f"{values[0]:,.2f} zł",
                "Wartość EUR": f"€ {values[1]:,.2f}"
            })
        
        st.table(data_rows)

    st.markdown("---")
    st.caption("Wersja demonstracyjna systemu rentowności. Dane pobierane z pliku config.json.")

if __name__ == "__main__":
    main()
