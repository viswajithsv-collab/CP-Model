"""
VAD Simulator - Compact Single Screen Version
Everything visible at once, NO scrolling needed!
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

# Compact CSS - everything smaller!
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1f35 0%, #0d1117 100%);
        padding: 5px;
    }
    
    .stMetric {
        background: rgba(0, 200, 255, 0.1);
        padding: 5px;
        border-radius: 8px;
        border-left: 3px solid #00c8ff;
    }
    
    .stMetric label {
        color: #00c8ff !important;
        font-size: 10px !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    
    h1, h2, h3, h4 {
        color: #00c8ff;
        font-family: 'Segoe UI', sans-serif;
        margin: 5px 0;
    }
    
    .stSlider {
        padding: 0px;
    }
    
    /* Make everything more compact */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
</style>
""", unsafe_allow_html=True)

# Title - smaller
st.markdown("<h2 style='text-align: center; margin: 0; padding: 5px; background: linear-gradient(90deg, #0099ff, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🫀 VAD SIMULATOR</h2>", unsafe_allow_html=True)

# =======================
# COMPACT PLAYBACK CONTROLS
# =======================
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
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

with control_col5:
    status = "🟢 RUNNING" if st.session_state.get('running', True) else "⏸️ PAUSED"
    if st.session_state.get('stopped', False):
        status = "⏹️ STOPPED"
    st.markdown(f"<div style='text-align: center; color: #00ffff; padding: 5px; background: rgba(0,255,255,0.1); border-radius: 5px; font-size: 14px;'>{status}</div>", unsafe_allow_html=True)

# Initialize session state
if 'running' not in st.session_state:
    st.session_state['running'] = True
if 'stopped' not in st.session_state:
    st.session_state['stopped'] = False
if 'selected_signal' not in st.session_state:
    st.session_state['selected_signal'] = 'LVP'
if 'scroll_window' not in st.session_state:
    st.session_state['scroll_window'] = 10.0

# =======================
# MAIN LAYOUT: CONTROLS (LEFT) + PLOT (RIGHT)
# =======================
col_controls, col_plot = st.columns([1, 2])

with col_controls:
    # =======================
    # HEART DISEASE - COMPACT
    # =======================
    st.markdown("<h4 style='margin: 5px 0;'>💊 HEART</h4>", unsafe_allow_html=True)
    
    Emaxlv = st.slider("💪 LV Contract", 0.5, 2.7, 2.0, 0.1, format="%.1f")
    Emaxrv = st.slider("💙 RV Contract", 0.5, 2.0, 1.2, 0.1, format="%.1f")
    
    # =======================
    # VITALS - COMPACT
    # =======================
    st.markdown("<h4 style='margin: 5px 0;'>📊 VITALS</h4>", unsafe_allow_html=True)
    
    HR = st.slider("💗 HR (bpm)", 40, 180, 75, 5)
    TBV = st.slider("🩸 Volume (ml)", 3000, 7000, 5300, 200)
    Rsa = st.slider("🌡️ Resistance", 0.05, 0.30, 0.20, 0.01, format="%.2f")
    Csa = st.slider("💨 Compliance", 0.1, 0.5, 0.28, 0.02, format="%.2f")
    
    # =======================
    # DISPLAY - COMPACT
    # =======================
    st.markdown("<h4 style='margin: 5px 0;'>🖥️ DISPLAY</h4>", unsafe_allow_html=True)
    scroll_window = st.slider("📺 Window (s)", 5.0, 30.0, 10.0, 5.0)
    st.session_state['scroll_window'] = scroll_window

with col_plot:
    # =======================
    # SIGNAL SELECTOR BUTTONS - COMPACT
    # =======================
    st.markdown("<h4 style='text-align: center; margin: 5px 0;'>📊 SIGNAL DISPLAY</h4>", unsafe_allow_html=True)
    
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
        if st.button("🔄 PV", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'PV' else "secondary"):
            st.session_state['selected_signal'] = 'PV'
    with btn_col7:
        if st.button("🩸 Art", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'Arterial' else "secondary"):
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

        duration = 30.0
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
            'Emaxlv': Emaxlv, 'Emaxrv': Emaxrv
        }
        
        # Calculate metrics
        systolic_BP = np.max(results['Psa'])
        diastolic_BP = np.min(results['Psa'])
        mean_BP = np.mean(results['Psa'])
        mean_PAP = np.mean(results['Ppa'])
        
        # Cardiac output
        last_10s_idx = results['time'] >= (results['time'][-1] - 10.0)
        mean_Qaov = np.mean(results['Qaov'][last_10s_idx])
        CO = mean_Qaov * 60 / 1000  # L/min
        SV = (60 * CO / HR) * 1000 if HR > 0 else 0  # ml
        EF = (SV / np.max(results['LVV'])) * 100 if np.max(results['LVV']) > 0 else 0
        
        # =======================
        # PLOT - SMALLER HEIGHT
        # =======================
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
                title=dict(text="💓 LEFT VENTRICULAR PRESSURE", font=dict(size=16, color='#ff006e')),
                yaxis_title="Pressure (mmHg)",
                height=350  # SMALLER!
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
                title=dict(text="💙 RIGHT VENTRICULAR PRESSURE", font=dict(size=16, color='#00d9ff')),
                yaxis_title="Pressure (mmHg)",
                height=350
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
                title=dict(text="📦 LEFT VENTRICULAR VOLUME", font=dict(size=16, color='#ff4d94')),
                yaxis_title="Volume (ml)",
                height=350
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
                title=dict(text="📦 RIGHT VENTRICULAR VOLUME", font=dict(size=16, color='#66e3ff')),
                yaxis_title="Volume (ml)",
                height=350
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
                title=dict(text="🌊 VALVE FLOWS", font=dict(size=16, color='#ffd60a')),
                yaxis_title="Flow (ml/s)",
                height=350,
                legend=dict(x=0.02, y=0.98, bgcolor='rgba(0,0,0,0.7)', font=dict(size=10))
            )
            
        elif selected == 'PV':
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
                title=dict(text="🔄 PV LOOPS", font=dict(size=16, color='#00ff88')),
                height=350,
                showlegend=False
            )
            
        elif selected == 'Arterial':
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Psa'][scroll_idx], 
                                    line=dict(color='#ff6b35', width=3), name="Aortic"))
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Ppa'][scroll_idx], 
                                    line=dict(color='#00d9ff', width=3), name="Pulmonary"))
            fig.update_layout(
                title=dict(text="🩸 ARTERIAL PRESSURES", font=dict(size=16, color='#ff6b35')),
                yaxis_title="Pressure (mmHg)",
                height=350,
                legend=dict(x=0.02, y=0.98, bgcolor='rgba(0,0,0,0.7)', font=dict(size=10))
            )
        
        # Common layout
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
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
            margin=dict(l=50, r=20, t=60, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True, key="main_plot")
        
        # =======================
        # METRICS ROW - COMPACT
        # =======================
        st.markdown("<h4 style='text-align: center; margin: 5px 0;'>📊 METRICS</h4>", unsafe_allow_html=True)
        
        met1, met2, met3, met4, met5, met6 = st.columns(6)
        
        with met1:
            st.metric("BP", f"{systolic_BP:.0f}/{diastolic_BP:.0f}")
        with met2:
            st.metric("MAP", f"{mean_BP:.0f}")
        with met3:
            st.metric("CO", f"{CO:.2f} L/min")
        with met4:
            st.metric("SV", f"{SV:.0f} ml")
        with met5:
            st.metric("EF", f"{EF:.0f}%")
        with met6:
            st.metric("PAP", f"{mean_PAP:.0f}")

# =======================
# EXPORT FOOTER - COMPACT
# =======================
export_col1, export_col2, export_col3 = st.columns(3)

with export_col1:
    if 'results' in st.session_state:
        df = pd.DataFrame({
            'Time_s': results['time'],
            'LVP_mmHg': results['LVP'],
            'LVV_ml': results['LVV'],
            'RVP_mmHg': results['RVP'],
            'RVV_ml': results['RVV'],
            'Psa_mmHg': results['Psa'],
            'Ppa_mmHg': results['Ppa'],
            'Qaov_ml_s': results['Qaov'],
            'Qmv_ml_s': results['Qmv'],
            'Qpulv_ml_s': results['Qpulv'],
            'Qtv_ml_s': results['Qtv']
        })
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 CSV",
            data=csv,
            file_name=f"vad_sim_HR{HR}_data.csv",
            mime="text/csv",
            use_container_width=True
        )

with export_col2:
    if 'params' in st.session_state:
        params_json = json.dumps(st.session_state['params'], indent=2)
        st.download_button(
            label="⚙️ Params",
            data=params_json,
            file_name=f"vad_sim_HR{HR}_params.json",
            mime="application/json",
            use_container_width=True
        )

with export_col3:
    if 'results' in st.session_state:
        summary = f"""VAD SIMULATOR REPORT
{'='*40}

HEMODYNAMICS:
- HR: {HR} bpm
- BP: {systolic_BP:.0f}/{diastolic_BP:.0f} mmHg
- MAP: {mean_BP:.0f} mmHg
- CO: {CO:.2f} L/min
- SV: {SV:.0f} ml
- EF: {EF:.0f}%
- PAP: {mean_PAP:.0f} mmHg

PARAMETERS:
- LV Contractility: {Emaxlv:.1f}
- RV Contractility: {Emaxrv:.1f}
- Resistance: {Rsa:.3f}
- Compliance: {Csa:.2f}
- Blood Volume: {TBV} ml

{'='*40}
{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        st.download_button(
            label="📄 Report",
            data=summary,
            file_name=f"vad_sim_HR{HR}_report.txt",
            mime="text/plain",
            use_container_width=True
        )
