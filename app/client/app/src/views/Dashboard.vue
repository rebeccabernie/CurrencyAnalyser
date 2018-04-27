<template>
  <section>

    <div class="container">
      <div style="width:100%; height:532px;">
        <live-currency-graph style="width:74.5%; float:right; display:block;height: inherit;"/>
        <live-currency-list style="width:24.5%; float:left; display:block;height: inherit;"/>
      </div>
      <div class="spacer"></div>
      <div style="width:100%; height:520px;">
        <ml-btc style="height: inherit;"/>
      </div>
      <div class="spacer"></div>
    </div>

  </section>
</template>
<script>
import LiveCurrencyGraph from '../components/LiveCurrencyGraph'
import LiveCurrencyList from '../components/LiveCurrencyList'
import MLBTC from '../components/MLBTC'
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
  name: 'Property',
  components: {
    'live-currency-graph': LiveCurrencyGraph,
    'live-currency-list': LiveCurrencyList,
    'ml-btc': MLBTC
  }
}
</script>

<style>
.spacer { clear: both; height: 30px; display: block; }
.right{ float: right; }
.left{ float: left; }
</style>