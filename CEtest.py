#!/usr/bin/env python
import rdflib
import cgi

form = cgi.FieldStorage()
year = form.getvalue('yr')

graph = rdflib.Graph()

top = """
<html lang="en"><head> <meta charset="utf-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1"> <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags --> <meta name="description" content=""> <meta name="author" content=""> <link rel="icon" href="http://165.82.13.162/images/favicon.ico"> <title>Linked Data</title> <!-- Bootstrap core CSS --> <link href="http://165.82.13.162/css/bootstrap/css/bootstrap.min.css" rel="stylesheet"> <!-- IE10 viewport hack for Surface/desktop Windows 8 bug --> <link href="http://165.82.13.162/css/bootstrap/css/assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet"> <!-- Custom styles for this template --> <link href="http://165.82.13.162/css/bootstrap/css/sticky-footer.css" rel="stylesheet"> </head> <body> <!-- Begin page content --> <div class="container"> <div class="page-header"> <h1>Linked Data</h1> </div>
"""

bottom = """
</div> <footer class="footer"> <div class="containe
r"> <p class="text-muted">Haverford College</p> </d
iv> </footer> </body></html>
"""



graph.parse('CEtravls.ttl',format='turtle')

if "-" in year: #assume its a range! DOESNT HANDLE INPUT ERROR WITH MULTIPLE "-"
	y1, y2 = year.split("-")
#	y1 = int(y1)
#	y2 = int(y2)

	queryString = """
	prefix p: <localhost:3030/ds/person#> 
	prefix t: <localhost:3030/ds/trip#> 
	prefix d:<localhost:3030/ds/date#>
	prefix letter:<localhost:3030/ds/letter#>	

	SELECT ?name ?loc ?month ?year 
	WHERE
	{ ?m p:Name ?name ;
               p:trip  ?thetrip .
	?thetrip t:location ?loc;
              d:date_m ?month;
              d:date_y ?year .
              FILTER( ?year >= YEAR2)
              FILTER( ?year <= YEAR1)
	}		
	"""

	queryString = queryString.replace("YEAR1",y2)
	queryString = queryString.replace("YEAR2",y1)
	
	result = graph.query(queryString)
        print """
        <html><head><title>results</title>
        <style type="text/css"> * { font-family: arial,helvetica}</style>
        </head><body>
        """
        print "<p>" + queryString + " </p>"

        print "<h1> Travels in : "+ str(year) + " </h1>"
        for row in result:
                print("<p>  %s traveled to  %s in  %s %s </p> " % row)

        print "</body></html>"

else:

	queryString = """
	prefix p: <localhost:3030/ds/person#> 
	prefix t: <localhost:3030/ds/trip#> 
	prefix d:<localhost:3030/ds/date#>
	prefix letter:<localhost:3030/ds/letter#>

	SELECT ?name ?loc ?month  
	WHERE
	{ ?m p:Name ?name ;
		p:trip  ?thetrip .
	?thetrip t:location ?loc ;
		d:date_m ?month ;
		d:date_y YEAR .
	}
	"""

	queryString = queryString.replace("YEAR",year)
	result = graph.query(queryString)
	print top
	print "<p>" + queryString + " </p>"

	print "<h1> Travels in : "+ str(year) + " </h1>" 
	for row in result:
    		print("<p>  %s traveled to  %s in  %s </p> " % row)

	print bottom
