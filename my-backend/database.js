const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, 'database.json');

// Initialize database file if it doesn't exist
if (!fs.existsSync(dbPath)) {
    const initialData = {
        users: [],
        resources: []
    };
    fs.writeFileSync(dbPath, JSON.stringify(initialData, null, 2));
    console.log('Database file created:', dbPath);
}

// Read database
function readDB() {
    let data;
    try {
        const rawData = fs.readFileSync(dbPath, 'utf8');
        data = JSON.parse(rawData);
    } catch (error) {
        console.error('Error reading database:', error);
        data = { users: [], resources: [] };
    }
    // Migrate existing users to add role
    data.users = data.users.map(user => ({
        ...user,
        role: user.role || 'student'
    }));
    return data;
}

// Write database
function writeDB(data) {
    try {
        fs.writeFileSync(dbPath, JSON.stringify(data, null, 2));
        return true;
    } catch (error) {
        console.error('Error writing database:', error);
        return false;
    }
}

// Database operations
const db = {
    // Users
    getUsers: () => {
        const data = readDB();
        return data.users;
    },
    
    getUserById: (id) => {
        const data = readDB();
        return data.users.find(u => u.id === id);
    },
    
    createUser: (user) => {
        const data = readDB();
        user.role = user.role || 'student';
        data.users.push(user);
        return writeDB(data);
    },

    
    // Resources
    getResources: () => {
        const data = readDB();
        return data.resources;
    },
    
    getResourceById: (id) => {
        const data = readDB();
        return data.resources.find(r => r.id === id);
    },
    
    getResourcesByUser: (userId) => {
        const data = readDB();
        return data.resources.filter(r => r.userId === userId);
    },
    
    getResourcesByStatus: (status) => {
        const data = readDB();
        return data.resources.filter(r => r.status === status);
    },
    
    createResource: (resource) => {
        const data = readDB();
        const newId = data.resources.length > 0 ? Math.max(...data.resources.map(r => r.id)) + 1 : 1;
        resource.id = newId;
        data.resources.push(resource);
        return writeDB(data) ? newId : false;
    },
    
    updateResource: (id, updates) => {
        const data = readDB();
        const index = data.resources.findIndex(r => r.id === id);
        if (index !== -1) {
            data.resources[index] = { ...data.resources[index], ...updates };
            return writeDB(data);
        }
        return false;
    },
    
    deleteResource: (id) => {
        const data = readDB();
        const index = data.resources.findIndex(r => r.id === id);
        if (index !== -1) {
            const deleted = data.resources.splice(index, 1)[0];
            return writeDB(data) ? deleted : false;
        }
        return false;
    }
};

module.exports = db;

// Seed initial data - DISABLED DEFAULT ADMIN
const data = readDB();
if (!data.users.find(u => u.id === '2208006')) {
    data.users.push({
        id: '2208006',
        name: 'Meherab Hossen',
        email: 'meherab@test.com',
        phone: '',
        batch: '2022',
        address: '',
        password: 'test123',
        role: 'student',
        createdAt: new Date().toISOString()
    });
    writeDB(data);
}

if (data.resources.length === 0) {
    // Seed sample resources
    const seedResources = [
        { userId: '2208006', userName: 'Meherab Hossen', batch: '2022', level: '3', term: '1', courseCode: 'ETE 301', courseName: 'Semiconductor Physics & Devices', resourceType: 'books', fileTitle: 'Chapter 1 - Introduction', description: 'Introduction to semiconductor physics', fileData: { filename: 'file-1772059922351-323079017.pdf', originalName: 'chapter1.pdf', size: 1024000, mimetype: 'application/pdf' }, status: 'approved', uploadedAt: '2024-11-25' },
        { userId: '2208006', userName: 'Meherab Hossen', batch: '2022', level: '3', term: '1', courseCode: 'ETE 303', courseName: 'Industrial Electronics', resourceType: 'notes', fileTitle: 'Lecture Notes - Chapter 1', description: 'Power electronics fundamentals', fileData: { filename: 'file-1772060429745-903487855.pdf', originalName: 'lecture1.pdf', size: 2048000, mimetype: 'application/pdf' }, status: 'approved', uploadedAt: '2024-11-25' },
        { userId: '2208006', userName: 'Meherab Hossen', batch: '2022', level: '3', term: '1', courseCode: 'ETE 305', courseName: 'Digital Communication', resourceType: 'questions', fileTitle: 'Previous Year Questions', description: 'Midterm questions from 2023', fileData: { filename: 'file-1772096550302-180389119.pdf', originalName: 'questions.pdf', size: 512000, mimetype: 'application/pdf' }, status: 'approved', uploadedAt: '2024-11-26' }
    ];
    
    let id = 1;
    seedResources.forEach(r => {
        r.id = id++;
        data.resources.push(r);
    });
    writeDB(data);
    console.log('Seed resources created');
}

console.log('Database connected:', dbPath);

