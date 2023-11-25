from flask import Flask, request, jsonify, render_template, Response, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import io
from openpyxl import Workbook
import pandas as pd
import sqlite3
import os

app = Flask(__name__, instance_relative_config=True)

# 경로 지정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'data.db')

app.config['SECRET_KEY'] = 'your_secret_key'  # 세션을 암호화하기 위한 시크릿 키 설정
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # add this line

# Dictionary to store memos (articleId -> memo)
memos = {}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_visit_user'), nullable=False)
    article_id = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.String(255), nullable=False)
    end_time = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)


class ReadArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_read_article_user'), nullable=False)
    article_id = db.Column(db.String(255), nullable=False, unique=True)
    author_info_clicked = db.Column(db.String(255), nullable=False)


class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_memo_user'), nullable=False)
    article_id = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_feedback_user'), nullable=False)
    article_id = db.Column(db.String(255), nullable=False)
    feedback = db.Column(db.String(1000), nullable=False)


# Serve the index.html template
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/preventback')
def preventback():
    return render_template('preventback.html')


@app.route('/end')
def end_page():
    # Visit 테이블에서 방문 기록을 가져옵니다.
    visit_history = Visit.query.filter_by(user_id=session['user_id']).all()

    # ReadArticle 테이블에서 읽은 기사를 가져옵니다.
    read_articles = ReadArticle.query.filter_by(user_id=session['user_id']).all()

    return render_template('end.html', visit_history=visit_history, read_articles=read_articles)


# Serve the styles.css file as a static file
@app.route('/static/styles.css')
def serve_styles():
    return app.send_static_file('styles.css')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return render_template('register.html', message='Please provide both username and password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', message='Username already exists')

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            session['user_name'] = user.username  # Save username in session
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid username or password')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


# Add a login check decorator to protect routes that require authentication
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/article<int:article_num>')
def article(article_num):
    return render_template(f'/article/article{article_num}.html')


@app.route('/record', methods=['POST'])
 
def record():
    data = request.get_json()
    article_id = data['article_id']
    start_time = data['start_time']
    end_time = data['end_time']
    duration = data['duration']

    # duration을 정수로 저장
    visit = Visit(user_id=session['user_id'], article_id=article_id, start_time=start_time, end_time=end_time,
                  duration=duration)

    db.session.add(visit)
    db.session.commit()

    return jsonify(message='Visit recorded successfully'), 200


@app.route('/mark-as-read', methods=['POST'])
 
def mark_as_read():
    try:
        data = request.get_json()
        article_id = data.get('articleId')
        new_author_info = data.get('authorInfoClicked')

        if not article_id:
            return jsonify({'message': 'articleId is required'}), 400

        # Check if the article has already been marked as read.
        existing_record = ReadArticle.query.filter_by(user_id=session['user_id'], article_id=article_id).first()

        if existing_record:
            # Compare the existing authorInfoClicked with the new value.
            if existing_record.author_info_clicked != new_author_info:
                # Update authorInfoClicked if there is a change.
                existing_record.author_info_clicked = new_author_info
                db.session.commit()

            return jsonify({'message': 'Article already marked as read'}), 200

        # If the article is not marked as read, create a new record.
        new_read_article = ReadArticle(user_id=session['user_id'], article_id=article_id,
                                       author_info_clicked=new_author_info)
        db.session.add(new_read_article)
        db.session.commit()

        return jsonify({'message': 'Article marked as read'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


# memo ----------------------------------------
@app.route('/save-memo', methods=['POST'])
 
def save_memo():
    data = request.get_json()
    article_id = data['articleId']
    memo_content = data['memo']

    # Create a new Memo instance and save it to the database
    memo = Memo(user_id=session['user_id'], article_id=article_id, content=memo_content)
    db.session.add(memo)
    db.session.commit()

    return jsonify({'message': 'Memo saved successfully'}), 200


@app.route('/get-memo', methods=['GET'])
 
def get_memo():
    article_id = request.args.get('articleId')
    memos_for_article = Memo.query.filter_by(user_id=session['user_id'], article_id=article_id).all()

    # Extract memo content and timestamps
    memo_data = [{'content': memo.content, 'timestamp': memo.timestamp} for memo in memos_for_article]

    return jsonify(memo_data), 200


@app.route('/get-all-memos', methods=['GET'])
 
def get_all_memos():
    all_memos = Memo.query.filter_by(user_id=session['user_id']).all()

    # Extract memo content, timestamps, and articleId
    memo_data = [{'articleId': memo.article_id, 'content': memo.content, 'timestamp': memo.timestamp} for memo in
                 all_memos]

    return jsonify(memo_data), 200


# ----------------------------------------------

# Feedback
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()
        article_id = data['articleId']
        feedback_text = data['feedback']

        # Save the feedback to the Feedback table in the database
        feedback_entry = Feedback(user_id=session['user_id'], article_id=article_id, feedback=feedback_text)
        db.session.add(feedback_entry)
        db.session.commit()

        # Return a JSON response instead of redirecting
        return jsonify({'message': 'Feedback submitted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/export-to-excel')
def export_to_excel():
    try:
        # Connect to your SQLite database
        db_path = os.path.join(app.instance_path, 'data.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Define the tables you want to export
        table_names = ['visit', 'memo', 'read_article', 'feedback']  # Replace with your table names

        # Create an Excel Workbook
        wb = Workbook()
        wb.save('output.xlsx')

        # Get unique user_ids and usernames
        users = db.session.query(User.id, User.username).distinct().all()

        for user_id, username in users:
            for table_name in table_names:
                # Execute a query to retrieve data from your database
                cursor.execute(f'SELECT * FROM {table_name} WHERE user_id = ?', (user_id,))
                data = cursor.fetchall()

                # Create a DataFrame from the retrieved data
                df = pd.DataFrame(data, columns=[description[0] for description in cursor.description])

                # Create an Excel writer for the current table
                writer = pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='a')
                df.to_excel(writer, sheet_name=f'{table_name}_{username}', index=False)
                writer.close()  # Close the ExcelWriter object

        # Create an in-memory buffer to save the Excel file
        output = io.BytesIO()
        with open('output.xlsx', 'rb') as f:
            output.write(f.read())
        output.seek(0)

        # Prepare the response with appropriate headers
        response = Response(output.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response.headers['Content-Disposition'] = 'attachment; filename=data.xlsx'

        return response

    except Exception as e:
        return str(e)




# Create the database tables within an application context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
