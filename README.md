# VAD Simulator - Single Plot Interface 🫀

## 🎉 What's New!

### ✨ Major Improvements

**BEFORE:** You had 6 separate plots requiring lots of scrolling 😓  
**AFTER:** ONE sleek plot with signal selector buttons! 🚀

### 🔥 Key Features

1. **Signal Selector Buttons**
   - 💓 LVP (Left Ventricular Pressure)
   - 💙 RVP (Right Ventricular Pressure)
   - 📦 LVV (Left Ventricular Volume)
   - 📦 RVV (Right Ventricular Volume)
   - 🌊 Flows (All 4 valves)
   - 🔄 PV Loops (Pressure-Volume loops)
   - 🩸 Arterial (Aortic & Pulmonary pressures)

2. **Scrolling Display**
   - Adjustable window size (5-30 seconds)
   - Shows most recent data like a real ECG monitor
   - Smooth, continuous updates

3. **Better Layout**
   - **Left column:** All controls (VAD, Heart Disease, Vitals)
   - **Right column:** ONE big beautiful plot
   - **Bottom:** Metrics in a clean single row
   - Everything visible at once - NO SCROLLING! 🎯

4. **Cleaner Interface**
   - Larger plot area for better visibility
   - More professional medical device look
   - Intuitive signal switching

## 📂 Files Included

- `app_vad_single_plot.py` - New single-plot version
- `cardiovascular_model.py` - Cardiovascular simulation engine
- `requirements.txt` - Python dependencies

## 🚀 How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_vad_single_plot.py
```

The app will open in your browser at `http://localhost:8501`

## 🎮 How to Use

1. **Control Simulation**
   - Press ▶️ PLAY to start
   - Press ⏸️ PAUSE to pause
   - Press ⏹️ STOP to stop and reset parameters
   - Press 🔄 RESET to clear everything

2. **Adjust Parameters** (Left Column)
   - **VAD Settings:** Turn pump on/off, adjust speed, pulsation
   - **Heart Disease:** Modify LV/RV contractility, add valve problems
   - **Vitals:** Change heart rate, blood volume, resistance
   - **Display:** Adjust scrolling window size

3. **View Signals** (Right Column)
   - Click any signal button to switch views
   - Watch the real-time scrolling display
   - PV Loops show the last cardiac cycle

4. **Check Metrics** (Bottom)
   - Blood Pressure, MAP, Cardiac Output
   - Stroke Volume, Ejection Fraction, Mean PAP

5. **Export Data**
   - 📊 CSV: All raw data
   - ⚙️ Params: All parameter settings
   - 📄 Report: Summary with metrics

## 💪 What Works Great

✅ Cardiovascular model (validated hemodynamics)  
✅ LV/RV contractility sliders affect output  
✅ 30-second simulation window  
✅ Play/Pause/Stop/Reset controls  
✅ Data export (CSV, JSON, Report)  
✅ **NEW:** Single plot with signal switching  
✅ **NEW:** Scrolling display window  
✅ **NEW:** Compact, no-scroll layout  

## 🎨 Design Philosophy

The new interface is modeled after real clinical monitors:
- **One screen, all controls visible**
- **Large display area for the signal**
- **Quick signal switching** with buttons
- **Scrolling window** shows recent data (like ECG)
- **Professional medical aesthetic**

## 📊 Signal Descriptions

| Signal | What It Shows | Color |
|--------|--------------|-------|
| LVP | Left ventricular pressure during cardiac cycle | Pink/Red |
| RVP | Right ventricular pressure during cardiac cycle | Cyan |
| LVV | Left ventricular volume changes | Pink |
| RVV | Right ventricular volume changes | Light Cyan |
| Flows | All 4 valve flows (Aortic, Mitral, Pulmonary, Tricuspid) | Multi-color |
| PV Loops | Pressure-Volume relationships (LV & RV) | Pink & Cyan |
| Arterial | Aortic & Pulmonary artery pressures | Orange & Cyan |

## 🔬 Medical Accuracy

The cardiovascular model includes:
- Time-varying elastance (realistic heart contraction)
- Valve dynamics (diodes with realistic opening/closing)
- Windkessel circulation models
- Physiologically accurate parameters
- Validated hemodynamics (BP ~120/80, CO ~5 L/min)

## 💡 Tips

- **Adjust window size** to see more/less cardiac cycles
- **Try different signals** to understand heart physiology
- **Reduce LV contractility** to simulate heart failure
- **Turn on the VAD pump** to see mechanical support effects
- **Export data** to analyze in Excel or Python

## 🆚 Comparison: Old vs New

### Old Version (app_vad_modern.py)
- ❌ 6 separate plots
- ❌ Lots of scrolling needed
- ❌ Plots in 3x2 grid
- ❌ Smaller individual plots
- ✅ All signals visible simultaneously

### New Version (app_vad_single_plot.py)
- ✅ 1 large plot
- ✅ No scrolling needed
- ✅ Signal selector buttons
- ✅ Larger, clearer display
- ✅ Scrolling time window
- ✅ More professional look

## 🎯 Use Cases

This simulator is perfect for:
- **Education:** Learn cardiovascular physiology
- **Medical Training:** Understand hemodynamics
- **VAD Research:** Test device settings
- **Clinical Scenarios:** Simulate heart failure & support
- **Algorithm Development:** Generate realistic cardiac data

## 🛠️ Customization

Want to modify it? Key areas:
- **Line 285-410:** Signal plotting logic
- **Line 137-176:** Control sliders
- **Line 517-533:** Metrics calculations
- **Line 28-86:** CSS styling

## 📈 Future Enhancements

Potential additions:
- Real-time streaming mode
- Multiple signal overlay
- Arrhythmia simulation
- Drug effect models
- Pediatric/adult presets
- Save/load scenarios

## 📝 Notes

- The simulation runs for 30 seconds on each update
- Smaller time steps (dt=0.001) ensure stability
- Results are stored in session state for export
- All calculations are physiologically based

---

**Made with ❤️ for the cardiovascular community**

Enjoy your new VAD simulator! 🚀🫀
