

from SPARQLWrapper import SPARQLWrapper, JSON, N3

#sparql = SPARQLWrapper("http://localhost:3030/dbcelsnovo/sparql")
sparql = SPARQLWrapper("http://dbcells.org:3030/cells/sparql")
sparql.setQuery("""
PREFIX db: <http://dbpedia.org/>
PREFIX dbr: <http://dbpedia.org/resource/>
prefix dbo: <http://dbpedia.org/ontology/> 
prefix geo: <http://www.opengis.net/ont/geosparql#>
prefix dbco: <http://purl.org/ontology/dbcells/cells#>
SELECT ?cell ?pol ?res
WHERE {
  ?cell <http://www.opengis.net/ont/geosparql#asWKT> ?pol.
  ?cell geo:sfWithin dbr:South_America.
  ?cell dbco:resolution 0.25.
}

""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# create layer
layer = QgsVectorLayer('Polygon?crs=epsg:4326?field=id:string','Grid025Graus',"memory")
pr = layer.dataProvider()
layer.startEditing()
pr.addAttributes([QgsField("id", QVariant.String )])

layer.updateFields()
features = []
for r in results["results"]["bindings"]:
    fet = QgsFeature()
    fet.setGeometry( QgsGeometry.fromWkt ( r["pol"]["value"])  )
    fet.setAttributes([  r["cell"]["value"]  ])
    layer.addFeatures([fet])
    layer.updateExtents()
    
   
layer.commitChanges()
QgsProject.instance().addMapLayer(layer)
