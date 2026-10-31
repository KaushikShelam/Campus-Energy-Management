
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="CampusEMS | Energy Management",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #e5e7eb;
}
[data-testid="stSidebar"] {
    background-color: #111827;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
/* PREMIUM KPI CARDS */

.kpi {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        135deg,
        #192b43 0%,
        #111e31 55%,
        #14263b 100%
    );
    padding: 22px 22px;
    border: 1px solid rgba(100, 145, 190, 0.25);
    border-radius: 16px;
    min-height: 132px;
    box-sizing: border-box;
    margin-bottom: 12px;
    box-shadow:
        0 8px 24px rgba(0, 0, 0, 0.22),
        inset 0 1px 0 rgba(255, 255, 255, 0.035);
    transition: all 0.3s ease;
}

/* Soft accent glow */
.kpi::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--accent, #38bdf8);
    box-shadow: 0 0 15px var(--accent, #38bdf8);
}

/* Decorative light */
.kpi::after {
    content: "";
    position: absolute;
    width: 110px;
    height: 110px;
    right: -42px;
    top: -48px;
    border-radius: 50%;
    background: var(--accent, #38bdf8);
    opacity: 0.09;
    filter: blur(24px);
    transition: opacity 0.3s ease;
}

.kpi:hover {
    transform: translateY(-5px);
    border-color: var(--accent, #38bdf8);
    box-shadow:
        0 12px 30px rgba(0, 0, 0, 0.32),
        0 0 18px color-mix(in srgb, var(--accent, #38bdf8) 20%, transparent);
}

.kpi:hover::after {
    opacity: 0.20;
}

.kpi-label {
    color: #a9bad0;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    position: relative;
    z-index: 1;
}

.kpi-value {
    font-size: 29px;
    font-weight: 750;
    color: #f8fafc;
    margin-top: 16px;
    letter-spacing: -0.7px;
    position: relative;
    z-index: 1;
}

.kpi-unit {
    font-size: 14px;
    color: var(--accent, #38bdf8);
    font-weight: 600;
}

.kpi-icon {
    position: absolute;
    top: 17px;
    right: 19px;
    font-size: 23px;
    opacity: 0.9;
    z-index: 2;
}
.section-title {
    font-size: 21px;
    font-weight: 700;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- BUILDING DATA ----------------
buildings = [
    "Engineering Block",
    "Library",
    "Administrative Block",
    "Laboratories",
    "Hostel Block"
]

# ---------------- SIMULATED READINGS ----------------
random.seed(42)

rows = []

for building in buildings:
    voltage = random.uniform(225, 240)
    current = random.uniform(8, 30)
    power = voltage * current / 1000
    pf = random.uniform(0.85, 0.99)
    solar = random.uniform(0.05, 0.30)
    grid = max(power - solar, 0)

    rows.append({
        "Building": building,
        "Voltage (V)": round(voltage, 2),
        "Current (A)": round(current, 2),
        "Active Power (kW)": round(power, 3),
        "Energy (kWh)": round(power * 8, 2),
        "Frequency (Hz)": round(random.uniform(49.8, 50.2), 2),
        "Power Factor": round(pf, 2),
        "Apparent Power (kVA)": round(power / pf, 3),
        "Solar Power (kW)": round(solar, 3),
        "Grid Power (kW)": round(grid, 3),
        "Temperature (°C)": round(random.uniform(26, 36), 1)
    })

df = pd.DataFrame(rows)

# ---------------- PROFESSIONAL CHART THEME ----------------

CHART_BG = "#111c2e"
PAPER_BG = "#0b1120"
GRID_COLOR = "#26364d"
TEXT_COLOR = "#dce6f1"

CHART_COLORS = [
    "#38bdf8",
    "#818cf8",
    "#34d399",
    "#fbbf24",
    "#f472b6"
]

def style_chart(fig, height=380):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=CHART_BG,
        font=dict(
            family="Inter, Arial",
            size=12,
            color=TEXT_COLOR
        ),
        title=dict(
            font=dict(size=18, color="#f1f5f9"),
            x=0.02,
            xanchor="left"
        ),
        margin=dict(l=25, r=25, t=65, b=35),
        hoverlabel=dict(
            bgcolor="#1e293b",
            bordercolor="#38bdf8",
            font=dict(color="white", size=13)
        ),
        legend=dict(
            orientation="h",
            y=1.12,
            x=0,
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor=GRID_COLOR,
            tickfont=dict(color="#94a3b8")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=False,
            tickfont=dict(color="#94a3b8")
        )
    )
    return fig

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚡ CampusEMS")
st.sidebar.caption("Campus Energy Management System")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Live Monitoring",
        "Building Analysis",
        "Energy Analytics",
        "Solar & Grid",
        "Alerts & Reports"
    ]
)

st.sidebar.divider()
st.sidebar.success("System Online")
st.sidebar.caption("Data: Simulated demonstration readings")

# ---------------- HEADER ----------------
st.title("⚡ Campus Energy Management")
st.caption(
    "Smart Campus Energy Monitoring and Analytics Dashboard"
)

col1, col2 = st.columns([3, 1])

with col1:
    st.write("Monitor electrical performance across campus buildings.")

with col2:
    st.caption("Last refreshed")
    st.write(datetime.now().strftime("%d %b %Y | %I:%M:%S %p"))

st.divider()

# ---------------- KPI VALUES ----------------
total_power = df["Active Power (kW)"].sum()
total_energy = df["Energy (kWh)"].sum()
avg_voltage = df["Voltage (V)"].mean()
total_current = df["Current (A)"].sum()
avg_frequency = df["Frequency (Hz)"].mean()
avg_pf = df["Power Factor"].mean()
total_apparent = df["Apparent Power (kVA)"].sum()
total_solar = df["Solar Power (kW)"].sum()
total_grid = df["Grid Power (kW)"].sum()

def metric_card(label, value, unit):

    card_styles = {
        "Voltage": ("#38bdf8", "⚡"),
        "Current": ("#a78bfa", "〰️"),
        "Active Power": ("#fbbf24", "◈"),
        "Energy Consumption": ("#34d399", "▤"),
        "Frequency": ("#fb7185", "∿"),
        "Power Factor": ("#22d3ee", "◉"),
        "Apparent Power": ("#c084fc", "◇"),
        "Solar Generation": ("#facc15", "☀️"),
        "Grid Power": ("#60a5fa", "▥")
    }

    accent, icon = card_styles.get(
        label, ("#38bdf8", "●")
    )

    st.markdown(
        f"""
        <div class="kpi" style="--accent:{accent}">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">
                {value}
                <span class="kpi-unit">{unit}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- OVERVIEW ----------------
if page == "Overview":

    st.subheader("Campus Overview")

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        metric_card("Voltage", f"{avg_voltage:.1f}", "V")
    with c2:
        metric_card("Current", f"{total_current:.1f}", "A")
    with c3:
        metric_card("Active Power", f"{total_power:.2f}", "kW")
    with c4:
        metric_card("Energy Consumption", f"{total_energy:.1f}", "kWh")

    c5, c6, c7, c8 = st.columns(4, gap="medium")

    with c5:
        metric_card("Frequency", f"{avg_frequency:.2f}", "Hz")
    with c6:
        metric_card("Power Factor", f"{avg_pf:.2f}", "PF")
    with c7:
        metric_card("Apparent Power", f"{total_apparent:.2f}", "kVA")
    with c8:
        metric_card("Solar Generation", f"{total_solar:.2f}", "kW")

    st.markdown('<div class="section-title">Building-wise Power Consumption</div>',
                unsafe_allow_html=True)

    fig = go.Figure()

    sorted_df = df.sort_values("Active Power (kW)")

    fig.add_trace(go.Bar(
        x=sorted_df["Active Power (kW)"],
        y=sorted_df["Building"],
        orientation="h",
        marker=dict(
            color=sorted_df["Active Power (kW)"],
            colorscale=[
                [0, "#2563eb"],
                [0.5, "#06b6d4"],
                [1, "#34d399"]
            ],
            line=dict(width=0),
            cornerradius=8
        ),
        text=sorted_df["Active Power (kW)"].map(
            lambda x: f"{x:.2f} kW"
        ),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Power: %{x:.3f} kW<extra></extra>"
    ))

    fig.update_layout(
        title="Building-wise Active Power Consumption",
        xaxis_title="Active Power (kW)",
        yaxis_title="",
        showlegend=False
    )

    style_chart(fig, 420)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Electrical Parameters</div>',
                unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ---------------- LIVE MONITORING ----------------
elif page == "Live Monitoring":

    st.subheader("Live Electrical Monitoring")

    selected = st.selectbox("Select Building", buildings)
    reading = df[df["Building"] == selected].iloc[0]

    a, b, c = st.columns(3)

    with a:
        metric_card("Voltage", reading["Voltage (V)"], "V")
    with b:
        metric_card("Current", reading["Current (A)"], "A")
    with c:
        metric_card("Active Power", reading["Active Power (kW)"], "kW")

    d, e, f = st.columns(3)

    with d:
        metric_card("Energy", reading["Energy (kWh)"], "kWh")
    with e:
        metric_card("Frequency", reading["Frequency (Hz)"], "Hz")
    with f:
        metric_card("Power Factor", reading["Power Factor"], "PF")

    st.info("These are simulated readings, not live hardware measurements.")

# ---------------- BUILDING ANALYSIS ----------------
elif page == "Building Analysis":

    st.subheader("Building-wise Energy Analysis")

    selected_building = st.selectbox("Choose Building", buildings)

    building_data = df[df["Building"] == selected_building]

    st.dataframe(building_data, use_container_width=True, hide_index=True)

    fig = px.bar(
        building_data.melt(
            id_vars="Building",
            value_vars=["Active Power (kW)", "Solar Power (kW)", "Grid Power (kW)"],
            var_name="Parameter",
            value_name="Power"
        ),
        x="Parameter",
        y="Power",
        color="Parameter",
        title=f"Power Distribution - {selected_building}"
    )

    style_chart(fig, 400)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- ENERGY ANALYTICS ----------------
elif page == "Energy Analytics":

    st.subheader("Energy Consumption Analytics")

    fig = go.Figure(data=[go.Pie(
        labels=df["Building"],
        values=df["Energy (kWh)"],
        hole=0.68,
        marker=dict(
            colors=CHART_COLORS,
            line=dict(color=CHART_BG, width=4)
        ),
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Energy: %{value:.2f} kWh<br>Share: %{percent}<extra></extra>"
    )])

    fig.update_layout(
        title="Campus Energy Distribution",
        showlegend=True,
        annotations=[dict(
            text=f"{total_energy:.1f}<br><span style='font-size:12px'>kWh Total</span>",
            x=0.5,
            y=0.5,
            font=dict(size=22, color="white"),
            showarrow=False
        )]
    )

    style_chart(fig, 420)
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        df,
        x="Building",
        y="Energy (kWh)",
        color="Building",
        title="Energy Consumption Comparison"
    )
    style_chart(fig2, 400)
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- SOLAR AND GRID ----------------
elif page == "Solar & Grid":

    st.subheader("Solar Generation vs Grid Consumption")

    solar_grid = pd.DataFrame({
        "Source": ["Solar", "Grid"],
        "Power (kW)": [total_solar, total_grid]
    })

    fig = px.pie(
        solar_grid,
        names="Source",
        values="Power (kW)",
        hole=0.6,
        title="Campus Power Source Distribution"
    )
    style_chart(fig, 400)
    st.plotly_chart(fig, use_container_width=True)

    st.write(f"**Total Solar Generation:** {total_solar:.2f} kW")
    st.write(f"**Total Grid Consumption:** {total_grid:.2f} kW")

# ---------------- ALERTS AND REPORTS ----------------
elif page == "Alerts & Reports":

    st.subheader("System Alerts")

    alerts = []

    for _, row in df.iterrows():
        if row["Voltage (V)"] < 210 or row["Voltage (V)"] > 250:
            alerts.append(f"Voltage abnormality at {row['Building']}")

        if row["Power Factor"] < 0.85:
            alerts.append(f"Low power factor at {row['Building']}")

    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("No abnormal readings detected in the simulated dataset.")

    st.subheader("Download Energy Report")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Campus Energy Report",
        data=csv,
        file_name="Campus_Energy_Report.csv",
        mime="text/csv"
    )

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "CampusEMS | Smart Campus Energy Management System | "
    "Demonstration Version"
)
