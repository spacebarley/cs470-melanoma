<template>
  <v-footer
    inset
    app
    height="100"
    id="main-footer"
  >
    <v-layout
      row
      wrap
      style="justify-content:center"
    >
      <v-btn
        color="white"
        rounded
        href="https://github.com/spacebarley/cs470-melanoma"
      >
        Github Repository
      </v-btn>
      <v-flex
        primary
        lighten-2
        py-3
        white--text
        xs12
        style="margin-top:15px; margin-bottom:10px; text-align:center;"
      >
        &copy;2020 — <strong>CS470 Team 30</strong>
      </v-flex>
    </v-layout>
  </v-footer>
</template>

<script>
export default {
  name: 'main-footer',

}
</script>

<style scoped>

</style>