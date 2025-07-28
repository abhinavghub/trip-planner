// Configuration for different environments
const config = {
  development: {
    backendUrl: 'http://localhost:8000'
  },
  production: {
    // This will be updated with your Railway backend URL
    backendUrl: 'https://trip-planner-production-61bd.up.railway.app'
  }
};

// Use development config for now, will be overridden in production
export const backendUrl = config.development.backendUrl; 
