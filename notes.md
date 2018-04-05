# Notes

## Mongo

Heroku MongoLab Sandbox (the only free version available as a Heroku addon) has only 496 MB worth of storage. Constantly updating Currency prices being saved to the database accumulates a vast amount of space. 

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

Use redis to signal the api and DB handler to do all writes. (Probably better)

## References

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