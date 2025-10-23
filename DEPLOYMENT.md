# 🚀 Quick Deployment Guide

## You have 3 options to deploy your app:

---

## ⚡ Option 1: Streamlit Cloud (EASIEST - FREE)

### Step 1: Push to GitHub
```bash
cd /path/to/your/Teaching/folder
mkdir Python
# Copy the 5 files into Python folder:
#   - app.py
#   - cardiovascular_model.py
#   - requirements.txt  
#   - README.md
#   - .gitignore

git add Python/
git commit -m "Add Python teaching version with Streamlit app"
git push
```

### Step 2: Deploy on Streamlit Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with GitHub
3. Click **"New app"**
4. Select repository: `viswajithsv-collab/CP-Model`
5. Set branch: `main`
6. Set file path: `Teaching/Python/app.py`
7. Click **"Deploy"**!

**Done!** Your app will be live at:
```
https://viswajithsv-collab-cp-model.streamlit.app
```

**Share with students** - just send them the link!

---

## 💻 Option 2: Run Locally (FOR TESTING)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Opens at: `http://localhost:8501`

---

## 🐳 Option 3: Docker (ADVANCED)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t cardio-app .
docker run -p 8501:8501 cardio-app
```

---

## 📦 What You Have

Your Python teaching app includes:

✅ **app.py** - Interactive Streamlit web interface  
✅ **cardiovascular_model.py** - Core simulation engine  
✅ **requirements.txt** - Python dependencies  
✅ **README.md** - Full documentation  
✅ **.gitignore** - Git ignore rules  

---

## 🎓 For Your Students

**Just share the deployed link!** Students can:
- Adjust heart rate, resistances, compliances
- See real-time pressure/flow/volume waveforms  
- View PV loops
- Learn with built-in educational notes

No installation needed - runs in the browser! 🎉

---

## ⚠️ Important: Which Model?

**Teaching Version (this):**
- Simple 2-branch model (lower/upper body)
- Perfect for education
- Fast simulations
- Easy to understand

**Research Version** (`/CP Model` folder):
- Complex 6-branch model
- LVAD support
- Baroreflex control
- For your LVAD research

**Keep them separate!** 

---

## 🆘 Troubleshooting

**App won't deploy on Streamlit Cloud?**
- Check `requirements.txt` is in same folder as `app.py`
- Make sure GitHub repo is public
- Verify file path is correct: `Teaching/Python/app.py`

**Simulation too slow?**
- Increase `dt` in the code (currently 0.001)
- Reduce duration
- Use fewer time steps

**Want to customize?**
- Edit `app.py` for UI changes
- Edit `cardiovascular_model.py` for model changes
- Colors, layouts, parameters - all customizable!

---

## 🎉 Next Steps

1. **Deploy to Streamlit Cloud** (10 minutes)
2. **Test with students** (give them the link)
3. **Collect feedback** (what parameters do they want?)
4. **Iterate!** (add features based on needs)

**You're ready to go!** 🚀
