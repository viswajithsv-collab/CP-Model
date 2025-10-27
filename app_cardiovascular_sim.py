"""
Cardiovascular Simulator - Custom Layout
LEFT: Parameters | CENTER: Plot | RIGHT: Signal Chooser
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
    
    /* Make sliders look better */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #0099ff, #00ff88);
    }
    
    h1, h2, h3, h4 {
        color: white;
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

with btn3:
    pause_btn = st.button("⏸️ Pause", use_container_width=True)
    if pause_btn:
        st.session_state['running'] = False

with btn4:
    st.button("💾 Save Data", use_container_width=True)

with btn5:
    st.button("📥 Download Params", use_container_width=True)

with btn6:
    st.button("📊 Save Plots", use_container_width=True)

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
# CENTER - MAIN PLOT
# =======================
with col_center:
    # Run simulation
    if st.session_state.get('running', True) and not st.session_state.get('stopped', False):
        params = CardiovascularParameters()
        params.Rsa = Rsa
        params.Csa = Csa
        params.TBV = TBV

        state = CardiovascularState()

        duration = 30.0
        dt = 0.001

        with st.spinner('Computing...'):
            results = simulate_cardiovascular_system(
                params, state, HR=HR, duration=duration, dt=dt,
                Emaxlv=Emaxlv, Emaxrv=Emaxrv
            )
        
        st.session_state['results'] = results
        st.session_state['params'] = {
            'HR': HR, 'TBV': TBV, 'Rsa': Rsa, 'Csa': Csa,
            'Emaxlv': Emaxlv, 'Emaxrv': Emaxrv
        }
        
        # Calculate metrics
        systolic_BP = np.max(results['Psa'])
        diastolic_BP = np.min(results['Psa'])
        mean_BP = np.mean(results['Psa'])
        
        # Get time window
        t = results['time']
        window_size = st.session_state['window_size']
        window_start = max(0, t[-1] - window_size)
        scroll_idx = t >= window_start
        t_scroll = t[scroll_idx]
        
        selected = st.session_state['selected_signal']
        
        # Create plot based on selection
        fig = go.Figure()
        
        if selected == 'LVP':
            fig.add_trace(go.Scatter(
                x=t_scroll, y=results['LVP'][scroll_idx],
                mode='lines',
                line=dict(color='#0066cc', width=2),
                name='LV Pressure'
            ))
            fig.update_layout(yaxis_title="Pressure (mmHg)", title="Left Ventricular Pressure")
            
        elif selected == 'RVP':
            fig.add_trace(go.Scatter(
                x=t_scroll, y=results['RVP'][scroll_idx],
                mode='lines',
                line=dict(color='#0066cc', width=2),
                name='RV Pressure'
            ))
            fig.update_layout(yaxis_title="Pressure (mmHg)", title="Right Ventricular Pressure")
            
        elif selected == 'LVV':
            fig.add_trace(go.Scatter(
                x=t_scroll, y=results['LVV'][scroll_idx],
                mode='lines',
                line=dict(color='#0066cc', width=2),
                name='LV Volume'
            ))
            fig.update_layout(yaxis_title="Volume (ml)", title="Left Ventricular Volume")
            
        elif selected == 'RVV':
            fig.add_trace(go.Scatter(
                x=t_scroll, y=results['RVV'][scroll_idx],
                mode='lines',
                line=dict(color='#0066cc', width=2),
                name='RV Volume'
            ))
            fig.update_layout(yaxis_title="Volume (ml)", title="Right Ventricular Volume")
            
        elif selected == 'Flows':
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Qaov'][scroll_idx], 
                                    line=dict(color='red', width=2), name="Aortic"))
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Qmv'][scroll_idx], 
                                    line=dict(color='blue', width=2), name="Mitral"))
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Qpulv'][scroll_idx], 
                                    line=dict(color='green', width=2), name="Pulmonary"))
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Qtv'][scroll_idx], 
                                    line=dict(color='orange', width=2), name="Tricuspid"))
            fig.update_layout(yaxis_title="Flow (ml/s)", title="Valve Flows")
            
        elif selected == 'PV':
            cycle_duration = 60.0 / HR
            last_cycle_idx = results['time'] >= (results['time'][-1] - cycle_duration)
            
            fig = make_subplots(rows=1, cols=2, subplot_titles=("LV Loop", "RV Loop"))
            
            fig.add_trace(go.Scatter(
                x=results['LVV'][last_cycle_idx], 
                y=results['LVP'][last_cycle_idx],
                mode='lines',
                line=dict(color='#0066cc', width=3),
                name='LV'
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=results['RVV'][last_cycle_idx], 
                y=results['RVP'][last_cycle_idx],
                mode='lines',
                line=dict(color='#0066cc', width=3),
                name='RV'
            ), row=1, col=2)
            
            fig.update_xaxes(title_text="Volume (ml)", row=1, col=1)
            fig.update_xaxes(title_text="Volume (ml)", row=1, col=2)
            fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=1)
            fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=2)
            
        elif selected == 'Arterial':
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Psa'][scroll_idx], 
                                    line=dict(color='red', width=2), name="Aortic"))
            fig.add_trace(go.Scatter(x=t_scroll, y=results['Ppa'][scroll_idx], 
                                    line=dict(color='blue', width=2), name="Pulmonary"))
            fig.update_layout(yaxis_title="Pressure (mmHg)", title="Arterial Pressures")
        
        # Common layout - GRID BACKGROUND LIKE YOUR DESIGN!
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
                dtick=0.5,  # Grid every 0.5 seconds
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
        
        st.plotly_chart(fig, use_container_width=True, key="main_plot")
        
        # Window size selector - DISABLE for PV Loops
        st.markdown("---")
        st.markdown("**Display Window Length**")
        
        if selected == 'PV':
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
    
    st.markdown("---")
    
    # Metrics display
    if 'results' in st.session_state:
        results = st.session_state['results']
        systolic_BP = np.max(results['Psa'])
        diastolic_BP = np.min(results['Psa'])
        mean_BP = np.mean(results['Psa'])
        
        last_10s_idx = results['time'] >= (results['time'][-1] - 10.0)
        mean_Qaov = np.mean(results['Qaov'][last_10s_idx])
        CO = mean_Qaov * 60 / 1000
        SV = (60 * CO / HR) * 1000 if HR > 0 else 0
        EF = (SV / np.max(results['LVV'])) * 100 if np.max(results['LVV']) > 0 else 0
        
        st.markdown("### Metrics")
        st.metric("BP", f"{systolic_BP:.0f}/{diastolic_BP:.0f} mmHg")
        st.metric("MAP", f"{mean_BP:.0f} mmHg")
        st.metric("CO", f"{CO:.2f} L/min")
        st.metric("SV", f"{SV:.0f} ml")
        st.metric("EF", f"{EF:.0f}%")
