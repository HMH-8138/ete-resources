# Render Deployment Setup Guide

## Step 1: Prepare for Render Deployment

### Prerequisites
- Render account (https://render.com)
- GitHub repository with the code
- Backend code in `/my-backend` directory

### What's Already Done
✅ Added `start` script to package.json
✅ Created render.yaml configuration
✅ Added health check endpoint (/api/health)

## Step 2: Deploy Backend to Render

### Manual Setup (if not using render.yaml)

1. **Go to Render Dashboard**
   - Sign in to https://dashboard.render.com

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository containing this code

3. **Configure Service**
   - **Name**: ete-resource-backend
   - **Runtime**: Node
   - **Build Command**: `cd my-backend && npm install`
   - **Start Command**: `cd my-backend && npm start`
   - **Environment**: Production
   - **Instance Type**: Choose based on needs (Free/Paid)

4. **Environment Variables**
   - No additional variables needed (PORT is automatically set by Render)

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-5 minutes)
   - Note the URL (e.g., https://ete-resource-backend.onrender.com)

## Step 3: Update Frontend API URLs

After backend is deployed, update all HTML files with the actual Render URL.

### Files to Update:
- admin_login.html
- admin_new.html
- login.html
- materials.html
- my-uploads.html
- register.html
- student_login.html
- upload.html

### Replace All Occurrences Of:
```javascript
const API_URL = 'http://localhost:3000/api';
```

With:
```javascript
const API_URL = 'https://ete-resource-backend.onrender.com/api';
```

### Also Update Upload Links:
Replace all:
```
http://localhost:3000/uploads/
```

With:
```
https://ete-resource-backend.onrender.com/uploads/
```

## Step 4: Deploy Frontend to Netlify

The frontend (in `/ETE_resourse_sharing_website`) is already configured for Netlify with the `netlify.toml` file.

1. **Connect to Netlify**
   - Go to https://netlify.com
   - Click "Add new site" → "Import an existing project"
   - Choose your GitHub repository

2. **Configure Build**
   - **Base directory**: ETE_resourse_sharing_website
   - **Build command**: (leave empty - static site)
   - **Publish directory**: . (current directory)

3. **Deploy**
   - Click "Deploy site"
   - Get your Netlify URL

## Step 5: Update CORS Settings (if needed)

If you encounter CORS errors, update the CORS middleware in `/my-backend/index.js`:

Current setting allows all origins:
```javascript
app.use(cors({ origin: '*' }));
```

To restrict to your Netlify domain (after deployed):
```javascript
app.use(cors({ origin: 'https://your-netlify-domain.netlify.app' }));
```

## Step 6: Verify Deployment

### Test Backend Health
```
https://ete-resource-backend.onrender.com/api/health
```

Should return:
```json
{
  "status": "ok",
  "message": "Server is running"
}
```

### Test Login
Try logging in through the frontend to verify API communication.

## Troubleshooting

### Backend not starting
- Check build logs in Render dashboard
- Ensure all dependencies in package.json are listed
- Verify Node version compatibility

### API calls failing
- Check browser console for CORS errors
- Verify API_URL in HTML files is correct
- Check Render service is running (green status)

### Uploads not working
- Ensure Render service has write permissions
- Note: Render ephemeral storage means uploads are temporary
- For persistence, consider adding database storage

## Important Notes

⚠️ **Render Free Tier Limitations:**
- Services spin down after 15 minutes of inactivity
- Uploads are stored temporarily (cleared after service restart)
- For production, use Paid Tier with persistent storage

### For Persistent File Storage:
Consider adding:
- Cloudinary (image hosting)
- AWS S3 (file storage)
- Firebase Storage (Google solution)

## Commands Reference

```bash
# Test locally before deploying
cd my-backend
npm install
npm start

# The service should run on http://localhost:3000
```

## Next Steps

1. Commit and push these changes to GitHub
2. Deploy backend to Render
3. Get the Render URL
4. Update all frontend API URLs
5. Deploy frontend to Netlify
6. Test the complete application

