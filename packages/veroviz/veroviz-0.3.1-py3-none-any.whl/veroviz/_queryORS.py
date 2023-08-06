from veroviz._common import *
from veroviz._internal import distributeTimeDist
from veroviz._internal import loc2Dict
from veroviz._internal import locs2Dict


def orsGetSnapToRoadLatLon(loc, APIkey):
	"""
	A function to get snapped latlng for one coordinate using ORS
	Parameters
	----------
	loc: list
		The location to be snapped to road
	Returns
	-------
	list
		A snapped location in the format of [lat, lon].  Note that this function will lose the info of altitude of the location.
	"""

	# There is no function in ORS that snaps to a road.
	# Instead, issue a driving request from a location to itself.
	dicLoc = loc2Dict(loc)
    
	# ORS uses [lon, lat] order:
	snapToRoadUrl = ('https://api.openrouteservice.org/v2/directions/driving-car?api_key=%s&start=%s,%s&end=%s,%s' % 
					(APIkey, dicLoc['lon'], dicLoc['lat'], dicLoc['lon'], dicLoc['lat']))
 
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', snapToRoadUrl)
		data = json.loads(response.data.decode('utf-8'))

		http_status = response.status

		if (http_status == 200):
			# OK
			# ORS uses [lon, lat] order:
			snapLoc = [data['features'][0]['geometry']['coordinates'][0][1], 
						data['features'][0]['geometry']['coordinates'][0][0]] 
            
			return snapLoc
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return
	except:
		print("Error: ", sys.exc_info()[1])
		raise 


def orsGetShapepointsTimeDist(startLoc, endLoc, travelMode='fastest', APIkey=None):
	"""
	A function to get a list of shapepoints from start coordinate to end coordinate. 
	Parameters
	----------
	startLoc: list
		Start location.  The format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt]
	endLoc: list
		End location.  The format is [lat, lon] (altitude, above sea level, set to be 0) or [lat, lon, alt]
	travelMode: string, {fastest}
		Optional, default as 'fastest'. Choose a travel mode as a parameter for ORS
	Returns
	-------
	path: list of lists
		A list of coordinates in sequence that shape the route from startLoc to endLoc
	timeInSeconds: double   FIXME????
		time between current shapepoint and previous shapepoint, the first element should be 0  FIXME???
	distInMeters: double    FIXME???
		distance between current shapepoint and previous shapepoint, the first element should be 0  FIXME???
	"""

	dicStartLoc = loc2Dict(startLoc)
	dicEndLoc = loc2Dict(endLoc)

	"""
	The following "profile" options are available in ORS:
		'driving-car'		('fastest')	
		'driving-hgv'		('truck' - fastest)
		'cycling-regular'	('cycling')
		'cycling-road'
		'cycling-mountain'
		'cycling-electric'
		'foot-walking'
		'foot-hiking'
		'wheelchair'
		
		There is no "shortest" option    
	"""
	
	try:
		travelMode = travelMode.lower()
	except:
		pass
	
	if (travelMode == 'fastest'):
		profile = 'driving-car'
	elif (travelMode == 'pedestrian'):
		profile = 'foot-walking'
	elif (travelMode == 'cycling'):
		profile = 'cycling-road'
	elif (travelMode == 'truck'):
		profile = 'driving-hgv'
	else:
		print("Error: Invalid travelMode.")
		return    
    
	# ORS uses [lon, lat] order:
	shapepointsUrl = ('https://api.openrouteservice.org/v2/directions/%s?api_key=%s&start=%s,%s&end=%s,%s' % 
					(profile, APIkey, dicStartLoc['lon'], dicStartLoc['lat'], dicEndLoc['lon'], dicEndLoc['lat']))

	try:
		http = urllib3.PoolManager()
		response = http.request('GET', shapepointsUrl)
		data = json.loads(response.data.decode('utf-8'))

		http_status = response.status

		if (http_status == 200):
			# OK
			# ORS uses [lon, lat] order:
			path = []
			timeInSeconds = []
			distInMeters = []
			for i in range(len(data['features'][0]['geometry']['coordinates'])):
				path.append([data['features'][0]['geometry']['coordinates'][i][1], 
							 data['features'][0]['geometry']['coordinates'][i][0]])

			for i in range(len(data['features'][0]['properties']['segments'])):
				for j in range(len(data['features'][0]['properties']['segments'][i]['steps'])):
					# Find arrival times for each shapepoint location.
					# ORS gives times for groups of waypoints...we need more granularity.

					subpathTimeSec = data['features'][0]['properties']['segments'][i]['steps'][j]['duration']
					wpStart = data['features'][0]['properties']['segments'][i]['steps'][j]['way_points'][0]
					wpEnd = data['features'][0]['properties']['segments'][i]['steps'][j]['way_points'][1]

					[tmpTimeSec, tmpDistMeters] = distributeTimeDist(path[wpStart:wpEnd+1], subpathTimeSec)
					if (len(timeInSeconds) == 0):
						timeInSeconds += tmpTimeSec
						distInMeters += tmpDistMeters
					else:
						timeInSeconds += tmpTimeSec[1:]
						distInMeters += tmpDistMeters[1:]
                    
			return [path, timeInSeconds, distInMeters]
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return

	except:
		print("Error: ", sys.exc_info()[1])
		raise


def orsGetTimeDistAll2All(locs, travelMode='fastest', APIkey=None):
	"""
	A function to generate distance and time matrices between given coordinates.
	Parameters
	----------
	locs: list of lists, Required
		The format is [[lat1, lon1], [lat2, lon2], ...]. A list of coordinates.
	travelMode: string, {fastest, pedestrian, cycling, truck}
		ORS provides multiple types of routing.  VeRoViz implements the following: 'fastest' (for car), 'pedestrian', 'cycling', and 'truck'.
	APIkey: string, Required
		Enables access to ORS server.
	
	Returns
	-------
	time: dictionary
		A square matrix, which provides the traveling time between each pair of coordinates.  Units are in seconds.
	dist: dictionary
		A square matrix, which provides the distance between each pair of coordinates.  Units are in meters.
	"""

	"""
	The following "profile" options are available in ORS:
		'driving-car'		('fastest')	
		'driving-hgv'
		'cycling-regular'
		'cycling-road'
		'cycling-mountain'
		'cycling-electric'
		'foot-walking'
		'foot-hiking'
		'wheelchair'
		
		There is no "shortest" option    
	"""
	
	try:
		travelMode = travelMode.lower()
	except:
		pass

	if (travelMode == 'fastest'):
		profile = 'driving-car'
	elif (travelMode == 'pedestrian'):
		profile = 'foot-walking'
	elif (travelMode == 'cycling'):
		profile = 'cycling-road'
	elif (travelMode == 'truck'):
		profile = 'driving-hgv'
	else:
		print("Error: Invalid travelMode.")
		return    
    
	maxBatchSize = 50   # 50 x 50
	numBatches = int(math.ceil(len(locs) / float(maxBatchSize)))

	all2AllUrl = ('https://api.openrouteservice.org/v2/matrix/%s' % (profile))

	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Authorization': APIkey,
				'Content-Type': 'application/json'}

	distMeters = {}
	timeSecs = {}

	try:
		for rowBatch in range(0, numBatches):
			sourceLocs = []
			sources = []

			# ORS uses [lon, lat] order:
			for i in range(maxBatchSize * rowBatch, min(len(locs), maxBatchSize * (rowBatch + 1))):
				sources.append(len(sourceLocs))
				sourceLocs.append([locs[i][1],locs[i][0]])

			for colBatch in range(0, numBatches):
				destinations = []
				locations = list(sourceLocs)
				if (colBatch == rowBatch):
					# We're on the diagonal. Sources and Destinations are the same (all-to-all).
					encoded_body = json.dumps({
						"locations": sourceLocs,
						"metrics": ["distance","duration"],
						"units": "m"})
				else:
					# We're off-diagonal.  Sources and Destinations differ.
					for i in range(maxBatchSize * colBatch, min(len(locs), maxBatchSize * (colBatch + 1))):
						destinations.append(len(locations))
						locations.append([locs[i][1],locs[i][0]])

					encoded_body = json.dumps({
						"locations": locations,
						"sources": sources,
						"destinations": destinations,
						"metrics": ["distance","duration"],
						"units": "m"})

				if (len(locations) <= 1):
					# We have a 1x1 matrix.  Nothing to do. 
					row = maxBatchSize * rowBatch
					col = maxBatchSize * colBatch
					distMeters[row, col] = 0.0
					timeSecs[row, col] = 0.0
				else:
					http = urllib3.PoolManager()
					response = http.request('POST', all2AllUrl, headers=headers, body=encoded_body)

					data = json.loads(response.data.decode('utf-8'))
					http_status = response.status

					if (http_status == 200):
						# OK
						row = maxBatchSize * rowBatch
						for i in range(0, len(data['durations'])):
							col = maxBatchSize * colBatch
							for j in range(0, len(data['durations'][i])):
								distMeters[row, col] = data['distances'][i][j]
								timeSecs[row, col] = data['durations'][i][j]
								col += 1
							row += 1    
					else:
						# Error of some kind
						http_status_description = responses[http_status]
						print("Error Code %s: %s" % (http_status, http_status_description))
						return

		return [timeSecs, distMeters]

	except:
		print("Error: ", sys.exc_info()[1])
		raise


def orsGetTimeDistOne2Many(fromLoc, toLocs, travelMode='fastest', APIkey=None):
	"""
	A function to generate distance and time matrices between given coordinates.
	Parameters
	----------
	fromLoc: list, Required
		One coordinate, in the format of [lat, lon].
	toLocs: list of lists, Required
		The format is [[lat1, lon1], [lat2, lon2], ...], a list of coordinates.
	travelMode: string, {fastest, pedestrian, cycling, truck}
		ORS provides multiple types of routing.  VeRoViz implements the following: 'fastest' (for car), 'pedestrian', 'cycling', and 'truck'.
	APIkey: string, Required
		Enables access to ORS server.
	
	Returns
	-------
	time: dictionary
		A 1-row matrix, which provides the travel time from a given location to numerous other locations. Units are in seconds.
	dist: dictionary
		A 1-row matrix, which provides the distance from a given location to numerous other locations. Units are in meters.
	"""

    
	"""
	The following "profile" options are available in ORS:
		'driving-car'		('fastest')	
		'driving-hgv'
		'cycling-regular'
		'cycling-road'
		'cycling-mountain'
		'cycling-electric'
		'foot-walking'
		'foot-hiking'
		'wheelchair'
		
		There is no "shortest" option    
	"""
	
	try:
		travelMode = travelMode.lower()
	except:
		pass

	if (travelMode == 'fastest'):
		profile = 'driving-car'
	elif (travelMode == 'pedestrian'):
		profile = 'foot-walking'
	elif (travelMode == 'cycling'):
		profile = 'cycling-road'
	elif (travelMode == 'truck'):
		profile = 'driving-hgv'
	else:
		print("Error: Invalid travelMode.")
		return    
    
	one2ManyBatchSize = 2500 # < 2500 (50 x 50)
	numBatches = int(math.ceil(len(toLocs) / float(one2ManyBatchSize)))
	one2ManyUrlBase = ('https://api.openrouteservice.org/v2/matrix/%s' % (profile))

	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Authorization': APIkey,
				'Content-Type': 'application/json'}

	distMeters = {}
	timeSecs = {}

	try:
		for batch in range(0, numBatches):
			locations = []
			sources = []
			destinations = []
    
			# ORS uses [lon, lat] order:
			sources.append(0)
			locations.append([fromLoc[1], fromLoc[0]])
			for i in range(one2ManyBatchSize * batch, min(len(toLocs), one2ManyBatchSize * (batch + 1))):
				destinations.append(len(locations))
				locations.append([toLocs[i][1],toLocs[i][0]])
        
			encoded_body = json.dumps({
				"locations": locations,
				"sources": sources,
				"destinations": destinations,
				"metrics": ["distance","duration"],
				"units": "m"})

			http = urllib3.PoolManager()
			response = http.request('POST', one2ManyUrlBase, headers=headers, body=encoded_body)

			data = json.loads(response.data.decode('utf-8'))
			http_status = response.status

			if (http_status == 200):
				# OK
				col = one2ManyBatchSize * batch
				for i in range(0, len(data['durations'])):
					for j in range(0, len(data['durations'][i])):
						# print(data['distances'][i][j])
						# print(data['durations'][i][j])
						distMeters[0, col] = data['distances'][i][j]
						timeSecs[0, col] = data['durations'][i][j]
						col += 1
			else:
				# Error of some kind
				http_status_description = responses[http_status]
				print("Error Code %s: %s" % (http_status, http_status_description))
				return

		return [timeSecs, distMeters]
                    
	except:
		print("Error: ", sys.exc_info()[1])
		raise


def orsGetTimeDistMany2One(fromLocs, toLoc, travelMode='fastest', APIkey=None):
	"""
	A function to generate distance and time matrices from one set of locations to a single location.
	Parameters
	----------
	fromLocs: list of lists, Required
		The format is [[lat1, lon1], [lat2, lon2], ...], a list of coordinates.
	toLoc: list, Required
		One coordinate, in the format of [lat, lon].
	travelMode: string, {fastest, pedestrian, cycling, truck}
		ORS provides multiple types of routing.  VeRoViz implements the following: 'fastest' (for car), 'pedestrian', 'cycling', and 'truck'.
	APIkey: string, Required
		Enables access to ORS server.
	
	Returns
	-------
	time: dictionary
		A 1-column matrix, which provides the travel time from a given set of locations a single location. Units are in seconds.
	dist: dictionary
		A 1-column matrix, which provides the distance from a given set of locations to a single location. Units are in meters.
	"""

    
	"""
	The following "profile" options are available in ORS:
		'driving-car'		('fastest')	
		'driving-hgv'
		'cycling-regular'
		'cycling-road'
		'cycling-mountain'
		'cycling-electric'
		'foot-walking'
		'foot-hiking'
		'wheelchair'
		
		There is no "shortest" option    
	"""
	
	try:
		travelMode = travelMode.lower()
	except:
		pass

	if (travelMode == 'fastest'):
		profile = 'driving-car'
	elif (travelMode == 'pedestrian'):
		profile = 'foot-walking'
	elif (travelMode == 'cycling'):
		profile = 'cycling-road'
	elif (travelMode == 'truck'):
		profile = 'driving-hgv'
	else:
		print("Error: Invalid travelMode.")
		return
    
    
	many2OneBatchSize = 2500 # < 2500 (50 x 50)
	numBatches = int(math.ceil(len(fromLocs) / float(many2OneBatchSize)))
	many2OneUrlBase = ('https://api.openrouteservice.org/v2/matrix/%s' % (profile))

	headers = {
				'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
				'Authorization': APIkey,
				'Content-Type': 'application/json'}

	distMeters = {}
	timeSecs = {}

	try:
		for batch in range(0, numBatches):
			locations = []
			sources = []
			destinations = []
    
			# ORS uses [lon, lat] order:
			for i in range(many2OneBatchSize * batch, min(len(fromLocs), many2OneBatchSize * (batch + 1))):
				sources.append(len(locations))
				locations.append([fromLocs[i][1],fromLocs[i][0]])
			destinations.append(len(locations))
			locations.append([toLoc[1],toLoc[0]])

			encoded_body = json.dumps({
				"locations": locations,
				"sources": sources,
				"destinations": destinations,
				"metrics": ["distance","duration"],
				"units": "m"})

			http = urllib3.PoolManager()
			response = http.request('POST', many2OneUrlBase, headers=headers, body=encoded_body)

			data = json.loads(response.data.decode('utf-8'))
			http_status = response.status

			if (http_status == 200):
				# OK
				row = many2OneBatchSize * batch
				for i in range(0, len(data['durations'])):
					for j in range(0, len(data['durations'][i])):
						# print(data['distances'][i][j])
						# print(data['durations'][i][j])
						distMeters[row, 0] = data['distances'][i][j]
						timeSecs[row, 0] = data['durations'][i][j]
						row += 1
			else:
				# Error of some kind
				http_status_description = responses[http_status]
				print("Error Code %s: %s" % (http_status, http_status_description))
				return

		return [timeSecs, distMeters]
                    
	except:
		print("Error: ", sys.exc_info()[1])
		raise


def orsGeocode(text, APIkey):
	"""
	Geocode from a text string using ORS
	
	Parameters
	----------
	text: string
		A text string describing an address, city, or landmark.
	    
	Returns
	-------
	loc: list
		A geocoded location in the format of [lat, lon].
	"""
    
	# ORS uses [lon, lat] order:
	geocodeUrl = ('https://api.openrouteservice.org/geocode/search?api_key=%s&text=%s&size=1' % (APIkey, text))
    
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', geocodeUrl)
		data = json.loads(response.data.decode('utf-8'))

		http_status = response.status

		if (http_status == 200):
			# OK
			# ORS uses [lon, lat] order:
			loc = [data['features'][0]['geometry']['coordinates'][1], 
				   data['features'][0]['geometry']['coordinates'][0]] 
			return loc
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return
	except:
		print("Error: ", sys.exc_info()[1])
		raise 
		
def orsReverseGeocode(loc, APIkey):
	"""
	Reverse Geocode from a [lat, lon] or [lat, lon, alt] location using ORS
	
	Parameters
	----------
	loc: list
		Of the form [lat, lon] or [lat, lon, alt].  If provided, altitude will be ignored.
	    
	Returns
	-------
	snapLoc: list
		Of the form [lat, lon].  This is the nearest point to the given (input) location.
	address: dictionary
		A dataProvider-specific dictionary containing address details.
	"""    
    
	# ORS uses [lon, lat] order:
	geocodeUrl = ('https://api.openrouteservice.org/geocode/reverse?api_key=%s&point.lon=%s&point.lat=%s&size=1' % (APIkey, loc[1], loc[0]))
	try:
		http = urllib3.PoolManager()
		response = http.request('GET', geocodeUrl)
		data = json.loads(response.data.decode('utf-8'))

		http_status = response.status

		if (http_status == 200):
			# OK
			# ORS uses [lon, lat] order:
			snapLoc = [data['features'][0]['geometry']['coordinates'][1], 
				       data['features'][0]['geometry']['coordinates'][0]] 
			address = data['features'][0]['properties']
			return (snapLoc, address)
		else:
			# Error of some kind
			http_status_description = responses[http_status]
			print("Error Code %s: %s" % (http_status, http_status_description))
			return
	except:
		print("Error: ", sys.exc_info()[1])
		raise 
		