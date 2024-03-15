from flask import Flask, render_template, request, redirect, url_for,session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/result_management"
mongo = PyMongo(app)

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Faculty registration route
@app.route('/faculty_register', methods=['GET', 'POST'])
def faculty_register():
    if request.method == 'POST':
        username = request.form['username']
        faculty_id = request.form['faculty_id']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            hashed_password = generate_password_hash(password)
            # Insert faculty data into MongoDB
            mongo.db.faculty.insert_one({
                'username': username,
                'faculty_id': faculty_id,
                'mobile': mobile,
                'email': email,
                'password': hashed_password
            })
            return render_template('index.html')
        else:
            return 'Passwords do not match'
    return render_template('faculty_register.html')

# Admin registration route
@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        admin_id = request.form['admin_id']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            hashed_password = generate_password_hash(password)
            # Insert admin data into MongoDB
            mongo.db.admin.insert_one({
                'username': username,
                'admin_id': admin_id,
                'mobile': mobile,
                'email': email,
                'password': hashed_password
            })
            return render_template('index.html')
        else:
            return 'Passwords do not match'
    return render_template('admin_register.html')

# Student registration route
@app.route('/student_register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['username']
        roll_number = request.form['roll_number']
        parent_name = request.form['parent_name']
        parent_mobile = request.form['parent_mobile']
        dob = request.form['dob']
        year = request.form['year']
        branch = request.form['branch']
        student_mobile = request.form['student_mobile']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            hashed_password = generate_password_hash(password)
            # Insert student data into MongoDB
            mongo.db.student.insert_one({
                'full_name': full_name,
                'username': username,
                'roll_number': roll_number,
                'parent_name': parent_name,
                'parent_mobile': parent_mobile,
                'dob': dob,
                'year': year,
                'branch': branch,
                'student_mobile': student_mobile,
                'email': email,
                'password': hashed_password
            })
            return render_template('index.html')
        else:
            return 'Passwords do not match'
    return render_template('student_regsiter.html')


# Admin dashboard route
@app.route('/faculty_login', methods=['GET', 'POST'])
def faculty_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        faculty = mongo.db.faculty.find_one({'username': username})

        if faculty and check_password_hash(faculty['password'], password):
            #session['username'] = username
            return render_template('faculty_login.html')
        else:
            return 'Invalid login credentials'
    return render_template('faculty_login.html')

# Admin login route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = mongo.db.admin.find_one({'username': username})

        if admin and check_password_hash(admin['password'], password):
            #session['username'] = username
            return render_template('admin_dashboard.html')
        else:
            return 'Invalid login credentials'
    return render_template('admin_dashboard.html')

# Student login route
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        #roll_number = request.form['roll_number']
        password = request.form['password']
        student = mongo.db.student.find_one({'username': username})

        if student and check_password_hash(student['password'], password):
            #session['full_name'] = full_name
            return render_template('student_login.html')
        else:
            return 'Invalid login credentials'
    return render_template('student_login.html')
@app.route('/add', methods=['GET','POST'])
def add():
   return render_template('add_result.html')
@app.route('/add_result', methods=['GET','POST'])
def add_result():
    if request.method == 'POST':
        # Retrieve form data
        student_name = request.form['student_name']
        username = request.form['username']
        student_roll = request.form['student_roll']
        year = request.form['year']
        branch = request.form['branch']
        semester = request.form['semester']
        subject1 = request.form['subject1']
        subject2 = request.form['subject2']
        subject3 = request.form['subject3']
        subject4 = request.form['subject4']
        subject5 = request.form['subject5']

        # Create a document to insert into the database
        result_data = {
            'student_name': student_name,
            'username' : username,
            'student_roll': student_roll,
            'year': year,
            'branch': branch,
            'semester': semester,
            'subject1': subject1,
            'subject2': subject2,
            'subject3': subject3,
            'subject4': subject4,
            'subject5': subject5
        }

        # Insert the document into the collection
        mongo.db.result.insert_one(result_data)

        # Redirect to the add result page after submission
        return render_template('index.html')
    return render_template('add_result.html')

@app.route('/retrieve_result', methods=['GET','POST'])
def retrieve_result():
    if request.method == 'POST':
        student_roll = request.form['student_roll']
        result = mongo.db.result.find_one({'student_roll': student_roll})
        if result:
            return f"Student Name: {result['student_name']}<br>" \
                   f"Year: {result['year']}<br>" \
                   f"Branch: {result['branch']}<br>" \
                   f"Semester: {result['semester']}<br>" \
                   f"Subject 1: {result['subject1']}<br>" \
                   f"Subject 2: {result['subject2']}<br>" \
                   f"Subject 3: {result['subject3']}<br>" \
                   f"Subject 4: {result['subject4']}<br>" \
                   f"Subject 5: {result['subject5']}<br>"
        else:
            return "No result found for the provided roll number."
    return render_template('retrieve_result.html')
@app.route('/retrieve_student', methods=['GET','POST'])
def retrieve_student():
    if request.method == 'POST':
        username = request.form['username']
        student_roll = request.form['student_roll']
        password = request.form['password']
        result = mongo.db.result.find_one({'student_roll': student_roll})
        if result:
            return f"Student Name: {result['student_name']}<br>" \
                   f"Year: {result['year']}<br>" \
                   f"Branch: {result['branch']}<br>" \
                   f"Semester: {result['semester']}<br>" \
                   f"Subject 1: {result['subject1']}<br>" \
                   f"Subject 2: {result['subject2']}<br>" \
                   f"Subject 3: {result['subject3']}<br>" \
                   f"Subject 4: {result['subject4']}<br>" \
                   f"Subject 5: {result['subject5']}<br>"
        else:
            return "No result found for the provided roll number."
    return render_template('retrieve_student.html')
@app.route('/admin_dashboard',methods=['GET','POST'])
def admin_dashboard():
        faculty_data = mongo.db.faculty.find()
        student_data = mongo.db.student.find()
        return render_template('admin_dashboard.html', faculty_data=faculty_data, student_data=student_data)
@app.route('/delete_user/<user_type>/<user_id>', methods=['GET', 'POST'])
def delete_user(user_type, user_id):
    if 'username' in session:  # Check if the admin is logged in
        # Delete user logic based on user type and user ID
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('admin_login'))  # Redirect to admin login if not logged in
if __name__ == '__main__':
    app.run(debug=True)
