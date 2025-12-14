<template>
  <div class="portal-container">
    <div class="portal-card">
      <div v-if="!passCreated" class="request-form">
        <h1>🃄 Request Access Pass</h1>
        <p class="subtitle">Fill in your details to get a digital access pass</p>
        
        <form @submit.prevent="requestPass">
          <div class="form-group">
            <label for="name">Full Name *</label>
            <input 
              id="name" 
              v-model="formData.guest_name" 
              type="text" 
              required
              placeholder="John Doe"
            />
          </div>
          
          <div class="form-group">
            <label for="company">Company</label>
            <input 
              id="company" 
              v-model="formData.guest_company" 
              type="text" 
              placeholder="Tech Corp"
            />
          </div>
          
          <div class="form-group">
            <label for="phone">Phone Number *</label>
            <input 
              id="phone" 
              v-model="formData.guest_phone" 
              type="tel" 
              required
              placeholder="+1234567890"
            />
          </div>
          
          <div class="form-group">
            <label for="email">Email *</label>
            <input 
              id="email" 
              v-model="formData.guest_email" 
              type="email" 
              required
              placeholder="john@example.com"
            />
          </div>
          
          <div class="form-group">
            <label for="duration">Duration (hours) *</label>
            <input 
              id="duration" 
              v-model.number="duration" 
              type="number" 
              min="1" 
              max="24" 
              required
              placeholder="8"
            />
          </div>
          
          <div v-if="error" class="alert alert-error">{{ error }}</div>
          
          <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
            {{ loading ? 'Processing...' : 'Request Pass' }}
          </button>
        </form>
      </div>
      
      <div v-else class="pass-display">
        <h1>✅ Pass Created!</h1>
        
        <div class="pass-info">
          <p><strong>Name:</strong> {{ formData.guest_name }}</p>
          <p v-if="formData.guest_company"><strong>Company:</strong> {{ formData.guest_company }}</p>
          <p><strong>Phone:</strong> {{ formData.guest_email }}</p>
          <p><strong>Valid for:</strong> {{ duration }} hours</p>
        </div>
        
        <div class="qr-code-container">
          <h2>Your QR Code</h2>
          <div ref="qrCodeElement" class="qr-code"></div>
          <p class="qr-hint">Show this QR code to the guard at the entrance</p>
        </div>
        
        <div class="notification-info">
          <p>📧 Pass details have been sent to:</p>
          <p><strong>{{ formData.guest_email }}</strong></p>
          <p class="small">Check your email for the full pass information</p>
        </div>
        
        <button @click="requestNewPass" class="btn btn-primary btn-full">
          Request Another Pass
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import QRCode from 'qrcode'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const formData = ref({
  guest_name: '',
  guest_company: '',
  guest_phone: '',
  guest_email: ''
})

const duration = ref(8)
const loading = ref(false)
const error = ref('')
const passCreated = ref(false)
const qrCodeElement = ref(null)
const passQRCode = ref('')

const requestPass = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Calculate validity dates
    const now = new Date()
    const validUntil = new Date(now.getTime() + duration.value * 60 * 60 * 1000)
    
    const response = await axios.post(`${API_URL}/api/passes/create`, {
      ...formData.value,
      valid_from: now.toISOString(),
      valid_until: validUntil.toISOString()
    })
    
    passQRCode.value = response.data.qr_code
    passCreated.value = true
    
    // Generate QR code
    setTimeout(() => {
      if (qrCodeElement.value) {
        QRCode.toCanvas(qrCodeElement.value, passQRCode.value, { width: 300 })
      }
    }, 100)
    
    console.log('[NOTIFICATION] Pass created and sent to email')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to create pass'
  } finally {
    loading.value = false
  }
}

const requestNewPass = () => {
  formData.value = {
    guest_name: '',
    guest_company: '',
    guest_phone: '',
    guest_email: ''
  }
  duration.value = 8
  error.value = ''
  passCreated.value = false
}
</script>

<style scoped>
.portal-container {
  width: 100%;
  padding: 1rem;
}

.portal-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
}

.request-form h1,
.pass-display h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  color: #7f8c8d;
  text-align: center;
  margin-bottom: 2rem;
}

.btn-full {
  width: 100%;
  margin-top: 1.5rem;
}

.pass-info {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border-left: 4px solid #3498db;
}

.pass-info p {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.qr-code-container {
  text-align: center;
  margin: 2rem 0;
  padding: 2rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.qr-code-container h2 {
  font-size: 1.125rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.qr-code {
  display: inline-block;
  padding: 1rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.qr-hint {
  margin-top: 1rem;
  color: #7f8c8d;
  font-size: 0.875rem;
}

.notification-info {
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
  color: #155724;
}

.notification-info p {
  margin-bottom: 0.5rem;
}

.small {
  font-size: 0.875rem;
  opacity: 0.8;
}
</style>
