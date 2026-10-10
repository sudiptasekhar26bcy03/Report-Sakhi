# ReportSakhi (റിപ്പോർട്ട് സഖി / रिपोर्ट सखी)

> **"Your AI health friend that explains medical lab reports to rural patients in their own language, by voice."**

---

## 🌟 Highlights
- **Mobile-First Phone Browser Design**: Works directly in Safari, Chrome, and any mobile browser without requiring app store installation.
- **Languages**: Malayalam (മലയാളം), Hindi (हिन्दी), Tamil (தமிழ்), English.
- **Four-Agent Pipeline**:
  1. **Reader Agent**: Vision-based extraction of test names, values, and units (with retake prompts for blurry images).
  2. **Checker Agent**: Fast deterministic System One rule-based decision engine (`ranges.json`). **Deliberately not an LLM** for clinical safety.
  3. **Explainer Agent**: Class 5 elementary reading level explanations adhering to strict safety rules (Never diagnoses, always includes safety disclaimer).
  4. **Voice Agent**: Indian language voice with provider switch (Bhashini, Sarvam, Web Speech failover).
- **Simple Mode**: Low-literacy mode with +40% font scaling, simplified icon cards, and automatic voice playback.
- **Find Help Action**: Direct hospital/clinic map finder when warning flags (yellow/red) are detected.

---

## 🛠 Tech Stack
- **Backend**: Python 3.10+ & FastAPI, Uvicorn
- **Architecture**: ARM64 Native for Apple Silicon (MacBook Air M5 / macOS)
- **Frontend**: Plain HTML5, CSS3, Vanilla JavaScript (zero framework bundle overhead)
- **AI / LLM**: Gemini 2.0 Flash (`google-genai`)
- **Speech**: Browser Web Speech API fallback + Bhashini / Sarvam hooks

---

## 🚀 Quickstart

### 1. Set Up Virtual Environment (ARM64 Native)
```bash
cd "/Applications/Report Sakhi"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Optional: Add GEMINI_API_KEY for live Vision extraction & LLM explanations
```

### 3. Run the Development Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000` on your desktop or `http://<your-ip>:8000` on any mobile browser on the same Wi-Fi.

---

## 📋 Core Safety Philosophy
> **"AI explains, rules decide, doctors diagnose."**
All color codes (Green / Yellow / Red) are generated from verified clinical reference limits in `app/data/ranges.json`.
