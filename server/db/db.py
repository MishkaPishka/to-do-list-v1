from datetime import datetime

from sqlalchemy.orm import relationship


def init_db(db):



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

        def as_dict(self):
            return {'username': self.username, 'ps': self.pw_hash}

    class ToDoList(db.Model):
        __tablename__ = 'todolist'
        id = db.Column(db.Integer, primary_key=True)
        # user_id = db.relationship('user', backref='todolist', lazy=True)
        user_id = db.Column(db.Integer, db.ForeignKey( User.id),nullable=False)

        date = db.Column(db.DateTime, nullable=True, default=None)
        comment =  db.Column(db.String(80), nullable=False)

        def as_dict(self):
            return {'id':self.id,'user_id': self.user_id, 'date': str(self.date), 'comment': self.comment}

    class Task(db.Model):
        __tablename__ = 'task'
        id = db.Column(db.Integer, primary_key=True)
        list_id = db.Column(db.Integer, db.ForeignKey(ToDoList.id),nullable=False)

        type = db.Column(db.String(80), nullable=False)
        text = db.Column(db.String(180), nullable=False)
        status = db.Column(db.String(10), nullable=False)
        begin_date = db.Column(db.DateTime, nullable=True, default=None)
        end_time = db.Column(db.DateTime, nullable=True, default=None)

        def as_dict(self):
            return {'id': self.id, 'list_id': self.list_id,'type': self.type,'text': self.text,'status': self.status,'begin_date': self.begin_date,'end_time': self.end_time}
    return User,Task,ToDoList

# def count_items_in_list(user_id,list_id):
#     pass
# def get_user_by_name(user_name,list_id):
#     pass