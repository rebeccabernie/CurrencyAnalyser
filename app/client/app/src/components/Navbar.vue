<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <!--<a class="navbar-item" href="#">
        <img src="../assets/img/logo.png">
      </a>-->
      <a class="center" href="#">
        Currency Analyser
      </a>
    </div>
    <div class="navbar-menu">
      <div class="navbar-end">
        <span class="navbar-item is-size-7 is-dark">{{version}}</span>
      </div>
    </div>
  </nav>
</template>
<script>

export default {
  name: 'Navbar',
  data () {
    return {
      version: this.$store.state.version
    }
  }
}
</script>
<style>
.navbar {
  background: #363636;
}
.navbar-brand{
  width: 100%;
}
.navbar .center {
  color:#f8f8f8f8;
  font-size: 1.25rem;
  margin: auto;
}
.navbar .center:hover {
  color:#fff;
}
</style>

<!--
<style lang="sass" scoped>

nav.navbar
  min-height: none
  background-color: $nav-background
  border-bottom: solid 1px #dbdbdb

.navbar-brand > .navbar-item
  color: #fff
  padding-left: 10px
  margin: 0 auto

.navbar-brand
  a
    &:hover
      color:yellow

  img
    height: 15px
</style>
-->

