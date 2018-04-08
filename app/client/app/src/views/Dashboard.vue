<template>
  <div class="container">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          Live Currency Comparison
        </p>
      </header>
      <div class="card-content">
        <line-chart :chart-data="chartData" :options="options"></line-chart>
        <button @click="fillData()">Randomize</button>
      </div>
    </div>
  </div>
</template>

<script>
import LineChart from '../charts/LineChart'

/*
The dashboard view contains cards with the currency data accumulated from the data scraping and analytics. The cards will
consist of cards to display the:

1) most recent currency data in an easy to read graph. Two currencies can be selected at one time.
2) most recent currency data in a list. Only the most popular currencies will be featured in this list.
3) ML bitcoin prediction.
4) ML bitcoin prediction graph with most recent past predictions and actual predictions?

The recent currency data will be polled/streamed from the server and will be filtered to fit the purpose of different cards.
The graph card will be filtered using the default currency selections. This will be refiltered once a user selects new
filters and when the data has been polled. The most popular will be filtered using a static list of relevant/well-known
currencies. Depending on how often the ML predictions will be updated, the data will be updated or requested once.
 */
export default {
  components: {
    LineChart
  },
  data: () => ({
    chartData: {},
    max: 50,
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  }),
  created () {
    /* Poll data for the first time here. */
    this.fillData()
  },

  mounted () {
    // this.renderChart(this.chartData, this.options)
    /*
      Every 3 seconds fill data. Poll data from API here.
    */
    setInterval(() => {
      this.fillData()
      console.log('Filling Data')
    }, 3000)
  },

  methods: {
    fillData () {
      /* Fake data for now. Will call the backend here. */
      this.chartData = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [
          {
            label: 'EURO',
            backgroundColor: 'rgba(255, 0, 0, 0.5)',
            data: [this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt()]
          },
          {
            label: 'BITCOIN',
            backgroundColor: 'rgba(169,169,169, 0.5)',
            data: [this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt()]
          }
        ]
      }
      this.max = 100
    },
    getRandomInt () {
      return Math.floor(Math.random() * (this.max - 5 + 1)) + 5
    }
  }
}
</script>

<style lang="sass" scoped>

</style>