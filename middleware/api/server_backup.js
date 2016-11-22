var express = require('express');
var bodyParser = require('body-parser');
var cassandra = require('cassandra-driver');

var client = new cassandra.Client( { contactPoints : [ '127.0.0.1' ] }, { protocolOptions : { port: 9042 } } );
client.connect(function(err, result) {
  //assert.ifError(err);
  console.log('Connected.');
});

var app = express();
var getRSVPCount = "SELECT time, count FROM meetlytix.rsvp_count where time >= ? ALLOW FILTERING;";
var getRSVPByGeo = "select * from meetlytix.rsvp_by_geo;";
var getEventCount = "select * from meetlytix.event_counts;";
var getTopics = "select * from meetlytix.topics limit 100;";
var getResponse = "select * from meetlytix.response_batch;";
var getHistogram = "select * from meetlytix.histogram;";
var getTotalRSVP = "select count(*) from meetlytix.meetlytix_raw_v3;";

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
 * @api {get} /getRSVPCount/:date Get RSVP Counts
 * @apiName getRSVPCount
 * @apiGroup RSVP
 *
 * @apiParam {Timestamp} date Users unique ID.
 *
 * @apiSuccess {Timestamp} time RSVP time window.
 * @apiSuccess {Integer} count number of RSVPs.
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

app.get('/getRSVPCount/:date', function(req, res) {
  var rangeDate = new Date(req.params.date);
  client.execute(getRSVPCount, [rangeDate], function(err, result) {
    if (err) {
      res.status(404).send({ "error" : 'Could not fetch RSVP counts' });
      //console.log(err);
    } else {
      res.json(result);        }
    });
  });

  /**
   * @api {get} /getRSVPByGeo Get RSVP By Geo-location
   * @apiName getRSVPByGeo
   * @apiGroup RSVP
   *
   * @apiSuccess {String} group_country Group Country.
   * @apiSuccess {String} group_state Group State.
   * @apiSuccess {String} group_city Group City.
   * @apiSuccess {Integer} count number of RSVPs.
   *
   * @apiSuccessExample Success-Response:
   *     HTTP/1.1 200 OK
   *     {
   *       "group_country": "ca",
   *       "group_state": "AB",
   *       "group_city": "Calgary",
   *       "count": 94
   *     }
   *
   * @apiError RSVPGeoCountError Could not fetch RSVP Geo counts.
   *
   * @apiErrorExample Error-Response:
   *     HTTP/1.1 404 Not Found
   *     {
   *       "error": "Could not fetch RSVP Geo counts"
   *     }
   */

app.get('/getRSVPByGeo', function(req, res) {
  client.execute(getRSVPByGeo, [], function(err, result) {
    if (err) {
      res.status(404).send({ "error" : 'Could not fetch RSVP Geo counts' });
      //console.log(err);
    } else {
      res.json(result);        }
    });
  });

  /**
   * @api {get} /getEventCount Get Event Count
   * @apiName getRSVPByGeo
   * @apiGroup RSVP
   *
   * @apiSuccess {String} event_name Event Name.
   * @apiSuccess {String} event_url Event URL.
   * @apiSuccess {Integer} count number of RSVPs.
   * @apiSuccess {String} group_city Group City.
   * @apiSuccess {String} group_country Group Country.
   * @apiSuccess {String} group_state Group State.
   *
   * @apiSuccessExample Success-Response:
   *     HTTP/1.1 200 OK
   *     {
   *       "event_name": "Group Meditation - Weekly - All Expertise",
   *       "event_url": "http://www.meetup.com/School-of-Metaphysics-Tulsa/events/233110066/",
   *       "count": 12,
   *       "group_city": "group_city",
   *       "group_country": "us",
   *       "group_state": "AZ"
   *     }
   *
   * @apiError EventCountError Could not fetch Event counts.
   *
   * @apiErrorExample Error-Response:
   *     HTTP/1.1 404 Not Found
   *     {
   *       "error": "Could not fetch Event counts"
   *     }
   */

app.get('/getEventCount', function(req, res) {
  client.execute(getEventCount, [], function(err, result) {
    if (err) {
      res.status(404).send({ "error" : 'Could not fetch Event counts' });
      //console.log(err);
    } else {
      res.json(result);        }
    });
  });

  /**
   * @api {get} /getTopics Get Topic Counts
   * @apiName getTopics
   * @apiGroup Topics
   *
   * @apiSuccess {String} group_topics Group Topics.
   * @apiSuccess {Integer} count number of RSVPs.
   *
   * @apiSuccessExample Success-Response:
   *     HTTP/1.1 200 OK
   *     {
   *       "group_topics": "Nonprofits Needing Help",
   *       "count": 12
   *     }
   *
   * @apiError TopicCountError Could not fetch topic counts.
   *
   * @apiErrorExample Error-Response:
   *     HTTP/1.1 404 Not Found
   *     {
   *       "error": "Could not fetch topic counts"
   *     }
   */

app.get('/getTopics', function(req, res) {
  client.execute(getTopics, [], function(err, result) {
    if (err) {
      res.status(404).send({ "error" : 'Could not fetch topic counts' });
      //console.log(err);
    } else {
      res.json(result);        }
    });
  });

  /**
   * @api {get} /getResponse Get Response Count
   * @apiName getResponse
   * @apiGroup RSVP
   *
   * @apiSuccess {String} days Days.
   * @apiSuccess {Integer} count number of RSVPs.
   *
   * @apiSuccessExample Success-Response:
   *     HTTP/1.1 200 OK
   *     {
   *       "days": "40",
   *       "count": 12
   *     }
   *
   * @apiError RSVPResponseError Could not fetch RSVP responses.
   *
   * @apiErrorExample Error-Response:
   *     HTTP/1.1 404 Not Found
   *     {
   *       "error": "Could not fetch RSVP responses"
   *     }
   */

app.get('/getResponse', function(req, res) {
  client.execute(getResponse, [], function(err, result) {
    if (err) {
      res.status(404).send({ "error" : 'Could not fetch RSVP responses' });
      //console.log(err);
    } else {
      res.json(result);        }
    });
  });

  /**
   * @api {get} /getHistogram Get Histogram
   * @apiName getHistogram
   * @apiGroup RSVP
   *
   * @apiSuccess {String} days Days.
   * @apiSuccess {Integer} count number of RSVPs.
   *
   * @apiSuccessExample Success-Response:
   *     HTTP/1.1 200 OK
   *     {
   *       "days": "40",
   *       "count": 12
   *     }
   *
   * @apiError HistogramError Could not fetch histogram.
   *
   * @apiErrorExample Error-Response:
   *     HTTP/1.1 404 Not Found
   *     {
   *       "error": "Could not fetch histogram"
   *     }
   */

app.get('/getHistogram', function(req, res) {
  client.execute(getHistogram, [], function(err, result) {
    if (err) {
      res.status(404).send({ "error" : 'Could not fetch histogram' });
      //console.log(err);
    } else {
      res.json(result);        }
    });
  });

app.get('/getTotalRSVP', function(req, res) {
  client.execute(getTotalRSVP, [], function(err, result) {
    if (err) {
      res.status(404).send({ "error" : 'Could not fetch total count' });
      //console.log(err);
    } else {
      res.json(result);        }
    });
  });

var server = app.listen(8080, function() {
  console.log('Listening on port %d', server.address().port);
});
