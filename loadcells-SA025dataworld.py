#https://download.data.world/s/xkq7gtcspz3r763x3ulhgsdehhr3hr


import csv
import requests

layer = QgsVectorLayer('Polygon?crs=epsg:4326?field=id:string','SouthAmerica025',"memory")
pr = layer.dataProvider()
layer.startEditing()
pr.addAttributes([QgsField("id", QVariant.String )])
layer.updateFields()
features = []


# carrega os dados disponiveis em data.world

url = 'https://query.data.world/s/lwmmzbkcbqeoykta4k3d3qhxcq7cmw'

response = requests.get(url)
if response.status_code != 200:
    print('Failed to get data:', response.status_code)
else:
    wrapper = csv.reader(response.text.strip().split('\n'))
    values = {}
    for record in wrapper:
        if (record[0] != 'cell'):
                fet = QgsFeature()
                fet.setGeometry( QgsGeometry.fromWkt ( record[1])  )
                fet.setAttributes([  record[0]  ])
                layer.addFeatures([fet])
                layer.updateExtents()

   
layer.commitChanges()
QgsProject.instance().addMapLayer(layer)

