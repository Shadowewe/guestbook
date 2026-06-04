from flask import Flask, render_template, request, redirect, session
from database import init_db, get_all_messages, add_message

app = Flask(__name__)
app.secret_key = 'arbuziki'
init_db()


@app.route('/')
def index():
    """Главная страница: показывает все сообщения."""
    messages = get_all_messages()
    return render_template('index.html', messages=messages)


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


if __name__ == '__main__':
    app.run(debug=True)