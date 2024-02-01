from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

booklist = Flask(__name__)
booklist.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(booklist)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True) 
    
with booklist.app_context():
    db.create_all()
    
@booklist.route('/')
def index():
    return render_template('index.html')

@booklist.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@booklist.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']
        added_book = Book(title=title, author=author, publication_year=publication_year)
        db.session.add(added_book)
        db.session.commit()
        return redirect('/books')
    return render_template('add_book.html')

if __name__ == "__main__":
    booklist.run(debug=True)