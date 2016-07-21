#!/usr/bin/env python
# filename: test.cgi
# CGI version of test.py

import sys
import cgi
#sys.path.append('/usr/home/bobd/lib/python/') # needed for hosted version
#sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7') # needed for hosted version
from SPARQLWrapper import SPARQLWrapper, JSON


form = cgi.FieldStorage()
director1 = form.getvalue('dir1')
director2 = form.getvalue('dir2')
#director1 = "Steven Spielberg"
#director2 = "Stanley Kubrick"

sparql = SPARQLWrapper("http://data.linkedmdb.org/sparql")
queryString = """
PREFIX m:    <http://data.linkedmdb.org/resource/movie/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT ?actorName ?freebaseURI WHERE {

  ?dir1     m:director_name "DIR1-NAME" .
  ?dir2     m:director_name "DIR2-NAME" .

  ?dir1film m:director ?dir1 ;
            m:actor ?actor .

  ?dir2film m:director ?dir2 ;
            m:actor ?actor .

  ?actor    m:actor_name ?actorName ;
            foaf:page ?freebaseURI . 
}
"""

queryString = queryString.replace("DIR1-NAME",director1)
queryString = queryString.replace("DIR2-NAME",director2)
sparql.setQuery(queryString)

sparql.setReturnFormat(JSON)

try:
  results = sparql.query().convert()
  requestGood = True
except Exception, e:
  results = str(e)
  requestGood = False

print """Content-type: text/html

<html><head><title>results</title>
<style type="text/css"> * { font-family: arial,helvetica}</style>
</head><body>
"""

if requestGood == False:
  print "<h1>Problem communicating with the server</h1>"
  print "<p>" + results + "</p>"
elif (len(results["results"]["bindings"]) == 0):
  print "<p>No results found.</p>"

else:

  print "<h1>Actors directed by both " + director1 + \
        " and " + director2 + "</h1>"

  for result in results["results"]["bindings"]:
    actorName = result["actorName"]["value"]
    freebaseURI = result["freebaseURI"]["value"]
    print "<p><a href=\"" + freebaseURI + "\">" + actorName + "</p>"

print "</body></html>"    
