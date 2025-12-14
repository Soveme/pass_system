<template>
  <div id="app" class="app-container">
    <nav class="navbar">
      <div class="navbar-brand">
        <h1>Pass System</h1>
        <span class="badge">Admin Panel</span>
      </div>
      <div class="navbar-menu">
        <router-link to="/" class="nav-link">Пропуска</router-link>
        <router-link to="/statistics" class="nav-link">Статистика</router-link>
        <router-link to="/users" class="nav-link">Пользователи</router-link>
        <router-link to="/audit" class="nav-link">Журнал аудита</router-link>
        <button @click="logout" class="btn btn-logout">Выход</button>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
    <CookieBanner v-if="!cookiesAccepted" @accept="acceptCookies" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import CookieBanner from './components/CookieBanner.vue'

const router = useRouter()
const cookiesAccepted = ref(localStorage.getItem('cookies_accepted') === 'true')

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const acceptCookies = () => {
  localStorage.setItem('cookies_accepted', 'true')
  cookiesAccepted.value = true
}

onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token && router.currentRoute.value.path !== '/login') {
    router.push('/login')
  }
})
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #f5f5f5;
}

.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.navbar-brand h1 {
  margin: 0;
  font-size: 1.5rem;
}

.badge {
  background-color: #27ae60;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
}

.navbar-menu {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-link {
  color: #ecf0f1;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: rgba(255,255,255,0.1);
}

.nav-link.router-link-active {
  background-color: #3498db;
  color: white;
}

.btn-logout {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-logout:hover {
  background-color: #c0392b;
}

.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
</style>
