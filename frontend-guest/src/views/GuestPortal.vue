<template>
  <div class="guest-portal">
    <h1>Guest Pass Request</h1>
    
    <div v-if="!passCreated" class="form-section">
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label>Name</label>
          <input v-model="form.guest_name" type="text" required>
        </div>
        
        <div class="form-group">
          <label>Company</label>
          <input v-model="form.guest_company" type="text" required>
        </div>
        
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.guest_email" type="email" required>
        </div>
        
        <div class="form-group">
          <label>Phone</label>
          <input v-model="form.guest_phone" type="tel" required>
        </div>
        
        <div class="form-group">
          <label>Valid From</label>
          <input v-model="form.valid_from" type="datetime-local" required>
        </div>
        
        <div class="form-group">
          <label>Valid Until</label>
          <input v-model="form.valid_until" type="datetime-local" required>
        </div>
        
        <button type="submit" class="btn-submit">Request Pass</button>
      </form>
    </div>

    <div v-else class="success-section">
      <h2>Pass Created Successfully!</h2>
      <p>Your pass has been created and sent to your email and SMS.</p>
      
      <div class="qr-section">
        <h3>Your QR Code</h3>
        <div class="qr-container">
          <canvas ref="qrCanvas"></canvas>
        </div>
        <p class="qr-info">Please scan this QR code at the entrance.</p>
        <p class="pass-uuid">Pass ID: {{ passQrCode }}</p>
      </div>
      
      <button @click="resetForm" class="btn-new-pass">Request Another Pass</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { apiClient } from '../services/api'
import QRCode from 'qrcode'

const form = ref({
  guest_name: '',
  guest_company: '',
  guest_email: '',
  guest_phone: '',
  valid_from: '',
  valid_until: ''
})

const passCreated = ref(false)
const passQrCode = ref('')
const qrCanvas = ref(null)

const submitForm = async () => {
  try {
    // Create pass
    const response = await apiClient.post('/api/passes/create', form.value)
    
    console.log('[NOTIFICATION] Pass created and sent to email')
    console.log(response.data)
    
    // Get the QR code from response
    passQrCode.value = response.data.qr_code || response.data.uuid
    
    passCreated.value = true
    
    // Generate QR code
    setTimeout(() => {
      generateQRCode()
    }, 100)
  } catch (error) {
    console.error('Failed to create pass:', error)
    alert('Failed to create pass: ' + (error.response?.data?.detail || error.message))
  }
}

const generateQRCode = async () => {
  try {
    const canvas = qrCanvas.value
    
    if (!canvas) {
      console.error('Canvas element not found')
      return
    }
    
    console.log('Generating QR code for:', passQrCode.value)
    
    // Generate QR code directly to canvas
    await QRCode.toCanvas(canvas, passQrCode.value, {
      errorCorrectionLevel: 'H',
      type: 'image/png',
      quality: 0.95,
      margin: 1,
      width: 300,
      color: {
        dark: '#000000',
        light: '#ffffff'
      }
    })
    
    console.log('QR code generated successfully')
  } catch (error) {
    console.error('Failed to generate QR code:', error)
    console.error('Canvas element:', qrCanvas.value)
    console.error('Canvas type:', typeof qrCanvas.value)
  }
}

const resetForm = () => {
  form.value = {
    guest_name: '',
    guest_company: '',
    guest_email: '',
    guest_phone: '',
    valid_from: '',
    valid_until: ''
  }
  passCreated.value = false
  passQrCode.value = ''
}
</script>

<style scoped>
.guest-portal {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

h2 {
  color: #28a745;
  margin-bottom: 15px;
}

h3 {
  margin-bottom: 15px;
  color: #333;
}

.form-section {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
}

.btn-submit {
  width: 100%;
  padding: 14px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-submit:hover {
  background: #0056b3;
}

.success-section {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  text-align: center;
}

.success-section p {
  color: #666;
  margin-bottom: 15px;
}

.qr-section {
  margin: 30px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.qr-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
  min-height: 320px;
}

.qr-container canvas {
  max-width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  background: white;
}

.qr-info {
  font-size: 14px;
  color: #666;
  margin: 10px 0 0 0;
}

.pass-uuid {
  font-size: 12px;
  color: #999;
  margin: 10px 0 0 0;
  word-break: break-all;
  font-family: monospace;
}

.btn-new-pass {
  width: 100%;
  padding: 14px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 20px;
}

.btn-new-pass:hover {
  background: #218838;
}
</style>
