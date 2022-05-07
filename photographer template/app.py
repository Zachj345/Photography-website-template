from flask import Flask
from flask import render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'shhhhhhstfu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email or email == '':
            flash('Hey please enter a valid email', category='error')
        else:
            new_email = Database(email=email)
            db.session.add(new_email)
            db.session.commit()
            flash('Email successfully added! We will get back to you as soon as possible!',
                  category='success')
            return redirect(url_for('contact'))
        print([i.email for i in Database.query.all()])
    return render_template('contact.html')


@app.route('/delete-email/<id>', methods=['GET', 'POST'])
def delete_email(id):
    email = Database.query.filter_by(id=id).first()
    if not email:
        flash('No email to delete bro', category='error')
    else:
        db.session.delete(email)
        db.session.commit()
    return redirect(url_for('contact'))


@app.route('/portfolio', methods=['GET'])
def portfolio():
    return render_template('portfolio.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
