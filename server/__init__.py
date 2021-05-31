import datetime
import os


from .fake_auth import auth_decorator, Middleware

# from pycharm - /home/misha/PycharmProjects/delete/server


import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

from flask import request, Flask, jsonify, Blueprint
from flask_cors import CORS, cross_origin

##DB##
from flask_sqlalchemy import SQLAlchemy

# from db import db as d #from IDE
from . db import db as d  #FROM  TERMINAL


# from flask_swagger import swagger
from flask_restplus import Api, Resource

# import constants, validator, request_parser - IDE
from . validations import  constants, validator, request_parser #TERMINAL

# from  validations import  constants, validator, request_parser #IDE

# from controllers import mainController # IDE
from . controllers import mainController # TERMINAL

def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    #BLUE PRINT FOR SWAGGER
    blueprint = Blueprint('api','__name__',url_prefix='/api/v1')
    api = Api(blueprint,doc='/documentation',version = "1.0",
		  title = "TODO LIST API",
		  description = "   TODO LIST API - \n\n"
                        "       USERS SIGN IN AND MANAGE THEIR REMINDERS \n"
                        "        TODO:  USE TO DO LIST - GET STATS - REMINDERS OF UPCOMING TASKS - AND SEE THEIR HISTORY")





    ns = api.namespace('task', description='Tasks')


    ns2= api.namespace('user', description='Tasks')


    ns3 = api.namespace('list', description='To-Do-List')


    ns4 = api.namespace('Combined', description='Things that envolve two or more parmeters of different elements ')


    ns5 = api.namespace('Fake Auth', description='AUTH API END POINT - TO DO ! ')

    app.register_blueprint(blueprint)

    app.config['SQLALCHEMY_DATABASE_URI'] = constants.DB_URI #SHOULD BE RED FROM A FILE
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False  #For Responses


    CORS(app, resources={r"/*": {"origins": "*"}}) #FOR COMUNICATING WITH REACT

    db = SQLAlchemy(app)
    d.init_db(db)

    # temp = True #should be passed as parameter from file - we don't always want to create DB
    # if temp :     db.create_all()

    main_controller = mainController.MainController(db)

    db.init_app(app) #SQLALCHEMY


    @app.before_request
    def hook():
        # request - flask.request
        print('endpoint: %s, url: %s, path: %s' % (
            request.endpoint,
            request.url,
            request.path))

    @ns.route('/<int:id>')
    class TaskResource(Resource):
      @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error',404:'Task Not Found'},
               params={'id': 'Specify the Id associated with the task'}
               )
      def get(self, id):
        res, valid,  = main_controller.todo_controller.get_task_by_id(id)
        if not valid:  return res[0], res[1]
        return ({'data': res.as_dict()}), 200

      @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Task Not Found'},
               params={'id': 'Specify the Id associated with the task to be deleted'}
               )

      def delete(self,id):
        res, valid = main_controller.todo_controller.delete_task_by_id(id)
        if not valid:   return {'data':res[0]} ,res[1]
        return {'data': res}, 200

      @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Task Not Found'},
               description='Updates Task ',
               params={
                   'id': 'Specify the Id associated with the task to be deleted',
                   'list_id': 'Id of the list to be deleted',
                   'type': 'String - type of task',
                   'text': 'String - text describing task',
                   'status': 'boolean - is completed',
                   'begin_date': 'begin time ',
                   'end_time': 'end time',

               }
           )
      def put(self, id):
          res, valid = request_parser.get_task_params_from_post_request(request.form)
          if not valid: return res[0], res[1]
          res, valid = main_controller.todo_controller.update_task(id, res)
          if not valid:    return res[0],res[1]
          return jsonify({'data': res}), 201


    # api.add_resource(TaskResource, '/task/<int:id>')
    @ns.route('/')
    class TaskResourcePost(Resource):

      @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Task Not Found'},description='Add Task',
               params={
                   'list_id': 'Id of the list to be added',
                   'type': 'String - type of task',
                   'text': 'String - text describing task',
                   'status': 'boolean - is completed',
                   'begin_date': 'begin time ',
                   'end_time': 'end time',

               }
               )
      def post(self):
        res, valid = request_parser.get_task_params_from_post_request(request)
        if not valid: return res[0], res[1]
        res, valid = main_controller.todo_controller.add_new_task(res)
        if not valid:  return res[0], res[1]
        reply = res.as_dict()
        return {'data': reply}, 201


    @ns2.route('/<int:id>')
    class UserResource(Resource):
      @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Task Not Found'},
               description='Get User by ID',
               params={'id': 'User Id'}
               )
      def get(self,id):
          res, valid = main_controller.user_controller.get_user_by_id(id)
          if not valid:   return res[0], res[1]
          return {'data': res.as_dict()}, 200

      @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Task Not Found'},
               description='Delete User By Id',
               params={'id': 'User Id'}
               )
      def delete(self,id):
        if not validator.valid_int(id):    return None, False, ('Error - invalid request param - id for task', 420)
        user,valid,err = main_controller.user_controller.delete_user_by_id(id)
        if not valid:   return err[0], err[1]
        return {'data': user},204

    # api.add_resource(UserResource, '/user/<int:id>')


    @ns2.route('/')
    
    class UserResourcePost(Resource):
      @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Task Not Found'},
               description='Add user',
               params={'username': 'String - Unique username','password': 'String - password'}
               )
      def post(self):
        res, valid = request_parser.get_user_data_from_post_request(dict(request.args))
        if not valid: return res[0], res[1]

        res, valid = main_controller.user_controller.add_user(res)

        if not valid:   return res[0], res[1]
        # return {'data':  user.as_dict()},201
        reply = res.as_dict()
        return {'data': reply}, 201

    # api.add_resource(UserResourcePost, '/user/')
    @ns3.route('/list/<int:id>')
    
    class ToDoListResource(Resource):
      @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Task Not Found'},
               description='Get List By ID',
               params={'id': 'int - list id'}
               )
      def get(self,id):
          res, valid = main_controller.todo_controller.get_list_by_id(id)
          if not valid:   return res[0], res[1]
          return {'data': res.as_dict()}, 201
      @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Task Not Found'},
               description='Update List By Id',
                 params={'id': 'int - list id', 'comment': 'string - comments on list', 'date': 'String - date',
                         'user_Id': 'id of list owner'}

               )
      def put(self, id):
          res, valid = request_parser.get_list_from_put_request(request, id)
          if not valid: return res[0], res[1]
          new_list, valid, err = main_controller.todo_controller.update_list(res, id)
          if not valid:   return err[0], err[1]
          return {'data': new_list}, 201

      @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Task Not Found'},
               description='Delete List By ID',
               params={'id': 'int - list id'}
               )
      def delete(self, id):
        deleted_task, valid, err = main_controller.todo_controller.delete_list_by_id(id)
        if not valid:   return err[0], err[1]
        return {'data': deleted_task}, 200

    # api.add_resource(ToDoListResource, '/list/<int:id>')
    @ns3.route('/list')
    
    class ToDoListResourcePost(Resource):
      @api.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error', 404: 'Task Not Found'},
               description='Add List ',
               params={'user_id': 'int - id of the user who owns the list', 'date': 'String - due date','comment': 'String - general comments'}
               )

      def post(self):
        res, valid = request_parser.get_to_do_list_from_post_request( dict(request.args))
        if not valid: return res[0], res[1]
        res['date'] = datetime.datetime.now()
        new_list, valid = main_controller.todo_controller.add_new_list(res)
        if not valid:        return new_list[0], new_list[1]
        reply = new_list.as_dict()
        return {'data': reply}, 201


    # api.add_resource(ToDoListResourcePost, '/list')


    @ns4.route('/tasks/<int:id>')
    
    class ListTaskResource(Resource):
        def get(self,id):
          res,valid ,  = main_controller.todo_controller.get_tasks_by_list_id(id)
          if valid == False:
            return jsonify({'data':res[0]}) ,res[1]
          return jsonify({'data': res.as_dict()}), 201

    # api.add_resource(ToDoListResourcePost, '/tasks/<int:id>')


    @ns4.route('/user/<int:id>/list')
    
    class ListUserResource(Resource):
        def get(self,id): #get_latest_list_by_user_id
            if not validator.valid_int(id):    return None, False, ('Error - invalid request param - id for task', 420)
            list, valid, err = main_controller.todo_controller.get_latest_list_by_user(id)
            if not valid:   return err[0], err[1]
            return {'data': list}, 200

    # api.add_resource(ListUserResource, '/user/<int:id>/list')

    @ns4.route('/user/<int:id>/stats')
    
    class StatsUserResource(Resource):
        def get(self,id): #get_user_stats
            if not validator.valid_int(id):    return None, False, ('Error - invalid request param - id for task', 420)
            user, valid, err = main_controller.todo_controller.get_stats_by_user_id(id)
            if not valid:   return err[0], err[1]
            return {'data': user}, 200


    # api.add_resource(StatsUserResource, '/user/<int:id>/stats')


    @ns4.route('/user/<int:id>/lists')
    
    class ListsUserResource(Resource):
        def get(self,id):
            if not validator.valid_int(id):    return None, False, ('Error - invalid request param - id for task', 420)
            all_lists, valid, err = main_controller.todo_controller.get_all_lists_by_user(id)
            if not valid:   return err[0], err[1]
            return {'data': all_lists}, 200


    # api.add_resource(ListsUserResource, '/user/<int:id>/lists')

    @ns4.route('/users/<int:id>/reminders')
    
    class GetReminderForUser(Resource):
        def get(self,id):
                if not validator.valid_int(id):    return None, False, (
                'Error - invalid request param - id for task', 420)
                reminders, valid, err = main_controller.todo_controller.get_valid_reminders_for_user(id)
                if not valid:   return err[0], err[1]
                return {'data': reminders}, 200

    # api.add_resource(ListsUserResource, '/users/<int:id>/reminders')




    @ns5.route('/logout')
    class logout(Resource):
        def post(self):
            return


    @ns5.route('/login')
    class login(Resource):
        def get(self):
            return {'token': 'ff', 'user': 'user data '}


    app.wsgi_app = Middleware(app.wsgi_app)

    return app





