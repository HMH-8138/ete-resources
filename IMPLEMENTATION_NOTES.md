# Syllabus & Routine Implementation Summary

## 📋 Changes Made

### 1. **New Files Created**

#### `syllabus.html` - Syllabus & Curriculum Upload Page
- **Features:**
  - Upload form for syllabus documents with fields for:
    - Academic Level (1-4)
    - Term (1-2)
    - Course Code & Name
    - Document Title
    - Description
    - File upload (PDF, DOCX, JPG, PNG)
  - File upload preview with selected filename display
  - Display all approved syllabus documents in a list
  - Download functionality for uploaded files
  - Status badges (pending, approved, rejected)
  - Responsive design matching your site theme
  - Quick links to related pages

#### `routine.html` - Class Routine Page
- **Features:**
  - Links to external routine documents for all 4 levels
  - Class timings reference information
  - FAQ section with expandable questions
  - Professional layout with clear navigation
  - External links open in new tabs (marked with ↗ symbol)
  - Placeholder URLs for Level 1-4 routines (update these with your actual links)

### 2. **Updated Files**

#### `index.html`
- Made "Syllabus & Curriculum" clickable → links to `syllabus.html`
- Made "Class Routine" clickable → links to `routine.html`
- Maintains proper styling and navigation

#### `app.py`
- Added new API endpoint: `/api/resources/type/<resource_type>`
- This endpoint retrieves all approved resources by type (e.g., "syllabus")
- Returns data in JSON format with proper formatting
- Filters by resource_type and status = "approved"
- Orders results by level, term, and upload date

---

## 🔧 How to Use

### For Students - Uploading Syllabus:
1. Go to **Syllabus & Curriculum** link from homepage
2. Fill out the upload form with course details
3. Select a file (PDF or image format recommended)
4. Click **Upload Syllabus**
5. Your upload will be sent for admin approval

### For Students - Viewing Routine:
1. Click **Class Routine** from the homepage
2. Select your level (1, 2, 3, or 4)
3. Click on the external link to view/download the routine
4. Read FAQ for common questions

### For Admins:
- Review uploads in the admin panel
- Approve/reject syllabus submissions
- Update external routine links as needed

---

## 📝 Important Notes

### Update These URLs in `routine.html`:
Replace the placeholder links with your actual routine URLs:
```html
<!-- Line ~170 -->
<a href="https://drive.google.com/file/d/1example1/view" target="_blank">
```

You can use:
- Google Drive links
- Dropbox links
- Direct file URLs
- Any external hosting service

### Database Integration:
- Syllabus uploads are stored in the `resources` table with `resource_type = 'syllabus'`
- Files are saved in the `uploads/` folder
- Status starts as 'pending' until admin approves

### Styling:
- Both pages use your existing color scheme (primary-blue, secondary-blue, accent-cyan)
- Responsive design for mobile and desktop
- Consistent with your existing site design

---

## 🚀 Next Steps (Optional)

1. **Update routine links** - Replace placeholder Google Drive links with actual routine URLs
2. **Add admin interface** - Create admin panel to manage syllabus approvals
3. **Add notifications** - Email students when syllabus is uploaded/approved
4. **Add search/filter** - Filter syllabi by level, term, or course
5. **Add versioning** - Track multiple versions of same syllabus

---

## ✅ Testing Checklist

- [ ] Test syllabus upload from syllabus.html
- [ ] Verify files are saved in uploads/ folder
- [ ] Check API endpoint `/api/resources/type/syllabus` returns data
- [ ] Test routine.html external links
- [ ] Test FAQ toggle functionality
- [ ] Check mobile responsiveness
- [ ] Verify navigation from index.html works
- [ ] Test admin approval workflow

---

**Status:** ✅ Implementation Complete
**Date:** May 5, 2026
