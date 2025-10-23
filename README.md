# Interactive Cardiovascular Model - Teaching Version

## Overview
This is an interactive web application for teaching cardiovascular hemodynamics, based on the simplified Ursino 1998 model with 2 systemic branches (lower body and upper body peripheral circulation).

**Converted from MATLAB to Python** with an interactive Streamlit interface for students to explore cardiovascular physiology!

## Features
- ❤️ Real-time cardiovascular simulation
- 📊 Interactive parameter adjustment
- 📈 Multiple visualization tabs (pressures, volumes, flows, PV loops)
- 🎓 Educational notes and clinical insights
- 📱 Mobile-friendly responsive design

## Model Structure
### Systemic Circulation (2 branches)
- Systemic Artery (Aorta)
- **Lower Body Peripheral** (originally Splanchnic)
- **Upper Body Peripheral** (originally Extrasplanchnic)  
- Lower Body Venous
- Upper Body Venous

### Pulmonary Circulation
- Pulmonary Artery
- Pulmonary Peripheral
- Pulmonary Veins

### Heart
- Left Atrium & Ventricle (time-varying elastance)
- Right Atrium & Ventricle (time-varying elastance)
- Four heart valves (mitral, aortic, tricuspid, pulmonary)

## Quick Start

### Local Installation
```bash
# Clone the repository
git clone https://github.com/viswajithsv-collab/CP-Model.git
cd CP-Model/Teaching/Python

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Files
- `app.py` - Streamlit web interface
- `cardiovascular_model.py` - Core simulation functions
- `requirements.txt` - Python dependencies

## Usage Guide

### 1. Adjust Parameters
Use the sidebar to modify:
- **Heart Rate** (40-180 bpm)
- **Simulation Duration** (2-20 seconds)
- **Advanced Parameters** (resistances, compliances, elastances)

### 2. Run Simulation
Click the "▶️ Run Simulation" button

### 3. Explore Results
Navigate through tabs:
- **Ventricular** - LV/RV pressures and volumes
- **Arterial Pressures** - Systemic and pulmonary
- **Flows** - Valve flow rates
- **PV Loops** - Pressure-volume relationships

### 4. Learn!
Expand the educational notes to understand:
- How parameters affect hemodynamics
- Clinical insights (hypertension, heart failure, etc.)
- Cardiovascular physiology concepts

## Deployment to Streamlit Cloud (FREE!)

### Option 1: Direct from GitHub (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository: `viswajithsv-collab/CP-Model`
6. Set the main file path: `Teaching/Python/app.py`
7. Click "Deploy"!

Your app will be live at: `https://your-username-cp-model.streamlit.app`

### Option 2: Deploy from Local
```bash
# Make sure you have Streamlit CLI
pip install streamlit

# Deploy
streamlit deploy app.py
```

## Educational Use Cases

### For Students
- Explore how heart rate affects cardiac output
- Understand the relationship between resistance and blood pressure
- Visualize the cardiac cycle timing
- Learn pressure-volume loop interpretation

### For Instructors
- Demonstrate pathophysiology (hypertension, heart failure)
- Show effects of pharmacological interventions
- Compare normal vs. abnormal hemodynamics
- Assign parameter exploration exercises

## Parameter Guide

### Key Parameters to Explore

**Cardiovascular Function:**
- `HR` (Heart Rate): 60-100 bpm normal, >100 tachycardia, <60 bradycardia
- `Emaxlv` (LV Contractility): ↑ = stronger contraction (exercise, inotropes)

**Systemic Circulation:**
- `Rsa` (Arterial Resistance): ↑ = hypertension
- `Csa` (Arterial Compliance): ↓ = stiff vessels (aging, atherosclerosis)
- `Rlbp/Rubp` (Peripheral Resistance): ↑ = increased afterload

**Clinical Scenarios to Simulate:**
1. **Exercise**: ↑ HR, ↑ Emaxlv, ↓ peripheral resistance
2. **Hypertension**: ↑ Rsa, ↑ Rlbp, ↑ Rubp
3. **Heart Failure**: ↓ Emaxlv
4. **Arterial Stiffness**: ↓ Csa (aging)

## Technical Details

### Numerical Method
- Explicit Euler integration
- Time step: 0.001 s (1 ms)
- Double-Hill activation function for ventricular contraction

### Model Equations
Based on:
- Time-varying elastance for ventricles
- RC circuits for vascular compartments
- Windkessel compliance
- Diode valves (unidirectional flow)

### Performance
- Simulation: ~2-5 seconds for 16 seconds of cardiac cycles
- Real-time parameter updates
- Smooth interactive plotting with Plotly

## Differences from Research Version

This **Teaching Version** is simplified:
- ✅ 2 systemic branches (lower/upper body)
- ✅ Simple RC models
- ✅ No baroreflex
- ✅ Fixed elastances

The **Research Version** (in `/CP Model` folder) includes:
- ❌ 6+ systemic branches
- ❌ Split ascending/descending aorta
- ❌ Coronary circulation
- ❌ Baroreflex control
- ❌ LVAD support modeling

## References
- Ursino, M. (1998). "Interaction between carotid baroregulation and the pulsating heart: a mathematical model." *American Journal of Physiology-Heart and Circulatory Physiology*, 275(5), H1733-H1747.

## Contributing
This is an educational tool! Contributions welcome:
- Bug fixes
- UI improvements
- Additional visualizations
- Educational content

## License
This code is provided for educational purposes.

## Contact
For questions about the model or deployment, open an issue on GitHub!

---
**Made with ❤️ for cardiovascular education**
