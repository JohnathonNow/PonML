#!/usr/bin/env python3
import cherrypy
import parse

class API(object):
    @cherrypy.expose
    def index(self, script):
        return parse.parse(script)

cherrypy.quickstart(API())
