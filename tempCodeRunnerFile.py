@app.route('/record', methods=['POST'])
# @login_required
# def record():
#     data = request.get_json()
#     article_id = data['article_id']
#     start_time = data['start_time']
#     end_time = data['end_time']
#     duration = data['duration']

#     # duration을 정수로 저장
#     visit = Visit(user_id=session['user_id'], article_id=article_id, start_time=start_time, end_time=end_time,
#                   duration=duration)

#     db.session.add(visit)
#     db.session.commit()

#     return jsonify(message='Visit recorded successfully'), 200
