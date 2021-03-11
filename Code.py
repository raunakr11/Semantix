import osmnx as ox 
ox.config(use_cache=True, log_console=True) 

import networkx as nx
import plotly.graph_objects as go
import numpy as np

city = ox.geocode_to_gdf('Bengaluru, India')
ax = ox.project_gdf(city).plot(fc='teal', ec='none')
_ = ax.axis('off')

north, east, south, west = 13.1512, 77.7881, 12.8512, 75.4505  
# Downloading the map as a graph object 
G = ox.graph_from_bbox(north, south, east, west, network_type = 'drive')  
# Plotting the map graph 
ox.plot_graph(G,bgcolor='white',node_color='teal',edge_color='pink')

# define origin and desination locations 
origin_point = (13.095893, 77.571627) #Purva Venezia, Yelahanka
destination_point = (13.051042, 77.593614) #Columbia Asia Hospital, Hebbal
# get the nearest nodes to the locations 
origin_node = ox.get_nearest_node(G, origin_point) 
destination_node = ox.get_nearest_node(G, destination_point)

# Finding the optimal path 
route = nx.shortest_path(G, origin_node, destination_node, weight = 'length')

#getting coordinates of the nodes
#we will store the longitudes and latitudes in following list 
long = [] 
lat = []  
for i in route:
     point = G.nodes[i]
     long.append(point['x'])
     lat.append(point['y']) 
     
def plot_path(lat, long, origin_point, destination_point):
    
    """
    Given a list of latitudes and longitudes, origin 
    and destination point, plots a path on a map
    
    Parameters
    ----------
    lat, long: list of latitudes and longitudes
    origin_point, destination_point: co-ordinates of origin
    and destination
    Returns
    -------
    Nothing. Only shows the map.
    """
    # adding the lines joining the nodes
    fig = go.Figure(go.Scattermapbox(
        name = "Path",
        mode = "lines",
        lon = long,
        lat = lat,
        marker = {'size': 10},
        line = dict(width = 4.5, color = 'blue')))
    # adding source marker
    fig.add_trace(go.Scattermapbox(
        name = "Source",
        mode = "markers",
        lon = [origin_point[1]],
        lat = [origin_point[0]],
        marker = {'size': 12, 'color':"red"}))
     
    # adding destination marker
    fig.add_trace(go.Scattermapbox(
        name = "Destination",
        mode = "markers",
        lon = [destination_point[1]],
        lat = [destination_point[0]],
        marker = {'size': 12, 'color':'green'}))
    
    # getting center for plots:
    lat_center = np.mean(lat)
    long_center = np.mean(long)
    # defining the layout using mapbox_style
    fig.update_layout(mapbox_style="stamen-terrain",
        mapbox_center_lat = 30, mapbox_center_lon=-80)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      mapbox = {
                          'center': {'lat': lat_center, 
                          'lon': long_center},
                          'zoom': 13})
    fig.show()
    
#comparing long and lat
def findpoint(ll,lon):
  for i in range(len(lat)):
    if lat[i]==ll:
      for j in range(len(long)):
        if long[j]==lon:
          sendsms()
          
#          
def sendsms():
  from twilio.rest import Client 
  
  account_sid = 'ACbb2a71dce2f1a735db0efbd425d6f3f8' 
  auth_token = '321842cb6e36f9b9343a1d0b2a238eb7' 
  client = Client(account_sid, auth_token) 
  
  message = client.messages.create( 
                                from_='whatsapp:+14155238886',  
                                body='ALERT!! You are on the path of an upcoming ambulance! Please make way to avoid traffic jams!',      
                                to='whatsapp:+918792880230' 
                            ) 
  
  print(message.sid)

#collecting live location
import geocoder
g = geocoder.ip('me')
ll=g.latlng[0]
lon=g.latlng[1]
print(ll,lon)
findpoint(ll,lon)

#plotting the graph
plot_path(lat, long, origin_point, destination_point)
