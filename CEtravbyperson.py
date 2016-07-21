#!/usr/bin/env python
import rdflib
import cgi

#form = cgi.FieldStorage()
#name = form.getvalue('name')

graph = rdflib.Graph()
graph.parse('CEtravls.ttl',format='turtle')

top = """
<html lang="en"><head> <meta charset="utf-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1"> <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags --> <meta name="description" content=""> <meta name="author" content=""> <link rel="icon" href="http://165.82.13.162/images/favicon.ico"> <title>Linked Data</title> <!-- Bootstrap core CSS --> <link href="http://165.82.13.162/css/bootstrap/css/bootstrap.min.css" rel="stylesheet"> <!-- IE10 viewport hack for Surface/desktop Windows 8 bug --> <link href="http://165.82.13.162/css/bootstrap/css/assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet"> <!-- Custom styles for this template --> <link href="http://165.82.13.162/css/bootstrap/css/sticky-footer.css" rel="stylesheet"> </head> <body> <!-- Begin page content --> <div class="container"> <div class="page-header"> <h1>Linked Data</h1> </div>
"""

bottom = """
</div> <footer class="footer"> <div class="containe
r"> <p class="text-muted">Haverford College</p> </d
iv> </footer> </body></html>
"""


queryString = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

SELECT ?loc ?month ?day ?year 
WHERE
{ ?m p:Name "Jonathan Evans" ;
	p:trip  ?thetrip .
?thetrip t:location ?loc ;
	d:date_m ?month ;
	d:date_d ?day ;
	d:date_y ?year .
}
"""

queryString = queryString.replace("REPLACEME",name)
result = graph.query(queryString)
print top
print "<p>" + queryString + " </p>"

print "<h1> Travels by  "+ str(name) + " </h1>" 
for row in result:
	print("<p>  traveled to  %s on  %s %s %s </p> " % row)

print bottom
