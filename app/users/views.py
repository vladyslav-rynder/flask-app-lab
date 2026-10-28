from datetime import datetime, timedelta
from app.users import user_bp
from flask import (
    abort,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# Заглушка
USER_DATA = {'username': 'user1', 'password': '123'}

@user_bp.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get('age', None, int)
    return render_template('hi.html', name=name, age=age)

@user_bp.route('/admin')
def admin():
    to_url = url_for(
        'users.greetings', name='administrator', age=45, _external=True
    )
    print(to_url)
    return redirect(to_url)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USER_DATA['username'] and password == USER_DATA['password']:
            session['username'] = username
            flash('Успішний вхід!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Wrong data! Try again!', 'error')
            return redirect(url_for('users.login'))

    return render_template('login.html')

@user_bp.route('/profile')
def profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть у систему.', 'error')
        return redirect(url_for('users.login'))

    username = session['username']
    current_theme = request.cookies.get('user_theme', 'light')

    return render_template(
        'profile.html', username=username, current_theme=current_theme
    )

@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли із системи.', 'success')
    return redirect(url_for('users.login'))

@user_bp.route('/profile/add_cookie', methods=['POST'])
def add_cookie():
    if 'username' not in session:
        flash('Будь ласка, увійдіть у систему.', 'error')
        return redirect(url_for('users.login'))

    key = request.form.get('cookie_key')
    value = request.form.get('cookie_value')
    max_age = request.form.get('cookie_max_age')

    if not key or not value:
        flash("Ключ і значення куки обов'язкові!", 'error')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))

    try:
        max_age_seconds = int(max_age) if max_age else 60 * 60 * 24 * 30  # за замовчуванням 30 днів
        response.set_cookie(key, value, max_age=max_age_seconds)
        flash(f"Кука '{key}' успішно додана!", 'success')
    except ValueError:
        flash('Термін дії має бути числом (у секундах)!', 'error')

    return response


@user_bp.route('/profile/delete_cookie', methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        flash('Будь ласка, увійдіть у систему.', 'error')
        return redirect(url_for('users.login'))

    key = request.form.get('delete_key')
    if not key:
        flash('Вкажіть ключ куки для видалення!', 'error')
        return redirect(url_for('users.profile'))

    response = make_response(redirect(url_for('users.profile')))
    response.delete_cookie(key)
    flash(f"Кука '{key}' успішно видалена!", 'success')
    return response


@user_bp.route('/profile/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    if 'username' not in session:
        flash('Будь ласка, увійдіть у систему.', 'error')
        return redirect(url_for('users.login'))

    response = make_response(redirect(url_for('users.profile')))
    for cookie_name in request.cookies.keys():
        response.delete_cookie(cookie_name)

    flash('Усі кукі успішно видалено!', 'success')
    return response

@user_bp.route('/profile/set_theme/<theme_name>')
def set_theme(theme_name):
    allowed_themes = ['light', 'dark', 'primary']
    if theme_name not in allowed_themes:
        theme_name = 'light'

    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('user_theme', theme_name, max_age=60 * 60 * 24 * 30)
    flash(f"Кольорову схему змінено на '{theme_name}'!", 'success')
    return response