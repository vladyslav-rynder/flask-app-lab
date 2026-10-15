from app.resume import resume_bp
from flask import render_template

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

@resume_bp.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контактна інформація')