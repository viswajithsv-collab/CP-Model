"""
Modern VAD Simulator - Sleek One-Screen Dashboard
Real-time cardiovascular + LVAD simulation
"""

import streamlit as st
import numpy as np
import pandas as pd
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from cardiovascular_model import (
    CardiovascularParameters, 
    CardiovascularState,
    simulate_cardiovascular_system
)

# Page config
st.set_page_config(
    page_title="VAD Simulator",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern Dark Theme CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 100%);
        padding: 10px;
    }
    
    /* Glass morphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        margin: 5px 0;
    }
    
    /* Modern metrics */
    .stMetric {
        background: rgba(0, 255, 255, 0.1);
        padding: 10px;
        border-radius: 10px;
        border-left: 3px solid #00ffff;
    }
    
    .stMetric label {
        color: #00ffff !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }
    
    .stMetric .metric-value {
        color: #ffffff !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }
    
    /* Sliders */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #ff006e, #00ffff);
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #00ffff;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 1px;
    }
    
    /* Toggle switches */
    .stCheckbox {
        color: #00ffff;
    }
    
    /* Number inputs */
    .stNumberInput {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Title with modern styling
st.markdown("<h1 style='text-align: center; margin: 0; padding: 10px; background: linear-gradient(90deg, #ff006e, #00ffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 36px;'>🫀 VAD SIMULATOR</h1>", unsafe_allow_html=True)

# =======================
# PLAYBACK CONTROLS
# =======================
st.markdown("<h4 style='text-align: center; color: #00ffff; margin: 5px 0;'>🎮 SIMULATION CONTROL</h4>", unsafe_allow_html=True)

control_col1, control_col2, control_col3, control_col4, control_col5 = st.columns([1,1,1,1,2])

with control_col1:
    if st.button("▶️ PLAY", use_container_width=True, type="primary"):
        st.session_state['running'] = True
        st.session_state['stopped'] = False
        
with control_col2:
    if st.button("⏸️ PAUSE", use_container_width=True):
        st.session_state['running'] = False
        
with control_col3:
    if st.button("⏹️ STOP", use_container_width=True):
        st.session_state['running'] = False
        st.session_state['stopped'] = True
        # Reset parameters to defaults
        
with control_col4:
    if st.button("🔄 RESET", use_container_width=True):
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

with control_col5:
    status = "🟢 RUNNING" if st.session_state.get('running', True) else "⏸️ PAUSED"
    if st.session_state.get('stopped', False):
        status = "⏹️ STOPPED"
    st.markdown(f"<div style='text-align: center; color: #00ffff; padding: 8px; background: rgba(0,255,255,0.1); border-radius: 5px;'>{status}</div>", unsafe_allow_html=True)

# Initialize session state
if 'running' not in st.session_state:
    st.session_state['running'] = True
if 'stopped' not in st.session_state:
    st.session_state['stopped'] = False

st.markdown("---")

# =======================
# TOP ROW: VAD CONTROLS + HEART DISEASE
# =======================
col_vad, col_heart, col_vitals = st.columns([1.5, 1.5, 2])

with col_vad:
    st.markdown("<h3>🔴 ROTARY VAD</h3>", unsafe_allow_html=True)
    
    pump_on = st.checkbox("⚡ PUMP ON", value=False, key="pump")
    
    col_vad1, col_vad2 = st.columns(2)
    with col_vad1:
        pump_speed = st.slider("🔄 Speed (RPM)", 0, 12000, 0, 500, disabled=not pump_on)
        pulsation = st.slider("💓 Pulsation", 0.0, 1.0, 0.25, 0.05, disabled=not pump_on)
    with col_vad2:
        ramp_mode = st.checkbox("📈 Ramp Mode", disabled=not pump_on)
        phase_shift = st.slider("⏰ Phase (deg)", 0, 360, 100, 10, disabled=not pump_on)

with col_heart:
    st.markdown("<h3>💊 HEART DISEASE</h3>", unsafe_allow_html=True)
    
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        Emaxlv = st.slider("💪 LV Contractility", 0.5, 5.0, 2.7, 0.1, format="%.1f")
        Emaxrv = st.slider("💙 RV Contractility", 0.3, 3.0, 1.6, 0.1, format="%.1f")
    with col_h2:
        aortic_stenosis = st.slider("🔴 Aortic Stenosis", 0.0, 1.0, 0.0, 0.1)
        mitral_regurg = st.slider("🔵 Mitral Regurg", 0.0, 1.0, 0.0, 0.1)

with col_vitals:
    st.markdown("<h3>📊 VITAL SIGNS</h3>", unsafe_allow_html=True)
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        HR = st.slider("💗 Heart Rate", 40, 180, 75, 5)
        TBV = st.slider("🩸 Blood Volume", 3000, 7000, 5300, 100, format="%d ml")
    with col_v2:
        Rsa = st.slider("🌡️ Sys Resistance", 0.02, 0.15, 0.06, 0.01, format="%.3f")
        Csa = st.slider("💨 Sys Compliance", 0.1, 0.5, 0.28, 0.02, format="%.2f")

st.markdown("---")

# =======================
# RUN SIMULATION (only if running)
# =======================
if st.session_state.get('running', True) and not st.session_state.get('stopped', False):
    params = CardiovascularParameters()
    params.Rsa = Rsa
    params.Csa = Csa
    params.TBV = TBV

    state = CardiovascularState()

    duration = 3.0
    dt = 0.01  # Increased from 0.005 - fewer points, smoother plots

    with st.spinner('🔄 Computing...'):
        results = simulate_cardiovascular_system(params, state, HR=HR, duration=duration, dt=dt)
    
    # Store results in session state for export
    st.session_state['results'] = results
    st.session_state['params'] = {
        'HR': HR, 'TBV': TBV, 'Rsa': Rsa, 'Csa': Csa,
        'Emaxlv': Emaxlv, 'Emaxrv': Emaxrv,
        'pump_on': pump_on, 'pump_speed': pump_speed,
        'pulsation': pulsation, 'phase_shift': phase_shift,
        'aortic_stenosis': aortic_stenosis, 'mitral_regurg': mitral_regurg
    }
else:
    # Use last results if paused, or show stopped message
    if 'results' in st.session_state and not st.session_state.get('stopped', False):
        results = st.session_state['results']
    else:
        st.warning("⏹️ Simulation stopped. Press PLAY to start.")
        st.stop()

# Calculate metrics
t = results['time']

# Downsample for plotting (plot every 5th point for smoother rendering)
plot_step = 5
t_plot = t[::plot_step]
results_plot = {key: val[::plot_step] for key, val in results.items()}

cardiac_period = 60 / HR
last_cycle_idx = t > (t[-1] - cardiac_period)

systolic_BP = np.max(results['Psa'][last_cycle_idx])
diastolic_BP = np.min(results['Psa'][last_cycle_idx])
mean_BP = np.mean(results['Psa'][last_cycle_idx])
max_LVV = np.max(results['LVV'][last_cycle_idx])
min_LVV = np.min(results['LVV'][last_cycle_idx])
SV = max_LVV - min_LVV
CO = (SV * HR) / 1000
EF = (SV / max_LVV) * 100
max_LVP = np.max(results['LVP'][last_cycle_idx])
mean_PAP = np.mean(results['Ppa'][last_cycle_idx])

# =======================
# METRICS ROW
# =======================
m1, m2, m3, m4, m5, m6, m7 = st.columns(7)
with m1:
    st.metric("HR", f"{HR}", "bpm")
with m2:
    st.metric("BP", f"{systolic_BP:.0f}/{diastolic_BP:.0f}")
with m3:
    st.metric("MAP", f"{mean_BP:.0f}", "mmHg")
with m4:
    st.metric("CO", f"{CO:.1f}", "L/min")
with m5:
    st.metric("SV", f"{SV:.0f}", "ml")
with m6:
    st.metric("EF", f"{EF:.0f}", "%")
with m7:
    st.metric("PAP", f"{mean_PAP:.0f}", "mmHg")

# =======================
# MAIN PLOTS GRID - 2x3
# =======================

# Row 1
plot_col1, plot_col2, plot_col3 = st.columns(3)

with plot_col1:
    st.markdown("<h4 style='text-align: center; color: #ff006e;'>LEFT VENTRICLE</h4>", unsafe_allow_html=True)
    fig1 = make_subplots(rows=2, cols=1, vertical_spacing=0.1, row_heights=[0.5, 0.5])
    
    fig1.add_trace(go.Scatter(x=t_plot, y=results_plot['LVP'], 
                             line=dict(color='#ff006e', width=2, simplify=True),
                             fill='tozeroy', fillcolor='rgba(255,0,110,0.2)',
                             name="LVP"), row=1, col=1)
    
    fig1.add_trace(go.Scatter(x=t_plot, y=results_plot['LVV'], 
                             line=dict(color='#ff4d94', width=2, simplify=True),
                             fill='tozeroy', fillcolor='rgba(255,77,148,0.2)',
                             name="LVV"), row=2, col=1)
    
    fig1.update_xaxes(showgrid=False, color='#00ffff', row=2, col=1)
    fig1.update_yaxes(title_text="P (mmHg)", showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff', row=1, col=1)
    fig1.update_yaxes(title_text="V (ml)", showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff', row=2, col=1)
    fig1.update_layout(height=280, showlegend=False, plot_bgcolor='rgba(0,0,0,0)', 
                      paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=10),
                      margin=dict(l=40, r=10, t=10, b=30))
    st.plotly_chart(fig1, use_container_width=True, key="lv")

with plot_col2:
    st.markdown("<h4 style='text-align: center; color: #00d9ff;'>RIGHT VENTRICLE</h4>", unsafe_allow_html=True)
    fig2 = make_subplots(rows=2, cols=1, vertical_spacing=0.1, row_heights=[0.5, 0.5])
    
    fig2.add_trace(go.Scatter(x=t_plot, y=results_plot['RVP'], 
                             line=dict(color='#00d9ff', width=2),
                             fill='tozeroy', fillcolor='rgba(0,217,255,0.2)',
                             name="RVP"), row=1, col=1)
    
    fig2.add_trace(go.Scatter(x=t_plot, y=results_plot['RVV'], 
                             line=dict(color='#66e3ff', width=2),
                             fill='tozeroy', fillcolor='rgba(102,227,255,0.2)',
                             name="RVV"), row=2, col=1)
    
    fig2.update_xaxes(showgrid=False, color='#00ffff', row=2, col=1)
    fig2.update_yaxes(title_text="P (mmHg)", showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff', row=1, col=1)
    fig2.update_yaxes(title_text="V (ml)", showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff', row=2, col=1)
    fig2.update_layout(height=280, showlegend=False, plot_bgcolor='rgba(0,0,0,0)', 
                      paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=10),
                      margin=dict(l=40, r=10, t=10, b=30))
    st.plotly_chart(fig2, use_container_width=True, key="rv")

with plot_col3:
    st.markdown("<h4 style='text-align: center; color: #00ff88;'>PV LOOPS</h4>", unsafe_allow_html=True)
    fig3 = make_subplots(rows=2, cols=1, vertical_spacing=0.15, row_heights=[0.5, 0.5],
                        subplot_titles=("LV", "RV"))
    
    # LV Loop
    fig3.add_trace(go.Scatter(x=results['LVV'][last_cycle_idx], y=results['LVP'][last_cycle_idx],
                             mode='lines', line=dict(color='#ff006e', width=3),
                             name="LV"), row=1, col=1)
    
    # RV Loop
    fig3.add_trace(go.Scatter(x=results['RVV'][last_cycle_idx], y=results['RVP'][last_cycle_idx],
                             mode='lines', line=dict(color='#00d9ff', width=3),
                             name="RV"), row=2, col=1)
    
    fig3.update_xaxes(title_text="V (ml)", showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff')
    fig3.update_yaxes(title_text="P", showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff')
    fig3.update_layout(height=280, showlegend=False, plot_bgcolor='rgba(0,0,0,0)', 
                      paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=9),
                      margin=dict(l=40, r=10, t=25, b=30))
    st.plotly_chart(fig3, use_container_width=True, key="pvloop")

# Row 2
plot_col4, plot_col5, plot_col6 = st.columns(3)

with plot_col4:
    st.markdown("<h4 style='text-align: center; color: #ff6b35;'>ARTERIAL PRESSURES</h4>", unsafe_allow_html=True)
    fig4 = go.Figure()
    
    fig4.add_trace(go.Scatter(x=t_plot, y=results_plot['Psa'], 
                             line=dict(color='#ff6b35', width=2),
                             name="Aortic"))
    fig4.add_trace(go.Scatter(x=t_plot, y=results_plot['Ppa'], 
                             line=dict(color='#00d9ff', width=2),
                             name="Pulmonary"))
    
    fig4.update_layout(height=240, xaxis_title="Time (s)", yaxis_title="Pressure (mmHg)",
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                      font=dict(color='white', size=10), 
                      legend=dict(x=0.7, y=0.95, bgcolor='rgba(0,0,0,0.5)', font=dict(size=9)),
                      margin=dict(l=40, r=10, t=10, b=40),
                      xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff'),
                      yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff'))
    st.plotly_chart(fig4, use_container_width=True, key="arterial")

with plot_col5:
    st.markdown("<h4 style='text-align: center; color: #ffd60a;'>VALVE FLOWS</h4>", unsafe_allow_html=True)
    fig5 = go.Figure()
    
    fig5.add_trace(go.Scatter(x=t_plot, y=results_plot['Qaov'], line=dict(color='#ff006e', width=2), name="Aortic"))
    fig5.add_trace(go.Scatter(x=t_plot, y=results_plot['Qmv'], line=dict(color='#ff4d94', width=2), name="Mitral"))
    fig5.add_trace(go.Scatter(x=t_plot, y=results_plot['Qpulv'], line=dict(color='#00d9ff', width=2), name="Pulm"))
    fig5.add_trace(go.Scatter(x=t_plot, y=results_plot['Qtv'], line=dict(color='#66e3ff', width=2), name="Tricusp"))
    
    fig5.update_layout(height=240, xaxis_title="Time (s)", yaxis_title="Flow (ml/s)",
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                      font=dict(color='white', size=10),
                      legend=dict(orientation='h', x=0.2, y=1.08, bgcolor='rgba(0,0,0,0.5)', font=dict(size=8)),
                      margin=dict(l=40, r=10, t=10, b=40),
                      xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff'),
                      yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff'))
    st.plotly_chart(fig5, use_container_width=True, key="flows")

with plot_col6:
    st.markdown("<h4 style='text-align: center; color: #06ffa5;'>ATRIAL PRESSURES</h4>", unsafe_allow_html=True)
    fig6 = go.Figure()
    
    fig6.add_trace(go.Scatter(x=t_plot, y=results_plot['LAP'], 
                             line=dict(color='#ff006e', width=2),
                             name="LA"))
    fig6.add_trace(go.Scatter(x=t_plot, y=results_plot['RAP'], 
                             line=dict(color='#00d9ff', width=2),
                             name="RA"))
    
    fig6.update_layout(height=240, xaxis_title="Time (s)", yaxis_title="Pressure (mmHg)",
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                      font=dict(color='white', size=10),
                      legend=dict(x=0.7, y=0.95, bgcolor='rgba(0,0,0,0.5)', font=dict(size=9)),
                      margin=dict(l=40, r=10, t=10, b=40),
                      xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff'),
                      yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#00ffff'))
    st.plotly_chart(fig6, use_container_width=True, key="atrial")

# Footer with data export
st.markdown("---")
export_col1, export_col2, export_col3, export_col4 = st.columns(4)

with export_col1:
    st.markdown("<div style='text-align: center; color: #00ffff; font-size: 12px;'>🟢 SYSTEM ACTIVE | ⚡ REAL-TIME | 🔄 AUTO-UPDATE</div>", unsafe_allow_html=True)

with export_col2:
    # Export hemodynamic data to CSV
    if 'results' in st.session_state:
        import pandas as pd
        
        # Create DataFrame with all results
        df = pd.DataFrame({
            'Time_s': results['time'],
            'LVP_mmHg': results['LVP'],
            'LVV_ml': results['LVV'],
            'RVP_mmHg': results['RVP'],
            'RVV_ml': results['RVV'],
            'Psa_mmHg': results['Psa'],
            'Ppa_mmHg': results['Ppa'],
            'LAP_mmHg': results['LAP'],
            'RAP_mmHg': results['RAP'],
            'Qaov_ml_s': results['Qaov'],
            'Qmv_ml_s': results['Qmv'],
            'Qpulv_ml_s': results['Qpulv'],
            'Qtv_ml_s': results['Qtv']
        })
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Export CSV",
            data=csv,
            file_name=f"vad_sim_HR{HR}_data.csv",
            mime="text/csv",
            use_container_width=True
        )

with export_col3:
    # Export parameters
    if 'params' in st.session_state:
        import json
        
        params_json = json.dumps(st.session_state['params'], indent=2)
        st.download_button(
            label="⚙️ Export Params",
            data=params_json,
            file_name=f"vad_sim_HR{HR}_params.json",
            mime="application/json",
            use_container_width=True
        )

with export_col4:
    # Export summary metrics
    if 'results' in st.session_state:
        summary = f"""VAD SIMULATOR - SUMMARY REPORT
{'='*50}

HEMODYNAMIC METRICS:
- Heart Rate: {HR} bpm
- Blood Pressure: {systolic_BP:.0f}/{diastolic_BP:.0f} mmHg
- Mean Arterial Pressure: {mean_BP:.0f} mmHg
- Cardiac Output: {CO:.2f} L/min
- Stroke Volume: {SV:.0f} ml
- Ejection Fraction: {EF:.0f}%
- Mean PAP: {mean_PAP:.0f} mmHg

DEVICE SETTINGS:
- VAD Pump: {'ON' if pump_on else 'OFF'}
- Pump Speed: {pump_speed} RPM
- Pulsation: {pulsation:.2f}
- Phase Shift: {phase_shift}°

HEART PARAMETERS:
- LV Contractility: {Emaxlv:.1f}
- RV Contractility: {Emaxrv:.1f}
- Aortic Stenosis: {aortic_stenosis:.1f}
- Mitral Regurgitation: {mitral_regurg:.1f}

SYSTEM PARAMETERS:
- Systemic Resistance: {Rsa:.3f} mmHg·s/ml
- Systemic Compliance: {Csa:.2f} ml/mmHg
- Total Blood Volume: {TBV} ml

{'='*50}
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        st.download_button(
            label="📄 Export Report",
            data=summary,
            file_name=f"vad_sim_HR{HR}_report.txt",
            mime="text/plain",
            use_container_width=True
        )
