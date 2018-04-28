# Notes

## Deployment

**In the ```root``` directory:**

```
git init

heroku login
  [email]
  [password]

heroku create [name]

heroku addons:create redistogo

heroku addons: create mongolab

heroku config:set FLASK_CONFIG=Production

heroku config:set SECRET=SECRETKEY
```

**In the ```app/client/app/src/http-common.js``` file:**

Make sure ```baseURL```  variable in the axios object named ```HTTP``` is set to the Heroku URL with ```/api/``` appended to the end.

**In the ```app/client/app``` directory:**

```
npm run build
```

**In the ```root``` directory:**

```
git add .

git commit -m "[commit msg]"

git push heroku master

heroku ps:scale worker=1

heroku ps:scale urgentworker=1
```

## Structure

- The web application consists of two seperate blueprints resgistered to the following URLs prefixes/subdomains: "" and "/api"
- [Blueprints](http://flask.pocoo.org/docs/0.12/blueprints/) define a collection of behaviours, views, templates, static files and can be then used anywhere in the application.
- Blueprints are used in this application to organize and seperate distinct components, in this case the client and the api.

- The client has the responsibility of serving the HTML files to the user, and can be accessed as such: https://currencyanalyser.herokuapp.com/
- The client has one route, "/", that returns the single page web application. 
- To be precise it returns the ```index.html``` file that links the built and minified Vue.js code in a script tag.
- The single page web application consists of two pages:
  * Home: root page with title. Accessed at: https://currencyanalyser.herokuapp.com/
  * Dashboard: displays a collection of cards containing the different currency related data(prices/rates, ml predictions). Cards containing graphs were originally going to be rendered using D3.js. The D3 library is a fantastic data-driven approach to DOM manipulation. However, D3 was unnecessarily sophisticated for it's use being soley to create dynamic graphs. Chart.js is a simple but powerful data visualization library, that serves our purposes perfectly. Accessed at: https://currencyanalyser.herokuapp.com/#/dashboard
  * About: details about the team, project and contact details. Accessed at https://currencyanalyser.herokuapp.com/#/about
  * Error: any URL containing the domain that is not mentioned above, will be mapped here. Accessed at https://currencyanalyser.herokuapp.com/#/[not_mentioned_above]

- The API has the responsibility of returning machine learning and currency data, and can be accessed as such: https://currencyanalyser.herokuapp.com/api/
- The API blueprint utilizes the Flask-RESTful extension. The api can be queried to get currency data.
- The data returned by the API is populated by background workers.
- The background workers are used to pull data at an scheduled intervals of *n* seconds to pull data, and to train the ML model with the previous days result and to predict the end price for the current day. 
- Initially, the api was act as the DB hander or DAO (Data Access Object), controlling and encapsulating actual communications to MongoDB. The scripts would publish the new values and the api listener threads would handle the data received. However during the implementation of this concept for handling data, we came upon the realization that the API would be unnecessarily dealing with Mongo. The web app only deals with the most recent data and could be optimized by being pre-formatted to suit the web application's data format requirements. The data from the API to the web application will be requested and constantly refreshed for the most recent currency data. It would be cumbersome to query Mongo and reformat the query result with every request. The scripts were already communicating with the API via Redis, it seemed optimal that the scripts handle mongo and use Redis solely to share the most recent data with the API. This would subsequently simplify the code and reduce the dependancies the scripts have on one another, e.g. the worker relies on the web application to save the data published, the worker needs to be ran to allow a clean shutdown of the web application. The web application's Heroku CPU allocation will no longer be competing with listener threads, and the management of Mongo will be abstracted from the API rather than delegated to it.
- As the ML algorithm developed we realized it would no longer require the live currency data, meaning it was no longer neccessary to save the next to real time currency data to Mongo. Now this data will soley be used for live currency data displayed on web application. 

## Web app

### Dashboard page

The dashboard view contains cards with the currency data accumulated from the data scraping and analytics. The cards will consist of cards to display the:

- [x] most recent currency data in an easy to read graph. Two currencies can be selected at one time.
- [x] most recent currency data in a list. Only the most popular currencies will be featured in this list.
- [x] ML bitcoin prediction.
- [x] ML bitcoin prediction graph with most recent past predictions and actual predictions?

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

### About page

- Team: names, github links, etc.
- About web application.
- Repositiory link.

## Future ambitions

SEEs

ref: https://stephennewey.com/realtime-websites-with-flask/

Why Server-Sent Event(SEE) Stream?
Websockets(WSs) are often favoured over SEEs as they provide a protocol surpassing that of SEEs. 
WSs provide bi-directional, full-duplex communication between the server and client.
However, this is only significant when two way communication is required.
For data that does not need to be sent from the client, traditional HTTP SEEs, that do not implement full-duplex communication and the subsequent new WS servers to handle this connection, are ideal.
Also, SSEs have a number of functionalities that WSs lack, such as automatic reconnection.
ref: https://www.html5rocks.com/en/tutorials/eventsource/basics/

## Notes

*The following are **rough** notes that were a product of development.*

### Mongo

[Heroku MongoLab Sandbox](https://elements.heroku.com/addons/mongolab) (the only free version available as a Heroku addon) has only 496 MB worth of storage. Constantly updating Currency prices being saved to the database accumulates a vast amount of space. 

We need to look at how data can be saved in the database. 

What we need to save:

+ Model in JSON format?
+ Machine learning data.
+ Currency data needed for ML.

UPDATE: we will no longer be saving the next to real time currency data to mongo. It is no longer required to use this data for the ML. Now this data will soley be used for live currency data displayed on web app.

### Background Scripts

1. pulling currency data.
2. removing data.

Either can add or delete from DB directly.

or

Use redis to signal the DB handler to do all writes. (Probably better)

- This can be done with the [Redis To Go](https://devcenter.heroku.com/articles/redistogo) Heroku plugin. Basically, redis, a in-memeory and key-value based DB, can be used to communicate with the main web application. Another script or the api will contain a class that will listen for the redis channel and add the to the DB. The api will act as the DB hander or DAO (Data Access Object), controlling and encapsulating actual communications to MongoDB. Listener code snippet:
```python
# <routing.py>

# Connect to redis and start thread to listen to the currency data channel.
r = redis.from_url(REDIS_URL)
client = Listener(r, [REDIS_CHAN_CURR])
client.start()

# <listen.py>

# Adapted from: https://github.com/JGCode/Heroku-Python-Redis-Comm
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

# <worker.py>

payload = json.dumps({
        'data': 'some data'
        })
    r.publish(REDIS_CHAN_CURR, payload)
 ```
  - **ISSUE**: The listener class in the api does not get shut down when trying to shutdown server. 
  - **SOVLED**: the modulale atexit can be used to detect when the worker is being shut down. A kill request can then be sent to the api listener, allowing the web app to shutdown.
    ```python
    # <worker.py>

    # Adapted from: https://docs.python.org/2/library/atexit.html
    @atexit.register
    def goodbye():
        print("Shutting down")
        print("Killing listener")
        payload = 'KILL'
        r.publish(REDIS_CHAN_CURR, payload)
    ```

~~**TODO:** pymongo in blueprint, try: https://stackoverflow.com/questions/33166612/blueprints-pymongo-in-flask~~

During the implementation of this concept for handling data, we came upon the realization that the API would be unnecessarily dealing with Mongo. The web app only deals with the most recent data and could be optimized by being pre-formatted to suit the web application's data format requirements. The data from the API to the web application will be requested and constantly refreshed for the most recent currency data. It would be cumbersome to query Mongo and reformat the query result with every request. The scripts were already communicating with the API via Redis, it seemed optimal that the scripts handle mongo and use Redis solely to share the most recent data with the API. This would subsequently simplify the code and reduce the dependancies the scripts have on one another, e.g. the worker relies on the web application to save the data published, the worker needs to be ran to allow a clean shutdown of the web application. The web application's Heroku CPU allocation will no longer be competing with listener threads, and the management of Mongo will be abstracted from the API rather than delegated to it.

**TODO:** look into RQ and schedular

RQ is currently unsupported by windows, or any operating system that doesn't support the use of ```os.fork()``` (https://github.com/rq/rq/issues/226) for that matter.

The schedular doesn't consistently call our pull data method every *n* seconds. Instead, it pulls the data in *n* seconds plus the time taken to carry out the said method. 

To implement this, we calculated how many seconds, *n*, until the next minute/day and put the thread to sleep for *n* seconds. The following is an example show code executing consitently every minute.

```python
# <dataworker.py>

# Adapted from: https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/38317060
import time

tic = 60.0

starttime=time.time()

while True:
  # Pull data
  time.sleep(60.0 - ((time.time() - starttime) % 60.0))
```

Similarly, to schedule when these loops start - the seconds until the next new minute and the next 3am is calculated and the thread will sleep for those amount of seconds.

## References

https://media.readthedocs.org/pdf/forex-python/latest/forex-python.pdf

https://devcenter.heroku.com/articles/python-rq

https://github.com/JGCode/Heroku-Python-Redis-Comm

https://medium.com/techtrument/handling-ajax-request-in-vue-applications-using-axios-1d26c47fab0

https://forum.vuejs.org/t/how-to-set-base-url-right/2540

https://devcenter.heroku.com/articles/redistogo

https://github.com/vuejs/vue-router/issues/866

https://github.com/gtalarico/flask-vuejs-template

https://mattstauffer.com/blog/getting-started-using-vues-vue-router-for-single-page-apps/

https://router.vuejs.org/en/essentials/dynamic-matching.html

https://router.vuejs.org/en/essentials/named-routes.html

https://stephennewey.com/realtime-websites-with-flask/

https://router.vuejs.org/en/essentials/getting-started.html

https://codepen.io/ztrayner/pen/VeJMRL

https://codepen.io/anon/pen/ppGeKJ?editors=1010

https://github.com/apertureless/vue-chartjs

 https://www.html5rocks.com/en/tutorials/eventsource/basics/

https://flask-restful.readthedocs.io/en/latest/quickstart.html#resourceful-routing

http://flask.pocoo.org/docs/0.12/blueprints/

https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/38317060

https://stephennewey.com/realtime-websites-with-flask/

https://forum.vuejs.org/t/how-to-set-base-url-right/2540/6

https://www.npmjs.com/package/vue-chart-js

https://www.npmjs.com/package/vue-chartjs

http://vue-chartjs.org/#/home?id=reactive-data

https://codepen.io/Mark_Bowley/pen/xEbuI

https://github.com/pallets/flask/issues/348

http://flask.pocoo.org/docs/0.12/blueprints/#static-files

https://stackoverflow.com/questions/15839433/how-to-close-server-sent-events-events
