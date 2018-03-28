from os import path
from unittest import TestCase, main
from app import app, db
from app.models import User
from config import basedir


class TestCase(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            f"sqlite:///{path.join(basedir, 'test.db')}"
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_avatar(self):
        u = User(nickname='mas', email='mas@email.com')
        avatar = u.avatar(128)
        expected = \
            'http://www.gravatar.com/avatar/258831cdbf17d25332d71f3e06f7723f'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        u = User(nickname='mas', email='mas@email.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('mas')
        assert nickname != 'mas'
        u = User(nickname=nickname, email='msa@email.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('mas')
        assert nickname2 != 'mas'
        assert nickname2 != nickname


if __name__ == '__main__':
    main()
