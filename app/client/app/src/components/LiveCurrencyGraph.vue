<template>
  <section>

    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          Live Prices
        </p>
      </header>
      <div class="card-content">
        <div class="container-select">
          <div class="select right">
            <select class="select-small" v-model="curr_1">
                <option v-for="c in currencies">{{ c }}</option>
            </select>
          </div>
          <div class="select left">
            <select v-model="curr_2">
                <option v-for="c in currencies">{{ c }}</option>
            </select>
          </div>
        </div>
        <div class="clear" ></div>
        <line-chart :chart-data="chartData" :options="options"></line-chart>
      </div>
    </div>

  </section>
</template>

<script>

import LineChart from '../charts/LineChart'
import { HTTP } from '../http-common.js'

export default {
  components: {
    LineChart
  },
  data: () => ({
    curr_1: '',
    curr_2: '',
    currencies: [],
    chartData: {
      labels: [],
      datasets: []
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  }),
  created () {
    /*
    As indicated here: https://stackoverflow.com/questions/45813347/difference-between-the-created-and-mounted-events-in-vue-js
    The created event is the optimal place to request data.
    */
    this.getCurrencies()
  },
  watch: {
    curr_1: function (val) {
      this.fillData()
    },
    curr_2: function (val) {
      this.fillData()
    }
  },
  methods: {
    fillData () {
      HTTP.get('/currencies/latest/graph/' + this.curr_1 + '/' + this.curr_2)
        .then((response) => {
          this.chartData = response.data
        }, (error) => {
          console.log('ERROR ' + error)
        })
    },
    getCurrencies () {
      HTTP.get(`/currencies/list`)
        .then((response) => {
          this.currencies = response.data.currencies
          this.curr_1 = this.currencies[0]
          this.curr_2 = this.currencies[1]
          /* Every 3 seconds fill data. Polling data from API. */
          setInterval(() => {
            this.fillData()
          }, 3000)
        }, (error) => {
          console.log('ERROR ' + error)
        })
    }
  }
}
</script>

<style>
.select-small{ height: 30px; }
.select select { font-size: 13px; height: 2em; color: #363636 }
.select:not(.is-multiple)::after { margin-top: -0.7em; margin-right: -0.3em; }
.right{ float: right; }
.left{ float: left; }
.clear{ clear:both; }
.container-select{ width: calc(100% - 15px); margin: 0 auto; }
</style>