from app import app, db, Question
import json
from sqlalchemy import exc

def add_sample_questions():
    with app.app_context():
        try:

            questions = [

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
