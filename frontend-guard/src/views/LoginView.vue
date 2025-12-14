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
import axios from 'axios'

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await axios.post(`${API_URL}/api/auth/login`, {
      username: username.value,
      password: password.value
    })
    
    localStorage.setItem('guard_token', response.data.access_token)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
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
