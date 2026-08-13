# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
copy .env.example .env
```

Edit `.env`:
```
FIGMA_TOKEN=your_figma_token
OPENAI_API_KEY=your_openai_key
```

### 3. Test Setup
```bash
python test_setup.py
```

### 4. Run Application
```bash
python app/main.py
```

### 5. Open Browser
```
http://localhost:8000
```

---

## Get API Keys

### Figma Token
1. Go to https://www.figma.com/settings
2. Scroll to "Personal access tokens"
3. Click "Create new token"
4. Copy and paste into `.env`

### OpenAI Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy and paste into `.env`

---

## Try It Out

1. Create a simple dashboard in Figma
2. Copy the file URL
3. Paste into the web app
4. Click "Convert"
5. View JSON/YAML output!

---

## Need Help?

- 📖 Read [README.md](README.md)
- 🔧 Check [SETUP.md](SETUP.md)
- 🏗️ See [ARCHITECTURE.md](ARCHITECTURE.md)
- 📊 Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

**That's it! You're ready to go! 🚀**
