const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const session = require('express-session');
const path = require('path');

const app = express();
const PORT = 3000;

// Middlewares
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(session({
  secret: 'secretKey',
  resave: false,
  saveUninitialized: true
}));

// Serve static files (like homepage.html) from the current directory
app.use(express.static(__dirname));

// Database connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'AdityaK@024',
  database: 'farming_db'
});

db.connect(err => {
  if (err) {
    console.error('❌ MySQL connection error:', err.message);
    process.exit(1);
  }
  console.log('💚 Connected to MySQL');
});

// Create users table
db.query(`
  CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    DOB DATE,
    gender ENUM('male','female','other'),
    password VARCHAR(255)
  )
`);

// Create contacts table
db.query(`
  CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    subject VARCHAR(255),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
`);

// ✨ SIGNUP route
app.post('/signup', (req, res) => {
  const { name, email, DOB, gender, password } = req.body;

  bcrypt.hash(password, 10, (err, hashedPassword) => {
    if (err) return res.status(500).json({ message: 'Error hashing password', err });

    const sql = `INSERT INTO users (name, email, DOB, gender, password) VALUES (?, ?, ?, ?, ?)`;
    db.query(sql, [name, email, DOB, gender, hashedPassword], (err, result) => {
      if (err) {
        if (err.code === 'ER_DUP_ENTRY') {
          return res.status(400).json({ message: 'Email already registered!' });
        }
        return res.status(500).json({ message: 'Database error', err });
      }
      res.status(201).json({ message: 'Account created successfully!' });
    });
  });
});

// ✨ LOGIN route with redirect
app.post('/login', (req, res) => {
  const { identifier, password } = req.body;

  db.query('SELECT * FROM users WHERE email = ?', [identifier], (err, results) => {
    if (err) return res.status(500).json({ message: 'DB Error', err });
    if (results.length === 0) return res.status(404).json({ message: 'User not found' });

    const user = results[0];
    bcrypt.compare(password, user.password, (err, match) => {
      if (err) return res.status(500).json({ message: 'Error', err });
      if (!match) return res.status(401).json({ message: 'Invalid password' });

      req.session.isLoggedIn = true;
      req.session.userId = user.id;

      // If it's an AJAX login (client fetch), send redirect URL
      res.status(200).json({ message: 'Login successful', redirect: '/homepage.html' });
    });
  });
});

// ✨ CONTACT US route
app.post('/contactus', (req, res) => {
  const { name, email, subject, message } = req.body;

  db.query(
    'INSERT INTO contacts (name, email, subject, message) VALUES (?, ?, ?, ?)',
    [name, email, subject, message],
    (err, result) => {
      if (err) return res.status(500).json({ message: 'DB Error', err });
      res.status(201).json({ message: 'Message sent successfully!' });
    }
  );
});

// Start the server
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
