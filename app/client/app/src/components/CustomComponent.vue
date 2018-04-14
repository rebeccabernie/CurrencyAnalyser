<template>
  <section>

    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          Live Currency Comparison
        </p>
      </header>
      <div class="card-content">
        <select v-model="curr_1">
            <option v-for="c in currencies">{{ c }}</option>
        </select>
        <select v-model="curr_2">
            <option v-for="c in currencies">{{ c }}</option>
        </select>
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
          /*
          TODO: Display error to user.
          */
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

<style lang="sass" scoped>


</style>
