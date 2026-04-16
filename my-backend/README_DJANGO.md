# Django Backend for ETE Resource Portal

This is a Python/Django rewrite of the Node.js Express backend for compatibility with PythonAnywhere free tier.

## Migration from Node.js to Django

The backend has been converted from Node.js/Express to Django/Python to work on PythonAnywhere's free tier.

### Key Changes:
- **API Endpoints**: All Express routes → Django views (same functionality)
- **Database**: SQLite with Django ORM models
- **Authentication**: Django user system
- **File Uploads**: Django file upload handling
- **CORS**: django-cors-headers middleware

## API Endpoints (Same as before)

- `POST /api/register` - Student registration
- `POST /api/login` - User login
- `GET /api/materials/:type/:level/:term` - Get materials by level/term
- `POST /api/upload` - Upload resource file
- `GET /api/user/my-uploads/:userId` - Get user's uploads
- `GET /api/admin/all-resources` - Get all resources (admin)
- `POST /api/admin/review-resource` - Review/approve resource
- `DELETE /api/admin/delete-resource/:id` - Delete resource
- `GET /api/health` - Health check

## Setup on PythonAnywhere

### 1. Upload Files
- Upload all Python files to PythonAnywhere
- Upload `requirements.txt`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Database
```bash
python manage.py migrate
```

### 4. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 5. Configure Web App
In PythonAnywhere Web app settings:
- **WSGI configuration file**: Point to `wsgi.py`
- **Working directory**: `/home/hmh8138/my-backend`
- **Python version**: 3.9+

### 6. Restart
Click "Reload" button on web app

## Files

- `models.py` - Database models (User, Resource)
- `views.py` - API endpoints/views
- `urls.py` - URL routing
- `settings.py` - Django configuration
- `wsgi.py` - WSGI application entry point
- `requirements.txt` - Python dependencies

## Backend URL

```
https://hmh8138.pythonanywhere.com/api/
```

## Testing

Health check:
```bash
curl https://hmh8138.pythonanywhere.com/api/health
```

## Notes

- All endpoints are CORS-enabled for GitHub Pages
- File uploads go to `/uploads/` directory
- Database is SQLite (suitable for small to medium projects)
- CORS is configured for `https://hmh-8138.github.io`

## Migration Complete ✅

Your backend is now running on Django and compatible with PythonAnywhere free tier!
