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
import webapp2, re, json

class Post:
    posts = []

    def __init__(self, msg):
        self.id = len(Post.posts)
        self.msg = msg
        self.comments = []
        self.posts.append(self.__dict__)

    def add_comment(self, new_comment):
        self.comments.append(new_comment)

    def __dict__(self):
        dict = {}
        dict["id"] = self.id
        dict["msg"] = self.msg
        dict["comments"] = self.comments
        return dict

    def getById(self, id):
        for post in self.posts:
            if id == post.id: return post
        return None


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class PostCollectionHandler(webapp2.RequestHandler):

    def get(self):
        self.response.out.write(json.dumps(Post.posts))
        self.response.set_status(200)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        # 200 (OK), list of Posts. JSON content-type

    def head(self):
        self.response.set_status(200)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        # 200 (OK), JSON content-type

    def post(self):
        post = Post(self.request.get("msg"))
        self.response.set_status(201)
        self.response.headers.add_header('Location', '/post' + str(post.id), charset='utf-8')
        #201 (Created), 'Location' header with link to /post/:id containing new ID.


class PostIndividualHandler(webapp2.RequestHandler):
    def get(self, id):
        post = Post.getById(id)
        if post:
            self.response.write(post.__dict__())
            self.response.set_status(200)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        else:
            self.response.set_status(404)
        #200 (OK), the post. 404 (Not Found), if ID not found or invalid. JSON content-type


    def head(self, id):
        post = Post.getById(id)
        if post:
            self.response.set_status(200)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        else:
            self.response.set_status(404)
        #200 (OK). 404 (Not Found), if ID not found or invalid. JSON content-type

    def put(self, id):
        #204 (No Content). 404 (Not Found), if ID not found or invalid.
        pass

    def delete(self, id):
        #200 (OK). 404 (Not Found), if ID not found or invalid.
        pass

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/post', PostCollectionHandler),
    (r'/post/(\d+)', PostIndividualHandler)
], debug=True)
