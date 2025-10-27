"""
Cardiovascular Simulator - REAL-TIME STREAMING
LEFT: Parameters | CENTER: Real-time Plot | RIGHT: Signal Chooser
"""

import streamlit as st
import numpy as np
import pandas as pd
import json
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from cardiovascular_model import (
    CardiovascularParameters, 
    CardiovascularState,
    simulate_cardiovascular_system
)

# Page config
st.set_page_config(
    page_title="Cardiovascular Simulator",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Medical monitor style
st.markdown("""
<style>
    .main {
        background: black;
        padding: 10px;
    }
    
    .stApp {
        background: black;
    }
    
    /* Title styling */
    .main-title {
        color: white;
        font-family: 'Georgia', serif;
        font-style: italic;
        font-size: 48px;
        text-align: center;
        margin: 10px 0;
        background: black;
        padding: 10px;
    }
    
    /* Button row */
    .button-row {
        background: #f0e9d8;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    
    /* Sidebar styling */
    .sidebar-left {
        background: black;
        color: white;
        padding: 20px;
        height: 100%;
    }
    
    .sidebar-right {
        background: #f0e9d8;
        padding: 20px;
        height: 100%;
    }
    
    /* Plot area */
    .plot-area {
        background: white;
        padding: 10px;
        border: 3px solid black;
    }
    
    /* Metrics styling - light color for dark background */
    .stMetric {
        background: rgba(0, 0, 0, 0.3);
        padding: 5px;
        border-radius: 5px;
    }
    
    .stMetric label {
        color: #FFFFF0 !important;
        font-size: 11px !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #FFFFF0 !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }
    
    /* Make sliders look better */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #0099ff, #00ff88);
    }
    
    /* All text on dark background should be #FFFFF0 */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #FFFFF0 !important;
    }
    
    /* Streamlit specific elements */
    .stMarkdown, .stText {
        color: #FFFFF0 !important;
    }
    
    /* Slider labels */
    .stSlider label {
        color: #FFFFF0 !important;
    }
    
    /* Button text */
    .stButton button {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>Cardiovascular Simulator</h1>", unsafe_allow_html=True)

# =======================
# TOP BUTTON ROW
# =======================
btn1, btn2, btn3, btn4, btn5, btn6 = st.columns(6)

with btn1:
    play_btn = st.button("▶️ Play", use_container_width=True, type="primary")
    if play_btn:
        st.session_state['running'] = True
        st.session_state['stopped'] = False

with btn2:
    stop_btn = st.button("⏹️ Stop", use_container_width=True)
    if stop_btn:
        st.session_state['running'] = False
        st.session_state['stopped'] = True
        # Clear all data buffers
        st.session_state['time_data'] = np.array([])
        st.session_state['LVP_data'] = np.array([])
        st.session_state['RVP_data'] = np.array([])
        st.session_state['LVV_data'] = np.array([])
        st.session_state['RVV_data'] = np.array([])
        st.session_state['Psa_data'] = np.array([])
        st.session_state['Ppa_data'] = np.array([])
        st.session_state['Qaov_data'] = np.array([])
        st.session_state['Qmv_data'] = np.array([])
        st.session_state['Qpulv_data'] = np.array([])
        st.session_state['Qtv_data'] = np.array([])
        st.session_state['current_time'] = 0.0
        st.rerun()

with btn3:
    pause_btn = st.button("⏸️ Pause", use_container_width=True)
    if pause_btn:
        st.session_state['running'] = False

with btn4:
    # Save Data button - export CSV
    if len(st.session_state.get('time_data', [])) > 0:
        df = pd.DataFrame({
            'Time_s': st.session_state['time_data'],
            'LVP_mmHg': st.session_state['LVP_data'],
            'RVP_mmHg': st.session_state['RVP_data'],
            'LVV_ml': st.session_state['LVV_data'],
            'RVV_ml': st.session_state['RVV_data'],
            'Psa_mmHg': st.session_state['Psa_data'],
            'Ppa_mmHg': st.session_state['Ppa_data'],
            'Qaov_ml_s': st.session_state['Qaov_data'],
            'Qmv_ml_s': st.session_state['Qmv_data'],
            'Qpulv_ml_s': st.session_state['Qpulv_data'],
            'Qtv_ml_s': st.session_state['Qtv_data']
        })
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Save Data",
            data=csv,
            file_name=f"cardiovascular_data_{st.session_state['current_time']:.0f}s.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.button("💾 Save Data", use_container_width=True, disabled=True)

with btn5:
    # Download Params button - export JSON
    if 'params' in st.session_state or True:  # Always available
        params_dict = {
            'HR': HR,
            'TBV': TBV,
            'Rsa': Rsa,
            'Csa': Csa,
            'Emaxlv': Emaxlv,
            'Emaxrv': Emaxrv,
            'window_size': st.session_state.get('window_size', 10),
            'selected_signal': st.session_state.get('selected_signal', 'LVP')
        }
        params_json = json.dumps(params_dict, indent=2)
        st.download_button(
            label="📥 Download Params",
            data=params_json,
            file_name="cardiovascular_params.json",
            mime="application/json",
            use_container_width=True
        )

with btn6:
    # Save Plots button - info for now
    if st.button("📊 Save Plots", use_container_width=True):
        st.info("Right-click on plot → 'Download plot as a png' to save the current plot image")


# Initialize session state
if 'running' not in st.session_state:
    st.session_state['running'] = True
if 'stopped' not in st.session_state:
    st.session_state['stopped'] = False
if 'selected_signal' not in st.session_state:
    st.session_state['selected_signal'] = 'LVP'
if 'window_size' not in st.session_state:
    st.session_state['window_size'] = 10

# =======================
# MAIN LAYOUT: LEFT | CENTER | RIGHT
# =======================
col_left, col_center, col_right = st.columns([1, 3, 1])

# =======================
# LEFT SIDEBAR - PARAMETERS
# =======================
with col_left:
    st.markdown("### Parameters")
    st.markdown("---")
    
    st.markdown("**💪 LV Contractility**")
    Emaxlv = st.slider("", 0.5, 2.7, 2.0, 0.1, format="%.1f", key="emaxlv", label_visibility="collapsed")
    
    st.markdown("**💙 RV Contractility**")
    Emaxrv = st.slider("", 0.5, 2.0, 1.2, 0.1, format="%.1f", key="emaxrv", label_visibility="collapsed")
    
    st.markdown("**💗 Heart Rate**")
    HR = st.slider("", 40, 180, 75, 5, key="hr", label_visibility="collapsed")
    
    st.markdown("**🩸 Blood Volume**")
    TBV = st.slider("", 3000, 7000, 5300, 100, key="tbv", label_visibility="collapsed")
    
    st.markdown("**🌡️ Resistance**")
    Rsa = st.slider("", 0.05, 0.30, 0.20, 0.01, format="%.2f", key="rsa", label_visibility="collapsed")
    
    st.markdown("**💨 Compliance**")
    Csa = st.slider("", 0.1, 0.5, 0.28, 0.02, format="%.2f", key="csa", label_visibility="collapsed")

# =======================
# CENTER - REAL-TIME PLOT
# =======================
with col_center:
    # Initialize data buffer if not exists
    if 'time_data' not in st.session_state:
        st.session_state['time_data'] = np.array([])
        st.session_state['LVP_data'] = np.array([])
        st.session_state['RVP_data'] = np.array([])
        st.session_state['LVV_data'] = np.array([])
        st.session_state['RVV_data'] = np.array([])
        st.session_state['Psa_data'] = np.array([])
        st.session_state['Ppa_data'] = np.array([])
        st.session_state['Qaov_data'] = np.array([])
        st.session_state['Qmv_data'] = np.array([])
        st.session_state['Qpulv_data'] = np.array([])
        st.session_state['Qtv_data'] = np.array([])
        st.session_state['current_time'] = 0.0
        st.session_state['sim_running'] = False
    
    # Create empty container for plot
    plot_container = st.empty()
    
    # Run simulation in chunks if running
    if st.session_state.get('running', False):
        # Simulation parameters
        params = CardiovascularParameters()
        params.Rsa = Rsa
        params.Csa = Csa
        params.TBV = TBV
        
        # Run a small chunk (0.5 seconds)
        chunk_duration = 0.5
        dt = 0.001
        
        state = CardiovascularState()
        
        # Run chunk
        chunk_results = simulate_cardiovascular_system(
            params, state, HR=HR, duration=chunk_duration, dt=dt,
            Emaxlv=Emaxlv, Emaxrv=Emaxrv
        )
        
        # Append to buffers
        st.session_state['time_data'] = np.append(
            st.session_state['time_data'], 
            chunk_results['time'] + st.session_state['current_time']
        )
        st.session_state['LVP_data'] = np.append(st.session_state['LVP_data'], chunk_results['LVP'])
        st.session_state['RVP_data'] = np.append(st.session_state['RVP_data'], chunk_results['RVP'])
        st.session_state['LVV_data'] = np.append(st.session_state['LVV_data'], chunk_results['LVV'])
        st.session_state['RVV_data'] = np.append(st.session_state['RVV_data'], chunk_results['RVV'])
        st.session_state['Psa_data'] = np.append(st.session_state['Psa_data'], chunk_results['Psa'])
        st.session_state['Ppa_data'] = np.append(st.session_state['Ppa_data'], chunk_results['Ppa'])
        st.session_state['Qaov_data'] = np.append(st.session_state['Qaov_data'], chunk_results['Qaov'])
        st.session_state['Qmv_data'] = np.append(st.session_state['Qmv_data'], chunk_results['Qmv'])
        st.session_state['Qpulv_data'] = np.append(st.session_state['Qpulv_data'], chunk_results['Qpulv'])
        st.session_state['Qtv_data'] = np.append(st.session_state['Qtv_data'], chunk_results['Qtv'])
        
        st.session_state['current_time'] += chunk_duration
        
        # Auto-rerun to continue simulation
        time.sleep(0.1)  # Small delay
        st.rerun()
    
    # Get data to display (rolling window)
    if len(st.session_state['time_data']) > 0:
        t_all = st.session_state['time_data']
        window_size = st.session_state['window_size']
        
        # Get last N seconds
        window_start = max(0, t_all[-1] - window_size)
        window_idx = t_all >= window_start
        
        t_display = t_all[window_idx]
        
        selected = st.session_state['selected_signal']
        
        # Create plot
        fig = go.Figure()
        
        if selected == 'LVP':
            fig.add_trace(go.Scatter(
                x=t_display, 
                y=st.session_state['LVP_data'][window_idx],
                mode='lines',
                line=dict(color='#0066cc', width=2),
                name='LV Pressure'
            ))
            fig.update_layout(yaxis_title="Pressure (mmHg)", title="Left Ventricular Pressure")
            
        elif selected == 'RVP':
            fig.add_trace(go.Scatter(
                x=t_display, 
                y=st.session_state['RVP_data'][window_idx],
                mode='lines',
                line=dict(color='#0066cc', width=2),
                name='RV Pressure'
            ))
            fig.update_layout(yaxis_title="Pressure (mmHg)", title="Right Ventricular Pressure")
            
        elif selected == 'LVV':
            fig.add_trace(go.Scatter(
                x=t_display, 
                y=st.session_state['LVV_data'][window_idx],
                mode='lines',
                line=dict(color='#0066cc', width=2),
                name='LV Volume'
            ))
            fig.update_layout(yaxis_title="Volume (ml)", title="Left Ventricular Volume")
            
        elif selected == 'RVV':
            fig.add_trace(go.Scatter(
                x=t_display, 
                y=st.session_state['RVV_data'][window_idx],
                mode='lines',
                line=dict(color='#0066cc', width=2),
                name='RV Volume'
            ))
            fig.update_layout(yaxis_title="Volume (ml)", title="Right Ventricular Volume")
            
        elif selected == 'Flows':
            fig.add_trace(go.Scatter(x=t_display, y=st.session_state['Qaov_data'][window_idx], 
                                    line=dict(color='red', width=2), name="Aortic"))
            fig.add_trace(go.Scatter(x=t_display, y=st.session_state['Qmv_data'][window_idx], 
                                    line=dict(color='blue', width=2), name="Mitral"))
            fig.add_trace(go.Scatter(x=t_display, y=st.session_state['Qpulv_data'][window_idx], 
                                    line=dict(color='green', width=2), name="Pulmonary"))
            fig.add_trace(go.Scatter(x=t_display, y=st.session_state['Qtv_data'][window_idx], 
                                    line=dict(color='orange', width=2), name="Tricuspid"))
            fig.update_layout(yaxis_title="Flow (ml/s)", title="Valve Flows")
            
        elif selected == 'PV':
            # For PV loops, use last cardiac cycle
            cycle_duration = 60.0 / HR
            last_cycle_idx = t_all >= (t_all[-1] - cycle_duration)
            
            fig = make_subplots(rows=1, cols=2, subplot_titles=("LV Loop", "RV Loop"))
            
            fig.add_trace(go.Scatter(
                x=st.session_state['LVV_data'][last_cycle_idx], 
                y=st.session_state['LVP_data'][last_cycle_idx],
                mode='lines',
                line=dict(color='#0066cc', width=3),
                name='LV'
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=st.session_state['RVV_data'][last_cycle_idx], 
                y=st.session_state['RVP_data'][last_cycle_idx],
                mode='lines',
                line=dict(color='#0066cc', width=3),
                name='RV'
            ), row=1, col=2)
            
            fig.update_xaxes(title_text="Volume (ml)", row=1, col=1)
            fig.update_xaxes(title_text="Volume (ml)", row=1, col=2)
            fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=1)
            fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=2)
            
        elif selected == 'Arterial':
            fig.add_trace(go.Scatter(x=t_display, y=st.session_state['Psa_data'][window_idx], 
                                    line=dict(color='red', width=2), name="Aortic"))
            fig.add_trace(go.Scatter(x=t_display, y=st.session_state['Ppa_data'][window_idx], 
                                    line=dict(color='blue', width=2), name="Pulmonary"))
            fig.update_layout(yaxis_title="Pressure (mmHg)", title="Arterial Pressures")
        
        # Common layout - GRID BACKGROUND
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black', size=12),
            height=450,
            xaxis=dict(
                title="Time (s)",
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                dtick=0.5,
                zeroline=True
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                zeroline=True
            ),
            margin=dict(l=60, r=20, t=40, b=40)
        )
        
        plot_container.plotly_chart(fig, use_container_width=True, key="main_plot")
    else:
        plot_container.info("Press Play to start simulation")
    
    # Window size selector
    st.markdown("---")
    st.markdown("**Display Window Length**")
    
    if st.session_state['selected_signal'] == 'PV':
        st.info("⚠️ Window selector disabled for PV Loops")
    else:
        w1, w2, w3 = st.columns(3)
        with w1:
            if st.button("5s", use_container_width=True, type="primary" if st.session_state['window_size'] == 5 else "secondary"):
                st.session_state['window_size'] = 5
                st.rerun()
        with w2:
            if st.button("10s", use_container_width=True, type="primary" if st.session_state['window_size'] == 10 else "secondary"):
                st.session_state['window_size'] = 10
                st.rerun()
        with w3:
            if st.button("30s", use_container_width=True, type="primary" if st.session_state['window_size'] == 30 else "secondary"):
                st.session_state['window_size'] = 30
                st.rerun()
    
    # METRICS BELOW TIME SELECTOR
    if len(st.session_state['time_data']) > 0:
        st.markdown("---")
        
        systolic_BP = np.max(st.session_state['Psa_data'])
        diastolic_BP = np.min(st.session_state['Psa_data'])
        mean_BP = np.mean(st.session_state['Psa_data'])
        
        # Use last 10 seconds for CO calculation
        last_10s_idx = st.session_state['time_data'] >= (st.session_state['time_data'][-1] - 10.0)
        if np.any(last_10s_idx):
            mean_Qaov = np.mean(st.session_state['Qaov_data'][last_10s_idx])
            CO = mean_Qaov * 60 / 1000
            SV = (60 * CO / HR) * 1000 if HR > 0 else 0
            EF = (SV / np.max(st.session_state['LVV_data'])) * 100 if np.max(st.session_state['LVV_data']) > 0 else 0
        else:
            CO = 0
            SV = 0
            EF = 0
        
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.metric("BP", f"{systolic_BP:.0f}/{diastolic_BP:.0f}")
        with m2:
            st.metric("MAP", f"{mean_BP:.0f}")
        with m3:
            st.metric("CO", f"{CO:.2f}")
        with m4:
            st.metric("SV", f"{SV:.0f}")
        with m5:
            st.metric("EF", f"{EF:.0f}%")

# =======================
# RIGHT SIDEBAR - PLOT CHOOSER
# =======================
with col_right:
    st.markdown("### Plot Chooser")
    st.markdown("---")
    
    if st.button("💓 LVP", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'LVP' else "secondary"):
        st.session_state['selected_signal'] = 'LVP'
        st.rerun()
    
    if st.button("💙 RVP", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'RVP' else "secondary"):
        st.session_state['selected_signal'] = 'RVP'
        st.rerun()
    
    if st.button("📦 LVV", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'LVV' else "secondary"):
        st.session_state['selected_signal'] = 'LVV'
        st.rerun()
    
    if st.button("📦 RVV", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'RVV' else "secondary"):
        st.session_state['selected_signal'] = 'RVV'
        st.rerun()
    
    if st.button("🌊 Flows", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'Flows' else "secondary"):
        st.session_state['selected_signal'] = 'Flows'
        st.rerun()
    
    if st.button("🔄 PV Loops", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'PV' else "secondary"):
        st.session_state['selected_signal'] = 'PV'
        st.rerun()
    
    if st.button("🩸 Arterial", use_container_width=True, type="primary" if st.session_state['selected_signal'] == 'Arterial' else "secondary"):
        st.session_state['selected_signal'] = 'Arterial'
        st.rerun()

