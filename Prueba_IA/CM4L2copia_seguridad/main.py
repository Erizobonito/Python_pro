# Importar
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para las sesiones

# Conectando SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

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
        # Obtener datos del formulario
        form_login = request.form.get('email')
        form_password = request.form.get('password')
        
        print(f"Intento de login - Email: {form_login}")  # Debug
        
        try:
            # Buscar usuario
            user = User.query.filter_by(login=form_login).first()
            
            if user and user.password == form_password:
                session['user_id'] = user.id
                print("Login exitoso!")  # Debug
                return redirect('/index')
            else:
                print("Credenciales incorrectas")  # Debug
                return render_template('login.html', error='Usuario o contraseña incorrectos')
            
        except Exception as e:
            print(f"Error en login: {e}")
            return render_template('login.html', error='Error al intentar iniciar sesión')
    
    return render_template('login.html')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form.get('email', '')
        password = request.form.get('password', '')
        
        # Verificar si el usuario ya existe
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
        cards = Card.query.order_by(Card.id).all()
        return render_template('index.html', cards=cards)
    except Exception as e:
        print(f"Error en index: {e}")
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/card/<int:id>')
def card(id):
    if 'user_id' not in session:
        return redirect('/')
    try:
        card = Card.query.get_or_404(id)
        return render_template('card.html', card=card)
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
                text=request.form['text']
            )
            db.session.add(card)
            db.session.commit()
            return redirect('/index')
        except Exception as e:
            print(f"Error al crear tarjeta: {e}")
            return render_template('create_card.html', error='Error al crear la tarjeta')
            
    return render_template('create_card.html')

if __name__ == "__main__":
    with app.app_context():
        print("Eliminando tablas existentes...")
        db.drop_all()
        print("Creando nuevas tablas...")
        db.create_all()
        
        # Crear un usuario de prueba
        try:
            test_user = User(login="test@test.com", password="test123")
            db.session.add(test_user)
            db.session.commit()
            print("Usuario de prueba creado exitosamente")
        except Exception as e:
            print(f"Error al crear usuario de prueba: {e}")
            db.session.rollback()
    
    app.run(debug=True)
