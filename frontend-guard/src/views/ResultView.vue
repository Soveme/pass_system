<template>
  <div class="result-container" :class="result?.status">
    <div class="result-content">
      <div class="status-icon">
        <span v-if="result?.is_valid" class="icon-success">✓</span>
        <span v-else class="icon-error">✗</span>
      </div>
      
      <h1 v-if="result?.is_valid" class="status-title">ALLOWED</h1>
      <h1 v-else class="status-title-error">DENIED</h1>
      
      <div class="pass-details" v-if="result?.is_valid">
        <p class="guest-name">{{ result.guest_name }}</p>
        <p class="guest-company" v-if="result.guest_company">{{ result.guest_company }}</p>
        <p class="valid-until">Valid until: {{ formatDate(result.valid_until) }}</p>
        <img v-if="result.guest_photo_url" :src="result.guest_photo_url" alt="Guest" class="guest-photo" />
      </div>
      
      <div v-else class="error-details">
        <p class="error-reason">{{ result?.reason }}</p>
      </div>
      
      <div class="action-buttons">
        <button 
          v-if="result?.is_valid" 
          @click="checkIn" 
          class="btn btn-primary btn-large"
          :disabled="checkingIn"
        >
          {{ checkingIn ? 'Processing...' : 'Check In' }}
        </button>
        
        <button @click="goBack" class="btn btn-secondary btn-large">
          Back to Scanner
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import dayjs from 'dayjs'

const router = useRouter()
const route = useRoute()
const result = ref(null)
const checkingIn = ref(false)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const formatDate = (date) => {
  return dayjs(date).format('DD.MM.YYYY HH:mm')
}

const checkIn = async () => {
  checkingIn.value = true
  try {
    const token = localStorage.getItem('guard_token')
    const response = await fetch(`${API_URL}/api/scan/check-in`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ pass_id: route.params.passId })
    })
    
    const data = await response.json()
    console.log('Check-in result:', data)
    
    setTimeout(() => {
      goBack()
    }, 2000)
  } catch (error) {
    console.error('Check-in error:', error)
  } finally {
    checkingIn.value = false
  }
}

const goBack = () => {
  router.push('/')
}

onMounted(() => {
  // In a real app, fetch pass details from API
  // For now, use mock data
  result.value = {
    is_valid: true,
    status: 'ALLOWED',
    guest_name: 'John Doe',
    guest_company: 'Tech Corp',
    valid_until: new Date().toISOString(),
    pass_id: route.params.passId
  }
})
</script>

<style scoped>
.result-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 1rem;
  transition: background-color 0.3s;
}

.result-container.ALLOWED {
  background: linear-gradient(135deg, #27ae60, #229954);
}

.result-container.DENIED {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
}

.result-content {
  text-align: center;
  background-color: rgba(0, 0, 0, 0.3);
  padding: 2rem;
  border-radius: 12px;
}

.status-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.icon-success {
  color: #27ae60;
}

.icon-error {
  color: #e74c3c;
}

.status-title {
  font-size: 2.5rem;
  margin: 1rem 0;
  color: #27ae60;
}

.status-title-error {
  font-size: 2.5rem;
  margin: 1rem 0;
  color: #e74c3c;
}

.pass-details {
  margin: 2rem 0;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 8px;
}

.guest-name {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.guest-company {
  font-size: 1.125rem;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.valid-until {
  font-size: 0.875rem;
  opacity: 0.7;
}

.guest-photo {
  width: 150px;
  height: 150px;
  border-radius: 8px;
  margin-top: 1rem;
  object-fit: cover;
}

.error-details {
  margin: 2rem 0;
}

.error-reason {
  font-size: 1.25rem;
  font-weight: bold;
  color: #fff;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  flex-direction: column;
}

.btn-large {
  padding: 1.25rem;
  font-size: 1.125rem;
}
</style>
