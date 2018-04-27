<template>
  <section>

    <div class="card" style="height: inherit;">
      <header class="card-header">
        <p class="card-header-title">
          Bitcoin Prediction
        </p>
      </header>
      <div class="card-content">
        <ml-btc-graph class="left" style="width:74.5%; display:block;"/>
        <ml-btc-prediction class="right"  style="width:24.5%; display:block;margin-top:20px;"/>
      </div>
    </div>

  </section>
</template>

<script>
import MLBTCGraph from '../components/MLBTCGraph'
import MLBTCPrediction from '../components/MLBTCPrediction'

export default {
  components: {
    'ml-btc-graph': MLBTCGraph,
    'ml-btc-prediction': MLBTCPrediction
  }
}
</script>

<style>
</style>