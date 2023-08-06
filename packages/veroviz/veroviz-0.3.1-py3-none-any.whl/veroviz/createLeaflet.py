from veroviz._common import *
from veroviz._validation import valCreateLeaflet
from veroviz._validation import valAddLeafletCircle
from veroviz._validation import valAddLeafletMarker
from veroviz._validation import valAddLeafletPolygon
from veroviz._validation import valAddLeafletPolyline
from veroviz._validation import valAddLeafletText
from veroviz._internal import replaceBackslashToSlash

from veroviz._deconstructAssignments import deconstructAssignments

from veroviz.utilities import getMapBoundary

from veroviz._geometry import geoDistancePath2D
from veroviz._geometry import geoMileageInPath2D
from veroviz._geometry import geoDistance2D

foliumMaps = [
	'cartodb positron', 
	'cartodb dark_matter', 
	'openstreetmap', 
	'stamen terrain', 
	'stamen toner', 
	'stamen watercolor'
]

customMaps = {
	'arcgis aerial': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
	},

	'arcgis gray': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
	},

	'arcgis ocean': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri'
	},

	'arcgis roadmap': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Source: Esri'
	},

	'arcgis shaded relief': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Source: Esri'
	},

	'arcgis topo': {
		'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
		'attr': 'Tiles &copy; Esri &mdash; Source: Esri'
	},

	'open topo': {
		'tiles': 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
		'attr': 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
	},
}
	
def createLeaflet(mapObject=None, mapFilename=None, mapBackground=VRV_DEFAULT_LEAFLET_MAPTILES, mapBoundary=None, zoomStart=None, nodes=None, iconPrefix=None, iconType=None, iconColor=None, iconText=None, arcs=None, arcWeight=None, arcStyle=None, arcOpacity=None, arcColor=None, useArrows=None, boundingRegion=None, boundingWeight=VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT, boundingOpacity=VRV_DEFAULT_LEAFLETBOUNDINGOPACITY, boundingStyle=VRV_DEFAULT_LEAFLETBOUNDINGSTYLE, boundingColor=VRV_DEFAULT_LEAFLETBOUNDINGCOLOR):

	"""
	createLeaflet is used to generate Leaflet objects using folium. The function takes a boundingRegion polygon, `Nodes`, `Arcs`, and `Assignments` dataframes as inputs, and creates a folium/leaflet map showing boundings, nodes and/or arcs. 

	Parameters
	----------
	mapObject: Folium object, Optional, default as None
		If you already have a map (as a Folium object), you can provide that object and add content to that map.
	mapFilename: string, Optional, default as None
		This is the name of the map file that will be created (e.g., "../output/map.html" or "map.html").  The filename should have a `.html` extension.  If `mapFilename` is not provided, no map file will be generated.  The returned map object can be viewed within a Jupyter notebook.
	mapBackground: string, Optional, default as 'CartoDB positron'
		Sets the background tiles of the map.  See :ref:`Leaflet Style` for the list of options.
	mapBoundary: list of lists, Optional, default as None
		Allows customization of the zoom level.  If a map boundary is provided, the zoom level will correspond to the rectangle defined by the two map boundary points. This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  Must be in the form [[south lat, west lon], [north lat, east lon]].
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	nodes: :ref:`Nodes`, Conditional, `nodes`, `arcs`, and `boundingRegion` can not be None at the same time
		A Nodes dataframe describing the collection of nodes to be displayed on the Leaflet map.  See :ref:`Nodes` for documentation on this type of dataframe.
	iconPrefix: string, Optional, default as None
		Overrides the `leafletIconPrefix` column of an input :ref:`Nodes` dataframe.  If provided, all nodes will use this icon prefix.  Valid options are "glyphicon" or "fa". See :ref:`Leaflet Style` for details.
	iconType: string, Optional, default as None
		Overrides the `leafletIconType` column of an input :ref:`Nodes` dataframe.  If provided, all nodes will use this icon type.  The valid `iconType` options depend on the choice of `iconPrefix`.  See :ref:`Leaflet Style` for the collection of valid icon prefix/type combinations.
	iconColor: string, Optional, default as None
		Overrides the `leafletColor` column of an input :ref:`Nodes` dataframe.  If provided, all icons will use this color when displayed on this Leaflet map.  See :ref:`Leaflet Style` for the list of available color options.
	iconText: string, Optional, default as None
		Overrides the `leafletIconText` column of an input :ref:`Nodes` dataframe.  If provided, all node markers in this Leaflet map will include this text as a label (you will need to click on the marker in the map to see this label).  
	arcs: :ref:`Arcs` or :ref:`Assignments`, Conditional, `nodes`, `arcs` and `boundingRegion` can not be None at the same time
		An :ref:`Arcs` or :ref:`Assignments` dataframe describing vehicle routes.  Each row of this dataframe will be shown as a line on the Leaflet map.  See the documentation on :ref:`Arcs` and :ref:`Assignments` for more information.
	arcWeight: int, Optional, default as None
		Overrides the `leafletWeight` column of an input :ref:`Arcs` or :ref:`Assignments` dataframe.  If provided, all arcs will be displayed with this line thickness (in pixels).  
	arcStyle: string, Optional, default as None
		Overrides the `leafletStyle` column of an input :ref:`Arcs` or :ref:`Assignments` dataframe. If provided, all arcs will be displayed with this type.  Valid options are 'solid', 'dotted', or 'dashed'.  See :ref:`Leaflet Style` for more information.
	arcOpacity: float in [0, 1], Optional, default as None
		Overrides the `leafletOpacity` column of an input :ref:`Arcs` or :ref:`Assignments` dataframe.  If provided, each arc will be displayed with this opacity.  Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	arcColor: string, Optional, default as None
		Overrides the `leafletColor` column of an input :ref:`Arcs` or :ref:`Assignments` dataframe.  If provided, all arcs will be displayed with this color.  See :ref:`Leaflet Style` for a list of available colors.
	useArrows: boolean, Optional, default as None
		Indicates whether arrows should be shown on all arcs on the Leaflet map.
	boundingRegion: list of lists, Conditional, `nodes`, `arcs` and `boundingRegion` can not be None at the same time
		A sequence of lat/lon coordinates defining a boundary polygon. The format is [[lat, lon], [lat, lon], ..., [lat, lon]].
	boundingWeight: int, Optional, default as 3
		Specifies the weight (in pixels) of the line defining the `boundingRegion` (if provided) when displayed in Leaflet.
	boundingStyle: string, Optional, default as 'dashed'
		Specifies the line style of the `boundingRegion` (if provided).  Valid options are 'solid', 'dotted', 'dashed'.  See :ref:`Leaflet Style` for more information.
	boundingOpacity: float in [0, 1], Optional, default as 0.6
		Specifies the opacity of the `boundingRegion` (if provided) when displayed in Leaflet.  Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	boundingColor: string, Optional, default as 'brown'
		Specifies the line color of the `boundingRegion` (if provided) when displayed in Leaflet. See :ref:`Leaflet Style` for a list of available colors.

	Return
	------
	Folium object
		A new/updated map that displays the nodes, arcs, and/or bounding region.

	Examples
	--------
	First, import veroviz and check the latest version
	    >>> import veroviz as vrv
	    >>> vrv.checkVersion()

	Now, generate some example nodes inside a bounding region
	    >>> bounding = [
	    ...     [42.98355351219673, -78.90518188476564], 
	    ...     [43.04731443361136, -78.83857727050783], 
	    ...     [43.02221961002041, -78.7108612060547], 
	    ...     [42.92777124914475, -78.68957519531251], 
	    ...     [42.866402688514626, -78.75343322753908], 
	    ...     [42.874957707517865, -78.82415771484375], 
	    ...     [42.90111863978987, -78.86878967285158], 
	    ...     [42.92224052343343, -78.8921356201172]]

	    >>> exampleNodes = vrv.generateNodes(
	    ...     nodeType         = 'customer', 
	    ...     nodeDistrib      = 'normalBB', 
	    ...     nodeDistribArgs  = {
	    ...         'center'         : [42.90, -78.80], 
	    ...         'stdDev'         : 10000,
	    ...         'boundingRegion' : bounding
	    ...     },
	    ...     numNodes         = 3,
	    ...     leafletColor     = 'orange')

	The first example is using all default setting for generating a set of given nodes in Nodes dataframe.
	    >>> vrv.createLeaflet(nodes=exampleNodes)

	Define some arcs based on the nodes we just generated:
	    >>> exampleArcs = vrv.createArcsFromNodeSeq(
	    ...     nodes   = exampleNodes,
	    ...     nodeSeq = [1, 2, 3])
	    >>> exampleArcs

	Display the nodes, arcs, and bounding region simultaneously:
	    >>> vrv.createLeaflet(
	    ...     nodes          = exampleNodes,
	    ...     arcs           = exampleArcs,
	    ...     boundingRegion = bounding)

	The createLeaflet function provides options to override styles that were defined in the input nodes and/or arcs dataframes.  Note:  These overrides will not change the contents in the dataframes.
		>>> nodesAndArcsMap = vrv.createLeaflet(
		...     nodes      = exampleNodes,
		...     iconPrefix = 'fa',
		...     iconType   = 'car',
		...     iconColor  = 'blue',
		...     arcs       = exampleArcs,
		...     arcStyle   = 'dotted')
		>>> nodesAndArcsMap

	If you already have a folium map object, you can add more into it.
	Here, we add a bounding region to the `nodesAndArcsMap` object defined above.
		>>> nodesAndArcsMap = vrv.createLeaflet(
		...     mapObject      = nodesAndArcsMap,
		...     boundingRegion = bounding)
		>>> nodesAndArcsMap
		
	A new collection of nodes is defined here:
		>>> newNodes = vrv.generateNodes(
		...     nodeType        = 'customer', 
		...     nodeDistrib     = 'uniformBB', 
		...     nodeDistribArgs = {
		...         'boundingRegion' : bounding
		...     },
		...     numNodes        = 4,
		...     leafletColor    = 'red')
		>>> newNodes
		
	We will add these nodes to our existing map,
	but we're overriding these new nodes with a green color:	
	Notice that the addition of new entities will not change the style of previous entities that were already added into the map.
		>>> newMapWithArcsAndMoreNodes = vrv.createLeaflet(
		...     mapObject = nodesAndArcsMap,
		...     nodes     = newNodes,
		...     iconColor = 'green')
		>>> newMapWithArcsAndMoreNodes

	The following example includes all of the function arguments.
		>>> vrv.createLeaflet(
		...     mapObject       = None, 
		...     mapFilename     = 'example.html', 
		...     mapBackground   = 'CartoDB positron', 
		...     mapBoundary     = None, 
		...     zoomStart       = 10, 
		...     nodes           = exampleNodes, 
		...     iconPrefix      = 'fa', 
		...     iconType        = 'flag', 
		...     iconColor       = 'red', 
		...     iconText        = 'Here are some nodes', 
		...     arcs            = exampleArcs, 
		...     arcWeight       = 5, 
		...     arcStyle        = 'dashed', 
		...     arcOpacity      = 1, 
		...     arcColor        = 'green', 
		...     useArrows       = True, 
		...     boundingRegion  = bounding, 
		...     boundingWeight  = 1, 
		...     boundingOpacity = 0.8, 
		...     boundingStyle   = 'dotted', 
		...     boundingColor   = 'black')
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valCreateLeaflet(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, nodes, iconPrefix, iconType, iconColor, iconText, arcs, arcWeight, arcStyle, arcOpacity, arcColor, useArrows, boundingRegion, boundingWeight, boundingOpacity, boundingStyle, boundingColor)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	# Replace backslash
	mapFilename = replaceBackslashToSlash(mapFilename)

	# Adjust the scope of the map to proper bounds
	[[minLat, maxLon], [maxLat, minLon]] = getMapBoundary(nodes, arcs, boundingRegion)

	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	# If no mapObject exists, set a new mapObject
	if (mapObject == None):
		midLat = (maxLat + minLat) / 2.0
		midLon = (maxLon + minLon) / 2.0
		if (mapBackground in foliumMaps):
			mapObject = folium.Map(
				location=[midLat, midLon], 
				zoom_start=zoomStart if (zoomStart != None) else 10, 
				tiles=mapBackground)
		elif (mapBackground in customMaps):
			mapObject = folium.Map(
				location=[midLat, midLon], 
				zoom_start=zoomStart if (zoomStart != None) else 10, 
				tiles=customMaps[mapBackground]['tiles'],
				attr=customMaps[mapBackground]['attr'])

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)
		elif (mapBoundary is None):
			mapObject.fit_bounds(getMapBoundary(nodes, arcs, boundingRegion))
	
	# Plot node markers
	if (type(nodes) is pd.core.frame.DataFrame):
		mapObject = _createLeafletNodes(mapObject, nodes, iconPrefix, iconType, iconColor, iconText)
	
	# Plot arcs
	if (type(arcs) is pd.core.frame.DataFrame):
		mapObject = _createLeafletArcs(mapObject, arcs, arcWeight, arcOpacity, arcStyle, arcColor, useArrows, VRV_DEFAULT_LEAFLET_ARROWSIZE, 4)
	
	# Plot bounding
	if (type(boundingRegion) is list):
		mapObject = _createLeafletBoundingRegion(mapObject, boundingRegion, boundingWeight, boundingOpacity, boundingStyle, boundingColor)

	if (mapFilename is not None):		
		mapDirectory = ""
		strList = mapFilename.split("/")
		for i in range(len(strList) - 1):
			mapDirectory += strList[i] + "/"
		if (mapDirectory != ""):
			if (not os.path.exists(mapDirectory)):
				os.makedirs(mapDirectory, exist_ok=True)

		mapObject.save(mapFilename)
		if (VRV_SETTING_SHOWOUTPUTMESSAGE):
			print("Message: Map page written to %s." % (mapFilename))
	
	return mapObject

def _createLeafletNodes(mapObject=None, nodes=None, iconPrefix=None, iconType=None, iconColor=None, iconText=None):
	"""
	A sub-function to create leaflet nodes

	Parameters
	----------
	mapObject: Folium object, Required
		Add content to a folium map.
	nodes: :ref:`Nodes`, Required
		The Nodes dataframe to be generated in Leaflet
	iconPrefix: string, Optional
		The collection of Leaflet icons.  Options are "glyphicon" or "fa". See :ref:`Leaflet Style`
	iconType: string, Optional
		The specific icon to be used for all generated nodes.  The list of available options depends on the choice of the iconType. See :ref:`Leaflet Style`
	iconColor: string, Optional
		The icon color of the generated nodes when displayed in Leaflet.  One of a collection of pre-specified colors. See :ref:`Leaflet Style`
	iconText: string, Optional
		Text that will be displayed within the node on a Leaflet map. See :ref:`Leaflet Style`

	return
	------
	Folium object
		A new/updated map that contains the nodes

	"""

	# Note: In nodes dataframe, we already checked 'leaflet-' columns, and those columns have default values, for sake of consistency in here I delete the 'fail safes'
	for i in range(0, len(nodes)):
		# If not overrided, use the info in nodes dataframe
		if (iconColor == None):
			newColor = nodes.iloc[i]['leafletColor']
		else:
			newColor = iconColor
			
		if ((iconPrefix == None) or (iconType == None)):
			newPrefix = nodes.iloc[i]['leafletIconPrefix']
			newType = nodes.iloc[i]['leafletIconType']
		else:
			newPrefix = iconPrefix
			newType = iconType

		if (iconText == None):
			newText = nodes.iloc[i]['leafletIconText']
		else:
			newText = iconText

		if (newColor != None):
			newColor = newColor.lower()
		if (newPrefix != None):
			newPrefix = newPrefix.lower()
		if (newType != None):
			newType = newType.lower()
					
		# Folium draw nodes
		folium.Marker(
			[nodes.iloc[i]['lat'], nodes.iloc[i]['lon']], 
			icon=folium.Icon(
				color=newColor, 
				prefix=newPrefix, 
				icon=newType), 
			popup=str(newText)
		).add_to(mapObject)

	return mapObject

def _createLeafletArcs(mapObject=None, arcs=None, arcWeight=None, arcOpacity=None, arcStyle=None, arcColor=None, useArrows=None, arrowSize=6, arrowsPerArc=4):
	"""
	A sub-function to create leaflet arcs
	
	Parameters
	----------
	mapObject: Folium object, Required
		Add content to a folium map.
	arcs: ref:`Arcs`/:ref:`Assignments`, Required
		The Arc dataframe to be generated in Leaflet
	arcWeight: string, Optional
		The weight of generated route when displayed in Leaflet. See :ref:`Leaflet Style`
	arcStyle: string, Optional, default as 'solid'
		The line style of geneareted route, options are 'solid', 'dotted', 'dashed'. See :ref:`Leaflet Style`
	arcOpacity: string, Optional
		The opacity of generated route when displayed in Leaflet, range from 0 (invisible) to 1. See :ref:`Leaflet Style`
	arcColor: string, Optional
		The color of generated route when displayed in Leaflet.  One of a collection of pre-specified colors. See :ref:`Leaflet Style`
	useArrows: boolean, Optional, default as None
		Whether or not to add arrows to leaflet map.
	arrowSize: int Optional, default as 
		Size of arrows

	return
	------
	Folium object
		A new/updated map that contains the arcs
	"""

	# In here "arcs" can be Arcs/Assignments, each path should have its own odID. Use lstPath as a list of Arcs/Assignments dataframe, each item in it is a path, with the same styles
	lstPath = []

	# For Arcs dataframe, each row is a path, i.e. each row should have different odID
	if (not {'startTimeSec'}.issubset(arcs.columns)):
		for i in range(0, len(arcs)):
			newPath = pd.DataFrame(columns=['odID', 'startLat', 'startLon', 'endLat', 'endLon', 'leafletColor', 'leafletWeight', 'leafletStyle', 'leafletOpacity', 'useArrows'])
			newPath = newPath.append({
				'odID' : arcs.iloc[i]['odID'],
				'startLat' : arcs.iloc[i]['startLat'],
				'startLon' : arcs.iloc[i]['startLon'],
				'endLat' : arcs.iloc[i]['endLat'],
				'endLon' : arcs.iloc[i]['endLon'],
				'leafletColor' : arcs.iloc[i]['leafletColor'],
				'leafletWeight' : arcs.iloc[i]['leafletWeight'],
				'leafletStyle' : arcs.iloc[i]['leafletStyle'],
				'leafletOpacity' : arcs.iloc[i]['leafletOpacity'],
				'useArrows' : arcs.iloc[i]['useArrows']
				}, ignore_index=True)
			lstPath.append(newPath.copy())

	# For Assignments dataframe, use deconstructAssignments to generate a list of assignments dataframe
	if ({'objectID'}.issubset(arcs.columns) and {'startTimeSec'}.issubset(arcs.columns)):
		lstPath = deconstructAssignments(assignments=arcs)

	# For each path, generate the arcs and arrows accordingly
	for i in range(len(lstPath)):
		lstPath[i] = lstPath[i].reset_index(drop=True)
		arcPath = []
		arcPath.append([lstPath[i]['startLat'][0], lstPath[i]['startLon'][0]])
		for j in range(len(lstPath[i])):
			arcPath.append([lstPath[i]['endLat'][j], lstPath[i]['endLon'][j]])

		# If not overrided, use the info in arcs dataframe
		if (arcColor == None):
			newColor = lstPath[i]['leafletColor'][0]
		else:
			newColor = arcColor
		if (arcWeight == None):
			newWeight = lstPath[i]['leafletWeight'][0]
		else:
			newWeight = arcWeight
		if (arcOpacity == None):
			newOpacity = lstPath[i]['leafletOpacity'][0]
		else:
			newOpacity = arcOpacity
		if (arcStyle == None):
			newStyle = lstPath[i]['leafletStyle'][0]
		else:
			newStyle = arcStyle.lower()

		# Interpret arc style
		if (newStyle == 'dashed'):
			dashArray = '30 10'
		elif (newStyle == 'dotted'):
			dashArray = '1 6'
		else:
			dashArray = None
		
		try:
			newColor = newColor.lower()
		except:
			pass
			
		# Folium draw arcs	
		folium.PolyLine(
			arcPath, 
			color = newColor, 
			weight = newWeight, 
			opacity = newOpacity, 
			dash_array = dashArray
		).add_to(mapObject)	

		# Check if we add arrows
		arrowFlag = False
		if (useArrows == True):
			arrowFlag = True
		elif (useArrows == None):
			if ({'useArrows'}.issubset(lstPath[i].columns)):
				if (lstPath[i].iloc[0]['useArrows'] == True):
					arrowFlag = True
			else:
				arrowFlag = False
		elif (useArrows == False):
			arrowFlag = False			
		if (arrowFlag):
			mapObject = _createLeafletArrowsPath(mapObject, arcPath, newColor, arrowSize, mode='equal_division_spacing', arrowsPerArc=arrowsPerArc, arrowDistanceInMeters=1000)

	return mapObject

def _createLeafletBoundingRegion(mapObject=None, boundingRegion=None, boundingWeight=VRV_DEFAULT_LEAFLETBOUNDINGWEIGHT, boundingOpacity=VRV_DEFAULT_LEAFLETBOUNDINGOPACITY, boundingStyle=VRV_DEFAULT_LEAFLETBOUNDINGSTYLE, boundingColor=VRV_DEFAULT_LEAFLETBOUNDINGCOLOR):
	"""
	A sub-function to create leaflet bounding region

	Parameters
	----------
	mapObject: Folium object, Required
		Add content to a folium map.
	boundingRegion: list of lists, Required
		A sequence of lat/lon coordinates defining the boundary of the objects.
	boundingWeight: string, Optional
		The weight of bounding region when displayed in Leaflet. See :ref:`Leaflet Style`
	boundingStyle: string, Optional, default as 'solid'
		The line style of bounding region, options are 'solid', 'dotted', 'dashed'. See :ref:`Leaflet Style`
	boundingOpacity: string, Optional
		The opacity of bounding region when displayed in Leaflet, range from 0 (invisible) to 1. See :ref:`Leaflet Style`
	boundingColor: string, Optional
		The color of bounding region when displayed in Leaflet.  One of a collection of pre-specified colors. See :ref:`Leaflet Style`

	return
	------
	Folium object
		A new/updated map that contains the boundings

	"""

	# Make the bounding region a closed circle
	boundings = boundingRegion[:]
	if (boundings[0] != boundings[len(boundings) - 1]):
		boundings.append(boundings[0])

	# Interpret bounding style
	try:
		boundingStyle = boundingStyle.lower()
	except:
		pass
		
	if (boundingStyle == 'dashed'):
		dashArray = '30 10'
	elif (boundingStyle == 'dotted'):
		dashArray = '1 6'
	else:
		dashArray = None

	try:
		boundingColor = boundingColor.lower()
	except:
		pass
		
	# Draw bounding region in folium (for now is not filled)
	folium.PolyLine(
		boundings, 
		color = boundingColor,
		weight = boundingWeight,
		opacity = boundingOpacity,
		dash_array = dashArray
	).add_to(mapObject)

	return mapObject

def _createLeafletArrowsPath(mapObject=None, path=None, color=None, size=7, mode='equal_division_spacing', arrowsPerArc=1, arrowDistanceInMeters=None):
	"""
	A sub-function to generate arrows for one path (i.e. with the same odID)

	Parameters
	----------
	mapObject: Folium object, Required
		Add content to a folium map.
	lats: list, Required
		A list of latitudes
	lons: list, Required
		A list of longitudes
	color: string, Required
		The color for arrow, we are not providing any default value here because it has to be consistent with the color of arcs/assignments
	size: int, Optional, default as 7
		The size of the arrow
	mode: string, Optional, default as 'equal_division_spacing'
		For 'equal_division_spacing', divide the entire path equally in to several parts and add arrows accordingly. For 'equal_distance_spacing', add arrow for every given distance.
	arrowsPerArc: int, Optional, default as 1
		If we are using 'equal_division_spacing', it defines the number of arrows in the path, otherwise it will be ignored
	arrowDistanceInMeters: float, Optional
		If we are using 'equal_distance_spacing', it defines the distance between arrows

	Return
	------
	Folium object
		A map that contains arrows above the arcs

	"""

	# Calculate totalDistance
	totalDistance = geoDistancePath2D(path)

	# Use different modes to decide how many arrows to be generated and where are them
	lstMilages = []
	if (mode == 'equal_division_spacing'):
		for i in range(1, arrowsPerArc + 1):
			lstMilages.append(totalDistance * (i / (arrowsPerArc + 1)))
	elif (mode == 'equal_distance_spacing'):
		accuDistance = 0
		while accuDistance < totalDistance:
			accuDistance += arrowDistanceInMeters
			lstMilages.append(accuDistance)
		remainingDistance = totalDistance - accuDistance
		for i in range(len(lstMilages)):
			lstMilages[i] = lstMilages[i] + remainingDistance/2
	else:
		return

	try:
		color = color.lower()
	except:
		pass
		
	# Draw arrows
	for i in range(len(lstMilages)):
		[loc, inPathFlag, bearingInDegree] = geoMileageInPath2D(path, lstMilages[i])
		folium.RegularPolygonMarker(
			location = loc,
			number_of_sides = 3,
			rotation = bearingInDegree-90,
			radius = size,
			color = color,
			fill_color = color,
			fill_opacity = 1.0
		).add_to(mapObject)
	
	return mapObject

def addLeafletCircle(mapObject=None, mapFilename=None, mapBackground=VRV_DEFAULT_LEAFLET_MAPTILES, mapBoundary=None, zoomStart=None, center=None, radius=None, lineWeight=3, lineColor=None, lineOpacity=0.8, lineStyle='solid', fillColor=VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE, fillOpacity=0.3):

	"""
	Add a circle, with a radius specified in [meters], to a Leaflet map.
	
	Note
	----
	This function differs from addLeafletMarker, in which the circle's radius is specified in [pixels].
	
	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the circle will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default as None
		This is the name of the map file that will be created (e.g., "../output/map.html" or "map.html").  The filename should have a `.html` extension.  If `mapFilename` is not provided, no map file will be generated.  The returned map object can be viewed within a Jupyter notebook.
	mapBackground: string, Optional, default as 'CartoDB positron'
		Sets the background tiles of the map.  See :ref:`Leaflet Style` for the list of options.
	mapBoundary: list of lists, Optional, default as None
		Allows customization of the zoom level.  If a map boundary is provided, the zoom level will correspond to the rectangle defined by the two map boundary points. This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  Must be in the form [[south lat, west lon], [north lat, east lon]].
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	center: list, Required, default None
		Specifies the center point of the circle.  Must be a list of the form `[lat, lon]` or `[lat, lon, alt]`.  If provided, the altitude component will be ignored (as all locations on Leaflet maps are assumed to be at ground level).
	radius: float, Required, default None
		The radius of the circle, in units of [meters]. 
	lineWeight: int, Optional, default 3
		The width of the circle's outline, in units of [pixels].  This value is ignored if `lineColor = None`. 
	lineColor: string, Optional, default None
		The color of the circle's outline.  `lineColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). No line will be drawn if `lineColor = None`. 
	lineOpacity: float in [0, 1], Optional, default 0.8
		Specifies the opacity of the circle's outline.  Valid values are in the range from 0 (invisible) to 1 (no transparency).
	lineStyle: string, Optional, default 'solid'
		The style of the circle's outline.  See :ref:`Leaflet Style` for a list of valid options.  
	fillColor: string, Optional, default 'red'
		The color of the interior of the circle. `fillColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). The circle will not be filled if `fillColor = None`.  
	fillOpacity: float in [0, 1], Optional, default 0.3
		Specifies the opacity of the circle's interior.  Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	
	Return
	------
	Folium object
		A Folium map object containing a circle (and pre-existing items previously specified in mapObject).
		
	Example
	-------
		>>> # Draw a circle of radius 10 meters, centered on the Univ. at Buffalo campus.
		>>> # Save this as "a_circle.html".
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletCircle(
		...     zoomStart=18,
		...     center=[43.00154, -78.7871],
		...     radius=100,
		...     mapFilename="a_circle.html")
		>>> myMap

		>>> # Draw a circle of radius 2000 meters, centered on the Univ. at Buffalo campus.
		>>> # This example includes all of the available function arguments.
		>>> import veroviz as vrv
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletCircle(
		...     mapObject = None,
		...     mapFilename = None,
		...     mapBackground = 'OpenStreetMap',
		...     mapBoundary = None,
		...     zoomStart = 13,
		...     center = [43.00154, -78.7871],
		...     radius = 2000,
		...     lineWeight = 6,
		...     lineColor = '#ff66ff',
		...     lineOpacity = 0.7,
		...     lineStyle = 'dotted',
		...     fillColor = 'green',
		...     fillOpacity = 0.4)
		>>> myMap
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletCircle(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, center, radius, lineWeight, lineColor, lineOpacity, lineStyle, fillColor, fillOpacity)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)
	
	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	center = [center[0], center[1]]

	# If no mapObject exists, set a new mapObject
	if (mapObject == None):
		if (mapBackground in foliumMaps):
			mapObject = folium.Map(
				location=center, 
				zoom_start=zoomStart if (zoomStart != None) else 10, 
				tiles=mapBackground)
		elif (mapBackground in customMaps):
			mapObject = folium.Map(
				location=center, 
				zoom_start=zoomStart if (zoomStart != None) else 10, 
				tiles=customMaps[mapBackground]['tiles'],
				attr=customMaps[mapBackground]['attr'])

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)

	try:
		lineStyle = lineStyle.lower()
	except:
		pass
	
	# Interpret line style
	if (lineStyle == 'dashed'):
		dashArray = '30 10'
	elif (lineStyle == 'dotted'):
		dashArray = '1 6'
	else:
		dashArray = None

	try:
		lineColor = lineColor.lower()
	except:
		pass
		
	try:
		fillColor = fillColor.lower()
	except:
		pass
		
	folium.Circle(center, 
		radius = radius,  
		stroke = True, 
		weight = lineWeight, 
		color = lineColor, 
		opacity = lineOpacity, 
		dash_array = dashArray,
		fill_color = fillColor,
		fill_opacity = fillOpacity
		).add_to(mapObject)

	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (VRV_SETTING_SHOWOUTPUTMESSAGE):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject
	
def addLeafletMarker(mapObject=None, mapFilename=None, mapBackground=VRV_DEFAULT_LEAFLET_MAPTILES, mapBoundary=None, zoomStart=None, center=None, radius=5, lineWeight=3, lineColor=None, lineOpacity=0.8, lineStyle='solid', fillColor=VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE, fillOpacity=0.3):

	"""
	Add a circle-shaped marker, with a radius specified in [pixels], to a Leaflet map.
	
	Note
	----
	This function differs from addLeafletCircle, in which the circle's radius is specified in [meters].
	
	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the marker will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default None 
		If provided, the map will be saved to this file, which should have a `.html` extension.  `mapFilename` can contain a filepath.  If `mapFilename` is not provided, no file will be generated.  The returned mapObject can be viewed within a Jupyter notebook. 
	mapBackground: string, Optional, default 'CartoDB positron'
		The tiles of the map, default to be 'CartoDB positron', for options, see :ref:`Leaflet Style`, also see folium documentation (https://python-visualization.github.io/folium/modules.html) for more options
	mapBoundary: list [LIST OF LISTS?], Optional, default None
		If provided, the mapBoundary coordinates are used to determine a zoom level such that these coordinates are contained within view when the map is opened.  This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  `mapBoundary` must be in the form [[south lat, west lon], [north lat, east lon]].	
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	center: list, Required, default None
		Specifies the center point of the circle marker.  Must be a list of the form `[lat, lon]` or `[lat, lon, alt]`.  If provided, the altitude component will be ignored (as all locations on Leaflet maps are assumed to be at ground level).
	radius: float, Required, default None
		The radius of the circle marker, in units of [pixels]. 
	lineWeight: int, Optional, default 3
		The width of the circle marker's outline, in units of [pixels].  This value is ignored if `line = False`. 
	lineColor: string, Optional, default 'red'
		The color of the circle marker's outline.  `lineColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). The line color is ignored if `line = False`. 
	lineOpacity: float in [0, 1], Optional, default 0.8
		The opacity of the circle marker's outline, where 0 is invisible and 1 represents no transparency.  See :ref:`Leaflet Style`
	lineStyle: string, Optional, default 'solid'
		The style of the circle marker's outline.  See :ref:`Leaflet Style` for a list of valid options.  
	fillColor: string, Optional, default None
		The color of the interior of the circle marker. `fillColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). The fill color is ignored if `fill = False`.  
	fillOpacity: float in [0, 1], Optional, default 0.3
		The opacity of the circle marker's interior, where 0 is invisible and 1 represents no transparency.  See :ref:`Leaflet Style`
	
	Return
	------
	Folium object
		A Folium map object containing a circle marker (and pre-existing items previously specified in mapObject).
		
	Example
	-------
		>>> # Draw a circle of radius 10 pixels, centered on the Univ. at Buffalo campus.
		>>> # Save this as "a_marker.html".
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletMarker(
		...     center=[43.00154, -78.7871],
		...     radius=10,
		...     mapFilename="a_marker.html")
		>>> myMap

		>>> # Draw a circle of radius 30 pixels, centered on the Univ. at Buffalo campus.
		>>> # This example includes all of the available function arguments.
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletMarker(
		...     mapObject = None, 
		...     mapFilename = None, 
		...     mapBackground = 'CartoDB positron', 
		...     mapBoundary = None, 
		...     zoomStart = 11, 
		...     center = [43.00154, -78.7871],
		...     radius = 30, 
		...     lineWeight = 3, 
		...     lineColor = 'orange', 
		...     lineOpacity = 0.6, 
		...     lineStyle = 'dashed',
		...     fillColor = 'blue', 
		...     fillOpacity = 0.3)
		>>> myMap
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletMarker(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, center, radius, lineWeight, lineColor, lineOpacity, lineStyle, fillColor, fillOpacity)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	center = [center[0], center[1]]

	# If no mapObject exists, set a new mapObject
	if (mapObject == None):
		if (mapBackground in foliumMaps):
			mapObject = folium.Map(
				location=center, 
				zoom_start=zoomStart if (zoomStart != None) else 10, 
				tiles=mapBackground)
		elif (mapBackground in customMaps):
			mapObject = folium.Map(
				location=center, 
				zoom_start=zoomStart if (zoomStart != None) else 10, 
				tiles=customMaps[mapBackground]['tiles'],
				attr=customMaps[mapBackground]['attr'])

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)
		
	try:
		lineStyle = lineStyle.lower()
	except:
		pass

	# Interpret line style
	if (lineStyle == 'dashed'):
		dashArray = '30 10'
	elif (lineStyle == 'dotted'):
		dashArray = '1 6'
	else:
		dashArray = None

	try:
		lineColor = lineColor.lower()
	except:
		pass
		
	try:
		fillColor = fillColor.lower()
	except:
		pass

	folium.CircleMarker(center, 
		radius = radius,  
		stroke = True, 
		weight = lineWeight, 
		color = lineColor, 
		opacity = lineOpacity, 
		dash_array = dashArray,
		fill_color = fillColor,
		fill_opacity = fillOpacity
		).add_to(mapObject)

	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (VRV_SETTING_SHOWOUTPUTMESSAGE):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject	

def addLeafletPolygon(mapObject=None, mapFilename=None, mapBackground=VRV_DEFAULT_LEAFLET_MAPTILES, mapBoundary=None, zoomStart=None, points=None, lineWeight=3, lineColor=VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE, lineOpacity=0.8, lineStyle='solid', fillColor=None, fillOpacity=0.3):
	"""
	Add a polygon, as defined by an ordered collection of lat/lon coordinates, to a Leaflet map.
		
	Note
	----
	There is also a "polyline" function, which does not assume a closed shape.
			
	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the polygon will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default as None
		This is the name of the map file that will be created (e.g., "../output/map.html" or "map.html").  The filename should have a `.html` extension.  If `mapFilename` is not provided, no map file will be generated.  The returned map object can be viewed within a Jupyter notebook.
	mapBackground: string, Optional, default as 'CartoDB positron'
		Sets the background tiles of the map.  See :ref:`Leaflet Style` for the list of options.
	mapBoundary: list of lists, Optional, default as None
		Allows customization of the zoom level.  If a map boundary is provided, the zoom level will correspond to the rectangle defined by the two map boundary points. This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  Must be in the form [[south lat, west lon], [north lat, east lon]].
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	points: list of lists, Required, default None
		Specifies the ordered collection of lat/lon coordinates comprising the polygon.  This must be a list of lists, of the form `[[lat1, lon1], [lat2, lon2], ..., [latn, lonn]]` or `[[lat1, lon1, alt1], [lat2, lon2, alt2], ..., [latn, lonn, altn]]`.  If an altitude is provided with each coordinate, this component will be ignored (as all Leaflet maps assume that objects are at ground level).  It is not necessary for `[lat1, lon1]` and `[latn, lonn]` to be the same point.  In other words, the polygon will automatically connect the first and last locations specified in the `points` list.		
	lineWeight: int, Optional, default 3
		The width of the polygon's outline, in units of [pixels].  This value is ignored if `lineColor = None`. 
	lineColor: string, Optional, default 'red'
		The color of the polygon's outline.  `lineColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). No line will be drawn if `lineColor = None`. 
	lineOpacity: float in [0, 1], Optional, default 0.8
		Specifies the opacity of the polygon's outline.  Valid values are in the range from 0 (invisible) to 1 (no transparency).
	lineStyle: string, Optional, default 'solid'
		The style of the polygon's outline.  See :ref:`Leaflet Style` for a list of valid options.  
	fillColor: string, Optional, default None
		The color of the interior of the polygon. `fillColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). The polygon will not be filled if `fillColor = None`.  
	fillOpacity: float in [0, 1], Optional, default 0.3
		Specifies the opacity of the polygon's interior.  Valid values are in the range from 0 (invisible) to 1 (no transparency). 
	
	Return
	------
	Folium object
		A Folium map object containing a polygon (and pre-existing items previously specified in mapObject).
		
	Example
	-------
		>>> # Draw a filled polygon around the Univ. at Buffalo campus.
		>>> # Save this as "a_polygon.html".
		>>> import veroviz as vrv
		>>> campusPoints = [[43.0121, -78.7858],
		...                 [43.0024, -78.7977],
		...                 [42.9967, -78.7921],
		...                 [42.9988, -78.7790]]
		>>> myMap = vrv.addLeafletPolygon(
		...     points=campusPoints,
		...     mapFilename="a_polygon.html")
		>>> myMap

		>>> # Draw a filled polygon around the Univ. at Buffalo campus.
		>>> # This example includes all of the available function arguments.
		>>> import veroviz as vrv
		>>> campusPoints = [[43.0121, -78.7858],
		...                 [43.0024, -78.7977],
		...                 [42.9967, -78.7921],
		...                 [42.9988, -78.7790]]
		>>> myMap = vrv.addLeafletPolygon(
		...     mapObject = None, 
		...     mapFilename = None, 
		...     mapBackground = 'OpenStreetMap', 
		...     mapBoundary = vrv.getMapBoundary(locs=campusPoints), 
		...     zoomStart = 15, 
		...     points = campusPoints, 
		...     lineWeight = 7, 
		...     lineColor = '#ff00ff', 
		...     lineOpacity = 0.9, 
		...     lineStyle = 'solid', 
		...     fillColor = '#ff66ff', 
		...     fillOpacity = 0.3)    
		>>> myMap
	"""
 

	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletPolygon(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, points, lineWeight, lineColor, lineOpacity, lineStyle, fillColor, fillOpacity)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	# Adjust the scope of the map to proper
	[[minLat, maxLon], [maxLat, minLon]] = getMapBoundary(None, None, points)

	# Do we have a rectangle?
	if (len(points) == 2):
		if ( (len(points[0]) == 2) & (len(points[1]) == 2)):
			points = [points[0], [points[0][0], points[1][1]], points[1], [points[1][0], points[0][1]]]
			if (VRV_SETTING_SHOWWARNINGMESSAGE):
				print("NOTE: Only two pairs of coordinates were provided in 'points'.  This is being interpreted as a rectangle.")

	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	# If no mapObject exists, set a new mapObject
	if (mapObject == None):
		midLat = (maxLat + minLat) / 2.0
		midLon = (maxLon + minLon) / 2.0
		if (mapBackground in foliumMaps):
			mapObject = folium.Map(
				location=[midLat, midLon], 
				zoom_start=zoomStart if (zoomStart != None) else 10, 
				tiles=mapBackground)
		elif (mapBackground in customMaps):
			mapObject = folium.Map(
				location=[midLat, midLon], 
				zoom_start=zoomStart if (zoomStart != None) else 10,  
				tiles=customMaps[mapBackground]['tiles'],
				attr=customMaps[mapBackground]['attr'])

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)
		elif (mapBoundary is None):
			mapObject.fit_bounds(getMapBoundary(None, None, points))
	try:
		lineStyle = lineStyle.lower()
	except:
		pass
		
	# Interpret line style
	if (lineStyle == 'dashed'):
		dashArray = '30 10'
	elif (lineStyle == 'dotted'):
		dashArray = '1 6'
	else:
		dashArray = None

	try:
		lineColor = lineColor.lower()
	except:
		pass
		
	try:
		fillColor = fillColor.lower()
	except:
		pass

	points2D = []
	for i in range(len(points)):
		points2D.append([points[i][0], points[i][1]])

	folium.Polygon(locations = points2D, 
		stroke = True, 
		weight = lineWeight, 
		color = lineColor, 
		opacity = lineOpacity, 
		dash_array = dashArray,
		fill_color = fillColor,
		fill_opacity = fillOpacity
		).add_to(mapObject)


	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (VRV_SETTING_SHOWOUTPUTMESSAGE):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject

def addLeafletPolyline(mapObject=None, mapFilename=None, mapBackground=VRV_DEFAULT_LEAFLET_MAPTILES, mapBoundary=None, zoomStart=None, points=None, lineWeight=3, lineColor=VRV_DEFAULT_LEAFLET_OBJECT_COLOR_LINE, lineOpacity=0.8, lineStyle='solid'):

	"""
	Add a polyline, as described by an ordered collection of lat/lon coordinates, to a Leaflet map.  
		
	Note
	----
	The polyline is an "open" shape, in the sense that there's nothing connecting the first and last locations.  By contrast, the "polygon" shape will automatically connect the first and last locations.

	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the polyline will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default as None
		This is the name of the map file that will be created (e.g., "../output/map.html" or "map.html").  The filename should have a `.html` extension.  If `mapFilename` is not provided, no map file will be generated.  The returned map object can be viewed within a Jupyter notebook.
	mapBackground: string, Optional, default as 'CartoDB positron'
		Sets the background tiles of the map.  See :ref:`Leaflet Style` for the list of options.
	mapBoundary: list of lists, Optional, default as None
		Allows customization of the zoom level.  If a map boundary is provided, the zoom level will correspond to the rectangle defined by the two map boundary points. This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  Must be in the form [[south lat, west lon], [north lat, east lon]].
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	points: list of lists, Required, default None
		Specifies the ordered collection of lat/lon coordinates comprising the polyline.   This must be a list of lists, of the form `[[lat1, lon1], [lat2, lon2], ..., [latn, lonn]]` or `[[lat1, lon1, alt1], [lat2, lon2, alt2], ..., [latn, lonn, altn]]`.  If an altitude is provided with each coordinate, this component will be ignored (as all Leaflet maps assume that objects are at ground level).  Note that the polyline will not automatically connect the first and last locations specified in the `points` list.  (By contrast the "polygon" function does connect those locatons.)
	lineWeight: int, Optional, default 3
		The width of the polyline's outline, in units of [pixels].  This value is ignored if `lineColor = None`. 
	lineColor: string, Optional, default 'red'
		The color of the polyline's outline.  `lineColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). No line will be drawn if `lineColor = None`. 
	lineOpacity: float in [0, 1], Optional, default 0.8
		Specifies the opacity of the polyline.  Valid values are in the range from 0 (invisible) to 1 (no transparency).
	lineStyle: string, Optional, default 'solid'
		The style of the polyine.  See :ref:`Leaflet Style` for a list of valid options.  
	
	Return
	------
	Folium object
		A Folium map object containing a polyline (and pre-existing items previously specified in mapObject).
		
	Example
	-------
		>>> # Draw a polyline around the northern portion of the Univ. at Buffalo campus.
		>>> # Save this as "a_polyline.html".
		>>> import veroviz as vrv
		>>> campusPoints = [[43.0024, -78.7977],
		...                 [43.0121, -78.7858],
		...                 [42.9988, -78.7790]]
		>>> myMap = vrv.addLeafletPolyline(
		...     points=campusPoints,
		...     mapFilename="a_polyline.html")
		>>> myMap

		>>> # Draw a polyline around the northern portion of the Univ. at Buffalo campus.
		>>> # This example includes all of the available function arguments.
		>>> import veroviz as vrv
		>>> campusPoints = [[43.0024, -78.7977],
		...                 [43.0121, -78.7858],
		...                 [42.9988, -78.7790]]
		>>> myMap = vrv.addLeafletPolyline(
		...     mapObject = None, 
		...     mapFilename = None, 
		...     mapBackground = 'CartoDB positron', 
		...     mapBoundary = vrv.getMapBoundary(locs=campusPoints),
		...     zoomStart = 14, 
		...     points = campusPoints,
		...     lineWeight = 13, 
		...     lineColor = '#0055ff', 
		...     lineOpacity = 0.8, 
		...     lineStyle = 'solid')
		>>> myMap
	"""

	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletPolyline(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, points, lineWeight, lineColor, lineOpacity, lineStyle)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	# Adjust the scope of the map to proper bounds
	[[minLat, maxLon], [maxLat, minLon]] = getMapBoundary(None, None, points)

	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	# If no mapObject exists, set a new mapObject
	if (mapObject == None):
		midLat = (maxLat + minLat) / 2.0
		midLon = (maxLon + minLon) / 2.0
		if (mapBackground in foliumMaps):
			mapObject = folium.Map(
				location=[midLat, midLon], 
				zoom_start=zoomStart if (zoomStart != None) else 10,  
				tiles=mapBackground)
		elif (mapBackground in customMaps):
			mapObject = folium.Map(
				location=[midLat, midLon], 
				zoom_start=zoomStart if (zoomStart != None) else 10, 
				tiles=customMaps[mapBackground]['tiles'],
				attr=customMaps[mapBackground]['attr'])

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)
		elif (mapBoundary is None):
			mapObject.fit_bounds(getMapBoundary(None, None, points))

	try:
		lineStyle = lineStyle.lower()
	except:
		pass
		
	# Interpret line style
	if (lineStyle == 'dashed'):
		dashArray = '30 10'
	elif (lineStyle == 'dotted'):
		dashArray = '1 6'
	else:
		dashArray = None

	try:
		lineColor = lineColor.lower()
	except:
		pass

	points2D = []
	for i in range(len(points)):
		points2D.append([points[i][0], points[i][1]])
		
	folium.PolyLine(locations = points2D, 
		stroke = True, 
		weight = lineWeight, 
		color = lineColor,
		opacity = lineOpacity, 
		dash_array = dashArray,
		fill = False
		).add_to(mapObject)


	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (VRV_SETTING_SHOWOUTPUTMESSAGE):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject

def addLeafletText(mapObject=None, mapFilename=None, mapBackground=VRV_DEFAULT_LEAFLET_MAPTILES, mapBoundary=None, zoomStart=None, anchorPoint=None, text=None, fontSize=VRV_DEFAULT_LEAFLET_FONTSIZE, fontColor=VRV_DEFAULT_LEAFLET_FONTCOLOR, horizAlign='center'):
	"""
	Add a text label to a Leaflet map. 
		
	Parameters
	----------
	mapObject: Folium object, Optional, default None
		A Folium map object.  If provided, the text label will be added to an existing map.  Otherwise, a new map will be created.
	mapFilename: string, Optional, default as None
		This is the name of the map file that will be created (e.g., "../output/map.html" or "map.html").  The filename should have a `.html` extension.  If `mapFilename` is not provided, no map file will be generated.  The returned map object can be viewed within a Jupyter notebook.
	mapBackground: string, Optional, default as 'CartoDB positron'
		Sets the background tiles of the map.  See :ref:`Leaflet Style` for the list of options.
	mapBoundary: list of lists, Optional, default as None
		Allows customization of the zoom level.  If a map boundary is provided, the zoom level will correspond to the rectangle defined by the two map boundary points. This feature is useful if you want to create multiple comparison maps, each with the same zoom level and centering.  Must be in the form [[south lat, west lon], [north lat, east lon]].
	zoomStart: int, Optional, default as None
		Specifies the default zoom level.  1 --> global view;  18 --> max zoom.  Note that some map tiles have maximum zoom levels less than 18.  The `zoomStart` will be overridden by a `mapBoundary` (if one is provided).
	anchorPoint: list, Required, default None
		Specifies an anchor point (location) for the text label.  Must be a list of the form `[lat, lon]` or `[lat, lon, alt]`.  If provided, the altitude component will be ignored (as all locations on Leaflet maps are assumed to be at ground level).  See also the `horizAlign` field below.
	text: string, Required, default None
		Specifies the text to be displayed on the map at the location of `anchorPoint`.
	fontSize: float, Optional, default 24
		The size of the font, in units of [points].  The default is 24-point font.
	fontColor: string, Optional, default 'orange'
		The color of the text string.  `fontColor` may be one of Leaflet's pre-specified colors (see :ref:`Leaflet style`), or it may be a hex value, such as `#ff0000` (see https://www.w3schools.com/colors/colors_picker.asp). 
	horizAlign: string, Optional, default 'center'
		The horizontal alignment of the text string, relative to the location specified by the `anchorPoint` input argument.  Valid options are 'left' (the text begins at the `anchorPoint` location), 'right' (the text ends at the `anchorPoint` location), or 'center' (the text is centered at the 'anchorPoint' location).  		
	
	Return
	------
	Folium object
		A Folium map object containing a text string (and pre-existing items previously specified in mapObject).
		
	Example
	-------
		>>> # Draw a text label at the location of Bell Hall on the 
		>>> # Univ. at Buffalo campus.
		>>> # Save this as "a_text_label.html".
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletText(
		...     anchorPoint=[43.00154, -78.7871],
		...     text="Bell Hall",
		...     mapFilename="a_text_label.html")

		>>> myMap

		>>> # Draw a text label at the location of Bell Hall on the
		>>> # Univ. at Buffalo campus.
		>>> # This example includes all of the available function arguments.
		>>> import veroviz as vrv
		>>> myMap = vrv.addLeafletText(
		...     mapObject=None, 
		...     mapFilename=None, 
		...     mapBackground='CartoDB positron', 
		...     mapBoundary=None, 
		...     zoomStart=10, 
		...     anchorPoint=[43.00154, -78.7871],
		...     text="Bell Hall",
		...     fontSize=34, 
		...     fontColor='black', 
		...     horizAlign='left')
		>>> myMap
	"""	
	
	# validation
	[valFlag, errorMsg, warningMsg] = valAddLeafletText(mapObject, mapFilename, mapBackground, mapBoundary, zoomStart, anchorPoint, text, fontSize, fontColor, horizAlign)
	if (not valFlag):
		print (errorMsg)
		return
	elif (VRV_SETTING_SHOWWARNINGMESSAGE and warningMsg != ""):
		print (warningMsg)

	try:
		mapBackground = mapBackground.lower()
	except:
		pass

	anchorPoint = [anchorPoint[0], anchorPoint[1]]
		
	# If there is no mapObject exists, set a new mapObject
	if (mapObject == None):
		if (mapBackground in foliumMaps):
			mapObject = folium.Map(
				location=anchorPoint, 
				zoom_start=zoomStart if (zoomStart != None) else 10, 
				tiles=mapBackground)
		elif (mapBackground in customMaps):
			mapObject = folium.Map(
				location=anchorPoint, 
				zoom_start=zoomStart if (zoomStart != None) else 10, 
				tiles=customMaps[mapBackground]['tiles'],
				attr=customMaps[mapBackground]['attr'])

	# set the map boundary for mapObject
	if (zoomStart is None):
		if (mapBoundary is not None):
			mapObject.fit_bounds(mapBoundary)

	iconSizeX = 900		# FIXME -- Not sure if this is good.
	
	try:
		horizAlign = horizAlign.lower()
	except:
		pass
		
	if (horizAlign == 'left'):
		iconAnchorX = 0
	elif (horizAlign == 'right'):
		iconAnchorX = iconSizeX
	else:
		iconAnchorX = iconSizeX / 2
				
	try:
		fontColor = fontColor.lower()
	except:
		pass
							
	folium.map.Marker(anchorPoint, icon=DivIcon(
		icon_size = (iconSizeX, fontSize), 
		icon_anchor = (iconAnchorX, fontSize), 
		html = "<div style=\"font-size: %dpt; color: %s; text-align: %s;\">%s</div>" %  (fontSize, fontColor, horizAlign, text)
		)).add_to(mapObject)

	if (mapFilename is not None):
		mapObject.save(mapFilename)
		if (VRV_SETTING_SHOWOUTPUTMESSAGE):
			print("Message: Map page written to %s." % (mapFilename))

	return mapObject