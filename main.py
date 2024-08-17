from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:supersecuritypassword@postgres_db:5432/appsec_db'
db = SQLAlchemy(app)

class AppSec(db.Model):
    name = db.Column(db.String, primary_key=True, nullable=False)
    description = db.Column(db.JSON, nullable=False)

with app.app_context():
    db.create_all()

    if AppSec.query.count() == 0:
        practices = [
            AppSec(name='practice_sast', description={
                'name': 'Static Application Security Testing (SAST)',
                'description': 'Static Application Security Testing (SAST) is a testing methodology where the code is analyzed for vulnerabilities without executing the program.'
            }),
            AppSec(name='practice_dast', description={
                'name': 'Dynamic Application Security Testing (DAST)',
                'description': 'Dynamic Application Security Testing (DAST) is a testing methodology where the application is tested for vulnerabilities while it is running.'
            }),
            AppSec(name='practice_iast', description={
                'name': 'Interactive Application Security Testing (IAST)',
                'description': 'Interactive Application Security Testing (IAST) is a testing methodology that combines elements of SAST and DAST to identify vulnerabilities during runtime with more context about the application.'
            })
        ]
        db.session.bulk_save_objects(practices)
        db.session.commit()


def create_tables():
    db.create_all()
    if AppSec.query.count() == 0:
        practices = [
            AppSec(name='practice_sast', description={
                'name': 'Static Application Security Testing (SAST)',
                'description': 'Static Application Security Testing (SAST) is a testing methodology where the code is analyzed for vulnerabilities without executing the program.'
            }),
            AppSec(name='practice_dast', description={
                'name': 'Dynamic Application Security Testing (DAST)',
                'description': 'Dynamic Application Security Testing (DAST) is a testing methodology where the application is tested for vulnerabilities while it is running.'
            }),
            AppSec(name='practice_iast', description={
                'name': 'Interactive Application Security Testing (IAST)',
                'description': 'Interactive Application Security Testing (IAST) is a testing methodology that combines elements of SAST and DAST to identify vulnerabilities during runtime with more context about the application.'
            })
        ]
        try:
            db.session.bulk_save_objects(practices)
            db.session.commit()
            print("Initial data inserted successfully")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while inserting initial data: {e}")

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'admin':
            return redirect(url_for('correct'))
        else:
            return redirect(url_for('incorrect'))

    return render_template('login.html')

@app.route('/correct')
def correct():
    return render_template('correct.html')

@app.route('/incorrect')
def incorrect():
    return render_template('incorrect.html')

@app.route('/appsec')
def appsec():
    key = request.args.get('key')

    if key == 'practice_main':
        return render_template('appsec.html')

    practice = AppSec.query.filter_by(name=key).first()
    if practice:
        practice_data = {
            'name': practice.name,
            'description': practice.description
        }
        return jsonify(practice_data)
    else:
        return jsonify({'error': 'Invalid key'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
