<template>
  <section>

    <div class="card">
      <header class="card-header">
        <p class="card-header-title">
          Currency Rates
        </p>
      </header>
      <div class="card-content list">
        <ul id="currency_list">
        <li v-for="c in currencies">
            <div> {{ c.name }} </div>
            <div> {{ c.data }} </div>
        </li>
        </ul>
      </div>
    </div>

  </section>
</template>

<script>
import { HTTP } from '../http-common.js'

export default {
  data: () => ({
    currencies: []
  }),
  created () {
    this.getCurrencies()
    setInterval(() => {
      this.getCurrencies()
    }, 3000)
  },
  methods: {
    getCurrencies () {
      HTTP.get(`/currencies/latest/list`)
        .then((response) => {
          this.currencies = response.data.currencies
        }, (error) => {
          console.log('ERROR ' + error)
        })
    }
  }
}
</script>

<style>
#currency_list li {
    font-weight:550;
    font-size: 12px;
    text-align:center;
    height:30px;
    height: 28px;
    padding: 5px 0px 0px 0px;
}
#currency_list li:not(:last-child){
    border-bottom: 1px dotted lightgrey;
}
#currency_list{
    margin-top: -10px;
}
#currency_list li div:last-child {
    width:50%;
    float:right;
    color:#666666;
}
#currency_list li div:first-child {
    color:black;
    width:50%;
    float:left;
}
.list.card-content {
    padding: 30px
}
</style>
