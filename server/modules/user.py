from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pw_hash = db.Column(db.String(80), nullable=False)

    # some extra feild
    def __init__(self, username, pw_hash):
        self.username = username
        self.pw_hash = pw_hash

    def __repr__(self):
        return '<User %r>' % self.username

    def delete(self):
        try:
            result = db.session.execute('DELETE  FROM user WHERE user.id = :val', {'val': id})
            return db.session.commit()
        except Exception as e:

                print("Exception:"+e )
                return None
    def as_dict(self):
        return {'username': self.username, 'ps': self.pw_hash}



