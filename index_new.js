const express = require('express');
const cors = require('cors');
const path = require('path');
const multer = require('multer');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Ensure uploads directory exists
const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadDir);
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        const ext = path.extname(file.originalname);
        cb(null, file.fieldname + '-' + uniqueSuffix + ext);
    }
});

// File filter to allow only PDF and PPTX
const fileFilter = (req, file, cb) => {
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'];
    if (allowedTypes.includes(file.mimetype) || 
        file.originalname.endsWith('.pdf') || 
        file.originalname.endsWith('.pptx')) {
        cb(null, true);
    } else {
        cb(new Error('Invalid file type. Only PDF and PPTX are allowed.'), false);
    }
};

const upload = multer({ 
    storage: storage,
    limits: { fileSize: 50 * 1024 * 1024 }, // 50 MB limit
    fileFilter: fileFilter
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use('/uploads', express.static(uploadDir));

// Serve frontend static files
const frontendPath = path.join(__dirname, '..', 'ETE_resourse_sharing_website');
console.log('Frontend path:', frontendPath);

// Serve index.html for root route FIRST
app.get('/', (req, res) => {
    res.sendFile(path.join(frontendPath, 'index.html'));
});

// Then serve static files
app.use(express.static(frontendPath));

// In-memory data store
const users = [];
const resources = [];

// Course data by Level and Term
const coursesDataByLevel = {
    '1-1': { courses: [{ id: 1, name: 'EEE 181', title: 'Basic Electrical Engineering' }, { id: 2, name: 'MATH 181', title: 'Differential and Integral Calculus' }, { id: 3, name: 'MATH 183', title: 'Ordinary & Partial Differential Equations and Matrix' }, { id: 4, name: 'CHEM 181', title: 'Chemistry' }, { id: 5, name: 'HUM 181', title: 'Technical English' }], labs: [{ id: 1, name: 'EEE 182', title: 'Basic Electrical Engineering Sessional' }, { id: 2, name: 'CHEM 182', title: 'Chemistry Sessional' }, { id: 3, name: 'ME 182', title: 'Mechanical Engineering Drawing' }] },
    '1-2': { courses: [{ id: 1, name: 'ETE 101', title: 'Electronics-I' }, { id: 2, name: 'EEE 183', title: 'Fundamentals of Electrical Machines' }, { id: 3, name: 'PHY 181', title: 'Engineering Physics' }, { id: 4, name: 'MATH 185', title: 'Vector Analysis & Operational Calculus' }, { id: 5, name: 'CSE 181', title: 'Computer Programming and Numerical Analysis' }], labs: [{ id: 1, name: 'ETE 102', title: 'Electronics-I Sessional' }, { id: 2, name: 'EEE 184', title: 'Fundamentals of Electrical Machines Sessional' }, { id: 3, name: 'PHY 182', title: 'Engineering Physics Sessional' }, { id: 4, name: 'CSE 182', title: 'Computer Programming and Numerical Analysis Sessional' }] },
    '2-1': { courses: [{ id: 1, name: 'ETE 201', title: 'Electronics-II' }, { id: 2, name: 'ETE 203', title: 'Signals and Systems' }, { id: 3, name: 'CSE 281', title: 'Data Structures and Algorithms' }, { id: 4, name: 'MATH 281', title: 'Engineering Statistics and Complex Variables' }, { id: 5, name: 'HUM 281', title: 'Financial Accounting and Management' }], labs: [{ id: 1, name: 'ETE 202', title: 'Electronics-II Sessional' }, { id: 2, name: 'ETE 204', title: 'Signals and Systems Sessional' }, { id: 3, name: 'CSE 282', title: 'Data Structures and Algorithms Sessional' }] },
    '2-2': { courses: [{ id: 1, name: 'ETE 205', title: 'Digital Logic Design' }, { id: 2, name: 'ETE 207', title: 'Electromagnetic Fields & Waves' }, { id: 3, name: 'ETE 209', title: 'Analog Communications' }, { id: 4, name: 'ETE 211', title: 'Control System Engineering' }, { id: 5, name: 'HUM 283', title: 'Economics and Sociology' }], labs: [{ id: 1, name: 'ETE 206', title: 'Digital Logic Design Sessional' }, { id: 2, name: 'ETE 210', title: 'Analog Communications Sessional' }, { id: 3, name: 'ETE 212', title: 'Control System Engineering Sessional' }, { id: 4, name: 'CSE 284', title: 'Object Oriented Programming' }] },
    '3-1': { courses: [{ id: 1, name: 'ETE 301', title: 'Semiconductor Physics & Devices' }, { id: 2, name: 'ETE 303', title: 'Industrial Electronics' }, { id: 3, name: 'ETE 305', title: 'Digital Communication' }, { id: 4, name: 'ETE 307', title: 'Microwave and Antenna Engineering' }, { id: 5, name: 'ETE 309', title: 'Digital Signal Processing' }], labs: [{ id: 1, name: 'ETE 304', title: 'Industrial Electronics Sessional' }, { id: 2, name: 'ETE 306', title: 'Digital Communication Sessional' }, { id: 3, name: 'ETE 308', title: 'Microwave and Antenna Engineering Sessional' }, { id: 4, name: 'ETE 310', title: 'Digital Signal Processing Sessional' }, { id: 5, name: 'CSE 380', title: 'Internet Programming' }] },
    '3-2': { courses: [{ id: 1, name: 'ETE 311', title: 'Information Theory and Coding' }, { id: 2, name: 'ETE 313', title: 'Electronic Measurement and Instrumentation' }, { id: 3, name: 'ETE 315', title: 'Computer Communications and Networks' }, { id: 4, name: 'ETE 317', title: 'Power System for Communication Engineering' }, { id: 5, name: 'ETE 319', title: 'Microprocessor and Microcontroller' }], labs: [{ id: 1, name: 'ETE 300', title: 'Electronic System Design and Project' }, { id: 2, name: 'ETE 314', title: 'Electronic Measurement and Instrumentation Sessional' }, { id: 3, name: 'ETE 316', title: 'Computer Communications and Networks Sessional' }, { id: 4, name: 'ETE 318', title: 'Power System for Communication Engineering Sessional' }, { id: 5, name: 'CSE 320', title: 'Microprocessor and Microcontroller Sessional' }] },
    '4-1': { courses: [{ id: 1, name: 'ETE 401', title: 'Telecommunication Networks and Switching' }, { id: 2, name: 'ETE 403', title: 'VLSI Technology' }, { id: 3, name: 'ETE 405', title: 'Wireless and Mobile Communication' }, { id: 4, name: 'ETE 407', title: 'Multimedia Communication' }, { id: 5, name: 'ETE*', title: 'Elective-I' }], labs: [{ id: 1, name: 'ETE 400', title: 'Project and Thesis' }, { id: 2, name: 'ETE 402', title: 'Telecommunication Networks and Switching Sessional' }, { id: 3, name: 'ETE 404', title: 'VLSI Technology Sessional' }, { id: 4, name: 'ETE 406', title: 'Wireless and Mobile Communication Sessional' }, { id: 5, name: 'ETE 408', title: 'Multimedia Communication Sessional' }] },
    '4-2': { courses: [{ id: 1, name: 'ETE 411', title: 'Optical Fiber Communications' }, { id: 2, name: 'ETE 413', title: 'Satellite Communications and RADAR' }, { id: 3, name: 'ETE 415', title: 'IoT and Industrial Automation' }, { id: 4, name: 'ETE 417', title: 'Engineering Ethics and Entrepreneurship' }, { id: 5, name: 'ETE*', title: 'Elective-II' }], labs: [{ id: 1, name: 'ETE 400', title: 'Project and Thesis' }, { id: 2, name: 'ETE 412', title: 'Optical Fiber Communications Sessional' }, { id: 3, name: 'ETE 414', title: 'Satellite Communications and RADAR Sessional' }, { id: 4, name: 'ETE 416', title: 'IoT and Industrial Automation Sessional' }, { id: 5, name: 'ETE*', title: 'Sessional based on Elective' }] }
};

const defaultCourses = [{ id: 1, name: 'EEE 181', title: 'Basic Electrical Engineering' }, { id: 2, name: 'MATH 183', title: 'Differential and Integral Calculus' }, { id: 3, name: 'MATH 183', title: 'Ordinary and Partial Differential Equation and Matrix' }, { id: 4, name: 'CHEM 181', title: 'Chemistry' }, { id: 5, name: 'HUM 181', title: 'Technical English' }];
const defaultLabs = [{ id: 1, name: 'EEE 182', title: 'Basic Electrical Engineering Sessional' }, { id: 2, name: 'CHEM 182', title: 'Chemistry Sessional' }, { id: 3, name: 'ME 182', title: 'Mechanical Drawing' }];

const materialTypesData = {
    books: [{ name: 'Book 1', title: 'Fundamentals Guide' }, { name: 'Book 2', title: 'Advanced Concepts' }, { name: 'Book 3', title: 'Practical Applications' }, { name: 'Book 4', title: 'Reference Manual' }],
    questions: [{ name: 'Question Set 1', title: '2023 Final Exam' }, { name: 'Question Set 2', title: '2022 Mid-term' }, { name: 'Question Set 3', title: 'Practice Problems' }, { name: 'Question Set 4', title: 'Model Papers' }],
    notes: [{ name: 'Notes 1', title: 'Chapter 1 & 2' }, { name: 'Notes 2', title: 'Chapter 3 & 4' }, { name: 'Notes 3', title: 'Important Formulas' }, { name: 'Notes 4', title: 'Summary & Revision' }],
    resources: [{ name: 'Resource 1', title: 'Tutorial Videos' }, { name: 'Resource 2', title: 'Online Tools' }, { name: 'Resource 3', title: 'Simulation Software' }, { name: 'Resource 4', title: 'Documentation' }]
};

// ============ API ROUTES ============

// POST /api/register
app.post('/api/register', (req, res) => {
    const { name, email, id, phone, batch, address, password } = req.body;
    const existingUser = users.find(u => u.id === id || u.email === email);
    if (existingUser) return res.status(400).json({ success: false, message: 'User with this ID or email already exists' });
    const newUser = { id, name, email, phone, batch, address, password, createdAt: new Date() };
    users.push(newUser);
    res.json({ success: true, message: 'Registration successful!', user: { id, name, email, batch } });
});

// POST /api/login
app.post('/api/login', (req, res) => {
    const { id, password } = req.body;
    const user = users.find(u => u.id === id && u.password === password);
    if (!user) return res.status(401).json({ success: false, message: 'Invalid ID or password' });
    res.json({ success: true, message: 'Login successful!', user: { id: user.id, name: user.name, email: user.email, batch: user.batch } });
});

// GET /api/materials/:type/:level/:term
app.get('/api/materials/:type/:level/:term', (req, res) => {
    const { type, level, term } = req.params;
    const levelTermKey = `${level}-${term}`;
    let courseData = defaultCourses, labData = defaultLabs;
    if (coursesDataByLevel[levelTermKey]) { courseData = coursesDataByLevel[levelTermKey].courses; labData = coursesDataByLevel[levelTermKey].labs; }
    
    // Get approved user-uploaded resources for this level and term
    // Convert both to strings for consistent comparison
    const approvedUploads = resources.filter(r => {
        const rLevel = String(r.level);
        const rTerm = String(r.term);
        const levelCompare = String(level);
        const termCompare = String(term);
        const isMatch = rLevel === levelCompare && rTerm === termCompare && r.status === 'approved';
        const isCorrectType = (type === 'labs' && r.resourceType === 'Lab') || (type !== 'labs' && r.resourceType !== 'Lab');
        return isMatch && isCorrectType;
    });
    
    // Add user uploads to the course/lab data
    const data = type === 'labs' ? labData : courseData;
    
    // Merge approved uploads into the data
    const mergedData = [...data];
    approvedUploads.forEach(upload => {
        // Check if this course already exists
        const existingIndex = mergedData.findIndex(d => d.name === upload.courseCode);
        if (existingIndex === -1) {
            // Add new course/lab from upload
            mergedData.push({
                id: mergedData.length + 1,
                name: upload.courseCode,
                title: upload.courseName,
                isUserUpload: true,
                fileTitle: upload.fileTitle,
                description: upload.description,
                uploadedBy: upload.userName,
                filename: upload.file ? upload.file.filename : null
            });
        } else {
            // Add upload info to existing course
            if (!mergedData[existingIndex].uploads) {
                mergedData[existingIndex].uploads = [];
            }
            mergedData[existingIndex].uploads.push({
                fileTitle: upload.fileTitle,
                description: upload.description,
                uploadedBy: upload.userName,
                filename: upload.file ? upload.file.filename : null
            });
        }
    });
    
    res.json({ success: true, type: type, level: level, term: term, data: mergedData });
});

// GET /api/materials/:type/:level/:term/:courseName/:materialType - NOW RETURNS USER UPLOADS TOO
app.get('/api/materials/:type/:level/:term/:courseName/:materialType', (req, res) => {
    const { level, term, courseName, materialType } = req.params;
    const levelStr = String(level);
    const termStr = String(term);
    
    // Get static materials
    const staticMaterials = materialTypesData[materialType] || [];
    
    // Get approved user uploads for this specific course and material type
    const userUploads = resources.filter(r => {
        const rLevel = String(r.level);
        const rTerm = String(r.term);
        return rLevel === levelStr && 
               rTerm === termStr && 
               r.courseCode === courseName && 
               r.resourceType === materialType &&
               r.status === 'approved';
    }).map(r => ({
        name: r.fileTitle || r.courseCode,
        title: r.description || 'User Upload',
        isUserUpload: true,
        uploadedBy: r.userName,
        filename: r.file ? r.file.filename : null
    }));
    
    // Combine static and user uploads
    const combinedMaterials = [...staticMaterials, ...userUploads];
    
    res.json({ success: true, materialType: materialType, data: combinedMaterials });
});

// POST /api/upload - Handle file upload with multer
app.post('/api/upload', upload.single('file'), (req, res) => {
    const { userId, userName, batch, level, term, courseCode, courseName, resourceType, fileTitle, description } = req.body;
    
    // Get file info if uploaded
    const fileInfo = req.file ? {
        filename: req.file.filename,
        originalName: req.file.originalname,
        size: req.file.size,
        mimetype: req.file.mimetype,
        path: req.file.path
    } : null;

    const newResource = {
        id: resources.length + 1,
        userId,
        userName,
        batch,
        level,
        term,
        courseCode,
        courseName,
        resourceType,
        fileTitle,
        description,
        file: fileInfo,
        uploadedAt: new Date(),
        status: 'pending'
    };

    resources.push(newResource);

    res.json({
        success: true,
        message: fileInfo ? 'File uploaded successfully! It will be reviewed soon.' : 'Resource metadata saved! It will be reviewed soon.',
        resource: newResource
    });
});

// GET /api/resources
app.get('/api/resources', (req, res) => {
    res.json({ success: true, count: resources.length, data: resources });
});

// GET /api/resources/:courseCode
app.get('/api/resources/:courseCode', (req, res) => {
    const { courseCode } = req.params;
    const courseResources = resources.filter(r => r.courseCode === courseCode && r.status === 'approved');
    res.json({ success: true, courseCode: courseCode, count: courseResources.length, data: courseResources });
});

// GET /api/admin/pending-resources
app.get('/api/admin/pending-resources', (req, res) => {
    const pendingResources = resources.filter(r => r.status === 'pending');
    res.json({ success: true, count: pendingResources.length, data: pendingResources });
});

// GET /api/admin/all-resources
app.get('/api/admin/all-resources', (req, res) => {
    res.json({ success: true, count: resources.length, data: resources });
});

// POST /api/admin/review-resource
app.post('/api/admin/review-resource', (req, res) => {
    const { resourceId, status, reviewComment, adminId } = req.body;
    if (!['approved', 'rejected'].includes(status)) return res.status(400).json({ success: false, message: 'Invalid status' });
    const resourceIndex = resources.findIndex(r => r.id === resourceId);
    if (resourceIndex === -1) return res.status(404).json({ success: false, message: 'Resource not found' });
    resources[resourceIndex].status = status;
    resources[resourceIndex].reviewComment = reviewComment || '';
    resources[resourceIndex].reviewedAt = new Date();
    resources[resourceIndex].adminId = adminId || 'admin';
    res.json({ success: true, message: `Resource ${status} successfully`, resource: resources[resourceIndex] });
});

// GET /api/user/my-uploads/:userId
app.get('/api/user/my-uploads/:userId', (req, res) => {
    const { userId } = req.params;
    const userResources = resources.filter(r => r.userId === userId);
    res.json({ success: true, count: userResources.length, data: userResources });
});

// GET /api/resources/approved
app.get('/api/resources/approved', (req, res) => {
    const approvedResources = resources.filter(r => r.status === 'approved');
    res.json({ success: true, count: approvedResources.length, data: approvedResources });
});

// DELETE /api/admin/delete-resource/:id - Admin only endpoint to delete resources
app.delete('/api/admin/delete-resource/:id', (req, res) => {
    const { id } = req.params;
    const resourceIndex = resources.findIndex(r => r.id === parseInt(id));
    if (resourceIndex === -1) return res.status(404).json({ success: false, message: 'Resource not found' });
    
    const deletedResource = resources[resourceIndex];
    
    // Delete the file from filesystem if it exists
    if (deletedResource.file && deletedResource.file.filename) {
        const filePath = path.join(uploadDir, deletedResource.file.filename);
        if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
        }
    }
    
    // Remove from resources array
    resources.splice(resourceIndex, 1);
    
    res.json({ success: true, message: 'Resource deleted successfully', deletedResource: deletedResource });
});

// GET /api/health
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', message: 'ETE Resource Portal API is running', usersCount: users.length, resourcesCount: resources.length });
});

// Catch-all route for SPA - serve index.html for any unknown routes
app.use((req, res) => {
    res.sendFile(path.join(frontendPath, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
