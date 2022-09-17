#code for mapping GPX files on folium
# Import libraries
import pandas as pd
import folium
import gpxpy
import gpxpy.gpx

#open GPX file
GPX_file='file.gpx'
GPX = gpxpy.parse(open(GPX_file))
try:
           tracks = GPX.tracks[0]
           line=tracks.segments[0]
except Exception as e:
           print("Please verify that there is at least one track or that the file is not corrupted")

def extract_points(GPX_obj_points):
    return GPX_obj_points.latitude,GPX_obj_points.longitude
def extract_all(GPX_obj_points):
    return GPX_obj_points.time,GPX_obj_points.longitude,GPX_obj_points.latitude,GPX_obj_points.elevation

points=list(map(extract_points,line.points))
df=pd.DataFrame(list(map(extract_all,line.points)),columns=['TIME','LON', 'LAT', 'ELEV'])

mmap = folium.Map( location=[ df.LAT.mean(), df.LON.mean()], zoom_start=13)
folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                 attr='Mapbox',name="satellite").add_to(mmap)
folium.LayerControl().add_to(mmap)
folium.PolyLine(points, color='red', weight=6.5, opacity=.5).add_to(mmap)
mmap.save("gpx_out.html")
