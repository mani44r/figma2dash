# Setup Guide - Figma to Dashboard Generator

## Step-by-Step Installation

### 1. Check Python Version

Make sure you have Python 3.10 or higher:

```bash
python --version
```

If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).

---

### 2. Install Dependencies

Navigate to the project folder and install required packages:

```bash
cd figma-to-dashboard
pip install -r requirements.txt
```

**For Windows users**, if you encounter issues, try:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

### 3. Get Your Figma Token

1. **Login to Figma**: Go to [figma.com](https://www.figma.com/)

2. **Open Settings**: Click your profile → Settings

3. **Generate Token**:
   - Scroll to "Personal access tokens"
   - Click "Create new token"
   - Name it something like "Dashboard Generator"
   - Copy the token (you won't see it again!)

4. **Test the token** (optional):
   ```bash
   curl -H "X-Figma-Token: YOUR_TOKEN" https://api.figma.com/v1/me
   ```

---

### 4. Get Your OpenAI API Key

1. **Sign up/Login**: Go to [platform.openai.com](https://platform.openai.com/)

2. **Create API Key**:
   - Go to [API Keys page](https://platform.openai.com/api-keys)
   - Click "Create new secret key"
   - Name it "Figma Dashboard Project"
   - Copy the key immediately

3. **Add Credits** (if needed):
   - Go to Billing section
   - Add payment method
   - You'll need ~$1-2 for testing (GPT-4o Vision costs ~$0.01 per image)

---

### 5. Configure Environment Variables

1. **Copy the example file**:
   ```bash
   copy .env.example .env
   ```

2. **Edit `.env` file** with your tokens:
   ```env
   FIGMA_TOKEN=figd_your_actual_figma_token_here
   OPENAI_API_KEY=sk-your_actual_openai_key_here
   ```

---

### 6. Test the Setup

Run the health check:

```bash
python -c "from app.figma.client import get_token; from app.classifier.vision_classifier import get_openai_client; print('✅ Configuration valid!')"
```

If you see "✅ Configuration valid!", you're all set!

---

### 7. Run the Application

**Option A: Using the batch file (Windows)**
```bash
run.bat
```

**Option B: Using Python directly**
```bash
python app/main.py
```

**Option C: Using uvicorn**
```bash
uvicorn app.main:app --reload
```

---

### 8. Open the Web Interface

Open your browser and go to:
```
http://localhost:8000
```

You should see the Figma to Dashboard Generator interface!

---

## Testing the Application

### Option 1: Use a Public Figma File

Try with a public Figma community file:
1. Go to [Figma Community](https://www.figma.com/community)
2. Find a dashboard template
3. Click "Duplicate" to add it to your files
4. Copy the URL
5. Paste into the app

### Option 2: Create Your Own Test Dashboard

1. **Create a new Figma file**
2. **Add a Frame** (press `F` key or use Rectangle tool)
3. **Add some components**:
   - Text layer (for headings)
   - Rectangle with text inside (for KPI cards)
   - Draw some shapes (simulating charts)
4. **Get the URL** from browser address bar
5. **Test in the app**

---

## Troubleshooting

### Error: "FIGMA_TOKEN not configured"

**Solution**: 
- Make sure `.env` file exists in the project root
- Check that `FIGMA_TOKEN=` line has your actual token
- No spaces around the `=` sign

### Error: "OPENAI_API_KEY not configured"

**Solution**:
- Add your OpenAI key to `.env` file
- Make sure you have credits in your OpenAI account

### Error: "Could not extract file key from URL"

**Solution**:
- Make sure URL is from Figma (starts with `https://www.figma.com/`)
- URL should look like: `https://www.figma.com/file/abc123xyz...`

### Error: "No frames found in Figma file"

**Solution**:
- Open your Figma file
- Make sure you have at least one **Frame** (not just shapes on canvas)
- Press `F` to create a frame in Figma

### Error: "401 Unauthorized" from Figma API

**Solution**:
- Your Figma token might be invalid or expired
- Generate a new token from Figma settings
- Update `.env` file

### Error: OpenAI API rate limit or quota exceeded

**Solution**:
- Check your OpenAI account billing
- Add payment method if needed
- Wait a few minutes and try again

---

## File Structure Quick Reference

```
figma-to-dashboard/
├── app/                    # Main application code
│   ├── main.py            # FastAPI server (start here)
│   ├── pipeline.py        # Processing pipeline
│   ├── models.py          # Data models
│   ├── figma/            # Figma API integration
│   ├── classifier/       # AI classification
│   ├── layout/           # Grid mapping
│   ├── generator/        # Config generation
│   └── templates/        # Web UI
├── .env                   # Your secrets (create this)
├── .env.example          # Template for .env
├── requirements.txt      # Python dependencies
├── run.bat              # Quick start script
└── README.md            # Full documentation
```

---

## Next Steps

1. ✅ Setup complete - try converting a Figma file
2. 📖 Read the full [README.md](README.md) for API usage
3. 🧪 Check [example_usage.py](example_usage.py) for Python examples
4. 🎨 Create your own dashboard designs in Figma
5. 📊 Export configs and integrate with your dashboard renderer

---

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [Figma API Docs](https://www.figma.com/developers/api)
- Review [OpenAI API Docs](https://platform.openai.com/docs)

---

**Happy Converting! 🎉**
