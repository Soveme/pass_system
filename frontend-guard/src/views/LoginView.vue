<template>
  <div class="login-container">
    <div class="login-card">
      <h1>🗑 Pass System</h1>
      <p>Guard Scanner</p>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <input 
            v-model="username" 
            type="text" 
            placeholder="Username"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <input 
            v-model="password" 
            type="password" 
            placeholder="Password"
            class="form-input"
          />
        </div>
        
        <div v-if="error" class="alert alert-error">{{ error }}</div>
        
        <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
          {{ loading ? 'Loading...' : 'Login' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  const success = await authStore.login(username.value, password.value)
  
  if (success) {
    router.push('/')
  } else {
    error.value = authStore.error
  }
  
  loading.value = false
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background-color: #2a2a2a;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
}

.login-card h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.login-card p {
  color: #999;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-input {
  width: 100%;
  padding: 1rem;
  background-color: #1a1a1a;
  border: 2px solid #444;
  color: white;
  font-size: 1.125rem;
  border-radius: 8px;
}

.form-input:focus {
  outline: none;
  border-color: #27ae60;
}

.btn-full {
  width: 100%;
  margin-top: 1rem;
}
</style>
