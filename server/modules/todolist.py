from flask_sqlalchemy import SQLAlchemy

from server.modules.user import User

db = SQLAlchemy()


class ToDoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.relationship('user', backref='todolist', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    date = db.Column(db.DateTime, nullable=True, default=None)
    comment = db.Column(db.String(80), nullable=False)

    def as_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'date': str(self.date), 'comment': self.comment}

