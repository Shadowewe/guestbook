from flask import Flask, render_template, request, redirect, session
from database import init_db, get_all_messages, add_message, delete_message, get_message_count, delete_all, sort_newest, sort_oldest

app = Flask(__name__)
app.secret_key = 'arbuziki'
init_db()


@app.route('/')
def index():
    messages = get_all_messages()
    total_count = get_message_count()
    return render_template('index.html', messages=messages, total_count=total_count)


@app.route('/add', methods=['POST'])
def add():
    """Обрабатывает отправку нового сообщения."""
    # Получаем данные из формы
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    
    # Проверяем, что оба поля не пустые
    if name and message:
        add_message(name, message)
        session['success'] = True
    
    # Перенаправляем на главную страницу
    return redirect('/')

@app.route('/delete/<int:message_id>')
def delete(message_id):
    delete_message(message_id)
    return redirect('/')

@app.route('/delete-all', methods=['GET', 'POST'])
def deleteall():
    delete_all()
    return redirect('/')

@app.route('/delete-all-confirm', methods=['POST'])
def deleteallc():
    delete_all()
    return redirect('/')

@app.route('/sort/newest')
def newest():
    sort_newest()
    return redirect('/')

@app.route('/sort/oldest')
def oldest():
    sort_oldest()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5001)