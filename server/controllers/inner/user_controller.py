from server.modules.user import User
from server.modules.task import Task
from server.modules.todolist import ToDoList


# from modules.user import User #IDE


class UserController():
    def __init__(self, db):
        self.db = db    # instance variable unique to each instance
    def add_user(self,user_data):
        try:
            user_to_add = User(user_data['username'],user_data['password']) #TODO password needs to be hashed
            print("user to add - before:"+ user_to_add.__repr__())
            self.db.session.add(user_to_add)
            self.db.session.commit()
            return user_to_add,True
        except Exception as e:
            print(e.__repr__())
            return  ("Couldn't add user",405), False

    def delete_user_by_id(self,user_id):
        try:
            user = User.query.get(user_id)
            if user is None:  return 'User ID not in System',404
            User.query.filter(User.id == user_id).delete()
            Task.query.filter(Task.user_id == user_id).delete()
            ToDoList.query.filter(ToDoList.user_id == user_id).delete()
            self.db.session.commit()
            return user.as_dict()
        except Exception as e:
            print(e.__repr__())
            return None, False, ("Couldn't delete user", 400)

    def get_user_by_id(self,id):
        try :
            user = User.query.get(id)
            if user is None:
                print("User with id:"+str(id)+" not in DB")
                return ("User Not Available",404),False
            return user, True
        except Exception as e:
            print("GET USER BY ID ERROR:"+e.__repr__())
            return (e.__repr__(),400), False


