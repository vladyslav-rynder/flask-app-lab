from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/resume')
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

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контактна інформація')

if __name__ == '__main__':
    app.run(debug=True)