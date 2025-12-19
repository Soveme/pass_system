<template>
  <div id="app" class="guard-app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token && router.currentRoute.value.path !== '/login') {
    router.push('/login')
  }
})
</script>

<style scoped>
.guard-app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #1a1a1a;
  color: white;
}
</style>
