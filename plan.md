# SQLite Database Implementation Plan

## Tasks:
- [ ] 1. Install SQLite package (better-sqlite3)
- [ ] 2. Create database setup file (database.js)
- [ ] 3. Create tables: users, resources
- [ ] 4. Update index.js to use SQLite instead of in-memory arrays
- [ ] 5. Seed initial data
- [ ] 6. Update TODO.md

## Implementation Details:

### Step 1: Install SQLite
- Run: npm install better-sqlite3

### Step 2: Create database.js
- Initialize SQLite database
- Create tables:
  - users (id, name, email, phone, batch, address, password, createdAt)
  - resources (id, userId, userName, batch, level, term, courseCode, courseName, resourceType, fileTitle, description, file data, status, uploadedAt, reviewedAt, reviewComment, adminId)

### Step 3: Update index.js
- Import database module
- Replace in-memory arrays with database queries
- Add CRUD operations for users and resources

### Files to modify:
- my-backend/package.json (add dependency)
- my-backend/database.js (create new)
- my-backend/index.js (update to use database)

### Followup:
- Test the backend
- Verify all API endpoints work with database
