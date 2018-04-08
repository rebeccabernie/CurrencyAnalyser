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

-- This can be done with the (Redis To Go)[https://devcenter.heroku.com/articles/redistogo] Heroku plugin. Basically, redis, a in-memeory and key-value based DB, can be used to communicate with the main web application. Another script or the api will contain a class that will listen for the redis channel and add the to the DB. The api will act as the DB hander or DAO (Data Access Object), controlling and encapsulating actual communications to MongoDB. 

-- Queues with RQ can be used to manage requests to the DB handler. So all data is processed.

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