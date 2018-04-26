<template>
  <section>

    <div class="card" style="height: inherit;">
      <header class="card-header">
        <p class="card-header-title">
          Live Rates
        </p>
      </header>
      <div class="card-content list">
        <ul id="currency_list">
        <li v-for="c in currencies">
            <div> <p v-tooltip.top-center="c.name + ' ' + c.symbol">{{ c.code }}</p> </div>
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
    font-size: 13px;
    text-align: center;
    height: 35px;
    padding: 8px 0px 0px 0px;
}
#currency_list li:not(:last-child){
    border-bottom: .01rem solid rgba(211,211,211,0.75);
}
#currency_list{
    margin-top: -8px;
}
#currency_list li div:last-child {
    width:50%;
    float:right;
    color:#666666;
}
#currency_list li div:first-child {
    /*color:#363636;*/
    width:50%;
    float:left;
}
.list.card-content {
    padding: 30px
}

.tooltip {
  display: block !important;
  z-index: 10000;
}

.tooltip .tooltip-inner {
  background: rgba(0,0,0,0.6);
  color: white;
  border-radius: 16px;
  padding: 5px 10px 4px;
}

.tooltip .tooltip-arrow {
  width: 0;
  height: 0;
  border-style: solid;
  position: absolute;
  margin: 5px;
  border-color: rgba(0,0,0,0.6);
}

.tooltip[x-placement^="top"] {
  margin-bottom: 5px;
}

.tooltip[x-placement^="top"] .tooltip-arrow {
  border-width: 5px 5px 0 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  bottom: -4px;
  left: calc(50% - 5px);
  margin-top: 1px;
  margin-bottom: 0;
}

.tooltip-arrow{
  top: calc(50% + 15px);
}

.tooltip[x-placement^="bottom"] {
  margin-top: 5px;
}

.tooltip[x-placement^="bottom"] .tooltip-arrow {
  border-width: 0 5px 5px 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-top-color: transparent !important;
  top: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^="right"] {
  margin-left: 5px;
}

.tooltip[x-placement^="right"] .tooltip-arrow {
  border-width: 5px 5px 5px 0;
  border-left-color: transparent !important;
  border-top-color: transparent !important;
  border-bottom-color: transparent !important;
  left: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip[x-placement^="left"] {
  margin-right: 5px;
}

.tooltip[x-placement^="left"] .tooltip-arrow {
  border-width: 5px 0 5px 5px;
  border-top-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  right: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip[aria-hidden='true'] {
  visibility: hidden;
  opacity: 0;
  transition: opacity .15s, visibility .15s;
}

.tooltip[aria-hidden='false'] {
  visibility: visible;
  opacity: 1;
  transition: opacity .15s;
}

</style>
