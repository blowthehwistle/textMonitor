from flask import Flask, request, jsonify, render_template, Response, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import io
from openpyxl import Workbook
import pandas as pd
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #경로 지정
db = SQLAlchemy(app)

# Dictionary to store memos (articleId -> memo)
memos = {}

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.String(255), nullable=False)  # start_time 필드 추가
    end_time = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)

class ReadArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.String(255), nullable=False, unique=True)
    authorInfoClicked = db.Column(db.String(255), nullable=False)

    def __init__(self, article_id, authorInfoClicked):
        self.article_id = article_id
        self.authorInfoClicked = authorInfoClicked

class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    visit_history = Visit.query.all()

    # ReadArticle 테이블에서 읽은 기사를 가져옵니다.
    read_articles = ReadArticle.query.all()

    return render_template('end.html', visit_history=visit_history, read_articles=read_articles)

# Serve the styles.css file as a static file
@app.route('/static/styles.css')
def serve_styles():
    return app.send_static_file('styles.css')

@app.route('/article1')
def article1():
    return render_template('/article/article1.html')
@app.route('/article2')
def article2():
    return render_template('/article/article2.html')
@app.route('/article3')
def article3():
    return render_template('/article/article3.html')
@app.route('/article4')
def article4():
    return render_template('/article/article4.html')
@app.route('/article5')
def article5():
    return render_template('/article/article5.html')
@app.route('/article6')
def article6():
    return render_template('/article/article6.html')
@app.route('/article7')
def article7():
    return render_template('/article/article7.html')
@app.route('/article8')
def article8():
    return render_template('/article/article8.html')

@app.route('/record', methods=['POST'])
def record():
    data = request.get_json()
    article_id = data['article_id']
    start_time = data['start_time']
    end_time = data['end_time']
    duration = data['duration']

    # duration을 정수로 저장
    visit = Visit(article_id=article_id, start_time=start_time, end_time=end_time, duration=duration)

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
        existing_record = ReadArticle.query.filter_by(article_id=article_id).first()

        if existing_record:
            # Compare the existing authorInfoClicked with the new value.
            if existing_record.authorInfoClicked != new_author_info:
                # Update authorInfoClicked if there is a change.
                existing_record.authorInfoClicked = new_author_info
                db.session.commit()

            return jsonify({'message': 'Article already marked as read'}), 200

        # If the article is not marked as read, create a new record.
        new_read_article = ReadArticle(article_id=article_id, authorInfoClicked=new_author_info)
        db.session.add(new_read_article)
        db.session.commit()

        return jsonify({'message': 'Article marked as read'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


#memo ----------------------------------------
@app.route('/save-memo', methods=['POST'])
def save_memo():
    data = request.get_json()
    article_id = data['articleId']
    memo_content = data['memo']

    # Create a new Memo instance and save it to the database
    memo = Memo(article_id=article_id, content=memo_content)
    db.session.add(memo)
    db.session.commit()

    return jsonify({'message': 'Memo saved successfully'}), 200

@app.route('/get-memo', methods=['GET'])
def get_memo():
    article_id = request.args.get('articleId')
    memos_for_article = Memo.query.filter_by(article_id=article_id).all()

    # Extract memo content and timestamps
    memo_data = [{'content': memo.content, 'timestamp': memo.timestamp} for memo in memos_for_article]

    return jsonify(memo_data), 200

@app.route('/get-all-memos', methods=['GET'])
def get_all_memos():
    all_memos = Memo.query.all()

    # Extract memo content, timestamps, and articleId
    memo_data = [{'articleId': memo.article_id, 'content': memo.content, 'timestamp': memo.timestamp} for memo in all_memos]

    return jsonify(memo_data), 200
#----------------------------------------------

#Feedback 
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()
        article_id = data['articleId']
        feedback_text = data['feedback']

        # Save the feedback to the Feedback table in the database
        feedback_entry = Feedback(article_id=article_id, feedback=feedback_text)
        db.session.add(feedback_entry)
        db.session.commit()

        return redirect(url_for('index'))  # Adjust the endpoint as needed
    except Exception as e:
        return jsonify({'message': str(e)}), 500




# Route to export data to Excel
@app.route('/export-to-excel')
def export_to_excel():
    try:
        # Connect to your SQLite database
        conn = sqlite3.connect('/Users/hwi/Develop/textMontor/data.db')  # Replace with your database path
        cursor = conn.cursor()

        # Define the tables you want to export
        table_names = ['visit', 'memo', 'read_article', 'feedback']  # Replace with your table names

        # Create an Excel Workbook
        wb = Workbook()

        for table_name in table_names:
            # Execute a query to retrieve data from your database
            cursor.execute(f'SELECT * FROM {table_name}')
            data = cursor.fetchall()

            # Create a DataFrame from the retrieved data
            df = pd.DataFrame(data, columns=[description[0] for description in cursor.description])

            # Create an Excel writer for the current table
            writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')
            writer.book = wb
            df.to_excel(writer, sheet_name=table_name, index=False)

        # Create an in-memory buffer to save the Excel file
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        # Prepare the response with appropriate headers
        response = Response(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response.headers['Content-Disposition'] = 'attachment; filename=data.xlsx'

        return response

    except Exception as e:
        return str(e)

    
# Create the database tables within an application context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
