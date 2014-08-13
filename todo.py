
import webapp2, re, json

class Todo:
    seed = 0
    todos = []

    def __init__(self, description):
      self.id = Todo.seed
      self.description = description
      self.done = False
      self.todos.append(self)
      Todo.seed += 1

    def todict(self):
        dict1 = {}
        dict1["id"] = self.id
        dict1["description"] = self.description
        dict1["done"] = self.done
        return dict1

def list_dicts_todos():
   dicts = []
   for todo in Todo.todos:
       dicts.append("http://rest-exercise.appspot.com/todo/"+ str(todo.id))
   return dicts

def get_by_id(id):
   for todo in Todo.todos:
       if int(id) == todo.id: 
          return todo
   return None            

class TodoCollectionHandler(webapp2.RequestHandler):

    def get(self):
        if self.request.headers["Accept"] == "application/json":
            self.response.out.write(json.dumps(list_dicts_todos()))
            self.response.set_status(200)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        elif self.request.headers["Accept"] == "text/html":
            pass  #TODO
        else:
            self.response.set_status(406)
        # 200 (OK), list of Posts. JSON content-type

    def head(self):
        if self.request.headers["Accept"] == "application/json":
            self.response.set_status(200)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        elif self.request.headers["Accept"] == "text/html":
            pass  #TODO
        else:
            self.response.set_status(406)
        # 200 (OK), JSON content-type

    def post(self):
        todo = Todo(self.request.get("description"))
        self.response.set_status(201)
        self.response.headers.add_header('Location', '/todo/' + str(todo.id), charset='utf-8')
        #201 (Created), 'Location' header with link to /post/:id containing new ID.

class TodoIndividualHandler(webapp2.RequestHandler):
    def get(self, id):
        todo = get_by_id(id)
        if todo:
            if self.request.headers["Accept"] == "application/json":
                self.response.write(json.dumps(todo.todict()))
                self.response.set_status(200)
                self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            elif self.request.headers["Accept"] == "text/html":
                pass  #TODO
            else:
                self.response.set_status(406)
        else:
            self.response.set_status(404)
        #200 (OK), the post. 404 (Not Found), if ID not found or invalid. JSON content-type

            
    def head(self, id):
        todo = get_by_id(id)
        if todo:
            if self.request.headers["Accept"] == "application/json":
                self.response.set_status(200)
                self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            elif self.request.headers["Accept"] == "text/html":
                pass  #TODO
            else:
                self.response.set_status(406)
        else:
            self.response.set_status(404)
        #200 (OK). 404 (Not Found), if ID not found or invalid. JSON content-type

    def put(self, id):
        todo = get_by_id(id)
        if todo:
            todo.description = self.request.get("description")
            todo.done = True if self.request.get("done") ==  "true" else False
            self.response.set_status(204)
        else:
            self.response.set_status(404)
        #204 (No Content). 404 (Not Found), if ID not found or invalid.
        

    def delete(self, id):
        todo = get_by_id(id)
        if todo:
            Todo.todos.remove(todo)
            self.response.set_status(200)          
        else:
            self.response.set_status(404)
        #200 (OK). 404 (Not Found), if ID not found or invalid.

app = webapp2.WSGIApplication([
    (r'/todo/(\d+)', TodoIndividualHandler),
    ('/todo', TodoCollectionHandler)
], debug=True)
