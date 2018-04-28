<template>
  <section>

      <div class="btc-ml">
          <img class="btc-ml-icon" src="../assets/img/Bitcoin-icon.png"/>
          <p class="btc-ml-title">Predicted close price ({{getDate}})</p>
          <p class="btc-ml-subtitle">Updated Daily</p>
          <p class="btc-ml-body">{{ prediction }}</p>
      </div>

  </section>
</template>

<script>
import { HTTP } from '../http-common.js'

export default {
  data: () => ({
    prediction: ''
  }),
  created () {
    this.getPrediction()
  },
  computed: {
    getDate () {
      return new Date().toJSON().slice(0, 10)
    }
  },
  methods: {
    getPrediction () {
      HTTP.get(`/currencies/ml/btc`)
        .then((response) => {
          this.prediction = response.data.prediction
        }, (error) => {
          this.prediction = 'Error'
          console.log('ERROR ' + error)
        })
    }
  }
}
</script>
<style>
.btc-ml{ text-align: center; }
.btc-ml-icon{ height: 100px; width:100px; margin: 0 auto; display: block; }
.btc-ml-title{ color: #363636; font-weight: bold; font-size: .85rem; }
.btc-ml-subtitle{ font-style: italic; font-size: .8rem; }
.btc-ml-body { color: #F6931F; font-weight: bold; margin-top:50px; font-size: x-large; }
</style>
