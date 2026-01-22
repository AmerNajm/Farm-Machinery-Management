import streamlit as st

# App Title and Description
st.title("🚜 Field Operations & Fuel Planner")
st.markdown("""
This simple tool helps you plan tractor activities and fuel needs for the Research Station.
Based on **ASABE (Metric) Standards**.
""")

# Sidebar for Technical Specs (Keep it simple)
st.sidebar.header("Tractor Specifications")
rated_power = st.sidebar.number_input("Tractor Rated PTO Power (kW)", min_value=1.0, value=75.0, help="Found on the tractor's spec plate.")

# Main App Tabs
tab1, tab2 = st.tabs(["🕒 Performance Planner", "⛽ Fuel Forecast"])

with tab1:
    st.header("Field Performance")
    col1, col2 = st.columns(2)
    
    with col1:
        width = st.number_input("Implement Width (meters)", min_value=0.1, value=3.0)
        speed = st.number_input("Travel Speed (km/h)", min_value=1.0, value=8.0)
    
    with col2:
        efficiency = st.slider("Field Efficiency (%)", 50, 100, 75, help="Use 70% for small plots, 85% for large fields.")
        area = st.number_input("Total Area to Work (Hectares)", min_value=0.1, value=10.0)

    # ASABE Calculation for Field Capacity
    # Formula: (Width * Speed * Efficiency) / 10
    capacity = (width * speed * (efficiency / 100)) / 10
    total_time = area / capacity

    st.success(f"**Performance Result:**")
    st.write(f"- You can cover **{capacity:.2f} hectares per hour**.")
    st.write(f"- Total time to complete the job: **{total_time:.1f} hours**.")

with tab2:
    st.header("Fuel Consumption")
    load_type = st.selectbox("How heavy is the task?", ["Light (Tillage/Seeding)", "Medium (Mowing)", "Heavy (Deep Plowing)"])
    
    # Fuel calculation based on specific volumetric fuel consumption
    # Average diesel use is approx 0.223 L/kWh based on research data
    if load_type == "Light":
        load_factor = 0.45
    elif load_type == "Medium":
        load_factor = 0.65
    else:
        load_factor = 0.85

    fuel_per_hour = 0.223 * rated_power * load_factor
    total_fuel = fuel_per_hour * total_time

    st.warning("**Fuel Prediction:**")
    st.write(f"- Estimated fuel use: **{fuel_per_hour:.2f} Liters per hour**.")
    st.write(f"- Total diesel needed for this activity: **{total_fuel:.1f} Liters**.")

st.info("💡 **Operations Tip:** To save fuel, 'Gear Up and Throttle Down' for light loads[cite: 171, 1812].")