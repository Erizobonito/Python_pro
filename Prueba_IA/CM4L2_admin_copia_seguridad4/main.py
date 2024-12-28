# Importar
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.secret_key = 'clave_admin_secreta'

# Conectando SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def generate_admin_password():
    """Genera una contraseña aleatoria para el admin"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Variable global para la contraseña de admin
ADMIN_PASSWORD = generate_admin_password()
print("\n=== CONTRASEÑA DE ADMINISTRADOR ===")
print(f"Contraseña: {ADMIN_PASSWORD}")
print("===================================\n")

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<User {self.login}>'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verificar si es un intento de login de administrador
        admin_password = request.form.get('admin_password')
        if admin_password:
            if admin_password == ADMIN_PASSWORD:
                session['admin'] = True
                return redirect('/admin')
            return render_template('login.html', error='Contraseña de administrador incorrecta')
        
        # Si no es admin, manejar login normal
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(login=email).first()
        
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect('/index')
        return render_template('login.html', error='Usuario o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form.get('email')
        password = request.form.get('password')
        
        if not login or not password:
            return render_template('registration.html', error='Por favor complete todos los campos')
            
        if User.query.filter_by(login=login).first():
            return render_template('registration.html', error='Usuario ya registrado')
        
        try:
            new_user = User(login=login, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error en registro: {e}")
            db.session.rollback()
            return render_template('registration.html', error='Error al registrar usuario')
    
    return render_template('registration.html')

@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect('/')
        
    try:
        cards = Card.query.filter_by(user_id=session['user_id']).order_by(Card.id).all()
        return render_template('index_admin.html', cards=cards)
    except Exception as e:
        print(f"Error en index: {e}")
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/card/<int:id>')
def card(id):
    if 'user_id' not in session:
        return redirect('/')
    try:
        # Obtener todas las tarjetas del usuario para encontrar el índice
        cards = Card.query.filter_by(user_id=session['user_id']).order_by(Card.id).all()
        card = Card.query.get_or_404(id)
        
        if card.user_id != session['user_id']:
            return redirect('/index')
            
        # Encontrar el índice de la tarjeta actual
        card_index = cards.index(card) + 1
        
        return render_template('card.html', card=card, loop={'index': card_index})
    except Exception as e:
        print(f"Error al mostrar tarjeta: {e}")
        return redirect('/index')

@app.route('/create')
def create():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create_card.html')

@app.route('/form_create', methods=['GET', 'POST'])
def form_create():
    if 'user_id' not in session:
        return redirect('/')
        
    if request.method == 'POST':
        try:
            card = Card(
                title=request.form['title'],
                subtitle=request.form['subtitle'],
                text=request.form['text'],
                user_id=session['user_id']
            )
            db.session.add(card)
            db.session.commit()
            return redirect('/index')
        except Exception as e:
            print(f"Error al crear tarjeta: {e}")
            return render_template('create_card.html', error='Error al crear la tarjeta')
            
    return render_template('create_card.html')

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/')
        
    try:
        users = User.query.all()
        user_data = []
        for user in users:
            cards = Card.query.filter_by(user_id=user.id).order_by(Card.id).all()
            user_data.append({
                'user': user,
                'cards': cards,
                'card_count': len(cards)
            })
        return render_template('admin.html', user_data=user_data)
    except Exception as e:
        print(f"Error en admin: {e}")
        return redirect('/')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    password = request.form.get('admin_password')
    if password == ADMIN_PASSWORD:
        session['admin'] = True
        return redirect('/admin')
    return render_template('login.html', error='Contraseña de administrador incorrecta')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)