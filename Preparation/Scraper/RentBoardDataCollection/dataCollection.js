//http://www.cityofberkeley.info/RentBoardUnitSearch.aspx
var GoogleMapsAPI = require("googlemaps");
var keyFile = require('./key');
var async = require('async');

var gmAPI = new GoogleMapsAPI({
	key: keyFile.KEY,
	stagger_time:       1000, // for elevationPath 
    encode_polylines:   false,
    secure:             true, // use https 
});

var genPoint = function(original_lat, original_lng, radius) {
	var r = radius/111300 // = 16000 meters ~ 10 miles
  , y0 = original_lat
  , x0 = original_lng
  , u = Math.random()
  , v = Math.random()
  , w = r * Math.sqrt(u)
  , t = 2 * Math.PI * v
  , x = w * Math.cos(t)
  , y1 = w * Math.sin(t)
  , x1 = x / Math.cos(y0)

	newY = y0 + y1;
	newX = x0 + x1;

	return {"lat": newX, "lon": newY}
}

function pointsGenner(numpts, radius, lat, lng) {
	l = [];
	for (var i = 0; i < numpts; i++) {
		l.push(genPoint(lat, lng, radius));
	}
	return l;
}

function asyncRevGeo(numpts, radius, lat, lon) {
	async.eachSeries(pointsGenner(numpts, radius, lat, lon), function gmaps(item, cb) {
			gmAPI.reverseGeocode({
			"latlng": item['lon'].toString() + ", " + item['lat'] //'37.872539, -122.263458',
			// "bounds": ['37.881475, -122.282017', '37.845395, -122.251977']
		}, function (err, result) {
			console.log(result);
			setImmediate(cb);
		});
	}, function donzo() {
		console.log("DONE");
	});
}

asyncRevGeo(25, 1500/*3218.69*/, 37.871419, -122.259707); //8k = five miles in meters


