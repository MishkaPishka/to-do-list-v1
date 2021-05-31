import os
#IDE
# from server.controllers.inner.to_do_list_controller import ToDoListController
# from server.controllers.inner.user_controller import UserController

print(os.getcwd())
from .inner.user_controller import UserController
from .inner.to_do_list_controller import ToDoListController


class MainController():

    def __init__(self, db):
        self.db = db  # instance variable unique to each instance
        self.user_controller = UserController(db)
        self.todo_controller = ToDoListController(db)
