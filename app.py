"""
Interactive Cardiovascular Model Web App
Based on Ursino 1998 simplified model
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
    page_title="Cardiovascular Model Simulator",
    page_icon="❤️",
    layout="wide"
)

# Title and description
st.title("❤️ Interactive Cardiovascular Model")
st.markdown("""
### Simplified 2-Branch Ursino Model (1998)
This interactive simulator demonstrates cardiovascular hemodynamics using a lumped-parameter model 
with **two systemic branches** (lower body and upper body peripheral circulation).

**Educational Tool** - Adjust parameters to see how they affect pressures, volumes, and flows!
""")

# Sidebar for parameters
st.sidebar.header("⚙️ Model Parameters")

# Heart rate
HR = st.sidebar.slider(
    "Heart Rate (bpm)", 
    min_value=40, 
    max_value=180, 
    value=75, 
    step=5,
    help="Normal resting HR: 60-100 bpm"
)

# Simulation settings
st.sidebar.subheader("Simulation Settings")
duration = st.sidebar.slider(
    "Duration (seconds)", 
    min_value=2.0, 
    max_value=20.0, 
    value=8.0, 
    step=1.0
)

# Advanced parameters
with st.sidebar.expander("🔧 Advanced Parameters"):
    st.markdown("**Systemic Resistances (mmHg·s/ml)**")
    Rsa = st.number_input("Systemic Arterial (Rsa)", value=0.06, format="%.3f", step=0.01)
    Rlbp = st.number_input("Lower Body Peripheral (Rlbp)", value=1.307, format="%.3f", step=0.1)
    Rubp = st.number_input("Upper Body Peripheral (Rubp)", value=1.407, format="%.3f", step=0.1)
    
    st.markdown("**Systemic Compliances (ml/mmHg)**")
    Csa = st.number_input("Systemic Arterial (Csa)", value=0.28, format="%.2f", step=0.05)
    Clbp = st.number_input("Lower Body Peripheral (Clbp)", value=2.05, format="%.2f", step=0.1)
    
    st.markdown("**Ventricular Elastances (mmHg/ml)**")
    Emaxlv = st.number_input("LV Max Elastance", value=2.7, format="%.2f", step=0.1)
    Emaxrv = st.number_input("RV Max Elastance", value=1.6, format="%.2f", step=0.1)

# Initialize parameters
params = CardiovascularParameters()
params.Rsa = Rsa
params.Rlbp = Rlbp
params.Rubp = Rubp
params.Csa = Csa
params.Clbp = Clbp

# Initial state
state = CardiovascularState()

# Run simulation button
if st.sidebar.button("▶️ Run Simulation", type="primary"):
    with st.spinner("Running cardiovascular simulation..."):
        # Run simulation
        results = simulate_cardiovascular_system(
            params, 
            state, 
            HR=HR, 
            duration=duration,
            dt=0.001  # Use larger dt for web app (faster)
        )
        
        # Store in session state
        st.session_state['results'] = results
        st.session_state['HR'] = HR

# Display results if available
if 'results' in st.session_state:
    results = st.session_state['results']
    
    # Display key metrics
    st.header("📊 Hemodynamic Metrics")
    
    # Calculate metrics from last cardiac cycle
    t = results['time']
    cardiac_period = 60 / st.session_state['HR']
    last_cycle_idx = t > (t[-1] - cardiac_period)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        systolic_BP = np.max(results['Psa'][last_cycle_idx])
        diastolic_BP = np.min(results['Psa'][last_cycle_idx])
        mean_BP = np.mean(results['Psa'][last_cycle_idx])
        st.metric("Systolic BP", f"{systolic_BP:.1f} mmHg")
        st.metric("Diastolic BP", f"{diastolic_BP:.1f} mmHg")
        st.metric("Mean BP", f"{mean_BP:.1f} mmHg")
    
    with col2:
        max_LVV = np.max(results['LVV'][last_cycle_idx])
        min_LVV = np.min(results['LVV'][last_cycle_idx])
        SV = max_LVV - min_LVV
        CO = (SV * st.session_state['HR']) / 1000  # L/min
        st.metric("Stroke Volume", f"{SV:.1f} ml")
        st.metric("Cardiac Output", f"{CO:.2f} L/min")
        st.metric("Ejection Fraction", f"{(SV/max_LVV)*100:.1f}%")
    
    with col3:
        max_LVP = np.max(results['LVP'][last_cycle_idx])
        mean_LAP = np.mean(results['LAP'][last_cycle_idx])
        st.metric("Max LV Pressure", f"{max_LVP:.1f} mmHg")
        st.metric("Mean LA Pressure", f"{mean_LAP:.1f} mmHg")
    
    with col4:
        max_RVP = np.max(results['RVP'][last_cycle_idx])
        mean_RAP = np.mean(results['RAP'][last_cycle_idx])
        mean_PAP = np.mean(results['Ppa'][last_cycle_idx])
        st.metric("Max RV Pressure", f"{max_RVP:.1f} mmHg")
        st.metric("Mean RA Pressure", f"{mean_RAP:.1f} mmHg")
        st.metric("Mean PA Pressure", f"{mean_PAP:.1f} mmHg")
    
    # Plotting
    st.header("📈 Hemodynamic Waveforms")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "🫀 Ventricular", 
        "🩸 Arterial Pressures", 
        "💉 Flows", 
        "🔄 PV Loops"
    ])
    
    with tab1:
        # Ventricular pressures and volumes
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Left Ventricular Pressure", "Right Ventricular Pressure",
                          "Left Ventricular Volume", "Right Ventricular Volume"),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # LV Pressure
        fig.add_trace(
            go.Scatter(x=t, y=results['LVP'], name="LVP", 
                      line=dict(color='red', width=2)),
            row=1, col=1
        )
        
        # RV Pressure
        fig.add_trace(
            go.Scatter(x=t, y=results['RVP'], name="RVP", 
                      line=dict(color='blue', width=2)),
            row=1, col=2
        )
        
        # LV Volume
        fig.add_trace(
            go.Scatter(x=t, y=results['LVV'], name="LVV", 
                      line=dict(color='darkred', width=2)),
            row=2, col=1
        )
        
        # RV Volume
        fig.add_trace(
            go.Scatter(x=t, y=results['RVV'], name="RVV", 
                      line=dict(color='darkblue', width=2)),
            row=2, col=2
        )
        
        fig.update_xaxes(title_text="Time (s)", row=2, col=1)
        fig.update_xaxes(title_text="Time (s)", row=2, col=2)
        fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=1)
        fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=2)
        fig.update_yaxes(title_text="Volume (ml)", row=2, col=1)
        fig.update_yaxes(title_text="Volume (ml)", row=2, col=2)
        
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Arterial pressures
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Systemic Arterial Pressure", "Pulmonary Arterial Pressure"),
            vertical_spacing=0.15
        )
        
        # Systemic
        fig.add_trace(
            go.Scatter(x=t, y=results['Psa'], name="Systemic Arterial", 
                      line=dict(color='crimson', width=2)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=t, y=results['Plbp'], name="Lower Body Peripheral", 
                      line=dict(color='orange', width=2)),
            row=1, col=1
        )
        
        # Pulmonary
        fig.add_trace(
            go.Scatter(x=t, y=results['Ppa'], name="Pulmonary Arterial", 
                      line=dict(color='steelblue', width=2)),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=t, y=results['Ppp'], name="Pulmonary Peripheral", 
                      line=dict(color='lightblue', width=2)),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Time (s)", row=2, col=1)
        fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=1)
        fig.update_yaxes(title_text="Pressure (mmHg)", row=2, col=1)
        
        fig.update_layout(height=600, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Valve flows
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=t, y=results['Qaov'], name="Aortic Valve",
                                line=dict(color='red', width=2)))
        fig.add_trace(go.Scatter(x=t, y=results['Qmv'], name="Mitral Valve",
                                line=dict(color='pink', width=2)))
        fig.add_trace(go.Scatter(x=t, y=results['Qpulv'], name="Pulmonary Valve",
                                line=dict(color='blue', width=2)))
        fig.add_trace(go.Scatter(x=t, y=results['Qtv'], name="Tricuspid Valve",
                                line=dict(color='lightblue', width=2)))
        
        fig.update_layout(
            title="Valve Flow Rates",
            xaxis_title="Time (s)",
            yaxis_title="Flow (ml/s)",
            height=500,
            showlegend=True,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # PV Loops
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Left Ventricle PV Loop", "Right Ventricle PV Loop")
        )
        
        # LV PV Loop
        fig.add_trace(
            go.Scatter(x=results['LVV'][last_cycle_idx], 
                      y=results['LVP'][last_cycle_idx],
                      mode='lines', name="LV",
                      line=dict(color='red', width=3)),
            row=1, col=1
        )
        
        # RV PV Loop
        fig.add_trace(
            go.Scatter(x=results['RVV'][last_cycle_idx], 
                      y=results['RVP'][last_cycle_idx],
                      mode='lines', name="RV",
                      line=dict(color='blue', width=3)),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Volume (ml)", row=1, col=1)
        fig.update_xaxes(title_text="Volume (ml)", row=1, col=2)
        fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=1)
        fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=2)
        
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Educational notes
    st.header("📚 Educational Notes")
    
    with st.expander("🔍 Understanding the Model"):
        st.markdown("""
        ### Model Structure
        This is a **lumped-parameter model** where the cardiovascular system is divided into compartments:
        
        **Systemic Circulation:**
        - Systemic Artery (Aorta)
        - Lower Body Peripheral (originally Splanchnic)
        - Upper Body Peripheral (originally Extrasplanchnic)
        - Lower Body Venous
        - Upper Body Venous
        
        **Pulmonary Circulation:**
        - Pulmonary Artery
        - Pulmonary Peripheral
        - Pulmonary Veins
        
        **Heart:**
        - Left Atrium & Ventricle
        - Right Atrium & Ventricle
        - Time-varying elastance model
        
        ### Key Concepts
        - **Compliance (C)**: Ability to expand with pressure (vessel elasticity)
        - **Resistance (R)**: Opposition to flow
        - **Elastance (E)**: Ventricular stiffness (changes during cardiac cycle)
        - **Frank-Starling**: Higher filling → stronger contraction
        """)
    
    with st.expander("🎓 Clinical Insights"):
        st.markdown("""
        ### What happens when you change parameters?
        
        **↑ Heart Rate:**
        - ↑ Cardiac output (up to a point)
        - ↓ Diastolic filling time
        - May ↓ stroke volume if too fast
        
        **↑ Systemic Resistance (Rsa, Rlbp, Rubp):**
        - ↑ Afterload on left ventricle
        - ↑ Blood pressure
        - ↓ Cardiac output
        - Simulates hypertension
        
        **↓ Systemic Compliance (Csa):**
        - ↑ Pulse pressure (wider systolic-diastolic gap)
        - Simulates arterial stiffening (aging, atherosclerosis)
        
        **↑ Ventricular Elastance (Emaxlv):**
        - ↑ Contractility
        - ↑ Stroke volume
        - Simulates inotropic effect (exercise, drugs)
        """)

else:
    # Instructions before first run
    st.info("👈 Adjust parameters in the sidebar and click **Run Simulation** to begin!")
    
    st.markdown("""
    ### Quick Start Guide
    1. **Set Heart Rate** - Normal is 60-100 bpm
    2. **Choose Duration** - 8 seconds shows ~10 cardiac cycles at HR=75
    3. **Adjust Advanced Parameters** (optional) - Change resistances, compliances, or contractility
    4. **Click Run** - Simulation takes a few seconds
    5. **Explore Results** - View pressure, volume, flow waveforms and PV loops
    
    ### Learning Objectives
    - Understand cardiovascular hemodynamics
    - See how resistances affect blood pressure
    - Visualize ventricular function (PV loops)
    - Explore the cardiac cycle timing
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Based on Ursino 1998 simplified cardiovascular model | For educational purposes</p>
</div>
""", unsafe_allow_html=True)
