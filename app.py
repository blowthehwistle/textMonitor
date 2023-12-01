from flask import Flask, flash, request, jsonify, render_template, Response, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKeyConstraint
from flask_migrate import Migrate
from datetime import datetime
import io
from openpyxl import Workbook
import pandas as pd
import sqlite3
import os
import traceback
import logging



app = Flask(__name__, instance_relative_config=True)


# 경로 지정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'data.db')

app.config['SECRET_KEY'] = 'your_secret_key'  # 세션을 암호화하기 위한 시크릿 키 설정
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # add this line

app.logger.setLevel(logging.INFO)

# Dictionary to store memos (articleId -> memo)
memos = {}

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(100))  # 저자 이름
    author_occupation = db.Column(db.String(100))  # 저자 직업
    author_email = db.Column(db.String(100))  # 저자 이메일
    author_description = db.Column(db.Text)  # 저자 설명
    ratings = db.relationship('Rating', backref='article', lazy=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_rating_user'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', name='fk_rating_article'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('ratings', lazy=True))




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



@app.errorhandler(403)
def handle_403_error(error):
    app.logger.error('403 error occurred: %s', error)
    return '403 error', 403

# Serve the index.html template
@app.route('/')
def home():
    return redirect(url_for('login')) 

@app.route('/index')
def index():
    articles = Article.query.all()  # 모든 기사를 조회
    return render_template('index.html', articles=articles)  # `articles` 변수를 템플릿에 전달


@app.route('/preventback')
def preventback():
    return render_template('preventback.html')


@app.route('/end')
def end_page():
    # Visit 테이블에서 방문 기록을 가져옵니다.
    visit_history = Visit.query.filter_by(user_id=session['user_id']).all()

    # ReadArticle 테이블에서 읽은 기사를 가져옵니다.
    read_articles = ReadArticle.query.filter_by(user_id=session['user_id']).all()
    articles = Article.query.all()

    return render_template('end.html', visit_history=visit_history, read_articles=read_articles, articles=articles)


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
    return redirect(url_for('login'))


# Add a login check decorator to protect routes that require authentication
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function




@app.route('/article/<int:article_id>')
def article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('/article/article.html', article=article)

@app.route('/edit_article', methods=['GET', 'POST'], defaults={'article_id': None})
@app.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    articles = Article.query.all()  # 모든 기사를 조회
    article = db.session.query(Article).get(article_id) if article_id else None  # 선택한 기사를 조회

    if request.method == 'POST':
        # 제목, 내용, 저자 정보를 수정하고 저장
        article.title = request.form.get('title')
        article.content = request.form.get('content')
        article.author_name = request.form.get('author_name')
        article.author_occupation = request.form.get('author_occupation')
        article.author_email = request.form.get('author_email')
        article.author_description = request.form.get('author_description')
        db.session.commit()

        # 수정이 완료되면 기사 목록 페이지로 리다이렉트
        return redirect(url_for('index'))

    return render_template('/article/edit_article.html', articles=articles, article=article)


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


@app.route('/rate', methods=['POST'])
def rate_article():
    try:
        all_article_ids = [article.id for article in Article.query.with_entities(Article.id).all()]
        user_id = session['user_id'] 
        print(all_article_ids)
        print(user_id)
        for article_id in all_article_ids:
            rating = request.form.get('rating_{}'.format(article_id))

            if rating is None:
                continue

            existing_rating = Rating.query.filter_by(article_id=article_id, user_id=user_id).first()

            if existing_rating is None:
                new_rating = Rating(article_id=article_id, rating=rating, user_id=user_id)
                db.session.add(new_rating)
            else:
                existing_rating.rating = rating

        db.session.commit()

        return redirect(url_for('end_page'))
    except Exception as e:
        return traceback.format_exc()


@app.route('/export-to-excel')
def export_to_excel():
    try:
        # Connect to your SQLite database
        db_path = os.path.join(app.instance_path, 'data.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Define the tables you want to export
        table_names = ['visit', 'memo', 'read_article', 'feedback', 'rating' ] 

        # Get unique user_ids and usernames
        users = db.session.query(User.id, User.username).distinct().all()

        # Create an Excel writer
        writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')

        for user_id, username in users:
            # Create a sheet for the user
            writer.book.create_sheet(username)

            start_row = 0
            start_col = 1  # 추가: 시작 열 설정
            has_data = False  # To check if the user has any data

            for table_name in table_names:
                # Execute a query to retrieve data from your database
                cursor.execute(f'SELECT * FROM {table_name} WHERE user_id = ?', (user_id,))
                data = cursor.fetchall()

                # Check if data is not empty
                if data:
                    has_data = True  # User has data

                    # Create a DataFrame from the retrieved data
                    df = pd.DataFrame(data, columns=[description[0] for description in cursor.description])

                    # Write table name above the table data
                    writer.sheets[username].cell(row=start_row + 1, column=start_col, value=table_name)  # 수정: 시작 열을 고려

                    # Write DataFrame to Excel with specified startrow and startcol
                    df.to_excel(writer, sheet_name=username, startrow=start_row + 1, startcol=start_col - 1, index=False)  # 수정: 시작 열을 고려

                    # Update start_row for next table
                    start_row += df.shape[0] + 3  # Leave a blank row between tables and the table name
            
            # 추가: 'article' 테이블 따로 처리
            cursor.execute('SELECT id, title, content FROM article')  # 수정: id, title, content 컬럼만 선택
            data = cursor.fetchall()
            if data:
                df = pd.DataFrame(data, columns=['id', 'title', 'content'])  # 수정: 컬럼 이름 지정
                writer.sheets[username].cell(row=1, column=10, value='article')  # 시작 열을 10으로 설정
                df.to_excel(writer, sheet_name=username, startrow=1, startcol=9, index=False)  # 시작 열을 10으로 설정

            # If the user has no data, remove the created sheet
            if not has_data and username in writer.sheets:
                del writer.sheets[username]

        # Close the ExcelWriter object
        writer.close()

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
        return traceback.format_exc()






@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    try:
        # Connect to your SQLite database
        db_path = os.path.join(app.instance_path, 'data.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Define the tables you want to clear
        table_names = ['visit', 'memo', 'read_article', 'feedback', 'rating']

        for table_name in table_names:
            # Execute a query to delete all data from the table
            cursor.execute(f'DELETE FROM {table_name}')

        # For 'user' table, delete all users except 'admin'
        cursor.execute("DELETE FROM user WHERE username != 'admin'")

        # Commit the changes
        conn.commit()

        # Remove the existing 'output.xlsx' file if it exists
        if os.path.exists('output.xlsx'):
            os.remove('output.xlsx')

        # Create a new 'output.xlsx' file
        with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
            # Add a blank sheet
            df = pd.DataFrame()
            df.to_excel(writer, sheet_name='Sheet1')
        # Send a one-time message
        flash("초기화가 성공적으로 완료되었습니다.")

        # Redirect to the index page
        return redirect(url_for('index'))

    except Exception as e:
        return str(e)

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Title and Content are required!')
            return render_template('add_article.html')

        article = Article(title=title, content=content)
        db.session.add(article)
        db.session.commit()

        return redirect(url_for('edit_article'))

    return render_template('add_article.html')


@app.route('/delete_article/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()

    return redirect(url_for('edit_article'))



@app.cli.command("create_articles")
def create_articles():
    for i in range(1, 9):
        new_article = Article(title=f'제목{i}', content=f'내용{i}')
        db.session.add(new_article)
    db.session.commit()
    print("Articles created successfully.")


# Create the database tables within an application context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
