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
import LineChart from '../charts/LineChart.js'

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
    this.fillData()
  },

  mounted () {
    // this.renderChart(this.chartData, this.options)

    setInterval(() => {
      this.fillData()
      console.log('Filling Data')
    }, 3000)
  },

  methods: {
    fillData () {
      this.chartData = {
        labels: ['January' + this.getRandomInt(), 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
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