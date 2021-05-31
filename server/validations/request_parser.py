from server.validations import validator

#VALIDATE AND PARSE

def get_task_id_from_request(data):
    return data['id']

def get_task_params_from_post_request(request):
  if not ( validator.get_post_task_schema().validate(dict(request.args))):    return ('Error - invalid request param -  for task',400),False
  # task_id_fields,valid  = get_task_id_from_request(request)
  # if not valid :   return  ('Error - invalid body parameter for task',400),False
  return dict(request.args), True

def get_to_do_list_from_post_request(data, todo_list_id= -1):
  if not validator.get_to_do_list_schema().validate(data):    return ('Error - invalid request param - id for to do list', 420), False
  return data ,True



def get_user_data_from_post_request(data_as_dict):
  if not   validator.get_user_registration_schema().validate(data_as_dict): return ('Error - invalid request for user ', 400), False
  return {'username': data_as_dict['username'], 'password': data_as_dict['password']}, True

def get_list_from_put_request(data, todo_list_id):
  if not (validator.valid_int(todo_list_id) or validator.get_to_do_list_schema().validate(data)):    return ('Error - invalid request param - id for to do list', 420), False

  return None