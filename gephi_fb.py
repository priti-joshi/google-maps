import facebook
import json
import re
import networkx
import networkx.readwrite.gexf as gf
import urllib,urllib2
from xml.etree.cElementTree import tostring
####################################################
# This program uses FB Python API along with Gephi
# to plot friends cluster. 
####################################################

acc_token='xx'
me = 'yy'
graph=facebook.GraphAPI(acc_token)
 
frnd_list= []
frnd_json = graph.get_connections(me,"friends")
if "data" in frnd_json:
      for frnd in frnd_json["data"]:
        frnd_list.append(frnd["id"])
app_user = [me]
for i  in frnd_list:
  query = 'SELECT uid from user WHERE is_app_user=1 and uid=' + str(i)
  try:
     user = graph_me.fql(query) 
     if user[0]["uid"] != None :
       app_user.append(user[0]["uid"])  
  except:
     pass

ntwk_grph = networkx.Graph()

for i in app_user:
  i = re.sub('[^0-9]','',str(i))
  try:
    app_frnd_json = graph.get_connections(i,"friends")
    if "data" in app_frnd_json:
       parent = graph.get_object(i)
#       print parent["first_name"],parent["last_name"],parent["id"]
       ntwk_grph.add_node(parent["id"],label=parent["first_name"]+' '+parent["last_name"],name=parent["first_name"]+' '+parent["last_name"],parentCC=parent["id"])
       for frnd in app_frnd_json["data"]:
           ntwk_grph.add_node(frnd["id"],label=frnd["name"],name=frnd["name"],parentCC=frnd["id"])
           ntwk_grph.add_edge(frnd["id"],parent["id"])
  except:
    pass
writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(ntwk_grph)
file = open("new_gephi.gdf","w")
file.write('nodedef> name VARCHAR, label VARCHAR, title VARCHAR\n')
x=tostring(writer.xml)
file.write(x)
file.close
