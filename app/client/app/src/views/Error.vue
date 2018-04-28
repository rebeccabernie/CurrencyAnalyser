<template>
  <section>

    <div class="error">Whoa! Where do you think you're going?</div>

  </section>
</template>

<script>
/*
The error view is the page that will alert the user that they have entered an invalid subdomain.
 */
export default {
  name: 'Error'
}
</script>

<style>
.error{
    text-align:center;
    font-size: 1.5rem;
    margin-top: 50px;
}
</style>
