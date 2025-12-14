<template>
  <div class="guest-app">
    <GuestPortal />
  </div>
</template>

<script setup>
import GuestPortal from './components/GuestPortal.vue'
</script>

<style scoped>
.guest-app {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
