from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/api/*": {
    "origins": ["https://hmh-8138.github.io"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}})

DB_FILE = 'database.db'
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db():
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id TEXT UNIQUE,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            batch TEXT,
            address TEXT,
            password TEXT,
            role TEXT DEFAULT 'student',
            created_at TEXT
        );
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            user_name TEXT,
            batch TEXT,
            level TEXT,
            term TEXT,
            course_code TEXT,
            course_name TEXT,
            resource_type TEXT,
            file_title TEXT,
            description TEXT,
            filename TEXT,
            status TEXT DEFAULT 'pending',
            uploaded_at TEXT,
            reviewed_at TEXT,
            review_comment TEXT,
            admin_id TEXT
        );
    ''')
    db.commit()
    db.close()

init_db()

@app.route('/api/health', methods=['GET'])
def health():
    db = get_db()
    users = db.execute('SELECT COUNT(*) as count FROM users').fetchone()
    resources = db.execute('SELECT COUNT(*) as count FROM resources').fetchone()
    db.close()
    return jsonify({
        'status': 'ok',
        'message': 'ETE Resource Portal API is running',
        'usersCount': users['count'],
        'resourcesCount': resources['count']
    })

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    db = get_db()
    
    try:
        db.execute('INSERT INTO users (user_id, name, email, phone, batch, address, password, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (data['id'], data['name'], data['email'], data.get('phone', ''), 
                    data.get('batch', ''), data.get('address', ''), data['password'], datetime.now().isoformat()))
        db.commit()
        db.close()
        return jsonify({'success': True, 'message': 'Registration successful!', 
                       'user': {'id': data['id'], 'name': data['name'], 'email': data['email']}})
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({'success': False, 'message': 'User already exists'}), 400
    except Exception as e:
        db.close()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE user_id = ?', (data['id'],)).fetchone()
    db.close()
    
    if not user or user['password'] != data['password']:
        return jsonify({'success': False, 'message': 'Invalid ID or password'}), 401
    
    return jsonify({'success': True, 'message': 'Login successful!',
                   'user': {'id': user['user_id'], 'name': user['name'], 'email': user['email'], 'batch': user['batch'], 'role': user['role']}})

@app.route('/api/upload', methods=['POST'])
def upload():
    db = get_db()
    file_obj = request.files.get('file')
    filename = None
    
    if file_obj:
        filename = secure_filename(file_obj.filename)
        file_obj.save(os.path.join(UPLOAD_FOLDER, filename))
    
    db.execute('INSERT INTO resources (user_id, user_name, batch, level, term, course_code, course_name, resource_type, file_title, description, filename, uploaded_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
               (request.form.get('userId'), request.form.get('userName'), request.form.get('batch'),
                request.form.get('level'), request.form.get('term'), request.form.get('courseCode'),
                request.form.get('courseName'), request.form.get('resourceType'), request.form.get('fileTitle'),
                request.form.get('description'), filename, datetime.now().isoformat()))
    db.commit()
    db.close()
    
    return jsonify({'success': True, 'message': 'File uploaded successfully!'})

@app.route('/api/user/my-uploads/<user_id>', methods=['GET'])
def my_uploads(user_id):
    db = get_db()
    resources = db.execute('SELECT * FROM resources WHERE user_id = ? ORDER BY uploaded_at DESC', (user_id,)).fetchall()
    db.close()
    
    data = [dict(r) for r in resources]
    return jsonify({'success': True, 'count': len(data), 'data': data})

@app.route('/api/admin/all-resources', methods=['GET'])
def admin_all_resources():
    db = get_db()
    resources = db.execute('SELECT * FROM resources ORDER BY uploaded_at DESC').fetchall()
    db.close()
    
    data = [dict(r) for r in resources]
    return jsonify({'success': True, 'count': len(data), 'data': data})

@app.route('/api/admin/review-resource', methods=['POST'])
def review_resource():
    data = request.get_json()
    db = get_db()
    
    db.execute('UPDATE resources SET status = ?, review_comment = ?, reviewed_at = ?, admin_id = ? WHERE id = ?',
               (data['status'], data.get('reviewComment', ''), datetime.now().isoformat(), data.get('adminId', 'admin'), data['resourceId']))
    db.commit()
    db.close()
    
    return jsonify({'success': True, 'message': f"Resource {data['status']} successfully"})

@app.route('/api/admin/delete-resource/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    db = get_db()
    resource = db.execute('SELECT * FROM resources WHERE id = ?', (resource_id,)).fetchone()
    
    if not resource:
        db.close()
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    if resource['filename']:
        filepath = os.path.join(UPLOAD_FOLDER, resource['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.execute('DELETE FROM resources WHERE id = ?', (resource_id,))
    db.commit()
    db.close()
    
    return jsonify({'success': True, 'message': 'Resource deleted successfully'})

@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    return app.send_static_file(os.path.join(UPLOAD_FOLDER, filename))

if __name__ == '__main__':
    app.run(debug=False)
