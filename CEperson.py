#!/usr/bin/env python
import rdflib
import cgi

form = cgi.FieldStorage()
name = form.getvalue('name')

top = """
<html lang="en"><head> <meta charset="utf-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1"> <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags --> <meta name="description" content=""> <meta name="author" content=""> <link rel="icon" href="http://165.82.13.100/images/favicon.ico"> <title>Linked Data</title> <!-- Bootstrap core CSS --> <link href="http://165.82.13.100/css/bootstrap/css/bootstrap.min.css" rel="stylesheet"> <!-- IE10 viewport hack for Surface/desktop Windows 8 bug --> <link href="http://165.82.13.100/css/bootstrap/css/assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet"> <!-- Custom styles for this template --> <link href="http://165.82.13.100/css/bootstrap/css/sticky-footer.css" rel="stylesheet"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script> <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script> </head> <body> <!-- Begin page content --> <div class="container"> <div class="page-header"> <h1>Linked Data</h1> </div>
"""

bottom = """
</div> <footer class="footer"> <div class="container"> <p class="text-muted">Haverford College</p> </div> </footer> </body></html>
"""


paneltop = """
<div class="panel-group"> <div class="panel panel-default"> <div class="panel-heading"> <h4 class="panel-title"> <a data-toggle="collapse" href="#collapse1">
"""
#name of panel goes inbetween
panelmid = """
</a> </h4> </div> <div id="collapse1" class="panel-collapse collapse"> <ul class="list-group">
"""

panelbottom = """
</ul></div> </div> </div>
"""


# ASSUMES PERFECT SPELLING ( NO REGEXP )
graph = rdflib.Graph()
graph.parse('CEletters.ttl',format='turtle')
graph.parse('CEpeople.ttl', format= 'turtle')
graph.parse('CEchild.ttl', format= 'turtle')
graph.parse('CEtravls.ttl', format ='turtle')
a


queryString = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

SELECT  ?birth ?death ?par1 ?par2
WHERE {
?x p:labelname "REPLACEME" ;
   p:birth ?birth ;
   p:death ?death ;
   p:parent_1 ?p1 ;
   p:parent_2 ?p2 .
   ?p1 p:labelname ?par1 .
   ?p2 p:labelname ?par2 .
}
"""

querychild = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>
prefix fhkb: <http://www.example.com/genealogy.owl#> 

SELECT (GROUP_CONCAT(?c;separator=", ") as ?concat_label) 
WHERE { 
	?m p:labelname "REPLACEME" ;
	fhkb:hasChild ?this .
        ?this p:labelname ?c . } 
"""

querysib = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>
prefix fhkb: <http://www.example.com/genealogy.owl#> 

SELECT (GROUP_CONCAT(?c;separator=", ") as ?concat_label)
WHERE
{ 
?X p:labelname "REPLACEME" ;
     p:parent_1 ?p1 ;
     p:parent_2 ?p2 . 
     ?p1 fhkb:hasChild ?that .
     ?that p:Name ?c .
     ?p2 fhkb:hasChild ?this .
     ?this p:labelname ?c .
}
"""


queryspouse = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

SELECT ?partners
WHERE
{
?m p:labelname "REPLACEME" .
?x p:parent_1 ?m;
   p:parent_1 ?person_id;
   ?person_id p:labelame ?person ;
   p:parent_2 ?partner_id;
   ?partner_id p:labelname ?partners . 
?y p:parent_2 ?m;
    p:parent_2 ?person_id;
    ?person_id p:labelname ?person ;
    p:parent_1 ?partner_id;
    ?partner_id p:labelname ?partners . 
}
"""


querywrote = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>


SELECT  ?recipient ?url ?title
WHERE {
?x p:labelname "REPLACEME" .

?m letter:Creator_ID ?x ;
      letter:Title ?title ;
      letter:Reference_URL ?url ;
      letter:Recipient_ID ?rt .
     ?rt p:labelname ?recipient .
}
"""

queryrecieved = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>


SELECT  ?person ?url ?title
WHERE {
?x p:labelname "REPLACEME" .

?m letter:Recipient_ID ?x ;
      letter:Title ?title ;
      letter:Reference_URL ?url ;
      letter:Creator_ID ?rt .
     ?rt p:labelname ?person .
}
"""



queryString = queryString.replace("REPLACEME",name)
querychild = querychild.replace("REPLACEME",name)
querysib = querysib.replace("REPLACEME",name)
#queryspouse = queryspouse.replace("REPLACEME",name)
#querywrote = querywrote.replace("REPLACEME",name)
#queryrecieved = queryrecieved.replace("REPLACEME",name)
#print queryString



result = graph.query(queryString)
resultchild = graph.query(querychild)
resultsib = graph.query(querysib)
#resultwrote = graph.query(querywrote)
#resultrecieved = graph.query(queryrecieved)

#resultspouse = graph.query(queryspouse)

print top

print "<p>" + queryString + " </p>"
print "<p>" + querychild + " </p>"
print "<p>" + querysib + " </p>"
#print "<p>" + queryspouse + " </p>"


print "<p class='lead'><b> Info: "+ str(name)+ "</b></p>" 
for row in result:
    print("<p>  %s - %s </p><p><b>Parents:</b> %s, %s</p>  " % row)
    
for row in resultsib:
    print("<p><b>Siblings:</b> %s</p> " % row)

#for row in resultspouse:
#    print("<p>Spouse: %s</p> " % row)
print"<p><b>Spouse:</b> Not Coded yet </p>"

for row in resultchild:
    print("<p><b>Children:</b> %s</p> " % row) 


print(paneltop + "TEST" + panelmid + "<li class='list-group-item'>One</li> <li class='list-group-item'>Two</li> <li class='list-group-item'>Three</li>" + panelbottom)


#print(paneltop + "Letters Written" + panelmid )
#for row in resultwrote:
#	print("<li class='list-group-item'> <p>  %s <a href='%s'> %s  </a> </p> </li> " % row)
#print panelbottom 

#print(paneltop + "Letters Recieved" + panelmid )
#for row in resultrecieved:
#        print("<li class='list-group-item'> <p>  %s <a href='%s'> %s  </a> </p> </li> " % row)

#print panelbottom


print bottom
