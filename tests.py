#!/usr/bin/env python

from datetime import datetime, timedelta
from os import path
from unittest import TestCase, main
from app import app, db
from app.models import User, Post
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

    def test_follow(self):
        u1 = User(nickname='mas', email='mas@email.com')
        u2 = User(nickname='msa', email='msa@email.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) is None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().nickname == 'msa'
        assert u2.followers.count() == 1
        assert u2.followers.first().nickname == 'mas'
        u = u1.unfollow(u2)
        assert u is not None
        db.session.add(u)
        db.session.commit()
        assert not u1.is_following(u2)
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

    def test_follow_posts(self):
        u1 = User(nickname='mas', email='mas@email.com')
        u2 = User(nickname='msa', email='msa@email.com')
        u3 = User(nickname='shen', email='shen@email.com')
        u4 = User(nickname='chen', email='chen@email.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        utcnow = datetime.utcnow()
        p1 = Post(body='post from mas', author=u1,
                  timestamp=utcnow + timedelta(seconds=1))
        p2 = Post(body='post from msa', author=u2,
                  timestamp=utcnow + timedelta(seconds=2))
        p3 = Post(body='post from shen', author=u3,
                  timestamp=utcnow + timedelta(seconds=3))
        p4 = Post(body='post from chen', author=u4,
                  timestamp=utcnow + timedelta(seconds=4))
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.commit()
        u1.follow(u1)
        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u2)
        u2.follow(u3)
        u3.follow(u3)
        u3.follow(u4)
        u4.follow(u4)
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        assert len(f1) == 3
        assert len(f2) == 2
        assert len(f3) == 2
        assert len(f4) == 1
        assert f1 == [p4, p2, p1]
        assert f2 == [p3, p2]
        assert f3 == [p4, p3]
        assert f4 == [p4]


if __name__ == '__main__':
    main()