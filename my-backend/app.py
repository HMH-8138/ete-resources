from flask import Flask, request, jsonify, send_from_directory
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
    
    data = []
    for r in resources:
        resource_dict = dict(r)
        # Convert snake_case to camelCase for frontend compatibility
        converted = {
            'id': resource_dict['id'],
            'userId': resource_dict['user_id'],
            'userName': resource_dict['user_name'],
            'batch': resource_dict['batch'],
            'level': resource_dict['level'],
            'term': resource_dict['term'],
            'courseCode': resource_dict['course_code'],
            'courseName': resource_dict['course_name'],
            'resourceType': resource_dict['resource_type'],
            'fileTitle': resource_dict['file_title'],
            'description': resource_dict['description'],
            'file': {'filename': resource_dict['filename']} if resource_dict['filename'] else None,
            'status': resource_dict['status'],
            'uploadedAt': resource_dict['uploaded_at'],
            'reviewedAt': resource_dict['reviewed_at'],
            'reviewComment': resource_dict['review_comment'],
            'adminId': resource_dict['admin_id']
        }
        data.append(converted)
    
    return jsonify({'success': True, 'count': len(data), 'data': data})

@app.route('/api/admin/all-resources', methods=['GET'])
def admin_all_resources():
    db = get_db()
    resources = db.execute('SELECT * FROM resources ORDER BY uploaded_at DESC').fetchall()
    db.close()
    
    data = []
    for r in resources:
        resource_dict = dict(r)
        # Convert snake_case to camelCase for frontend compatibility
        converted = {
            'id': resource_dict['id'],
            'userId': resource_dict['user_id'],
            'userName': resource_dict['user_name'],
            'batch': resource_dict['batch'],
            'level': resource_dict['level'],
            'term': resource_dict['term'],
            'courseCode': resource_dict['course_code'],
            'courseName': resource_dict['course_name'],
            'resourceType': resource_dict['resource_type'],
            'fileTitle': resource_dict['file_title'],
            'description': resource_dict['description'],
            'file': {'filename': resource_dict['filename']} if resource_dict['filename'] else None,
            'status': resource_dict['status'],
            'uploadedAt': resource_dict['uploaded_at'],
            'reviewedAt': resource_dict['reviewed_at'],
            'reviewComment': resource_dict['review_comment'],
            'adminId': resource_dict['admin_id']
        }
        data.append(converted)
    
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

# Course and Lab data structure
COURSES_DATA = {
    '1-1': {
        'courses': [
            {'name': 'EEE 181', 'title': 'Basic Electrical Engineering'},
            {'name': 'MATH 181', 'title': 'Differential and Integral Calculus'},
            {'name': 'MATH 183', 'title': 'Ordinary & Partial Differential Equations and Matrix'},
            {'name': 'CHEM 181', 'title': 'Chemistry'},
            {'name': 'HUM 181', 'title': 'Technical English'}
        ],
        'labs': [
            {'name': 'EEE 182', 'title': 'Basic Electrical Engineering Sessional'},
            {'name': 'CHEM 182', 'title': 'Chemistry Sessional'},
            {'name': 'ME 182', 'title': 'Mechanical Engineering Drawing'}
        ]
    },
    '1-2': {
        'courses': [
            {'name': 'ETE 101', 'title': 'Electronics-I'},
            {'name': 'EEE 183', 'title': 'Fundamentals of Electrical Machines'},
            {'name': 'PHY 181', 'title': 'Engineering Physics'},
            {'name': 'MATH 185', 'title': 'Vector Analysis and Operational Calculus'},
            {'name': 'CSE 181', 'title': 'Computer Programming and Numerical Analysis'}
        ],
        'labs': [
            {'name': 'ETE 102', 'title': 'Electronics-I Sessional'},
            {'name': 'EEE 184', 'title': 'Fundamentals of Electrical Machines Sessional'},
            {'name': 'PHY 182', 'title': 'Engineering Physics Sessional'},
            {'name': 'CSE 182', 'title': 'Computer Programming and Numerical Analysis Sessional'}
        ]
    },
    '2-1': {
        'courses': [
            {'name': 'ETE 201', 'title': 'Electronics-II'},
            {'name': 'ETE 203', 'title': 'Signals and Systems'},
            {'name': 'CSE 281', 'title': 'Data Structures and Algorithms'},
            {'name': 'MATH 281', 'title': 'Engineering Statistics and Complex Variables'},
            {'name': 'HUM 281', 'title': 'Financial Accounting and Management'}
        ],
        'labs': [
            {'name': 'ETE 202', 'title': 'Electronics-II Sessional'},
            {'name': 'ETE 204', 'title': 'Signals and Systems Sessional'},
            {'name': 'CSE 282', 'title': 'Data Structures and Algorithms Sessional'}
        ]
    },
    '2-2': {
        'courses': [
            {'name': 'ETE 205', 'title': 'Digital Logic Design'},
            {'name': 'ETE 207', 'title': 'Electromagnetic Fields and Waves'},
            {'name': 'ETE 209', 'title': 'Analog Communications'},
            {'name': 'ETE 211', 'title': 'Control System Engineering'},
            {'name': 'CSE 284', 'title': 'Object Oriented Programming'},
            {'name': 'HUM 283', 'title': 'Economics and Sociology'}
        ],
        'labs': [
            {'name': 'ETE 206', 'title': 'Digital Logic Design Sessional'},
            {'name': 'ETE 210', 'title': 'Analog Communications Sessional'},
            {'name': 'ETE 212', 'title': 'Control System Engineering Sessional'}
        ]
    },
    '3-1': {
        'courses': [
            {'name': 'ETE 301', 'title': 'Semiconductor Physics & Devices'},
            {'name': 'ETE 303', 'title': 'Industrial Electronics'},
            {'name': 'ETE 305', 'title': 'Digital Communication'},
            {'name': 'ETE 307', 'title': 'Microwave and Antenna Engineering'},
            {'name': 'ETE 309', 'title': 'Digital Signal Processing'}
        ],
        'labs': [
            {'name': 'ETE 304', 'title': 'Industrial Electronics Sessional'},
            {'name': 'ETE 306', 'title': 'Digital Communication Sessional'},
            {'name': 'ETE 308', 'title': 'Microwave and Antenna Engineering Sessional'},
            {'name': 'ETE 310', 'title': 'Digital Signal Processing Sessional'},
            {'name': 'CSE 380', 'title': 'Internet Programming'}
        ]
    },
    '3-2': {
        'courses': [
            {'name': 'ETE 300', 'title': 'Electronic System Design and Project'},
            {'name': 'ETE 311', 'title': 'Information Theory and Coding'},
            {'name': 'ETE 313', 'title': 'Electronic Measurement and Instrumentation'},
            {'name': 'ETE 315', 'title': 'Computer Communications and Networks'},
            {'name': 'ETE 317', 'title': 'Power System for Communication Engineering'},
            {'name': 'ETE 319', 'title': 'Microprocessor and Microcontroller'}
        ],
        'labs': [
            {'name': 'ETE 314', 'title': 'Electronic Measurement and Instrumentation Sessional'},
            {'name': 'ETE 316', 'title': 'Computer Communications and Networks Sessional'},
            {'name': 'ETE 318', 'title': 'Power System for Communication Engineering Sessional'},
            {'name': 'ETE 320', 'title': 'Microprocessor and Microcontroller Sessional'}
        ]
    },
    '4-1': {
        'courses': [
            {'name': 'ETE 400', 'title': 'Project and Thesis'},
            {'name': 'ETE 480', 'title': 'Industrial Training (2 Weeks)'},
            {'name': 'ETE 401', 'title': 'Telecommunication Networks and Switching'},
            {'name': 'ETE 403', 'title': 'VLSI Technology'},
            {'name': 'ETE 405', 'title': 'Wireless and Mobile Communication'},
            {'name': 'ETE 407', 'title': 'Multimedia Communication'},
            {'name': 'ETE *', 'title': 'Elective I'}
        ],
        'labs': [
            {'name': 'ETE 402', 'title': 'Telecommunication Networks and Switching Sessional'},
            {'name': 'ETE 404', 'title': 'VLSI Technology Sessional'},
            {'name': 'ETE 406', 'title': 'Wireless and Mobile Communication Sessional'},
            {'name': 'ETE 408', 'title': 'Multimedia Communication Sessional'},
            {'name': 'ETE +++', 'title': 'Sessional based on ETE***'}
        ]
    },
    '4-2': {
        'courses': [
            {'name': 'ETE 400', 'title': 'Project and Thesis'},
            {'name': 'ETE 411', 'title': 'Optical Fiber Communications'},
            {'name': 'ETE 413', 'title': 'Satellite Communications and RADAR'},
            {'name': 'ETE 415', 'title': 'IoT and Industrial Automation'},
            {'name': 'ETE 417', 'title': 'Engineering Ethics and Entrepreneurship'},
            {'name': 'ETE ^^^', 'title': 'Elective II'}
        ],
        'labs': [
            {'name': 'ETE 412', 'title': 'Optical Fiber Communications Sessional'},
            {'name': 'ETE 414', 'title': 'Satellite Communications and RADAR Sessional'},
            {'name': 'ETE 416', 'title': 'IoT and Industrial Automation Sessional'},
            {'name': 'ETE ***', 'title': 'Sessional Based on ETE^^^'}
        ]
    }
}

@app.route('/api/materials/<material_type>/<level>/<term>', methods=['GET'])
def get_materials_list(material_type, level, term):
    """Get list of courses or labs for a given level and term"""
    key = f"{level}-{term}"
    
    if key not in COURSES_DATA:
        return jsonify({'success': False, 'message': 'Invalid level or term'}), 400
    
    data = COURSES_DATA[key]
    items = data.get(material_type + 's' if material_type == 'lab' else material_type, [])
    
    return jsonify({'success': True, 'data': items})

@app.route('/api/materials/<material_type>/<level>/<term>/<course_name>/<resource_type>', methods=['GET'])
def get_materials_by_type(material_type, level, term, course_name, resource_type):
    """Get approved resources by material type, level, term, course, and resource type"""
    db = get_db()
    
    resources = db.execute(
        'SELECT * FROM resources WHERE level = ? AND term = ? AND course_code = ? AND resource_type = ? AND status = "approved" ORDER BY uploaded_at DESC',
        (level, term, course_name, resource_type)
    ).fetchall()
    db.close()
    
    data = []
    for r in resources:
        resource_dict = dict(r)
        converted = {
            'id': resource_dict['id'],
            'fileTitle': resource_dict['file_title'],
            'fileName': resource_dict['filename'],
            'description': resource_dict['description'],
            'uploadedBy': resource_dict['user_name'],
            'batch': resource_dict['batch'],
            'uploadedAt': resource_dict['uploaded_at'],
            'file': {'filename': resource_dict['filename']} if resource_dict['filename'] else None
        }
        data.append(converted)
    
    return jsonify({'success': True, 'count': len(data), 'data': data})

@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(os.path.abspath(UPLOAD_FOLDER), filename)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)
