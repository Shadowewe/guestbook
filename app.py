from flask import Flask, render_template, request, redirect, session
from database import init_db, get_all_messages, add_message, delete_message, get_message_count, delete_all, sort_newest, sort_oldest, check_user

app = Flask(__name__)
app.secret_key = 'arbuziki'
init_db()


@app.route('/')
def index():
    """
    Главная страница — показывает список сообщений.
    """
    messages = get_all_messages()
    total_count = get_message_count()
    
    # Передаём в шаблон:
    # сообщения, счётчик, и флаг авторизации
    return render_template(
        'index.html',
        messages=messages,
        total_count=total_count,
        logged_in=session.get('logged_in', False),  # по умолчанию False
        username=session.get('username')  # имя пользователя или None
    )

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
    """
    Удаляет сообщение по id.
    Только авторизованный пользователь может удалять.
    """
    # Проверяем, авторизован ли пользователь
    # session.get('logged_in') возвращает True/False или None
    if not session.get('logged_in'):
        # Если не авторизован — отправляем на страницу входа
        return redirect('/login')
    
    # Если авторизован — удаляем сообщение
    delete_message(message_id)
    return redirect('/')

@app.route('/delete-all', methods=['GET', 'POST'])
def deleteall():
    if not session.get('logged_in'):
        return redirect('/login')
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Страница входа в приложение.
    GET — показывает форму входа.
    POST — обрабатывает отправленные логин и пароль.
    """
    error = None  # переменная для сообщения об ошибке
    
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Проверяем, правильные ли логин и пароль
        if check_user(username, password):
            # Сохраняем информацию о входе в сессию
            # session — это словарь, который хранится на сервере
            # данные привязаны к конкретному браузеру через cookies
            session['logged_in'] = True   # флаг, что пользователь вошёл
            session['username'] = username  # сохраняем имя пользователя
            return redirect('/')  # перенаправляем на главную
        else:
            # Если логин или пароль неверные
            error = 'Неверный логин или пароль'
    
    # GET-запрос или ошибка — показываем форму входа
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """
    Выход из приложения.
    Удаляет данные пользователя из сессии.
    """
    # pop удаляет ключ из словаря session
    # Если ключа нет, ничего не происходит
    session.pop('logged_in', None)
    session.pop('username', None)
    
    # Перенаправляем на главную страницу
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5001)