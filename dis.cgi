#!/usr/bin/env python
import rdflib
import cgi

form = cgi.FieldStorage()
name = form.getvalue('name')

top = """
<html lang="en"><head> <meta charset="utf-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1"> <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags --> <meta name="description" content=""> <meta name="author" content=""> <link rel="icon" href="http://165.82.13.162/images/favicon.ico"> <title>Linked Data</title> <!-- Bootstrap core CSS --> <link href="http://165.82.13.162/css/bootstrap/css/bootstrap.min.css" rel="stylesheet"> <link href="http://165.82.13.162/css/style.css" rel="stylesheet"> <!-- IE10 viewport hack for Surface/desktop Windows 8 bug --> <link href="http://165.82.13.162/css/bootstrap/css/assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet"> <!-- Custom styles for this template --> <link href="http://165.82.13.162/css/bootstrap/css/sticky-footer.css" rel="stylesheet"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script> <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script> </head> <body> <!-- Begin page content --> <div class="container"> <div class="page-header"> <h1><a href='http://165.82.13.162/LinkedData.html'>Linked Data</a></h1> </div>
"""

bottom = """
</div> <footer class="footer"> <div class="container"> <p class="text-muted">Haverford College</p> </div> </footer> </body></html>
"""


paneltop = """
<div class="panel-group"> <div class="panel panel-default"> <div class="panel-heading"> <h4 class="panel-title"> <a data-toggle="collapse" href="#collapse1">
"""
#name of panel goes inbetween
panelmid = """
</a><span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span> </h4> </div> <div id="collapse1" class="panel-collapse collapse"> <ul class="list-group">
"""

panelbottom = """
</ul></div> </div> </div>
"""


# ASSUMES PERFECT SPELLING ( NO REGEXP )
graph = rdflib.Graph()
graph.parse('CEpeople.ttl', format= 'turtle')


querynames = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d: <localhost:3030/ds/date#>

SELECT ?id ?name 
WHERE {
  ?id p:labelname ?name .
  FILTER (REGEX(?name, "REPLACEME", "i"))

}
"""                  



querynames = querynames.replace("REPLACEME",name)
#print queryString

#stores the searches
result = graph.query(querynames)


x = len(result)
print("<div class='sidebar' style='float:left;'><b><p>" + str(x) + " Similar results for " + str(name)+"</p></b>")
for row in result:
        print("<a href=http://165.82.13.162/cgi-bin/CEperson.cgi?name=%s> <p>  %s</p> </a> " % row)
print"</div>"






print panelbottom
