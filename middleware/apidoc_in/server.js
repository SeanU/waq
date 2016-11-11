var express = require('express');
var bodyParser = require('body-parser');
var cassandra = require('cassandra-driver');

var client = new cassandra.Client( { contactPoints : [ '127.0.0.1' ] }, { protocolOptions : { port: 9042 } } );
client.connect(function(err, result) {
  //assert.ifError(err);
  console.log('Connected.');
});

var app = express();
var getAirQuality = "SELECT * FROM WAQ.air_quality;";

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

var server = app.listen(8080, function() {
  console.log('Listening on port %d', server.address().port);
});
