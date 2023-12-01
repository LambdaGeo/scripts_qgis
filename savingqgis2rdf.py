
from rdflib.namespace import RDF, FOAF
from rdflib import URIRef, BNode, Literal
from rdflib import Graph
from rdflib import Namespace

from rdflib.plugins.stores import sparqlstore

query_endpoint = 'http://localhost:3030/dbcells_1/query'
update_endpoint = 'http://localhost:3030/dbcells_1/update'
store = sparqlstore.SPARQLUpdateStore()
store.open((query_endpoint, update_endpoint))

#g = Graph()
g = Graph(identifier = URIRef('http://localhost:3030/dbcells_1/sparql'))

geo = Namespace("http://www.opengis.net/ont/geosparql#")
g.bind("geo", geo)

url = "http://dbcells.org/one/"

layer = iface.activeLayer()
for i in range (100):
    f = layer.getFeature(i)
    geom = f.geometry()
    cell = URIRef(url+str(i))
    g.add( (cell, geo.asWKT,  Literal(geom.asWkt() )  ) )

output = g.serialize(format='xml')
print (output)

file = open("/home/sergio/saida.xml","w") 
file.write(output.decode())
file.close()

#g.parse(data=r, format='turtle')
store.add_graph(g)

