<template>
  <div id="app">
    <Navbar />
    <router-view />
    <Footer />
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  background-color: #ffebee; /* 与logo同色系浅粉背景 */
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
