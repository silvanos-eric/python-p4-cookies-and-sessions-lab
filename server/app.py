#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, session
from flask_migrate import Migrate
from models import Article, User, db

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/clear')
def clear_session():
    session['page_views'] = 0

    return {'message': '200: Successfully cleared session data.'}, 200


@app.route('/articles')
def index_articles():
    article_list = Article.query.all()

    article_dict_list = [
        article.to_dict(rules=('-content', )) for article in article_list
    ]

    return article_dict_list


@app.route('/articles/<int:id>')
def show_article(id):
    if 'page_views' not in session:
        session['page_views'] = 0

    print(session['page_views'])

    if session['page_views'] < 3:
        article = db.session.get(Article, id)

        session['page_views'] += 1

        return jsonify(article.to_dict())

    else:
        session['page_views'] += 1

        return jsonify(message='Maximum pageview limit reached'), 401


if __name__ == '__main__':
    app.run(port=5555)
