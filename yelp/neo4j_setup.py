 ###Setting up the HTTP or HTTPS connection:
 #import os
 #from py2neo import Graph
 ##from py2neo import authenticate
 #from urlparse import urlparse, urlunparse
 #
 #url = urlparse(os.environ.get("GRAPHENEDB_URL"))
 #url_without_auth = urlunparse((url.scheme, "{0}:{1}".format(url.hostname, url.port), '', None, None, None))
 #user = url.username
 #password = url.password
 #
 ##authenticate(url_without_auth, user, password)
 #graph = Graph(url_without_auth, bolt = False)

##Setting up the Bolt/TLS connection:
import os
from py2neo import Graph

graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")
graph = Graph(graphenedb_url, user=graphenedb_user, password=graphenedb_pass, bolt = True, secure = True, http_port = 24789, https_port = 24780)


