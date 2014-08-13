#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, re, json, jinja2, os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Comment:
    def __init__(self, comment, id):
        self.id = id
        self.comment = comment
     
    def todict(self):
        dict1 = {}
        dict1["id"] = self.id
        dict1["comment"] = self.comment
        return dict1
    

class Post:
    posts = []
    seed = 0

    def __init__(self, msg):
        self.id = Post.seed
        self.msg = msg
        self.comments = []
        self.posts.append(self)
        self.comment_seed = 0
        Post.seed += 1

    def add_comment(self, new_comment):
        self.comments.append(Comment(new_comment, self.comment_seed))
        self.comment_seed += 1
        return self.comment_seed - 1

    def todict(self):
        dict1 = {}
        dict1["id"] = self.id
        dict1["msg"] = self.msg
        dict1["comments"] = []
        for comment in self.comments:
            dict1["comments"].append(comment.todict())
        return dict1

def list_dicts_posts():
   dicts = []
   for post in Post.posts:
       dicts.append("http://rest-exercise.appspot.com/post/"+str(post.id))
   return dicts

def list_dicts_comments(id_post):
   dicts = []
   post = get_by_id(id_post)
   if post:
       for comment in post.comments:
           dicts.append("http://rest-exercise.appspot.com/post/"+str(post.id) +"/comment/" + str(comment.id))
   return dicts

def get_by_id(id):
   for post in Post.posts:
       if int(id) == post.id: return post
   return None


def get_comment_by_id(id_post, id_comment):
   post = get_by_id(id_post)
   if post:
        for comment in post.comments:
            if int(id_comment) == comment.id: 
                return comment
   return None

class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_values = {}
        main = jinja_environment.get_template('main.html')
        self.response.out.write(main.render(main_values))

class PostCollectionHandler(webapp2.RequestHandler):

    def get(self):
        if self.request.headers["Accept"] == "application/json":
            self.response.out.write(json.dumps(list_dicts_posts()))
            self.response.set_status(200)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            # 200 (OK), list of Posts. JSON content-type
        elif self.request.headers["Accept"] == "text/html":
            pass  #TODO
        else:
            self.response.set_status(406)

    def head(self):
        if self.request.headers["Accept"] == "application/json":
            self.response.set_status(200)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            # 200 (OK), JSON content-type
        elif self.request.headers["Accept"] == "text/html":
            pass  #TODO
        else:
            self.response.set_status(406)

    def post(self):
        post = Post(self.request.get("msg"))
        self.response.set_status(201)
        self.response.headers.add_header('Location', '/post/' + str(post.id), charset='utf-8')
        #201 (Created), 'Location' header with link to /post/:id containing new ID.


class PostIndividualHandler(webapp2.RequestHandler):
    def get(self, id):
        post = get_by_id(id)
        if post:
            if self.request.headers["Accept"] == "application/json":
                self.response.write(json.dumps(post.todict()))
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
        post = get_by_id(id)
        if post:
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
        post = get_by_id(id)
        if post:
            post.msg = self.request.get("msg")
            self.response.set_status(204)
        else:
            self.response.set_status(404)
        #204 (No Content). 404 (Not Found), if ID not found or invalid.
        

    def delete(self, id):
        post = get_by_id(id)
        if post:
            Post.posts.remove(post)
            self.response.set_status(200)	    
        else:
            self.response.set_status(404)
        #200 (OK). 404 (Not Found), if ID not found or invalid.
        

class CommentCollectionHandler(webapp2.RequestHandler):

    def get(self, id):
        post = get_by_id(id)
        if post:
            if self.request.headers["Accept"] == "application/json":
                self.response.out.write(json.dumps(list_dicts_comments(id)))
                self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
                self.response.set_status(200)
            elif self.request.headers["Accept"] == "text/html":
                pass # TODO
            else:
                self.response.set_status(406)
        else:
            self.response.set_status(404)
        # 200 (OK), list of Comments. JSON content-type

    def head(self, id):
        post = get_by_id(id)
        if post:
            if self.request.headers["Accept"] == "application/json":
                self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
                self.response.set_status(200)
            elif self.request.headers["Accept"] == "text/html":
                pass # TODO
            else:
                self.response.set_status(406)
        else:
            self.response.set_status(404)
        # 200 (OK), JSON content-type

    def post(self, id):
        post = get_by_id(id)
        if post:
            id_comment = post.add_comment(self.request.get("msg"))
            self.response.set_status(201)	    
            self.response.headers.add_header('Location', '/post/' + str(post.id) + "/comment/" + str(id_comment), charset='utf-8')
        else:
            self.response.set_status(404)
        #201 (Created), 'Location' header with link to /post/:id/comment/:id containing new ID.


class CommentIndividualHandler(webapp2.RequestHandler):
    def get(self, id_post, id_comment):
        post = get_by_id(id_post)
        if post:
            comment = get_comment_by_id(id_post, id_comment)
            if comment:
                if self.request.headers["Accept"] == "application/json":
                    self.response.out.write(json.dumps(comment.todict()))
                    self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
                    self.response.set_status(200)
                elif self.request.headers["Accept"] == "text/html":
                    pass # TODO
                else:
                    self.response.set_status(406)
            else:
                self.response.set_status(404)
        else:
            self.response.set_status(404)
        #200 (OK), the post. 404 (Not Found), if ID not found or invalid. JSON content-type


    def head(self, id_post, id_comment):
        post = get_by_id(id_post)
        if post:
            comment = get_comment_by_id(id_post, id_comment)
            if comment:
                if self.request.headers["Accept"] == "application/json":
                    self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
                    self.response.set_status(200)
                elif self.request.headers["Accept"] == "text/html":
                    pass # TODO
                else:
                    self.response.set_status(406)
            else:
                self.response.set_status(404)
        else:
            self.response.set_status(404)
        #200 (OK). 404 (Not Found), if ID not found or invalid. JSON content-type

    def put(self, id_post, id_comment):
        post = get_by_id(id_post)
        if post:
            comment = get_comment_by_id(id_post, id_comment)
            if comment:
                comment.comment = self.request.get("msg")
                self.response.set_status(204)
            else:
                self.response.set_status(404)
        else:
            self.response.set_status(404)
        #204 (No Content). 404 (Not Found), if ID not found or invalid.
        

    def delete(self, id_post, id_comment):
        post = get_by_id(id_post)
        if post:
            comment = get_comment_by_id(id_post, id_comment)
            if comment:
                post.comments.remove(comment)
                self.response.set_status(200)
            else:
                self.response.set_status(404)
        else:
            self.response.set_status(404)
        #200 (OK). 404 (Not Found), if ID not found or invalid.
        


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    (r'/post/(\d+)', PostIndividualHandler),
    ('/post', PostCollectionHandler),
     (r'/post/(\d+)/comment', CommentCollectionHandler),
    (r'/post/(\d+)/comment/(\d+)', CommentIndividualHandler)
   
], debug=True)
