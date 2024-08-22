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
import random
import json
import re
import zipfile


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
    display_on_index = db.Column(db.Boolean, default=False)
    ratings = db.relationship('Rating', backref='article', lazy=True)

class ArticleDisplay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)  # 위치를 저장

    user = db.relationship('User', backref=db.backref('article_displays', lazy=True))
    article = db.relationship('Article', backref=db.backref('article_displays', lazy=True))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    article_order = db.Column(db.String(255), nullable=True)

    def set_article_order(self, order):
        self.article_order = json.dumps(order)

    def get_article_order(self):
        return json.loads(self.article_order)

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
    author_info_clicked = db.Column(db.Boolean, default=False)  # 추가된 필드

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
    user = User.query.get(session['user_id'])
    
    # 사용자의 기사 디스플레이 데이터를 가져옴
    article_displays = ArticleDisplay.query.filter_by(user_id=user.id).order_by(ArticleDisplay.position).all()

    # 만약 사용자가 기사 디스플레이 데이터를 갖고 있지 않다면, 새로운 데이터를 생성
    if not article_displays:
        display_articles = Article.query.filter_by(display_on_index=True).all()
        if len(display_articles) > 6:
            display_articles = random.sample(display_articles, 6)

        # 새로 생성한 디스플레이 데이터를 저장
        for idx, article in enumerate(display_articles):
            new_display = ArticleDisplay(user_id=user.id, article_id=article.id, position=idx)
            db.session.add(new_display)
        db.session.commit()
        
        # 디스플레이 데이터를 다시 불러옴
        article_displays = ArticleDisplay.query.filter_by(user_id=user.id).order_by(ArticleDisplay.position).all()

    # 사용자의 기사 디스플레이 순서대로 기사를 가져옴
    articles = [display.article for display in article_displays]
    
    return render_template('index.html', articles=articles)


@app.route('/api/get_data', methods=['GET'])
def get_data():
    try:
        # 데이터베이스에서 모든 기사 조회
        articles = Article.query.all()
        articles_data = []

        # 각 기사를 딕셔너리로 변환하여 리스트에 추가
        for article in articles:
            articles_data.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'author_name': article.author_name,
                'author_occupation': article.author_occupation,
                'author_email': article.author_email,
                'author_description': article.author_description
            })

        # JSON 형식으로 반환
        return jsonify({'articles': articles_data}), 200
    except Exception as e:
        app.logger.error('Error fetching articles: %s', str(e))
        return jsonify({'message': 'Error fetching articles: {}'.format(str(e))}), 500

@app.route('/preventback')
def preventback():
    return render_template('preventback.html')


@app.route('/end')
def end_page():
    # Visit 테이블에서 방문 기록을 가져옵니다.
    visit_history = Visit.query.filter_by(user_id=session['user_id']).all()
    articles = Article.query.all()

    return render_template('end.html', visit_history=visit_history, articles=articles)


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
    
    # 현재 기사 제외한 다른 기사 중 최대 6개 랜덤으로 선택
    other_articles = Article.query.filter(Article.id != article_id).all()
    random_articles = random.sample(other_articles, min(6, len(other_articles))) if other_articles else []

    return render_template('/article/article.html', article=article, random_articles=random_articles)


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
        article.display_on_index = 'display_on_index' in request.form
        db.session.commit()

        # 수정이 완료되면 기사 목록 페이지로 리다이렉트
        return render_template('/article/edit_article.html',articles=articles, article=article)

    return render_template('/article/edit_article.html', articles=articles, article=article)


@app.route('/record', methods=['POST'])
def record():   
    data = request.get_json()
    article_id = data.get('article_id')
    if not article_id:
        return jsonify(error='Missing article_id'), 400

    start_time = data['start_time']
    end_time = data['end_time']
    duration = data['duration']
    author_info_clicked = data.get('author_info_clicked', False)

    visit = Visit(user_id=session['user_id'], article_id=article_id, start_time=start_time, end_time=end_time,
                  duration=duration, author_info_clicked=author_info_clicked)

    db.session.add(visit)
    db.session.commit()

    return jsonify(message='Visit recorded successfully'), 200


# memo ----------------------------------------


@app.route('/save-memo', methods=['POST'])
def save_memo():
    try:
        data = request.get_json()
        app.logger.info('Received memo data: %s', data)  # Log received data
        article_id = int(data['articleId'])  # Convert articleId to integer
        memo_content = data['memo']
        timestamp_str = data['timestamp']
        
        # Convert timestamp string to datetime object
        timestamp = datetime.fromisoformat(timestamp_str[:-1])

        app.logger.info('Parsed memo data: user_id=%s, article_id=%s, content=%s, timestamp=%s', session['user_id'], article_id, memo_content, timestamp)

        # Create a new Memo instance and save it to the database
        memo = Memo(user_id=session['user_id'], article_id=article_id, content=memo_content, timestamp=timestamp)
        db.session.add(memo)
        db.session.commit()

        return jsonify({'message': 'Memo saved successfully'}), 200
    except Exception as e:
        app.logger.error('Error saving memo: %s', str(e))
        return jsonify({'message': 'Error saving memo: {}'.format(str(e))}), 500


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
    memo_data = [
        {
            'articleId': memo.article_id,
            'content': memo.content,
            'timestamp': memo.timestamp,
            'title': Article.query.get(int(memo.article_id)).title  # Get the title of the article
        } for memo in all_memos
    ]

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


def clean_string(s):
    """Removes characters that are not allowed in Excel cells."""
    if not isinstance(s, str):
        return s
    return re.sub(r'[\x00-\x1f]', '', s)


@app.route('/export-to-excel')
def export_to_excel():
    try:
        if 'user_id' not in session:
            return "You need to be logged in to export data."

        db_path = os.path.join(app.instance_path, 'data.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        user_id = session['user_id']
        username = session['user_name']

        excel_buffer = io.BytesIO()
        writer = pd.ExcelWriter(excel_buffer, engine='openpyxl')

        has_data = False

        # Export article sheet with all articles
        cursor.execute('SELECT * FROM article')
        all_articles = cursor.fetchall()
        df_all_articles = pd.DataFrame(all_articles, columns=[description[0] for description in cursor.description])
        df_all_articles = df_all_articles.applymap(clean_string)
        df_all_articles.to_excel(writer, sheet_name='article', index=False)

        # Export visit sheet with article titles and adjusted duration
        cursor.execute(f'''
            SELECT v.article_id, a.title, v.duration / 1000.0 AS "duration (seconds)"
            FROM visit v
            JOIN article a ON v.article_id = a.id
            WHERE v.user_id = ?
        ''', (user_id,))
        visit_data = cursor.fetchall()
        if visit_data:
            has_data = True
            df_visits = pd.DataFrame(visit_data, columns=['article_id', 'title', 'duration (seconds)'])
            df_visits = df_visits.applymap(clean_string)
            df_visits.to_excel(writer, sheet_name='visit', index=False)

        # Export rating sheet with article titles
        cursor.execute(f'''
            SELECT r.article_id, a.title, r.rating
            FROM rating r
            JOIN article a ON r.article_id = a.id
            WHERE r.user_id = ?
        ''', (user_id,))
        rating_data = cursor.fetchall()
        if rating_data:
            has_data = True
            df_ratings = pd.DataFrame(rating_data, columns=['article_id', 'title', 'rating'])
            df_ratings = df_ratings.applymap(clean_string)
            df_ratings.to_excel(writer, sheet_name='rating', index=False)

        # Export memo sheet with article titles
        cursor.execute(f'''
            SELECT m.*, a.title
            FROM memo m
            JOIN article a ON m.article_id = a.id
            WHERE m.user_id = ?
        ''', (user_id,))
        memo_data = cursor.fetchall()
        if memo_data:
            has_data = True
            df_memo = pd.DataFrame(memo_data, columns=[description[0] for description in cursor.description])
            df_memo = df_memo.applymap(clean_string)
            df_memo.to_excel(writer, sheet_name='memo', index=False)

        # Export feedback sheet with article titles
        cursor.execute(f'''
            SELECT f.*, a.title
            FROM feedback f
            JOIN article a ON f.article_id = a.id
            WHERE f.user_id = ?
        ''', (user_id,))
        feedback_data = cursor.fetchall()
        if feedback_data:
            has_data = True
            df_feedback = pd.DataFrame(feedback_data, columns=[description[0] for description in cursor.description])
            df_feedback = df_feedback.applymap(clean_string)
            df_feedback.to_excel(writer, sheet_name='feedback', index=False)

        # Export ArticleDisplay data
        cursor.execute(f'''
            SELECT ad.*, a.title
            FROM article_display ad
            JOIN article a ON ad.article_id = a.id
            WHERE ad.user_id = ?
        ''', (user_id,))
        article_display_data = cursor.fetchall()
        if article_display_data:
            has_data = True
            df_article_display = pd.DataFrame(article_display_data, columns=[description[0] for description in cursor.description])
            df_article_display = df_article_display.applymap(clean_string)
            df_article_display.to_excel(writer, sheet_name='ArticleDisplay', index=False)

        if has_data:
            writer.close()
            excel_buffer.seek(0)
            response = Response(excel_buffer.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response.headers['Content-Disposition'] = f'attachment; filename={username}.xlsx'
            return response
        else:
            return "No data found for the user."

    except Exception as e:
        return traceback.format_exc()

@app.route('/export-all-to-excel')
def export_all_to_excel():
    try:
        if 'user_name' not in session or session['user_name'] != 'admin':
            return "You need to be an admin to export all data."

        db_path = os.path.join(app.instance_path, 'data.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        table_names = ['visit', 'memo', 'feedback', 'rating', 'article']
        users = db.session.query(User.id, User.username).distinct().all()

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
            for user_id, username in users:
                excel_buffer = io.BytesIO()
                writer = pd.ExcelWriter(excel_buffer, engine='openpyxl')

                has_data = False

                # Export article sheet with all articles
                cursor.execute('SELECT * FROM article')
                all_articles = cursor.fetchall()
                df_all_articles = pd.DataFrame(all_articles, columns=[description[0] for description in cursor.description])
                df_all_articles = df_all_articles.applymap(clean_string)
                df_all_articles.to_excel(writer, sheet_name='article', index=False)

                # Export visit sheet with article titles and adjusted duration
                cursor.execute(f'''
                    SELECT v.article_id, a.title, v.duration / 1000.0 AS "duration (seconds)"
                    FROM visit v
                    JOIN article a ON v.article_id = a.id
                    WHERE v.user_id = ?
                ''', (user_id,))
                visit_data = cursor.fetchall()
                if visit_data:
                    has_data = True
                    df_visits = pd.DataFrame(visit_data, columns=['article_id', 'title', 'duration (seconds)'])
                    df_visits = df_visits.applymap(clean_string)
                    df_visits.to_excel(writer, sheet_name='visit', index=False)

                # Export rating sheet with article titles
                cursor.execute(f'''
                    SELECT r.article_id, a.title, r.rating
                    FROM rating r
                    JOIN article a ON r.article_id = a.id
                    WHERE r.user_id = ?
                ''', (user_id,))
                rating_data = cursor.fetchall()
                if rating_data:
                    has_data = True
                    df_ratings = pd.DataFrame(rating_data, columns=['article_id', 'title', 'rating'])
                    df_ratings = df_ratings.applymap(clean_string)
                    df_ratings.to_excel(writer, sheet_name='rating', index=False)

                # Export memo sheet with article titles
                cursor.execute(f'''
                    SELECT m.*, a.title
                    FROM memo m
                    JOIN article a ON m.article_id = a.id
                    WHERE m.user_id = ?
                ''', (user_id,))
                memo_data = cursor.fetchall()
                if memo_data:
                    has_data = True
                    df_memo = pd.DataFrame(memo_data, columns=[description[0] for description in cursor.description])
                    df_memo = df_memo.applymap(clean_string)
                    df_memo.to_excel(writer, sheet_name='memo', index=False)

                # Export feedback sheet with article titles
                cursor.execute(f'''
                    SELECT f.*, a.title
                    FROM feedback f
                    JOIN article a ON f.article_id = a.id
                    WHERE f.user_id = ?
                ''', (user_id,))
                feedback_data = cursor.fetchall()
                if feedback_data:
                    has_data = True
                    df_feedback = pd.DataFrame(feedback_data, columns=[description[0] for description in cursor.description])
                    df_feedback = df_feedback.applymap(clean_string)
                    df_feedback.to_excel(writer, sheet_name='feedback', index=False)

                # Export ArticleDisplay data
                cursor.execute(f'''
                    SELECT ad.*, a.title
                    FROM ArticleDisplay ad
                    JOIN article a ON ad.article_id = a.id
                    WHERE ad.user_id = ?
                ''', (user_id,))
                article_display_data = cursor.fetchall()
                if article_display_data:
                    has_data = True
                    df_article_display = pd.DataFrame(article_display_data, columns=[description[0] for description in cursor.description])
                    df_article_display = df_article_display.applymap(clean_string)
                    df_article_display.to_excel(writer, sheet_name='ArticleDisplay', index=False)

                # Continue with the export-all-to-excel function
                if has_data:
                    writer.close()
                    excel_buffer.seek(0)
                    zip_file.writestr(f'{username}.xlsx', excel_buffer.read())


        zip_buffer.seek(0)
        response = Response(zip_buffer.read(), content_type='application/zip')
        response.headers['Content-Disposition'] = 'attachment; filename=all_data.zip'
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
        author_name = request.form.get('author_name')
        author_occupation = request.form.get('author_occupation')
        author_email = request.form.get('author_email')
        author_description = request.form.get('author_description')
        display_on_index = 'display_on_index' in request.form  # Checkbox for display on index

        if not title or not content:
            flash('Title and content are required.', 'error')
            return redirect(url_for('add_article'))

        # Create a new Article instance
        new_article = Article(
            title=title,
            content=content,
            author_name=author_name,
            author_occupation=author_occupation,
            author_email=author_email,
            author_description=author_description,
            display_on_index=display_on_index
        )
        
        # Add to the session and commit to the database
        db.session.add(new_article)
        db.session.commit()

        flash('Article added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('/article/add_article.html')

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
    app.run(host='0.0.0.0', debug=True)


