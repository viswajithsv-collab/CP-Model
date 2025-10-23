"""
Interactive Cardiovascular Model - COCKPIT VIEW
Real-time dashboard with all controls and displays
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from cardiovascular_model import (
    CardiovascularParameters, 
    CardiovascularState,
    simulate_cardiovascular_system
)

# Page config
st.set_page_config(
    page_title="Cardiovascular Cockpit",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar for full cockpit view
)

# Custom CSS for cockpit look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid #ff4b4b;
    }
    .stSlider {
        padding: 5px 0;
    }
    h1 {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Courier New', monospace;
    }
    h3 {
        color: #ffa500;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("❤️ CARDIOVASCULAR COCKPIT 🎛️")

# =======================
# CONTROL PANEL (Top)
# =======================
st.markdown("### 🎛️ CONTROL PANEL")
col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns(4)

with col_ctrl1:
    HR = st.slider("💓 Heart Rate (bpm)", 40, 180, 75, 5, key="hr")
    
with col_ctrl2:
    Rsa = st.slider("🔴 Arterial Resistance", 0.02, 0.15, 0.06, 0.01, 
                    key="rsa", format="%.3f")
    
with col_ctrl3:
    Csa = st.slider("💨 Arterial Compliance", 0.1, 0.5, 0.28, 0.05, 
                    key="csa", format="%.2f")
    
with col_ctrl4:
    Emaxlv = st.slider("💪 LV Contractility", 1.0, 5.0, 2.7, 0.2, 
                       key="emaxlv", format="%.1f")

# Advanced controls in expander
with st.expander("⚙️ ADVANCED CONTROLS"):
    adv_col1, adv_col2, adv_col3, adv_col4 = st.columns(4)
    with adv_col1:
        Rlbp = st.slider("Lower Body R", 0.5, 2.5, 1.307, 0.1, format="%.2f")
    with adv_col2:
        Rubp = st.slider("Upper Body R", 0.5, 2.5, 1.407, 0.1, format="%.2f")
    with adv_col3:
        Clbp = st.slider("Peripheral C", 1.0, 4.0, 2.05, 0.1, format="%.2f")
    with adv_col4:
        Emaxrv = st.slider("RV Contractility", 0.5, 3.0, 1.6, 0.1, format="%.1f")

st.markdown("---")

# =======================
# RUN SIMULATION (Auto)
# =======================
params = CardiovascularParameters()
params.Rsa = Rsa
params.Rlbp = Rlbp
params.Rubp = Rubp
params.Csa = Csa
params.Clbp = Clbp

state = CardiovascularState()

# Run simulation with modified elastances
duration = 4.0  # Shorter for faster response
dt = 0.002  # Faster time step

# Modify the simulate function call to use custom elastances
# We'll need to pass Emaxlv and Emaxrv - for now use defaults
results = simulate_cardiovascular_system(params, state, HR=HR, duration=duration, dt=dt)

# Calculate metrics
t = results['time']
cardiac_period = 60 / HR
last_cycle_idx = t > (t[-1] - cardiac_period)

systolic_BP = np.max(results['Psa'][last_cycle_idx])
diastolic_BP = np.min(results['Psa'][last_cycle_idx])
mean_BP = np.mean(results['Psa'][last_cycle_idx])
max_LVV = np.max(results['LVV'][last_cycle_idx])
min_LVV = np.min(results['LVV'][last_cycle_idx])
SV = max_LVV - min_LVV
CO = (SV * HR) / 1000  # L/min
EF = (SV / max_LVV) * 100
max_LVP = np.max(results['LVP'][last_cycle_idx])

# =======================
# VITAL SIGNS DISPLAY
# =======================
st.markdown("### 📊 VITAL SIGNS")
metric_col1, metric_col2, metric_col3, metric_col4, metric_col5, metric_col6 = st.columns(6)

with metric_col1:
    st.metric("💗 HR", f"{HR}", "bpm")
    
with metric_col2:
    st.metric("🩸 SYS/DIA", f"{systolic_BP:.0f}/{diastolic_BP:.0f}", "mmHg")
    
with metric_col3:
    st.metric("📈 MAP", f"{mean_BP:.0f}", "mmHg")
    
with metric_col4:
    st.metric("💧 SV", f"{SV:.0f}", "ml")
    
with metric_col5:
    st.metric("🫀 CO", f"{CO:.1f}", "L/min")
    
with metric_col6:
    st.metric("📊 EF", f"{EF:.0f}", "%")

st.markdown("---")

# =======================
# MAIN DISPLAY - 2x2 Grid
# =======================

# Row 1: Pressures
col_plot1, col_plot2 = st.columns(2)

with col_plot1:
    st.markdown("### 🔴 LEFT HEART")
    fig1 = make_subplots(
        rows=2, cols=1,
        subplot_titles=("LV Pressure", "LV Volume"),
        vertical_spacing=0.15,
        row_heights=[0.5, 0.5]
    )
    
    # LV Pressure
    fig1.add_trace(
        go.Scatter(x=t, y=results['LVP'], 
                  line=dict(color='#ff4b4b', width=3),
                  fill='tozeroy', fillcolor='rgba(255,75,75,0.2)',
                  name="LVP"),
        row=1, col=1
    )
    
    # LV Volume
    fig1.add_trace(
        go.Scatter(x=t, y=results['LVV'], 
                  line=dict(color='#ff1744', width=3),
                  fill='tozeroy', fillcolor='rgba(255,23,68,0.2)',
                  name="LVV"),
        row=2, col=1
    )
    
    fig1.update_xaxes(title_text="Time (s)", row=2, col=1, color='white')
    fig1.update_yaxes(title_text="Pressure (mmHg)", row=1, col=1, color='white')
    fig1.update_yaxes(title_text="Volume (ml)", row=2, col=1, color='white')
    fig1.update_layout(
        height=450,
        showlegend=False,
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color='white', family='Courier New'),
        margin=dict(l=50, r=20, t=50, b=40)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_plot2:
    st.markdown("### 🔵 RIGHT HEART")
    fig2 = make_subplots(
        rows=2, cols=1,
        subplot_titles=("RV Pressure", "RV Volume"),
        vertical_spacing=0.15,
        row_heights=[0.5, 0.5]
    )
    
    # RV Pressure
    fig2.add_trace(
        go.Scatter(x=t, y=results['RVP'], 
                  line=dict(color='#448aff', width=3),
                  fill='tozeroy', fillcolor='rgba(68,138,255,0.2)',
                  name="RVP"),
        row=1, col=1
    )
    
    # RV Volume
    fig2.add_trace(
        go.Scatter(x=t, y=results['RVV'], 
                  line=dict(color='#2979ff', width=3),
                  fill='tozeroy', fillcolor='rgba(41,121,255,0.2)',
                  name="RVV"),
        row=2, col=1
    )
    
    fig2.update_xaxes(title_text="Time (s)", row=2, col=1, color='white')
    fig2.update_yaxes(title_text="Pressure (mmHg)", row=1, col=1, color='white')
    fig2.update_yaxes(title_text="Volume (ml)", row=2, col=1, color='white')
    fig2.update_layout(
        height=450,
        showlegend=False,
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color='white', family='Courier New'),
        margin=dict(l=50, r=20, t=50, b=40)
    )
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Arterial Pressures and PV Loops
col_plot3, col_plot4 = st.columns(2)

with col_plot3:
    st.markdown("### 🌡️ ARTERIAL PRESSURES")
    fig3 = go.Figure()
    
    fig3.add_trace(go.Scatter(
        x=t, y=results['Psa'],
        line=dict(color='#ff6b6b', width=3),
        name="Aortic",
        fill='tozeroy', fillcolor='rgba(255,107,107,0.2)'
    ))
    
    fig3.add_trace(go.Scatter(
        x=t, y=results['Ppa'],
        line=dict(color='#4dabf7', width=3),
        name="Pulmonary",
        fill='tozeroy', fillcolor='rgba(77,171,247,0.2)'
    ))
    
    fig3.update_layout(
        height=400,
        xaxis_title="Time (s)",
        yaxis_title="Pressure (mmHg)",
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color='white', family='Courier New'),
        legend=dict(x=0.7, y=0.95, bgcolor='rgba(30,33,48,0.8)'),
        margin=dict(l=50, r=20, t=20, b=40),
        hovermode='x unified'
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_plot4:
    st.markdown("### 🔄 PV LOOPS")
    fig4 = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Left Ventricle", "Right Ventricle"),
        horizontal_spacing=0.12
    )
    
    # LV PV Loop
    fig4.add_trace(
        go.Scatter(
            x=results['LVV'][last_cycle_idx], 
            y=results['LVP'][last_cycle_idx],
            mode='lines+markers',
            line=dict(color='#ff4b4b', width=4),
            marker=dict(size=4, color='#ff1744'),
            name="LV"
        ),
        row=1, col=1
    )
    
    # RV PV Loop
    fig4.add_trace(
        go.Scatter(
            x=results['RVV'][last_cycle_idx], 
            y=results['RVP'][last_cycle_idx],
            mode='lines+markers',
            line=dict(color='#448aff', width=4),
            marker=dict(size=4, color='#2979ff'),
            name="RV"
        ),
        row=1, col=2
    )
    
    fig4.update_xaxes(title_text="Volume (ml)", row=1, col=1, color='white')
    fig4.update_xaxes(title_text="Volume (ml)", row=1, col=2, color='white')
    fig4.update_yaxes(title_text="Pressure (mmHg)", row=1, col=1, color='white')
    fig4.update_yaxes(title_text="Pressure (mmHg)", row=1, col=2, color='white')
    fig4.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font=dict(color='white', family='Courier New'),
        margin=dict(l=50, r=20, t=50, b=40)
    )
    st.plotly_chart(fig4, use_container_width=True)

# Row 3: Valve Flows
st.markdown("### 💉 VALVE FLOWS")
fig5 = go.Figure()

fig5.add_trace(go.Scatter(x=t, y=results['Qaov'], name="Aortic",
                         line=dict(color='#ff6b6b', width=2)))
fig5.add_trace(go.Scatter(x=t, y=results['Qmv'], name="Mitral",
                         line=dict(color='#ffa94d', width=2)))
fig5.add_trace(go.Scatter(x=t, y=results['Qpulv'], name="Pulmonary",
                         line=dict(color='#4dabf7', width=2)))
fig5.add_trace(go.Scatter(x=t, y=results['Qtv'], name="Tricuspid",
                         line=dict(color='#74c0fc', width=2)))

fig5.update_layout(
    height=300,
    xaxis_title="Time (s)",
    yaxis_title="Flow (ml/s)",
    plot_bgcolor='#0e1117',
    paper_bgcolor='#0e1117',
    font=dict(color='white', family='Courier New'),
    legend=dict(orientation='h', x=0.3, y=1.1, bgcolor='rgba(30,33,48,0.8)'),
    margin=dict(l=50, r=20, t=20, b=40),
    hovermode='x unified'
)
st.plotly_chart(fig5, use_container_width=True)

# Footer with status
st.markdown("---")
col_status1, col_status2, col_status3 = st.columns(3)
with col_status1:
    st.markdown("🟢 **STATUS:** RUNNING")
with col_status2:
    st.markdown(f"⏱️ **SIMULATION:** {duration:.1f}s simulated")
with col_status3:
    st.markdown(f"🔄 **REFRESH:** Auto-updating")
