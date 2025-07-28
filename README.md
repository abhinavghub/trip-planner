# AI Trip Planner

A beautiful, AI-powered trip planning application built with React, FastAPI, and LangGraph.

## 🚀 Features

- **AI-Powered Itineraries**: Uses Hugging Face API for intelligent trip planning
- **Multi-Agent Workflow**: Research → Generate → Critique pipeline
- **Beautiful UI**: Modern, responsive design with animations
- **Dynamic Planning**: Considers trip duration and user preferences
- **Real-time Suggestions**: AI review and improvement suggestions

## 🏗️ Architecture

- **Frontend**: React with modern CSS animations
- **Backend**: FastAPI with LangGraph multi-agent workflow
- **AI**: Hugging Face inference API (free tier)
- **Deployment**: Railway for full-stack hosting

## 🚀 Quick Deploy to Railway

### Option 1: Deploy from GitHub (Recommended)

1. **Fork this repository** to your GitHub account
2. **Go to** [railway.app](https://railway.app)
3. **Sign up/Login** with your GitHub account
4. **Click "New Project"** → "Deploy from GitHub repo"
5. **Select your forked repository**
6. **Railway will automatically detect** and deploy both frontend and backend

### Option 2: Deploy from Local Files

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize and deploy**:
   ```bash
   railway init
   railway up
   ```

## 🔧 Environment Variables

The backend uses Hugging Face's free API by default. No API keys required!

If you want to use OpenAI instead:
```bash
OPENAI_API_KEY=your_openai_key_here
```

## 📁 Project Structure

```
trip_planner/
├── frontend/trip-planner-frontend/    # React frontend
│   ├── src/
│   │   ├── App.js                     # Main component
│   │   ├── App.css                    # Beautiful styles
│   │   └── config.js                  # Environment config
│   └── build/                         # Production build
├── backend/                           # FastAPI backend
│   ├── main.py                        # Main API
│   ├── requirements.txt               # Python dependencies
│   └── Procfile                       # Railway deployment
├── railway.json                       # Railway configuration
└── README.md                          # This file
```

## 🎨 Features

### Frontend
- **Gradient Hero Section** with animated text
- **Modern Card Design** with hover effects
- **Responsive Layout** for all devices
- **Loading Animations** with spinner
- **Dynamic Itinerary Display** with day cards
- **AI Review Section** with suggestions

### Backend
- **Multi-Agent Workflow**: Research → Generate → Critique
- **Dynamic Itinerary Generation** based on duration and preferences
- **Preference Analysis** for personalized activities
- **Fallback Responses** when API is unavailable
- **CORS Configuration** for cross-origin requests

## 🔄 Development

### Frontend
```bash
cd frontend/trip-planner-frontend
npm start
```

### Backend
```bash
cd backend
python3 -m uvicorn main:app --reload --port 8000
```

## 🌐 Deployment URLs

After Railway deployment, you'll get:
- **Frontend**: `https://your-app-name.railway.app`
- **Backend**: `https://your-app-name-backend.railway.app`

## 🎯 Usage

1. **Enter destination** (e.g., "Paris", "Tokyo")
2. **Select dates** for your trip
3. **Add preferences** (e.g., "museums, food, culture")
4. **Click "Plan My Trip"**
5. **View your AI-generated itinerary** with day-by-day activities
6. **Read AI suggestions** for improvements

## 🛠️ Customization

### Adding New AI Providers
Edit `backend/main.py` to add new AI providers:
```python
def call_anthropic_api(prompt: str) -> str:
    # Add Anthropic Claude integration
    pass
```

### Styling Changes
Edit `frontend/src/App.css` for custom styling:
```css
.hero-section {
  background: linear-gradient(135deg, #your-colors);
}
```

## 📊 Performance

- **Frontend**: Optimized React build with code splitting
- **Backend**: FastAPI with async processing
- **AI**: Hugging Face free tier (200 requests/hour)
- **Deployment**: Railway's global CDN

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use this project for your own applications!

## 🆘 Support

If you encounter issues:
1. Check the Railway logs in your dashboard
2. Verify environment variables are set correctly
3. Test the backend API endpoint directly
4. Check the browser console for frontend errors

---

**Built with ❤️ using React, FastAPI, and LangGraph** 