from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, exc
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError as exc
import os, json
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Environment configuration
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quiz.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour session timeout

db = SQLAlchemy(app)

# Custom error handler
class QuizException(Exception):
    pass

# Database models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)  # Yeni sütun
    password_hash = db.Column(db.String(128))  # Yeni sütun
    high_score = db.Column(db.Integer, default=0)
    last_score = db.Column(db.Integer, default=0)
    attempts = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)  # Yeni sütun

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    options = db.Column(db.JSON, nullable=False)  # {'1': 'Option A', '2': 'Option B', ...}
    correct_option = db.Column(db.Integer, nullable=False)  # 1-4
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), default='medium')
    is_active = db.Column(db.Boolean, default=True)

def initialize_db():
    with app.app_context():
        try:
            # Veritabanı dosyası ve tabloları kontrol et
            inspector = inspect(db.engine)
            tables_exist = inspector.get_table_names()
            
            # Eğer hiç tablo yoksa oluştur
            if not tables_exist:
                db.create_all()
                app.logger.info("Database tables created successfully")
                
                # Admin kullanıcısını oluştur (eğer yoksa)
                if not User.query.filter_by(is_admin=True).first():
                    admin = User(
                        username='admin',
                        email='admin@quizapp.com',
                        is_admin=True
                    )
                    admin.set_password('admin123')
                    db.session.add(admin)
                    db.session.commit()
                    app.logger.info("Admin user created successfully")
                add_sample_questions()
            else:
                app.logger.info("Database already exists, skipping creation")
                
        except exc as e:
            app.logger.error(f"Database initialization failed: {str(e)}")
            raise QuizException("Database initialization error")
        

def add_sample_questions():
    with app.app_context():
        try:
            # Tüm kategorilerden 2'şer soru
            questions = [
                # 1. Discord.py (Sohbet Botu)
                {
                    "text": "Discord.py'de yeni bir bot komutu oluşturmak için hangisi kullanılır?",
                    "options": {
                        "1": "@bot.command()",
                        "2": "@commands.command()", 
                        "3": "@client.command()",
                        "4": "@discord.command()"
                    },
                    "correct_option": 2,
                    "category": "Discord.py",
                    "difficulty": "easy"
                },
                {
                    "text": "Discord botunda bir mesaj geldiğinde çalışacak event hangisidir?",
                    "options": {
                        "1": "on_ready()",
                        "2": "on_message()", 
                        "3": "on_command()",
                        "4": "on_reaction()"
                    },
                    "correct_option": 2,
                    "category": "Discord.py",
                    "difficulty": "medium"
                },
                
                # 2. Flask (Web Geliştirme)
                {
                    "text": "Flask uygulaması oluşturmak için hangi obje kullanılır?",
                    "options": {
                        "1": "Flask()",
                        "2": "Application()", 
                        "3": "WebApp()",
                        "4": "Server()"
                    },
                    "correct_option": 1,
                    "category": "Flask",
                    "difficulty": "easy"
                },
                {
                    "text": "Flask'ta dinamik URL parametresi nasıl tanımlanır?",
                    "options": {
                        "1": "/user/<username>",
                        "2": "/user/:username", 
                        "3": "/user/{username}",
                        "4": "/user/[username]"
                    },
                    "correct_option": 1,
                    "category": "Flask", 
                    "difficulty": "medium"
                },
                
                # 3. Yapay Zeka
                {
                    "text": "Python'da derin öğrenme için en yaygın kütüphane hangisidir?",
                    "options": {
                        "1": "TensorFlow",
                        "2": "Scikit-learn", 
                        "3": "Pandas",
                        "4": "NumPy"
                    },
                    "correct_option": 1,
                    "category": "Yapay Zeka",
                    "difficulty": "easy"
                },
                {
                    "text": "Sinir ağlarında overfitting'i önlemek için hangisi kullanılır?",
                    "options": {
                        "1": "Dropout",
                        "2": "Batch Normalization", 
                        "3": "Data Augmentation",
                        "4": "Hepsi"
                    },
                    "correct_option": 4,
                    "category": "Yapay Zeka",
                    "difficulty": "hard"
                },
                
                # 4. Bilgisayar Görüşü
                {
                    "text": "OpenCV hangi amaçla kullanılır?",
                    "options": {
                        "1": "Veri analizi",
                        "2": "Görüntü işleme", 
                        "3": "Web geliştirme",
                        "4": "Veritabanı yönetimi"
                    },
                    "correct_option": 2,
                    "category": "Bilgisayar Görüşü",
                    "difficulty": "easy"
                },
                {
                    "text": "Nesne tanımada kullanılan YOLO algoritması neyin kısaltmasıdır?",
                    "options": {
                        "1": "You Only Look Once",
                        "2": "Your Object Location Observer", 
                        "3": "Yield Oriented Learning Object",
                        "4": "Young Optimized Learning Operator"
                    },
                    "correct_option": 1,
                    "category": "Bilgisayar Görüşü",
                    "difficulty": "medium"
                },
                
                # 5. Doğal Dil İşleme (NLP)
                {
                    "text": "NLTK kütüphanesinin temel kullanım amacı nedir?",
                    "options": {
                        "1": "Veri görselleştirme",
                        "2": "Doğal dil işleme", 
                        "3": "Web scraping",
                        "4": "Makine öğrenmesi"
                    },
                    "correct_option": 2,
                    "category": "NLP",
                    "difficulty": "easy"
                },
                {
                    "text": "Kelime vektörü temsilleri için hangi teknik kullanılır?",
                    "options": {
                        "1": "TF-IDF",
                        "2": "Word2Vec", 
                        "3": "Bag of Words",
                        "4": "Hepsi"
                    },
                    "correct_option": 4,
                    "category": "NLP",
                    "difficulty": "medium"
                },
                
                # 6. Web Scraping
                {
                    "text": "BeautifulSoup genellikle hangi kütüphane ile birlikte kullanılır?",
                    "options": {
                        "1": "requests",
                        "2": "numpy", 
                        "3": "pandas",
                        "4": "matplotlib"
                    },
                    "correct_option": 1,
                    "category": "Web Scraping",
                    "difficulty": "easy"
                },
                {
                    "text": "Web scraping yaparken hangisine dikkat edilmelidir?",
                    "options": {
                        "1": "robots.txt kuralları",
                        "2": "Sunucu yükü", 
                        "3": "Yasal düzenlemeler",
                        "4": "Hepsi"
                    },
                    "correct_option": 4,
                    "category": "Web Scraping",
                    "difficulty": "medium"
                }
            ]

            # Veritabanına ekleme
            added_count = 0
            for q in questions:
                if not Question.query.filter_by(text=q['text']).first():
                    question = Question(
                        text=q['text'],
                        options=json.dumps(q['options']),
                        correct_option=q['correct_option'],
                        category=q['category'],
                        difficulty=q.get('difficulty', 'medium'),
                        is_active=True
                    )
                    db.session.add(question)
                    added_count += 1

            db.session.commit()
            print(f"Başarıyla {added_count} yeni soru eklendi. Toplam soru sayısı: {Question.query.count()}")

        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(f"Veritabanı hatası: {str(e)}")
        except Exception as e:
            print(f"Beklenmeyen hata: {str(e)}")

if __name__ == '__main__':
    add_sample_questions()

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(QuizException)
def handle_quiz_exception(e):
    return render_template('errors/quiz_error.html', error=str(e)), 400

# Main routes
@app.route('/')
def home():
    try:
        global_high = db.session.query(func.max(User.high_score)).scalar() or 0
        user_high = 0
        
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])
            user_high = user.high_score if user else 0
        
        return render_template('index.html',
                            global_high=global_high,
                            user_high=user_high)
    except exc.SQLAlchemyError:
        raise QuizException("Database error occurred")

@app.route('/start', methods=['POST'])
def start_quiz():
    try:
        username = request.form.get('username', '').strip()
        if not username:
            flash('Username is required', 'error')
            return redirect(url_for('home'))
        
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        
        session['user_id'] = user.id
        session.permanent = True
        return redirect(url_for('quiz'))
    except exc.IntegrityError:
        db.session.rollback()
        flash('Username already exists', 'error')
        return redirect(url_for('home'))
    except exc.SQLAlchemyError:
        raise QuizException("Failed to start quiz")

@app.route('/quiz')
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    try:
        questions = Question.query.filter_by(is_active=True)\
                       .order_by(func.random())\
                       .limit(5)\
                       .all()
        
        # JSON string'leri Python dict'e çevir
        for q in questions:
            q.options = json.loads(q.options)
        
        if not questions:
            flash('Şu anda aktif soru bulunmamaktadır', 'error')
            return redirect(url_for('home'))
        
        global_high = db.session.query(func.max(User.high_score)).scalar() or 0
        user_high = 0
        
        if 'user_id' in session:
            user = db.session.get(User, session['user_id'])
            user_high = user.high_score if user else 0
            
        return render_template('quiz.html', questions=questions, global_high=global_high, user_high=user_high)
    except exc.SQLAlchemyError:
        flash('Veritabanı hatası oluştu', 'error')
        return redirect(url_for('home'))

@app.route('/submit', methods=['POST'])
def submit():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    try:
        user = db.session.get(User, session['user_id'])
        if not user:
            return redirect(url_for('home'))
        
        score = 0
        questions = Question.query.filter_by(is_active=True).all()
        
        for question in questions:
            user_answer = request.form.get(f'q{question.id}')
            if user_answer and int(user_answer) == question.correct_option:
                score += 10  # 10 points per question
        
        user.last_score = score
        if score > user.high_score:
            user.high_score = score
        user.attempts += 1
        db.session.commit()
        
        return redirect(url_for('results'))
    except exc.SQLAlchemyError:
        db.session.rollback()
        raise QuizException("Failed to submit quiz")

@app.route('/results')
def results():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    try:
        user = db.session.get(User, session['user_id'])
        if not user:
            return redirect(url_for('home'))
        
        global_high = db.session.query(func.max(User.high_score)).scalar()
        
        # Calculate rank
        rank = db.session.query(
            func.count(User.id)
        ).filter(
            User.high_score > user.high_score
        ).scalar() + 1
        
        return render_template('results.html',
                            last_score=user.last_score,
                            high_score=user.high_score,
                            global_high=global_high,
                            rank=rank,
                            attempts=user.attempts)
    except exc.SQLAlchemyError:
        raise QuizException("Failed to load results")

# Admin routes
@app.route('/admin/questions')
def manage_questions():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin:
        return redirect(url_for('home'))
    
    questions = Question.query.all()
    return render_template('admin/questions.html', questions=questions)

# API endpoints
@app.route('/api/stats')
def get_stats():
    try:
        total_users = db.session.query(func.count(User.id)).scalar()
        total_attempts = db.session.query(func.sum(User.attempts)).scalar()
        avg_score = db.session.query(func.avg(User.high_score)).scalar()
        
        return {
            'total_users': total_users,
            'total_attempts': total_attempts,
            'average_score': round(float(avg_score or 0), 2)
        }
    except exc.SQLAlchemyError:
        raise QuizException("Failed to fetch statistics")

if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', False))