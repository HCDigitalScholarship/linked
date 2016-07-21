#!/usr/bin/env python
import rdflib

#form = cgi.FieldStorage()
#year = form.getvalue('yr')
year = 1873

graph = rdflib.Graph()

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
	d:date_y 1873 .
}
"""

#queryString = queryString.replace("YEAR",year)

graph.parse('CEtravls.ttl',format='turtle')
result = graph.query(queryString)


print """
<html><head><title>results</title>
<style type="text/css"> * { font-family: arial,helvetica}</style>
</head><body>
"""


print "<h1> Travels in :"+ str(year) + " </h1>" 
for row in result:
    print("<p>  %s traveled to  %s on  %s </p> " % row)

print "</body></html>"
