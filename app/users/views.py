from app.users import user_bp
from flask import abort, flash, redirect, render_template, request, session, url_for

# Заглушка
USER_DATA = {'username': 'user1', 'password': '123'}

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
        flash("Будь ласка, увійдіть у систему.", 'error')
        return redirect(url_for('users.login'))

    username = session['username']
    return render_template('profile.html', username=username)

@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли із системи.', 'success')
    return redirect(url_for('users.login'))

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