# Trip Planner Deployment Guide

## 🚀 Quick Deploy Options

### Option 1: Netlify Drop (Frontend Only - 30 seconds)
1. Go to [netlify.com/drop](https://netlify.com/drop)
2. Drag the `frontend/trip-planner-frontend/build` folder
3. Get instant URL like `https://amazing-trip-planner-123.netlify.app`

### Option 2: GitHub Pages (Frontend Only - Free)
1. Create GitHub repository named `trip-planner`
2. Push your code to GitHub
3. Run: `npm run deploy` in the frontend folder
4. Your app will be at: `https://yourusername.github.io/trip-planner`

### Option 3: Railway (Full Stack - Recommended)
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Deploy both frontend and backend automatically

## 🔧 Backend Deployment

### Railway Backend Setup:
1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will automatically detect the Python backend
4. Set environment variables if needed
5. Get your backend URL (e.g., `https://your-app.railway.app`)

### Update Frontend Config:
After getting your backend URL, update `frontend/src/config.js`:
```javascript
production: {
  backendUrl: 'https://your-backend-url.railway.app'
}
```

## 🌐 Alternative Platforms

### Frontend Only:
- **Vercel**: `npx vercel` (if SSL issues resolved)
- **Netlify**: Drag & drop build folder
- **GitHub Pages**: `npm run deploy`
- **Firebase Hosting**: `firebase deploy`

### Full Stack:
- **Railway**: Automatic deployment
- **Render**: Free tier available
- **Heroku**: Paid but reliable
- **DigitalOcean App Platform**: Good performance

## 📝 Environment Variables

For production backend, you might need:
```bash
OPENAI_API_KEY=your_key_here  # If using OpenAI
HUGGINGFACE_API_KEY=your_key_here  # If using Hugging Face
```

## 🔗 CORS Configuration

The backend already has CORS configured for `*` origins, so it should work with any frontend URL.

## 🎯 Recommended Approach

1. **Start with Netlify Drop** for instant frontend deployment
2. **Deploy backend to Railway** for full functionality
3. **Update frontend config** with your backend URL
4. **Redeploy frontend** with updated config

## 🚨 Important Notes

- The current backend uses Hugging Face's free API (no auth required)
- For production, consider using a paid API for better reliability
- The frontend is configured to work with localhost by default
- Update the config.js file after getting your backend URL 