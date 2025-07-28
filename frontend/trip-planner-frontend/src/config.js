// Configuration for different environments
const config = {
  development: {
    backendUrl: 'http://localhost:8000'
  },
  production: {
    // You'll need to deploy your backend to a service like Railway, Render, or Heroku
    backendUrl: 'https://your-backend-url.railway.app' // Replace with your actual backend URL
  }
};

// Use development config for now
export const backendUrl = config.development.backendUrl; 