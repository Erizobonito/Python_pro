# Importar
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import string
from datetime import datetime, timedelta

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

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_login = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Ban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verificar si es un intento de login de administrador
        admin_password = request.form.get('admin_password')
        if admin_password:
            if admin_password == ADMIN_PASSWORD:
                session.clear()  # Limpiar cualquier sesión anterior
                session['admin'] = True
                return redirect('/admin')
            return render_template('login.html', error='Contraseña de administrador incorrecta')
        
        # Si no es admin, manejar login normal
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(login=email).first()
        
        if user and user.password == password:
            session.clear()  # Limpiar cualquier sesión anterior
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
    # Primero verificar si hay sesión
    if not session.get('user_id') and not session.get('admin'):
        return redirect('/')
        
    try:
        # Si es administrador y está intentando acceder a /index, redirigir a /admin
        if session.get('admin'):
            return redirect('/admin')
            
        # Si es usuario normal, mostrar sus tarjetas
        cards = Card.query.filter_by(user_id=session['user_id']).order_by(Card.id).all()
        user = User.query.get(session['user_id'])
        return render_template('index_admin.html', cards=cards, user=user)
    except Exception as e:
        print(f"Error en index: {e}")
        session.clear()  # Limpiar la sesión si hay error
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
        comments = Comment.query.order_by(Comment.created_at.desc()).all()
        bans = Ban.query.filter(Ban.end_date > datetime.utcnow()).all()
        
        user_data = []
        for user in users:
            cards = Card.query.filter_by(user_id=user.id).all()
            is_banned = any(ban.user_login == user.login for ban in bans)
            ban_info = next((ban for ban in bans if ban.user_login == user.login), None)
            
            user_data.append({
                'user': user,
                'cards': cards,
                'card_count': len(cards),
                'is_banned': is_banned,
                'ban_info': ban_info
            })
            
        return render_template('admin.html', 
                             user_data=user_data, 
                             comments=comments,
                             active_bans=bans)
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

@app.route('/admin/ban_user', methods=['POST'])
def ban_user():
    if not session.get('admin'):
        return jsonify({'error': 'No autorizado'}), 403
        
    user_login = request.form.get('user_login')
    reason = request.form.get('reason')
    duration_days = int(request.form.get('duration', 1))
    
    try:
        end_date = datetime.utcnow() + timedelta(days=duration_days)
        ban = Ban(
            user_login=user_login,
            reason=reason,
            end_date=end_date
        )
        db.session.add(ban)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error al banear usuario: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/admin/unban_user', methods=['POST'])
def unban_user():
    if not session.get('admin'):
        return jsonify({'error': 'No autorizado'}), 403
        
    user_login = request.form.get('user_login')
    
    try:
        bans = Ban.query.filter_by(user_login=user_login).all()
        for ban in bans:
            ban.end_date = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if session.get('admin'):
        # Si es admin, crear comentario como admin
        text = request.form.get('comment_text')
        if text:
            comment = Comment(text=text, user_login="Administrador")
            db.session.add(comment)
            db.session.commit()
            return jsonify({'success': True})
    elif session.get('user_id'):
        # Si es usuario normal, verificar ban
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
            
        active_ban = Ban.query.filter_by(user_login=user.login)\
                             .filter(Ban.end_date > datetime.utcnow())\
                             .first()
        if active_ban:
            return jsonify({
                'error': f'Usuario baneado hasta {active_ban.end_date.strftime("%Y-%m-%d %H:%M")}. Razón: {active_ban.reason}'
            }), 403
        
        text = request.form.get('comment_text')
        if text:
            comment = Comment(text=text, user_login=user.login)
            db.session.add(comment)
            db.session.commit()
            return jsonify({'success': True})
    
    return jsonify({'error': 'No autorizado'}), 403

@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    if not session.get('admin'):
        return jsonify({'error': 'No autorizado'}), 403
        
    comment_id = request.form.get('comment_id')
    try:
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'error': 'Comentario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_comments')
def get_comments():
    comments = Comment.query.order_by(Comment.created_at).all()  # Orden cronológico
    return jsonify([{
        'id': c.id,
        'text': c.text,
        'user': c.user_login,
        'date': c.created_at.strftime('%Y-%m-%d %H:%M'),
        'isAdmin': c.user_login == "Administrador"
    } for c in comments])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)