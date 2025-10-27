"""
Modern VAD Simulator - Single Plot Interface
Real-time cardiovascular + LVAD simulation with signal selector
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

# Modern Medical Theme CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1f35 0%, #0d1117 100%);
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
        background: rgba(0, 200, 255, 0.1);
        padding: 8px;
        border-radius: 8px;
        border-left: 3px solid #00c8ff;
    }
    
    .stMetric label {
        color: #00c8ff !important;
        font-size: 11px !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 20px !important;
        font-weight: 700 !important;
    }
    
    /* Sliders */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #0099ff, #00ff88);
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #00c8ff;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 1px;
    }
    
    /* Signal selector buttons */
    .signal-button {
        display: inline-block;
        padding: 8px 16px;
        margin: 4px;
        background: rgba(0, 200, 255, 0.1);
        border: 2px solid #00c8ff;
        border-radius: 8px;
        color: #00c8ff;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .signal-button:hover {
        background: rgba(0, 200, 255, 0.3);
        transform: scale(1.05);
    }
    
    .signal-button-active {
        background: linear-gradient(90deg, #0099ff, #00ff88);
        color: #000;
        border-color: #00ff88;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; margin: 0; padding: 10px; background: linear-gradient(90deg, #0099ff, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 36px;'>🫀 VAD SIMULATOR</h1>", unsafe_allow_html=True)

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
if 'selected_signal' not in st.session_state:
    st.session_state['selected_signal'] = 'LVP'
if 'scroll_window' not in st.session_state:
    st.session_state['scroll_window'] = 10.0  # seconds

st.markdown("---")

# =======================
# MAIN LAYOUT: CONTROLS (LEFT) + PLOT (RIGHT)
# =======================
col_controls, col_plot = st.columns([1, 2.5])

with col_controls:
    # =======================
    # VAD CONTROLS
    # =======================
    st.markdown("<h3>🔴 ROTARY VAD</h3>", unsafe_allow_html=True)
    
    pump_on = st.checkbox("⚡ PUMP ON", value=False, key="pump")
    pump_speed = st.slider("🔄 Speed (RPM)", 0, 12000, 0, 500, disabled=not pump_on)
    pulsation = st.slider("💓 Pulsation", 0.0, 1.0, 0.25, 0.05, disabled=not pump_on)
    ramp_mode = st.checkbox("📈 Ramp Mode", disabled=not pump_on)
    phase_shift = st.slider("⏰ Phase (deg)", 0, 360, 100, 10, disabled=not pump_on)
    
    st.markdown("---")
    
    # =======================
    # HEART DISEASE
    # =======================
    st.markdown("<h3>💊 HEART DISEASE</h3>", unsafe_allow_html=True)
    
    Emaxlv = st.slider("💪 LV Contractility", 0.0, 2.7, 2.0, 0.1, format="%.1f")
    Emaxrv = st.slider("💙 RV Contractility", 0.0, 2.0, 1.2, 0.1, format="%.1f")
    aortic_stenosis = st.slider("🔴 Aortic Stenosis", 0.0, 1.0, 0.0, 0.1)
    mitral_regurg = st.slider("🔵 Mitral Regurg", 0.0, 1.0, 0.0, 0.1)
    
    st.markdown("---")
    
    # =======================
    # VITALS
    # =======================
    st.markdown("<h3>📊 VITAL SIGNS</h3>", unsafe_allow_html=True)
    
    HR = st.slider("💗 Heart Rate", 40, 180, 75, 5)
    TBV = st.slider("🩸 Blood Volume", 3000, 7000, 5300, 100, format="%d ml")
    Rsa = st.slider("🌡️ Sys Resistance", 0.05, 0.30, 0.20, 0.01, format="%.2f")
    Csa = st.slider("💨 Sys Compliance", 0.1, 0.5, 0.28, 0.02, format="%.2f")
    
    st.markdown("---")
    
    # =======================
    # SCROLL WINDOW CONTROL
    # =======================
    st.markdown("<h3>🖥️ DISPLAY</h3>", unsafe_allow_html=True)
    scroll_window = st.slider("📺 Window (sec)", 5.0, 30.0, 10.0, 1.0)
    st.session_state['scroll_window'] = scroll_window

with col_plot:
    # =======================
    # SIGNAL SELECTOR BUTTONS
    # =======================
    st.markdown("<h3 style='text-align: center;'>📊 SIGNAL DISPLAY</h3>", unsafe_allow_html=True)
    
    # Create signal selector buttons
    btn_col1, btn_col2, btn_col3, btn_col4, btn_col5, btn_col6, btn_col7 = st.columns(7)
    
    with btn_col1:
        if st.button("💓 LVP", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'LVP' else "secondary"):
            st.session_state['selected_signal'] = 'LVP'
    with btn_col2:
        if st.button("💙 RVP", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'RVP' else "secondary"):
            st.session_state['selected_signal'] = 'RVP'
    with btn_col3:
        if st.button("📦 LVV", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'LVV' else "secondary"):
            st.session_state['selected_signal'] = 'LVV'
    with btn_col4:
        if st.button("📦 RVV", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'RVV' else "secondary"):
            st.session_state['selected_signal'] = 'RVV'
    with btn_col5:
        if st.button("🌊 Flows", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'Flows' else "secondary"):
            st.session_state['selected_signal'] = 'Flows'
    with btn_col6:
        if st.button("🔄 PV Loops", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'PV' else "secondary"):
            st.session_state['selected_signal'] = 'PV'
    with btn_col7:
        if st.button("🩸 Arterial", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'Arterial' else "secondary"):
            st.session_state['selected_signal'] = 'Arterial'
    
    # =======================
    # RUN SIMULATION
    # =======================
    if st.session_state.get('running', True) and not st.session_state.get('stopped', False):
        params = CardiovascularParameters()
        params.Rsa = Rsa
        params.Csa = Csa
        params.TBV = TBV

        state = CardiovascularState()

        duration = 30.0  # 30 seconds
        dt = 0.001

        with st.spinner('🔄 Computing...'):
            results = simulate_cardiovascular_system(
                params, state, HR=HR, duration=duration, dt=dt,
                Emaxlv=Emaxlv, Emaxrv=Emaxrv
            )
        
        # Store results
        st.session_state['results'] = results
        st.session_state['params'] = {
            'HR': HR, 'TBV': TBV, 'Rsa': Rsa, 'Csa': Csa,
            'Emaxlv': Emaxlv, 'Emaxrv': Emaxrv,
            'pump_on': pump_on, 'pump_speed': pump_speed,
            'pulsation': pulsation, 'phase_shift': phase_shift,
            'aortic_stenosis': aortic_stenosis, 'mitral_regurg': mitral_regurg
        }
        
        # Calculate metrics
        systolic_BP = np.max(results['Psa'])
        diastolic_BP = np.min(results['Psa'])
        mean_BP = np.mean(results['Psa'])
        mean_PAP = np.mean(results['Ppa'])
        
        # Cardiac output (use last few cycles)
        last_10s_idx = results['time'] >= (results['time'][-1] - 10.0)
        mean_Qaov = np.mean(results['Qaov'][last_10s_idx])
        CO = mean_Qaov * 60 / 1000  # L/min
        SV = (60 * CO / HR) * 1000  # ml
        EF = (SV / np.max(results['LVV'])) * 100
        
        # =======================
        # DISPLAY SELECTED SIGNAL (SCROLLING)
        # =======================
        # Get scrolling window (last N seconds)
        t = results['time']
        window_start = max(0, t[-1] - scroll_window)
        scroll_idx = t >= window_start
        t_scroll = t[scroll_idx]
        
        selected = st.session_state['selected_signal']
        
        fig = go.Figure()
        
        if selected == 'LVP':
            fig.add_trace(go.Scatter(
                x=t_scroll, y=results['LVP'][scroll_idx],
                mode='lines',
                line=dict(color='#ff006e', width=3),
                fill='tozeroy',
                fillcolor='rgba(255, 0, 110, 0.2)',
                name='LV Pressure'
            ))
            fig.update_layout(
                title=dict(text="💓 LEFT VENTRICULAR PRESSURE", font=dict(size=20, color='#ff006e')),
                yaxis_title="Pressure (mmHg)",
                height=500
            )
            
        elif selected == 'RVP':
            fig.add_trace(go.Scatter(
                x=t_scroll, y=results['RVP'][scroll_idx],
                mode='lines',
                line=dict(color='#00d9ff', width=3),
                fill='tozeroy',
                fillcolor='rgba(0, 217, 255, 0.2)',
                name='RV Pressure'
            ))
            fig.update_layout(
                title=dict(text="💙 RIGHT VENTRICULAR PRESSURE", font=dict(size=20, color='#00d9ff')),
                yaxis_title="Pressure (mmHg)",
                height=500
            )
            
        elif selected == 'LVV':
            fig.add_trace(go.Scatter(
                x=t_scroll, y=results['LVV'][scroll_idx],
                mode='lines',
                line=dict(color='#ff4d94', width=3),
                fill='tozeroy',
                fillcolor='rgba(255, 77, 148, 0.2)',
                name='LV Volume'
            ))
            fig.update_layout(
                title=dict(text="📦 LEFT VENTRICULAR VOLUME", font=dict(size=20, color='#ff4d94')),
                yaxis_title="Volume (ml)",
                height=500
            )
            
        elif selected == 'RVV':
            fig.add_trace(go.Scatter(
                x=t_scroll, y=results['RVV'][scroll_idx],
                mode='lines',
                line=dict(color='#66e3ff', width=3),
                fill='tozeroy',
                fillcolor='rgba(102, 227, 255, 0.2)',
                name='RV Volume'
            ))
            fig.update_layout(
                title=dict(text="📦 RIGHT VENTRICULAR VOLUME", font=dict(size=20, color='#66e3ff')),
                yaxis_title="Volume (ml)",
                height=500
            )
            
        elif selected == 'Flows':
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Qaov'][scroll_idx], 
                                    line=dict(color='#ff006e', width=2), name="Aortic"))
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Qmv'][scroll_idx], 
                                    line=dict(color='#ff4d94', width=2), name="Mitral"))
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Qpulv'][scroll_idx], 
                                    line=dict(color='#00d9ff', width=2), name="Pulmonary"))
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Qtv'][scroll_idx], 
                                    line=dict(color='#66e3ff', width=2), name="Tricuspid"))
            fig.update_layout(
                title=dict(text="🌊 VALVE FLOWS", font=dict(size=20, color='#ffd60a')),
                yaxis_title="Flow (ml/s)",
                height=500,
                legend=dict(x=0.02, y=0.98, bgcolor='rgba(0,0,0,0.7)')
            )
            
        elif selected == 'PV':
            # PV Loops - show last cardiac cycle
            cycle_duration = 60.0 / HR
            last_cycle_idx = results['time'] >= (results['time'][-1] - cycle_duration)
            
            fig = make_subplots(rows=1, cols=2, subplot_titles=("LV Loop", "RV Loop"))
            
            fig.add_trace(go.Scatter(
                x=results['LVV'][last_cycle_idx], 
                y=results['LVP'][last_cycle_idx],
                mode='lines',
                line=dict(color='#ff006e', width=4),
                name='LV'
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=results['RVV'][last_cycle_idx], 
                y=results['RVP'][last_cycle_idx],
                mode='lines',
                line=dict(color='#00d9ff', width=4),
                name='RV'
            ), row=1, col=2)
            
            fig.update_xaxes(title_text="Volume (ml)", row=1, col=1)
            fig.update_xaxes(title_text="Volume (ml)", row=1, col=2)
            fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=1)
            fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=2)
            
            fig.update_layout(
                title=dict(text="🔄 PRESSURE-VOLUME LOOPS", font=dict(size=20, color='#00ff88')),
                height=500,
                showlegend=False
            )
            
        elif selected == 'Arterial':
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Psa'][scroll_idx], 
                                    line=dict(color='#ff6b35', width=3), name="Aortic"))
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Ppa'][scroll_idx], 
                                    line=dict(color='#00d9ff', width=3), name="Pulmonary"))
            fig.update_layout(
                title=dict(text="🩸 ARTERIAL PRESSURES", font=dict(size=20, color='#ff6b35')),
                yaxis_title="Pressure (mmHg)",
                height=500,
                legend=dict(x=0.02, y=0.98, bgcolor='rgba(0,0,0,0.7)')
            )
        
        # Common layout settings
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=14),
            xaxis=dict(
                title="Time (s)",
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                color='#00ffff'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                color='#00ffff'
            ),
            margin=dict(l=60, r=30, t=80, b=60)
        )
        
        st.plotly_chart(fig, use_container_width=True, key="main_plot")
        
        # =======================
        # METRICS ROW
        # =======================
        st.markdown("---")
        st.markdown("<h3 style='text-align: center;'>📊 HEMODYNAMIC METRICS</h3>", unsafe_allow_html=True)
        
        met1, met2, met3, met4, met5, met6 = st.columns(6)
        
        with met1:
            st.metric("Blood Pressure", f"{systolic_BP:.0f}/{diastolic_BP:.0f}")
        with met2:
            st.metric("MAP", f"{mean_BP:.0f} mmHg")
        with met3:
            st.metric("Cardiac Output", f"{CO:.2f} L/min")
        with met4:
            st.metric("Stroke Volume", f"{SV:.0f} ml")
        with met5:
            st.metric("Ejection Fraction", f"{EF:.0f}%")
        with met6:
            st.metric("Mean PAP", f"{mean_PAP:.0f} mmHg")

# =======================
# EXPORT FOOTER
# =======================
st.markdown("---")
export_col1, export_col2, export_col3, export_col4 = st.columns(4)

with export_col1:
    st.markdown("<div style='text-align: center; color: #00ffff; font-size: 12px;'>🟢 SYSTEM ACTIVE | ⚡ REAL-TIME | 🔄 AUTO-UPDATE</div>", unsafe_allow_html=True)

with export_col2:
    if 'results' in st.session_state:
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
    if 'params' in st.session_state:
        params_json = json.dumps(st.session_state['params'], indent=2)
        st.download_button(
            label="⚙️ Export Params",
            data=params_json,
            file_name=f"vad_sim_HR{HR}_params.json",
            mime="application/json",
            use_container_width=True
        )

with export_col4:
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
