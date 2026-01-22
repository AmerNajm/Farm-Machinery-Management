import streamlit as st
import pandas as pd
from io import BytesIO

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Farm Calibration Toolkit",
    page_icon="🚜",
    layout="wide"
)

# -----------------------------
# Branding (logo optional)
# -----------------------------
with st.sidebar:
    st.header("Branding")
    logo_file = st.file_uploader("Upload logo (PNG/JPG)", type=["png","jpg","jpeg"])

if logo_file is not None:
    st.image(logo_file, width=220)

st.title("🧰 Farm Calibration Toolkit")
st.caption("Simple calculators for non-technical users (metric units).")

# -----------------------------
# Helper functions
# -----------------------------

def to_excel_bytes(sheets: dict) -> bytes:
    """sheets: {sheet_name: dataframe}"""
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="xlsxwriter") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
    return bio.getvalue()


def safe_div(a, b):
    return a / b if b not in (0, 0.0, None) else None


# -----------------------------
# Tabs
# -----------------------------

tab1, tab2, tab3 = st.tabs([
    "1) Sprayer Calibration",
    "2) Seeder Calibration",
    "3) Quick Fuel & Field Capacity (optional)"
])

# =========================================================
# TAB 1: SPRAYER CALIBRATION
# =========================================================
with tab1:
    st.subheader("1) Sprayer Calibration (L/ha)")
    st.write("Use this when calibrating boom sprayers or knapsack sprayers for correct application rate.")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("**A. Measure travel speed**")
        distance_m = st.number_input("Measured distance (m)", min_value=10.0, value=100.0, step=10.0)
        time_s = st.number_input("Time to travel the distance (seconds)", min_value=1.0, value=60.0, step=1.0)
        speed_kmh = (distance_m / time_s) * 3.6 if time_s > 0 else 0
        st.success(f"Estimated speed: **{speed_kmh:.2f} km/h**")

        st.markdown("**B. Nozzle output (catch test)**")
        method = st.radio(
            "How did you measure flow?",
            ["Per nozzle (recommended for boom)", "Total boom / total flow"],
            horizontal=False
        )

        if method == "Per nozzle (recommended for boom)":
            nozzle_flow_lpm = st.number_input("Average nozzle flow (L/min) — from 1 minute catch", min_value=0.01, value=1.20, step=0.01)
            nozzle_spacing_m = st.number_input("Nozzle spacing (m)", min_value=0.10, value=0.50, step=0.05)
            # ASABE/industry standard relationship: Rate(L/ha)=600*Q/(S*W)
            rate_lpha = (600 * nozzle_flow_lpm) / (speed_kmh * nozzle_spacing_m) if speed_kmh > 0 and nozzle_spacing_m > 0 else 0
            st.info("Formula used: **Rate (L/ha) = 600 × Q(L/min) ÷ [Speed(km/h) × Nozzle spacing(m)]**")

            df_inputs = pd.DataFrame([{
                "Distance (m)": distance_m,
                "Time (s)": time_s,
                "Speed (km/h)": round(speed_kmh, 3),
                "Nozzle flow (L/min)": nozzle_flow_lpm,
                "Nozzle spacing (m)": nozzle_spacing_m,
            }])

        else:
            total_flow_lpm = st.number_input("Total sprayer flow (L/min) — all nozzles combined", min_value=0.01, value=24.0, step=0.1)
            swath_width_m = st.number_input("Spray width (m) (boom width or effective swath)", min_value=0.50, value=12.0, step=0.5)
            rate_lpha = (600 * total_flow_lpm) / (speed_kmh * swath_width_m) if speed_kmh > 0 and swath_width_m > 0 else 0
            st.info("Formula used: **Rate (L/ha) = 600 × TotalFlow(L/min) ÷ [Speed(km/h) × Swath(m)]**")

            df_inputs = pd.DataFrame([{
                "Distance (m)": distance_m,
                "Time (s)": time_s,
                "Speed (km/h)": round(speed_kmh, 3),
                "Total flow (L/min)": total_flow_lpm,
                "Swath width (m)": swath_width_m,
            }])

    with colB:
        st.markdown("**C. Results**")
        st.metric("Application rate", f"{rate_lpha:.1f} L/ha")

        st.markdown("**D. Tank & chemical planning (optional)**")
        tank_volume_l = st.number_input("Tank volume (L)", min_value=0.0, value=400.0, step=10.0)
        if rate_lpha > 0:
            area_per_tank_ha = tank_volume_l / rate_lpha
        else:
            area_per_tank_ha = 0
        st.write(f"Estimated area covered per tank: **{area_per_tank_ha:.2f} ha**")

        product_rate = st.number_input("Product rate (e.g., L/ha or kg/ha)", min_value=0.0, value=1.0, step=0.1)
        product_per_tank = product_rate * area_per_tank_ha
        st.write(f"Product needed per tank: **{product_per_tank:.2f} units**")

        st.markdown("---")
        st.markdown("**Quick guidance**")
        st.write(
            "- If rate is too high: reduce pressure/flow, increase speed, or use smaller nozzles.\n"
            "- If rate is too low: increase pressure/flow, reduce speed, or use larger nozzles.\n"
            "- Replace nozzles if one nozzle differs >10% from the average."
        )

    # Download
    df_results = pd.DataFrame([{
        "Speed (km/h)": round(speed_kmh, 3),
        "Application rate (L/ha)": round(rate_lpha, 2),
        "Tank volume (L)": tank_volume_l,
        "Area per tank (ha)": round(area_per_tank_ha, 3),
        "Product rate (units/ha)": product_rate,
        "Product per tank (units)": round(product_per_tank, 3)
    }])

    st.markdown("### Export")
    xbytes = to_excel_bytes({"Sprayer_Inputs": df_inputs, "Sprayer_Results": df_results})
    st.download_button(
        "⬇️ Download sprayer calibration as Excel",
        data=xbytes,
        file_name="sprayer_calibration.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# =========================================================
# TAB 2: SEEDER CALIBRATION
# =========================================================
with tab2:
    st.subheader("2) Seeder Calibration")
    st.write("Two simple methods: **(A) weight-based (kg/ha)** and **(B) population-based (seeds/ha)**.")

    subtabA, subtabB = st.tabs(["A) Weight-based (kg/ha)", "B) Population-based (seeds/ha)"])

    # ---------- A) Weight-based ----------
    with subtabA:
        st.markdown("### A) Weight-based calibration (kg/ha)")
        st.write("Best for drills/seeders when you can collect seed output during a known wheel rotation count.")

        col1, col2 = st.columns(2)
        with col1:
            # Area simulated by drive wheel rotations
            wheel_circ_m = st.number_input("Drive wheel circumference (m)", min_value=0.10, value=2.00, step=0.01)
            machine_width_m = st.number_input("Effective machine width (m)", min_value=0.50, value=3.00, step=0.10)
            revolutions = st.number_input("Number of wheel revolutions", min_value=1, value=20, step=1)
            collected_kg = st.number_input("Seed collected during test (kg)", min_value=0.001, value=2.50, step=0.01)

        with col2:
            area_m2 = wheel_circ_m * machine_width_m * revolutions
            area_ha = area_m2 / 10000
            seed_rate_kg_ha = collected_kg / area_ha if area_ha > 0 else 0

            st.info("Area tested (ha) = Circumference × Width × Revolutions ÷ 10,000")
            st.metric("Test area", f"{area_ha:.4f} ha")
            st.metric("Estimated seeding rate", f"{seed_rate_kg_ha:.1f} kg/ha")

        target_rate = st.number_input("Target seeding rate (kg/ha)", min_value=0.0, value=120.0, step=1.0)
        if target_rate > 0:
            error_pct = ((seed_rate_kg_ha - target_rate) / target_rate) * 100
            st.write(f"Difference from target: **{error_pct:+.1f}%**")
            st.caption("If your drill has an adjustment lever, change it and repeat the test until you are close to target.")

        dfA_inputs = pd.DataFrame([{
            "Wheel circumference (m)": wheel_circ_m,
            "Machine width (m)": machine_width_m,
            "Revolutions": revolutions,
            "Collected seed (kg)": collected_kg,
            "Test area (ha)": round(area_ha, 6),
            "Seeding rate (kg/ha)": round(seed_rate_kg_ha, 2),
            "Target (kg/ha)": target_rate,
            "Error (%)": round(error_pct, 2) if target_rate > 0 else None
        }])

        xbytesA = to_excel_bytes({"Seeder_WeightBased": dfA_inputs})
        st.download_button(
            "⬇️ Download weight-based calibration as Excel",
            data=xbytesA,
            file_name="seeder_calibration_weight_based.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # ---------- B) Population-based ----------
    with subtabB:
        st.markdown("### B) Population-based calibration (seeds/ha)")
        st.write("Useful when you know **target plant population** (seeds/ha) and row spacing.")

        col3, col4 = st.columns(2)
        with col3:
            target_seeds_ha = st.number_input("Target population (seeds/ha)", min_value=1, value=200000, step=1000)
            row_spacing_m = st.number_input("Row spacing (m)", min_value=0.10, value=0.75, step=0.05)

            st.caption("Examples: maize 0.70–0.80 m, wheat drill 0.15–0.25 m")

        with col4:
            # Plants per meter of row = seeds/ha * row_spacing / 10,000
            seeds_per_m_row = (target_seeds_ha * row_spacing_m) / 10000
            in_row_spacing_m = safe_div(1, seeds_per_m_row)
            st.metric("Seeds per meter of row", f"{seeds_per_m_row:.2f}")
            st.metric("Expected in-row spacing", f"{in_row_spacing_m:.3f} m" if in_row_spacing_m else "N/A")

        st.markdown("**Quick field check (planter):**")
        check_distance_m = st.number_input("Row length to check (m)", min_value=5.0, value=50.0, step=5.0)
        expected_seeds = seeds_per_m_row * check_distance_m
        st.write(f"Expected seeds in {check_distance_m:.0f} m of one row: **{expected_seeds:.0f} seeds**")

        actual_seeds = st.number_input("Actual seeds counted in that distance (optional)", min_value=0, value=0, step=1)
        if actual_seeds > 0:
            actual_seeds_ha = (actual_seeds / check_distance_m) * (10000 / row_spacing_m) if check_distance_m > 0 and row_spacing_m > 0 else 0
            diff_pct = ((actual_seeds_ha - target_seeds_ha) / target_seeds_ha) * 100
            st.write(f"Estimated actual population: **{actual_seeds_ha:.0f} seeds/ha**")
            st.write(f"Difference from target: **{diff_pct:+.1f}%**")

        dfB = pd.DataFrame([{
            "Target (seeds/ha)": target_seeds_ha,
            "Row spacing (m)": row_spacing_m,
            "Seeds per meter of row": round(seeds_per_m_row, 3),
            "Expected in-row spacing (m)": round(in_row_spacing_m, 4) if in_row_spacing_m else None,
            "Check distance (m)": check_distance_m,
            "Expected seeds in check": round(expected_seeds, 0),
            "Actual seeds counted": actual_seeds if actual_seeds > 0 else None,
        }])

        xbytesB = to_excel_bytes({"Seeder_PopulationBased": dfB})
        st.download_button(
            "⬇️ Download population-based calibration as Excel",
            data=xbytesB,
            file_name="seeder_calibration_population_based.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


# =========================================================
# TAB 3 (OPTIONAL): QUICK FUEL & FIELD CAPACITY
# =========================================================
with tab3:
    st.subheader("3) Quick Fuel & Field Capacity (Optional)")
    st.write("A minimal planning calculator (kept intentionally simple).")

    c1, c2 = st.columns(2)
    with c1:
        engine_kw = st.number_input("Engine power (kW)", min_value=1.0, value=75.0, step=1.0)
        load = st.slider("Load factor", 0.0, 1.0, 0.7, 0.05)
        hrs = st.number_input("Hours", min_value=0.0, value=8.0, step=0.5)
        svfc = st.number_input("SVFC (L/kWh)", min_value=0.10, value=0.24, step=0.01)
        price = st.number_input("Fuel price (per L)", min_value=0.0, value=1.2, step=0.1)

    with c2:
        speed = st.number_input("Speed (km/h)", min_value=0.5, value=6.0, step=0.5)
        width = st.number_input("Working width (m)", min_value=0.5, value=3.0, step=0.5)
        eff = st.number_input("Field efficiency (%)", min_value=50.0, max_value=100.0, value=80.0, step=1.0)
        area = st.number_input("Field area (ha)", min_value=0.0, value=10.0, step=1.0)

    energy = engine_kw * load * hrs
    fuel = energy * svfc
    cost = fuel * price
    efc = (speed * width * (eff/100)) / 10
    time_req = area / efc if efc > 0 else 0

    st.metric("Energy output", f"{energy:.1f} kWh")
    st.metric("Fuel", f"{fuel:.1f} L")
    st.metric("Fuel cost", f"{cost:.1f}")
    st.metric("Effective field capacity", f"{efc:.2f} ha/h")
    st.metric("Time required", f"{time_req:.2f} h")

    df3 = pd.DataFrame([{
        "Engine (kW)": engine_kw,
        "Load factor": load,
        "Hours": hrs,
        "SVFC (L/kWh)": svfc,
        "Fuel price": price,
        "Energy (kWh)": round(energy, 2),
        "Fuel (L)": round(fuel, 2),
        "Fuel cost": round(cost, 2),
        "Speed (km/h)": speed,
        "Width (m)": width,
        "Efficiency (%)": eff,
        "Area (ha)": area,
        "EFC (ha/h)": round(efc, 3),
        "Time (h)": round(time_req, 3),
    }])

    xbytes3 = to_excel_bytes({"Quick_Planning": df3})
    st.download_button(
        "⬇️ Download quick planning as Excel",
        data=xbytes3,
        file_name="quick_planning.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
