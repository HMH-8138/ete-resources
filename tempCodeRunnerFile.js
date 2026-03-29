const express = require('express');
const app = express();
const port = 3000;

// Middleware to parse JSON
app.use(express.json());

// Test route
app.get('/', (req, res) => {
    res.send('Hello from backend!');
});

// Example: Users array
let users = [
    { id: 1, name: 'Meherab', email: 'meherab@example.com' },
    { id: 2, name: 'Ali', email: 'ali@example.com' }
];

// GET all users
app.get('/users', (req, res) => {
    res.json(users);
});

// GET single user by id
app.get('/users/:id', (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));
    if (!user) return res.status(404).send('User not found');
    res.json(user);
});

// POST new user
app.post('/users', (req, res) => {
    const newUser = {
        id: users.length + 1,
        name: req.body.name,
        email: req.body.email
    };
    users.push(newUser);
    res.status(201).json(newUser);
});

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});