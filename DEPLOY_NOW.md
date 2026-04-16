# 🚀 DEPLOYMENT - All You Need (One File)

## Setup: GitHub Pages + PythonAnywhere Backend (Django)

Your website will be at: `https://hmh-8138.github.io/ete-resources/`  
Your backend API at: `https://hmh8138.pythonanywhere.com/api`

---

## 📋 Prerequisites

- [ ] PythonAnywhere account (free): https://www.pythonanywhere.com
- [ ] Logged in to PythonAnywhere
- [ ] Git installed
- [ ] Node.js installed (for frontend only)

---

## ⚡ Step 1: Update API URLs (5 minutes)

Already done! Files updated to use: `https://hmh8138.pythonanywhere.com`

---

## 📤 Step 2: Deploy to GitHub (5 minutes)

```bash
cd e:\Folder\CODE\WEBSITE
git add .
git commit -m "Deploy to GitHub Pages + Django backend on PythonAnywhere"
git push origin main
```

**Enable GitHub Pages:**
1. Go to: https://github.com/hmh-8138/ete-resources/settings/pages
2. Select branch: `main`
3. Select folder: `/ (root)`
4. Click Save
5. Wait 1-2 minutes

Your website is now live at: https://hmh-8138.github.io/ete-resources/

---

## 🖥️ Step 3: Deploy Django Backend (15 minutes)

**Backend has been converted from Node.js to Django for free PythonAnywhere!**

### In PythonAnywhere Files Section:

1. **Upload these files** from `my-backend`:
   - `models.py`
   - `views.py`
   - `urls.py`
   - `wsgi.py`
   - `settings.py`
   - `requirements.txt`
   - `database.json` (optional)

2. **Delete these** (not needed anymore):
   - `index.js`
   - `package.json`
   - `database.js`

### In PythonAnywhere Bash Console:

```bash
cd my-backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

When asked for superuser:
- Username: `admin`
- Email: `admin@ete.local`
- Password: (your choice)

---

## ⚙️ Step 4: Configure Web App

1. Go to **Web apps** in PythonAnywhere
2. Click on your web app (hmh8138.pythonanywhere.com)
3. **WSGI configuration file**: Change to:
   ```
   /home/hmh8138/my-backend/wsgi.py
   ```
4. **Working directory**: Change to:
   ```
   /home/hmh8138/my-backend
   ```
5. Scroll down and click **Reload** (green button)

Wait for it to reload... ✅

---

## ✅ Step 5: Test Everything (10 minutes)

### Test Backend API:
```bash
curl https://hmh8138.pythonanywhere.com/api/health
```

Should return: `{"status": "ok", ...}`

### Test Website:
1. Visit: https://hmh-8138.github.io/ete-resources/
2. Press F12 → Console tab
3. Look for any errors (should be none)
4. Try student login
5. Try uploading a file

**If you see CORS errors:**
- Backend CORS is already configured for GitHub Pages
- Make sure backend is reloaded on PythonAnywhere

---

## 🎯 Success Checklist

- [ ] Website loads: https://hmh-8138.github.io/ete-resources/
- [ ] No 404 errors
- [ ] All pages display
- [ ] Login works
- [ ] No CORS errors in console (F12)
- [ ] File upload works
- [ ] Backend health check works

---

## 🆘 Troubleshooting

### Backend health check fails
```bash
# In PythonAnywhere Bash:
cd my-backend
python manage.py migrate
# Then reload web app
```

### CORS errors still showing
- Check that wsgi.py points to correct location
- Verify web app is reloaded
- Check settings.py has correct CORS origin

### Website shows old API URL
```bash
git status  # Check if files changed
git diff    # View changes
git push origin main  # Push again
# Hard refresh browser: Ctrl+Shift+R
```

### Can't upload files
- Check uploads folder has write permissions in PythonAnywhere
- Verify file size is under 100MB
- Check Django logs in PythonAnywhere

---

## 📚 Files Reference

| File | Purpose |
|------|---------|
| `models.py` | Database models (User, Resource) |
| `views.py` | API endpoints |
| `urls.py` | URL routing |
| `wsgi.py` | WSGI entry point |
| `settings.py` | Django configuration |
| `requirements.txt` | Python dependencies |
| `README_DJANGO.md` | Django setup guide |

---

## 🔗 Important URLs

| Item | URL |
|------|-----|
| Website | https://hmh-8138.github.io/ete-resources/ |
| GitHub Repo | https://github.com/hmh-8138/ete-resources |
| Backend API | https://hmh8138.pythonanywhere.com/api |
| PythonAnywhere | https://www.pythonanywhere.com/user/hmh8138 |

---

## 📊 Summary

✅ **Backend converted from Node.js to Django**  
✅ **API endpoints identical (same functionality)**  
✅ **CORS configured for GitHub Pages**  
✅ **Free tier on PythonAnywhere supported**  
✅ **Database migrated to Django ORM**  

---

**Status**: ✅ Ready for production  
**Backend**: Django on PythonAnywhere (free)  
**Frontend**: GitHub Pages (free)  
**Total Cost**: $0 🎉

---

*Created: April 16, 2026*  
*Backend Type: Django/Python*  
*Status: Complete and ready for deployment*
