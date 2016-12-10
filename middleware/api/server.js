var express = require('express');
var bodyParser = require('body-parser');
var cassandra = require('cassandra-driver');

var client = new cassandra.Client( { contactPoints : [ '127.0.0.1' ] }, { protocolOptions : { port: 9042 } } );
client.connect(function(err, result) {
  //assert.ifError(err);
  console.log('Connected.');
});

const BigDecimal = require('cassandra-driver').types.BigDecimal;
var app = express();
var getAirQuality = "SELECT * FROM WAQ.air_quality;";
const getWaterSites = "SELECT * FROM waq.water_sites WHERE solr_query='LatitudeMeasure:[~SWLat TO ~NELat] AND LongitudeMeasure:[~SWLon TO ~NELon]' limit 10000;"
const getMeasurementData = "SELECT * FROM waq.measurement_data WHERE solr_query='lat:[~SWLat TO ~NELat] AND lng:[~SWLon TO ~NELon]' limit 10000;"
const getMeasurements = "SELECT * FROM waq.measurement_data WHERE solr_query='lat:[~SWLat TO ~NELat] AND lng:[~SWLon TO ~NELon] AND contaminant_type:~Type' limit 10000;"

app.use(bodyParser.json());
app.set('json spaces', 2);

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.get('/metadata', function(req, res) {
  //console.log(res);
  res.send(client.hosts.slice(0).map(function (node) {
    return { address : node.address, rack : node.rack, datacenter : node.datacenter }
  }));
});

/**
 * @api {get} /getAirQuality/:date Get Air Quality Metrics
 * @apiName getAirQuality
 * @apiGroup AirQuality
 *
 * @apiParam {Timestamp} date Users unique ID.
 *
 * @apiSuccess {Timestamp} time Air Quality time window.
 *
 * @apiSuccessExample Success-Response:
 *     HTTP/1.1 200 OK
 *     {
 *       "time": "2016-08-22T09:16:47.000Z",
 *       "count": 11
 *     }
 *
 * @apiError RSVPCountError Could not fetch RSVP counts.
 *
 * @apiErrorExample Error-Response:
 *     HTTP/1.1 404 Not Found
 *     {
 *       "error": "Could not fetch RSVP counts"
 *     }
 */

 app.get('/getAirQuality', function(req, res) {
   client.execute(getAirQuality, [], function(err, result) {
     if (err) {
       res.status(404).send({ "error" : 'Could not fetch air quality data' });
       //console.log(err);
     } else {
       res.json(result);        }
     });
   });

/**
* @api {get} /getWaterSites/:SWLat/:SWLon/:NELat/:NELon Get Water Sites in square boundaries
* @apiName getWaterSites
* @apiGroup WaterQuality
*
* @apiParam {SWLat} decimal SW Corner Latitude.
* @apiParam {SWLon} decimal SW Corner Longitude.
* @apiParam {NELat} decimal NE Corner Latitude.
* @apiParam {NELon} decimal NE Corner Longitude.
*
* @apiSuccess {MonitoringLocationIdentifier} string Monitoring Site Identifier.
* @apiSuccess {MonitoringLocationTypeName} string Monitoring Site Identifier.
* @apiSuccess {MonitoringLocationName} string Monitoring Site Identifier.
* @apiSuccess {CountyCode} float Monitoring Site Identifier.
* @apiSuccess {CountyName} string Monitoring Site Identifier.
* @apiSuccess {LatitudeMeasure} decimal Monitoring Site Identifier.
* @apiSuccess {LongitudeMeasure} decimal Monitoring Site Identifier.
*
* @apiSuccessExample Success-Response:
*     HTTP/1.1 200 OK
*     {
*       "time": "2016-08-22T09:16:47.000Z",
*       "count": 11
*     }
*
* @apiError RSVPCountError Could not fetch RSVP counts.
*
* @apiErrorExample Error-Response:
*     HTTP/1.1 404 Not Found
*     {
*       "error": "Could not fetch RSVP counts"
*     }
*/

app.get('/getWaterSites/:SWLat/:SWLon/:NELat/:NELon', function(req, res) {
  var SWLat = parseFloat(req.params.SWLat);
  var SWLon = parseFloat(req.params.SWLon);
  var NELat = parseFloat(req.params.NELat);
  var NELon = parseFloat(req.params.NELon);
  query = getWaterSites.replace("~SWLat",SWLat).replace("~SWLon",SWLon).replace("~NELat",NELat).replace("~NELon",NELon);
  //console.log(SWLat,SWLon,NELat,NELon);
  //console.log(query);
  client.execute(query, function(err, result) {
    if (err) {
      res.status(404).send({ "error" : 'Could not fetch water monitoring sites' });
      //console.log(err);
    } else {
      res.json(result.rows);        }
    });
  });

app.get('/getMeasurementData/:SWLat/:SWLon/:NELat/:NELon', function(req, res) {
  var SWLat = parseFloat(req.params.SWLat);
  var SWLon = parseFloat(req.params.SWLon);
  var NELat = parseFloat(req.params.NELat);
  var NELon = parseFloat(req.params.NELon);
  query = getMeasurementData.replace("~SWLat",SWLat).replace("~SWLon",SWLon).replace("~NELat",NELat).replace("~NELon",NELon);
  //console.log(SWLat,SWLon,NELat,NELon);
  //console.log(query);
  client.execute(query, function(err, result) {
    if (err) {
      res.status(404).send({ "error" : 'Could not fetch measurement data' });
      //console.log(err);
    } else {
      res.json(result.rows);        }
    });
  });

app.get('/getMeasurements/:Type/:SWLat/:SWLon/:NELat/:NELon', function(req, res) {
  var SWLat = parseFloat(req.params.SWLat);
  var SWLon = parseFloat(req.params.SWLon);
  var NELat = parseFloat(req.params.NELat);
  var NELon = parseFloat(req.params.NELon);
  console.log(req.params.Type);
  query = getMeasurements.replace("~SWLat",SWLat).replace("~SWLon",SWLon).replace("~NELat",NELat).replace("~NELon",NELon).replace("~Type",req.params.Type);
  //console.log(SWLat,SWLon,NELat,NELon);
  //console.log(query);
  client.execute(query, function(err, result) {
    if (err) {
      res.status(404).send({ "error" : 'Could not fetch measurement data' });
      //console.log(err);
    } else {
      res.json(result.rows);        }
    });
  });

app.get('/getStateCounts/', function(req, res) {
  console.log("getStateCounts");
  console.log(req.query.type);
  console.log(req.query.state);
  var response = [];
  response[0] = {};
  response[0]['name'] = "Ankit";
  res.json(response);
});

var server = app.listen(8080, function() {
  console.log('Listening on port %d', server.address().port);
});
