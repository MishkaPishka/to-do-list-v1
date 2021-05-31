from cerberus import Validator



from functools import wraps

def get_user_id_schema():
    schema =  {'id':{'type': 'int', 'required': True}}
    return Validator(schema)

def is_id_valid(val):
    try:
         str(val)
         return True

    except ValueError:
        return False

def get_user_registration_schema():
    user_registeration_schema = {'username': {'type': 'string', 'required': True},
                                 'password': {'type': 'string', 'required': True}}

    return Validator(user_registeration_schema)
def user_registeration_validation():
    return Validator(get_user_registration_schema())
#TODO
#schema for every request type ex

def get_to_do_list_schema():
    schema = {
        'user_id': {'required': True}, # this version doesnt support int - Changed in version 0.5.1: Added support for the int type.
                 'date': {'type': 'string', 'required': True},
                'comment': {'type': 'string', 'required': True}

              }
    return Validator(schema)


def get_post_task_schema():
    schema = {
              'list_id': {'type': 'string', 'required': True} ,
              'type': {'type': 'string', 'required': True},
               'text': {'type': 'string', 'required': True},
               'status': {'type': 'string', 'required': True},
               # 'begin_date': {'type': 'DateTime', 'required': True},
        #       'end_time': {'type': 'DateTime', 'required': True},

              }

    return Validator(schema)



