#!/usr/bin/env python
import rdflib
import cgi

form = cgi.FieldStorage()
name = form.getvalue('name')
aut = form.getvalue('option1')
recip = form.getvalue('option2')

paneltop = """
<div class="panel-group"> <div class="panel panel-default"> <div class="panel-heading"> <h4 class="panel-title"> <a data-toggle="collapse" href="#collapse1">
"""
#name of panel goes inbetween
panelmid = """
</a> <span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span></h4> </div> <div id="collapse1" class="panel-collapse collapse"> <ul class="list-group">
"""

panelbottom = """
</ul></div> </div> </div>
"""





# ASSUMES PERFECT SPELLING ( NO REGEXP )
graph = rdflib.Graph()
graph.parse('CEletters.ttl',format='turtle')
graph.parse('CEpeople.ttl', format= 'turtle')

#if aut == "aut" and recip != "recip": # they wants the ones they wrote  
querywrote = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

SELECT  ?url ?title ?urlrecip ?recipient ?subj
WHERE {
?x p:labelname "REPLACEME" .
?m letter:Creator_ID ?x ;
      letter:Title ?title ;
      letter:Subject ?subj ;
      letter:Reference_URL ?url ;
      letter:Recipient_ID ?rt .
     ?rt p:labelname ?recipient .
     BIND(REPLACE(?recipient, " ", "+", "i") AS ?urlrecip)
}
"""

queryrecieved = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d:<localhost:3030/ds/date#>
prefix letter:<localhost:3030/ds/letter#>

SELECT  ?url ?title ?urlrecip ?recipient ?subj
WHERE {
?x p:labelname "REPLACEME" .
?m letter:Recipient_ID ?x ;
      letter:Title ?title ;
      letter:Subject ?subj ;
      letter:Reference_URL ?url ;
      letter:Creator_ID ?rt .
     ?rt p:labelname ?recipient .
BIND(REPLACE(?recipient, " ", "+", "i") AS ?urlrecip)     
}
"""


queryone = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d: <localhost:3030/ds/date#>

SELECT ?name 
WHERE {
  ?id p:labelname ?name .
  FILTER (REGEX(?name, "REPLACEME", "i"))

}
ORDER BY ?name
LIMIT 1
"""


querynames = """
prefix p: <localhost:3030/ds/person#> 
prefix t: <localhost:3030/ds/trip#> 
prefix d: <localhost:3030/ds/date#>

SELECT ?url ?name 
WHERE {
  ?id p:labelname ?name .
  FILTER (REGEX(?name, "REPLACEME", "i"))
  BIND(REPLACE(?name, " ", "+", "i") AS ?url)

}
ORDER BY ?name
OFFSET 1
"""

queryone = queryone.replace("REPLACEME",name)
oneresult = graph.query(queryone)

for row in oneresult: #finds the closest match name and assigns it
        thename = row[0]

querywrote = querywrote.replace("REPLACEME", thename)
queryrecieved = queryrecieved.replace("REPLACEME", thename)
#print queryString
#if 
resultwrote = graph.query(querywrote)
resultrecieved = graph.query(queryrecieved)


querynames = querynames.replace("REPLACEME",name)
namesresult = graph.query(querynames) #finds the similar names to offer as other links in side bar




print """
<html lang="en"><head> <meta charset="utf-8"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> <meta name="viewport" content="width=device-width, initial-scale=1"> <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags --> <meta name="description" content=""> <meta name="author" content=""> <link rel="icon" href="http://165.82.13.162/images/favicon.ico"> <title>Linked Data</title> <!-- Bootstrap core CSS --> <link href="http://165.82.13.162/css/bootstrap/css/bootstrap.min.css" rel="stylesheet"> <link href="http://165.82.13.162/css/style.css" rel="stylesheet"><!-- IE10 viewport hack for Surface/desktop Windows 8 bug --> <link href="http://165.82.100/css/bootstrap/css/assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet"> <!-- Custom styles for this template --> <link href="http://165.82.13.162/css/bootstrap/css/sticky-footer.css" rel="stylesheet"> <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script> <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script></head> <body> <!-- Begin page content --> <div class="container"> <div class="page-header"> <h1><a href='http://165.82.13.162/LinkedData.html'>Linked Data</a></h1> </div>
"""




paneltop2 = paneltop.replace("collapse1","collapse2")
panelmid2 = panelmid.replace("collapse1","collapse2")


x = len(namesresult)
print("<div class='sidebar' style='float:left;'><b><p>" + str(x) + " Similar results for " + str(name)+"</p></b>")
for row in namesresult:
        print("<a href=http://165.82.13.162/cgi-bin/CEperson.cgi?name=%s> <p>  %s</p> </a> " % row)
print"</div>"
#print("<h1> test" + str(namesresult[0]) + "</h1>")

print("<div class='container info'>")



print "<p class='lead'><b>Letters: " + str(thename) + " </b></p>" 
#print("<h1>" + str(aut) + "</h1>")
#print("<h1>" + str(recip) + "</h1>")





if str(recip) == "recip" and str(aut) == "aut":
	#do the thing both
        print(paneltop + "Letters Written" + panelmid )
        for row in resultwrote:
  	     	print("<li class='list-group-item'> <p style='margin:0 0 0px;'> <a href='%s'> %s  </a> to <a href=http://165.82.13.162/cgi-bin/CEperson.cgi?name=%s> %s</a> </p><p style='font-size:smaller;margin:0 0 0px;'>Subject: %s </p> </li> " % row)
        print panelbottom

        print(paneltop2 + "Letters Recieved" + panelmid2 )
        for row in resultrecieved:                print("<li class='list-group-item'> <p style='margin:0 0 0px;'> <a href='%s'> %s  </a> by <a href=http://165.82.13.162/cgi-bin/CEperson.cgi?name=%s> %s </a> </p><p style='font-size:smaller;margin:0 0 0px;'>Subject: %s </p> </li> " % row)
        print panelbottom


elif str(aut) == "aut": # they wants the ones they wrote 


        print(paneltop + "Letters Written" + panelmid )
        for row in resultwrote:
                print("<li class='list-group-item'> <p style='margin:0 0 0px;'> <a href='%s'> %s  </a> to <a href=http://165.82.13.162/cgi-bin/CEperson.cgi?name=%s> %s </a> </p><p style='font-size:smaller;margin:0 0 0px;'>Subject: %s</p> </li> " % row)
        print panelbottom


elif str(recip) == "recip":
        #do the thing
        print(paneltop2 + "Letters Recieved" + panelmid2 )
        for row in resultrecieved:                
		print("<li class='list-group-item'> <p style='margin:0 0 0px;'> <a href='%s'> %s  </a> by <a href=http://165.82.13.162/cgi-bin/CEperson.cgi?name=%s> %s</a> </p><p style='font-size:smaller;margin:0 0 0px;'>Subject: %s </p> </li> " % row)
        print panelbottom


else:
	print "<p class='lead' > an error has occured </p>"


print "</div>"
print """
</div> <footer class="footer"> <div class="container"> <p class="text-muted">Haverford College</p> </div> </footer> </body></html>
"""






