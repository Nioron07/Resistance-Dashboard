<template>
  <v-container fluid class="fill-height d-flex justify-center align-center">
    <SignUpCard />
  </v-container>
</template>

<script setup lang="ts">
// Set the title of the page
useHead({
  title: 'Sign Up'
})
</script>

<style scoped>
.fill-height {
  min-height: 80vh;
}
</style>