# Notes

## Mongo

(Heroku MongoLab Sandbox)[https://elements.heroku.com/addons/mongolab] (the only free version available as a Heroku addon) has only 496 MB worth of storage. Constantly updating Currency prices being saved to the database accumulates a vast amount of space. 

We need to look at how data can be saved in the database. 

What we need to save:

+ Model in JSON format?
+ Machine learning data.
+ Currency data needed for ML.

## Background Scripts

```worker``` pulling currency data.
```purge``` removing data.

Either can add or delete from DB directly.

or

Use redis to signal the DB handler to do all writes. (Probably better)

- This can be done with the (Redis To Go)[https://devcenter.heroku.com/articles/redistogo] Heroku plugin. Basically, redis, a in-memeory and key-value based DB, can be used to communicate with the main web application. Another script or the api will contain a class that will listen for the redis channel and add the to the DB. The api will act as the DB hander or DAO (Data Access Object), controlling and encapsulating actual communications to MongoDB. Listener code snippet:
```
// <routing.py>
// Connect to redis and start thread to listen to the currency data channel.
r = redis.from_url(REDIS_URL)
client = Listener(r, [REDIS_CHAN_CURR])
client.start()

// <listen.py>
class Listener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):
        // add to database
        self.redis.set(REDIS_CHAN_GRAPH, item['data'])
        #print("Item recived: " + str(item['data']))

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == b'KILL':
                self.pubsub.unsubscribe()
                print(self, "unsubsribed")
                break
            else:
                self.work(item)
```
    - **Issue 1**: The listener class in the api does not get shut down when trying to shutdown server. SOVLED: the modulale atexit can be used to detect when the worker is being shut down. A kill request can then be sent to the api listener, allowing the web app to shutdown.
    ```
    # Adapted from: https://docs.python.org/2/library/atexit.html
    @atexit.register
    def goodbye():
        print("Shutting down")
        print("Killing listener")
        payload = 'KILL'
        r.publish(REDIS_CHAN_CURR, payload)
    ```
- Queues with RQ can be used to manage requests to the DB handler. So all data is processed.

During the implementation of this concept for handling data, we came upon the realization that the API would be unnecessarily dealing with Mongo. The web app only deals with the most recent data and could be optimized by being pre-formatted to suit the web application's data format requirements. The data from the API to the web application will be requested and constantly refreshed for the most recent currency data. It would be cumbersome to query Mongo and reformat the query result with every request. The scripts were already communicating with the API via Redis, it seemed optimal that the scripts handle mongo and use Redis solely to share the most recent data with the API. This would inevitably require us to change our Mongo driver to MongoEngine, as PyMongo is a Flask module and our scripts will not be Flasks applications. On the bright side, the web application's Heroku CPU allocation will no longer be competing with listener threads, and the management of Mongo will be abstracted from the API rather than delegated to it.

~~TODO: pymongo in blueprint, try: https://stackoverflow.com/questions/33166612/blueprints-pymongo-in-flask~~

## Web app

### Dashboard page

The dashboard view contains cards with the currency data accumulated from the data scraping and analytics. The cards will consist of cards to display the:

- most recent currency data in an easy to read graph. Two currencies can be selected at one time.
- most recent currency data in a list. Only the most popular currencies will be featured in this list.
- ML bitcoin prediction.
- ML bitcoin prediction graph with most recent past predictions and actual predictions?

The recent currency data will be polled/streamed from the server and will be filtered to fit the purpose of different cards.

The graph card will be filtered using the default currency selections. This will be refiltered once a user selects new
filters and when the data has been polled. 

The most popular will be filtered using a static list of relevant/well-known currencies. 

Depending on how often the ML predictions will be updated, the data will be updated or requested once.

Data will be formatted python or vue side to adhere to the following format for the use of chart js:

```
 chartData : {
        labels: [String],
        datasets: [
          {
            label: String,
            backgroundColor: String,
            data: [number]
          },
          {
            label: String,
            backgroundColor: String,
            data: [number]
          }
        ]
      }
```

E.g.

```
 chartData : {
        labels: ['5:34', '5:36'],
        datasets: [
          {
            label: 'EURO',
            backgroundColor: 'rgba(255, 0, 0, 0.5)',
            data: [2000.68, 2000.71]
          },
          {
            label: 'BITCOIN',
            backgroundColor: 'rgba(169,169,169, 0.5)',
            data: [4467.05, 4467.93]
          }
        ]
      }
```

## References

https://medium.com/techtrument/handling-ajax-request-in-vue-applications-using-axios-1d26c47fab0

https://forum.vuejs.org/t/how-to-set-base-url-right/2540

https://devcenter.heroku.com/articles/redistogo

https://github.com/vuejs/vue-router/issues/866

https://github.com/gtalarico/flask-vuejs-template

https://mattstauffer.com/blog/getting-started-using-vues-vue-router-for-single-page-apps/

https://router.vuejs.org/en/essentials/dynamic-matching.html

https://router.vuejs.org/en/essentials/named-routes.html

https://router.vuejs.org/en/essentials/getting-started.html

https://codepen.io/ztrayner/pen/VeJMRL

https://codepen.io/anon/pen/ppGeKJ?editors=1010

https://github.com/apertureless/vue-chartjs

https://flask-restful.readthedocs.io/en/latest/quickstart.html#resourceful-routing

http://flask.pocoo.org/docs/0.12/blueprints/

https://stephennewey.com/realtime-websites-with-flask/

https://forum.vuejs.org/t/how-to-set-base-url-right/2540/6

https://www.npmjs.com/package/vue-chart-js

https://www.npmjs.com/package/vue-chartjs

http://vue-chartjs.org/#/home?id=reactive-data

https://codepen.io/Mark_Bowley/pen/xEbuI

https://github.com/pallets/flask/issues/348

http://flask.pocoo.org/docs/0.12/blueprints/#static-files

https://stackoverflow.com/questions/15839433/how-to-close-server-sent-events-events