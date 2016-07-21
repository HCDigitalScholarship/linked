#!/usr/bin/env python
import rdflib




graph = rdflib.Graph()

queryString = """
SELECT *
WHERE{
?s ?p ?o
}
"""


graph.parse('CEtravls.ttl',format='turtle')
result = graph.query(queryString)


print """
<html><head><title>results</title>
<style type="text/css"> * { font-family: arial,helvetica}</style>
</head><body>
"""


for row in result:
    for item in row:
        print "<p>" + item + "</p>"


print "</body></html>"
