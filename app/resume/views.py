import logging
from app.resume import resume_bp
from app.resume.forms import ContactForm
from flask import flash, redirect, render_template, request, url_for

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

@resume_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data

        logging.info(
            f'Contact Form Submitted: Name={name}, Email={email}, Phone={phone}, Subject={subject}'
        )

        flash(
            'Повідомлення успішно відправлено та дані збережено!', 'success'
        )
        return redirect(url_for('resume.contact'))

    if form.errors and request.method == 'POST':
        flash('Помилка при заповненні форми. Перевірте введені дані.', 'error')

    return render_template('contact.html', form=form)

@resume_bp.route('/')
def resume():
    return render_template(
        'resume.html',
        title='Моє Резюме',
        name='Риндер Владислав',
        skills=['Python', 'Flask', 'Git', 'HTML/CSS', 'SQL'],
        projects=[
            {
                'name': 'Веб-додаток на Flask',
                'desc': 'Розгортання сайту-резюме на Render',
            },
        ],
    )