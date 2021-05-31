from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


from server.modules.todolist import ToDoList

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey(ToDoList.id), nullable=False)

    type = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(180), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    begin_date = db.Column(db.DateTime, nullable=True, default=None)
    end_time = db.Column(db.DateTime, nullable=True, default=None)

    def as_dict(self):
        return {'id': self.id, 'list_id': self.list_id, 'type': self.type, 'text': self.text, 'status': self.status,
                'begin_date': self.begin_date, 'end_time': self.end_time}
