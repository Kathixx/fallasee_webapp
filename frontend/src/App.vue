<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="row">
      <div class="col-md-4 col-12 logo">
        <h1>FallaSee</h1>
        <h3>Logic Fallacies<br> Detection</h3>
      </div>
      <div class="col-md-8 col-12">
        <nav>
          <RouterLink to="/">Detection</RouterLink>
          <RouterLink to="/logical-fallacies">Fallacies</RouterLink>
          <!-- <RouterLink to="/">About</RouterLink> -->
      </nav>
      </div>
      
    </div>
  </header>

  <main>
    <RouterView />
  </main>
</template>

<style scoped>

</style>
