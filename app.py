from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    level = db.Column(db.String(50))
    quest_type = db.Column(db.String(50))
    difficulty = db.Column(db.Integer)
    link = db.Column(db.String(300))
    npc_coords = db.Column(db.String(50))

# Создание базы данных
with app.app_context():
    db.create_all()
    
    # Проверка и заполнение данными (актуально 2025)
    if Quest.query.count() == 0:
        quests_data = [
            {'title': 'Стартовые квесты Людей', 'description': 'Деревня Людей 1-19 lvl. Базовые задания для новичков.', 'level': '1-19', 'quest_type': 'human', 'difficulty': 2, 'link': 'https://pwdata.ru/?page_id=362', 'npc_coords': '227,554'},
            {'title': 'Стартовые квесты Сидов', 'description': 'Гора Сидов 1-19 lvl. Квесты магистров.', 'level': '1-19', 'quest_type': 'elf', 'difficulty': 2, 'link': 'https://pwdata.ru/?page_id=362', 'npc_coords': 'Дворец Сидов'},
            {'title': 'Поиск всех квестов', 'description': 'Полная база pwdatabase.com (актуально 2025)', 'level': '1-100+', 'quest_type': '', 'difficulty': 1, 'link': 'https://www.pwdatabase.com/ru/search_quest'},
            {'title': 'Квесты на уважение 29+ lvl', 'description': 'Даос Манман (324,422). Уважение фракции.', 'level': '29+', 'quest_type': 'respect', 'difficulty': 3, 'link': 'https://pwdata.ru/?page_id=362', 'npc_coords': '324,422'},
            {'title': 'Погнутая брошь за виллу', 'description': 'Ежедневный квест география + вилла в награду.', 'level': 'daily', 'quest_type': 'daily', 'difficulty': 4, 'link': 'https://pwdata.ru/?page_id=362'},
            {'title': 'Летающий меч для Людей', 'description': 'Квест на полет 29 lvl. Обязательный для мобильности.', 'level': '29', 'quest_type': 'human', 'difficulty': 3, 'npc_coords': 'Город Людей'},
            {'title': 'Милость создателя', 'description': 'Бесплатные хирки ежедневно. Не пропускайте!', 'level': 'daily', 'quest_type': 'daily', 'difficulty': 1},
            {'title': 'Квесты Дракона 20-91 lvl', 'description': 'Цю Ню, Я Цы. Цепочка мощных квестов.', 'level': '20-91', 'quest_type': 'dragon', 'difficulty': 5, 'link': 'https://pwdata.ru/?page_id=362'},
        ]
        for q in quests_data:
            quest = Quest(**q)
            db.session.add(quest)
        db.session.commit()

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    level_filter = request.args.get('level', '')
    type_filter = request.args.get('type', '')
    diff_filter = request.args.get('difficulty', 5, type=int)
    
    query = Quest.query
    
    if search:
        query = query.filter(
            db.or_(
                Quest.title.ilike(f'%{search}%'),
                Quest.description.ilike(f'%{search}%')
            )
        )
    
    if level_filter:
        query = query.filter(Quest.level.ilike(f'%{level_filter}%'))
    
    if type_filter:
        query = query.filter(Quest.quest_type.ilike(f'%{type_filter}%'))
    
    query = query.filter(Quest.difficulty <= diff_filter)
    quests = query.paginate(page=page, per_page=9, error_out=False)
    
    return render_template('index.html', quests=quests, search=search, 
                         level_filter=level_filter, type_filter=type_filter)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
