<template>
  <section>

    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          Live Currency Comparison
        </p>
      </header>
      <div class="card-content">
        <div class="content">
          Content
          <div>{{ r }}</div>
        </div>
      </div>
    </div>

  </section>
</template>

<script>

import { HTTP } from '../http-common.js'

export default {
  name: 'CustomComponent',
  data () {
    return {
      r: ''
    }
  },
  watch: {
    viewToggleOther (bool) {
      this.setToggle('other', bool)
    }
  },
  methods: {
    setToggle: function (name, bool) {
      console.log('Toggle Called')
    },
    getRandomInt () {
      return Math.floor(Math.random() * (100 - 5 + 1)) + 5
    },
    getResource () {
      HTTP.get(`resource/one`)
        .then((response) => {
          this.r = response.data
        }, (error) => {
          this.r = 'Error: ' + error
        })
    }
  },
  /*
  computed: {
    resource () {
      // To display `resourceOne` value from the backend
      console.log(this.$store.state.resource)
      return this.$store.state.resource
    }
  },
  */
  mounted () {
    this.getResource()
  }
}
</script>

<style lang="sass" scoped>


</style>
