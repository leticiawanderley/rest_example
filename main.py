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
import webapp2, re

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class PostCollectionHandler(webapp2.RequestHandler):

    def get(self):
        # 200 (OK), list of Posts. JSON content-type
        pass

    def head(self):
        # 200 (OK), JSON content-type
        pass

    def post(self):
        #201 (Created), 'Location' header with link to /post/:id containing new ID.
        pass


class PostIndividualHandler(webapp2.RequestHandler):
    def get(self, id):
        #200 (OK), the post. 404 (Not Found), if ID not found or invalid. JSON content-type
        pass

    def head(self, id):
        #200 (OK). 404 (Not Found), if ID not found or invalid. JSON content-type
        pass

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
