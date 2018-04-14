<template>
  <section>

    <div class="container">
      <custom-component style="width:75%" :data="'DataFromParent'"/>
    </div>

  </section>
</template>
<script>
import CustomComponent from '../components/CustomComponent'
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
    'custom-component': CustomComponent
  },
  data () {
    return {

    }
  },
  computed: {
    isLoading () {
      return this.$store.state.isLoading
    }
  }
}
</script>

<style lang="sass" scoped>

</style>