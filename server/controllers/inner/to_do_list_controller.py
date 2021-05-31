from sqlalchemy import func

#IDE
# from server.modules.todolist import ToDoList
# from server.modules.task import Task

#TERMINAL
# from modules.todolist import ToDoList
# from modules.task import Task

#TERMINAL
import os
print(os.getcwd())

#IDE
from server.modules.task import Task
from server.modules.todolist import ToDoList


class ToDoListController():
    def __init__(self, db):
        self.db = db  # instance variable unique to each instance
    def get_session(self):
        return self.db.session

    #TODO
    def update_task(self, taskid, task_id_fields):
        #$GET TASK
        try:
            task = self.db.session.query(Task).filter(Task.id == taskid)
            reply = self.db.session.query(Task).filter(Task.id == taskid).update(task_id_fields)
            self.db.session.commit()
            return reply,True
        except Exception as e:
            return e.__repr__(),400
        #CHANCHE FELDS
        #commit


    def get_latest_list_by_user(self,user_id):
        self.db.session.query(func.max(ToDoList.id)).scalar()
        self.db.session.query(ToDoList). filter(ToDoList.user_id == user_id)
        query_str ='SELECT MAX(id),user_id from todolist where user_id ='+user_id +' GROUP BY (user_id)'
        result = self.db.session.execute(query_str)
        return self.db.session.commit()

    def get_all_lists_by_user(self, user_id):
        self.db.session.query(ToDoList).filter(ToDoList.user_id == user_id)
        query_str = 'SELECT * from todolist where todolist.user_id like '+str(user_id)
        return self.db.session.connection().execute(query_str)


    def get_valid_reminders_for_user(self, id):
        #GET TASKS FOR USER
        #GET TAKS WHERE TIME IS RIGHT NOW
        query_str = 'SELECT * from task where task.list_id in (select todolist.id from todolist join user on todolist.id = user.list_id and user.id like '+str(id)
        print(query_str)
        return self.db.session.connection().execute(query_str)


    def add_new_task(self, task_id_fields):
        try:
            task = Task(**task_id_fields)
            self.db.session.add(task)
            self.db.session.commit()
            return task,True
        except Exception as e :
            return e.__repr__(),False

    def delete_task_by_id(self, id):
        try:

            task = Task.query.get(id)
            if task is None:  return None, False, ("Task with id:{} Not Found".format(id),404)
            self.db.session.delete(task)
            self.db.session.commit()
            return task,True
        except Exception as e:
            return e.__repr__(), False

    def get_task_by_id(self,id):
            task = Task.query.get(id)
            if task is None:  return  ("Task with id:{} Not Found".format(id),404),False
            return task,True

    def get_tasks_by_list_id(self, id):
        val =  ToDoList.query.filter(ToDoList.id == id)
        if val is None:  return  ("Task with id:{} Not Found".format(id),404), False
        return  val, True,

    def add_new_list(self, list_fields):
        try:
            list = ToDoList(**list_fields)
            self.db.session.add(list)
            self.db.session.commit()
            return list, True
        except Exception as e:
            print(e.__repr__())
            return (e.__repr__(),400),False

    def get_list_by_id(self,id):
        try:
            list = ToDoList.query.get(id)
            return list, True
        except Exception as e:
            print(e.__repr__())
            return (e.__repr__(),400),False
    def delete_list_by_id(self, id):
        #DELETE LIST
        #DELETE TASKS OF LIST
        #SHOULD BE A TRANSACTION
        try :
            ToDoList.query.filter(ToDoList.id == id).delete()
            Task.query.filter(Task.list_id == id).delete()
            return 'deleted_task', True, None
        except Exception as e:
            print(e.__repr__())
            return '"ERROR"', True,

    def update_list(self, list_fields, id):
        try:
            reply = self.db.session.query(ToDoList).filter_by(id=id).update(list_fields)
            return reply, True
        except Exception as e:
            print(e)
            return 'update_list error', False

    def get_stats_by_user_id(self,user_id):
        query_str = 'SELECT Count(*),status from task where task.list_id in (select todolist.id from todolist join user on todolist.id = user.list_id and user.id like ' + str(
            id) + ' GROUP BY (status)'
        res =  self.db.session.connection().execute(query_str)
        done = res[1][0]
        not_done = res[0][0]
        return float(done)/not_done, True













