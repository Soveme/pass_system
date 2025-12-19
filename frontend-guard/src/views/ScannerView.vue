<template>
  <div class="scanner-container">
    <div class="header">
      <h1>Pass Scanner</h1>
      <div class="user-info" v-if="currentUser">
        <span>{{ currentUser.username }}</span>
        <button @click="logout" class="btn-logout">Logout</button>
      </div>
    </div>
    
    <div v-if="!isAuthenticated" class="login-prompt">
      <p>Please login first to scan passes</p>
      <button @click="goToLogin" class="btn-login">Go to Login</button>
    </div>

    <div v-if="isAuthenticated" class="scanner-content">
      <div class="camera-section">
        <video ref="videoElement" class="video-preview"></video>
        <canvas ref="canvasElement" style="display: none"></canvas>
      </div>

      <div class="scanner-controls">
        <button @click="startScanning" class="btn-start">Start Camera</button>
        <button @click="stopScanning" class="btn-stop">Stop Camera</button>
      </div>

      <div class="manual-scan">
        <h3>Manual QR Code</h3>
        <input 
          v-model="manualQrCode" 
          type="text" 
          placeholder="Paste QR code text here"
          @keyup.enter="submitManualQR"
        >
        <button @click="submitManualQR" class="btn-submit">Submit</button>
      </div>

      <div class="scan-result" v-if="scanResult && !isScanning">
        <div v-if="scanResult && !isScanning" class="pass-details-card">
          <div class="pass-header">
            <h2>{{ scanResult.guest_name }}</h2>
          </div>
          
          <div class="pass-validity">
            <p><strong>Действителен до:</strong></p>
            <p class="time">{{ formatDate(scanResult.valid_until) }}</p>
          </div>
          
          <div :class="['status-badge', scanResult.status]">
            {{ scanResult.status === 'ALLOWED' ? '✅ РАЗРЕШЁН' : scanResult.status === 'EXIT' ? '🚪 ВЫШЕЛ' : '❌ ЗАПРЕЩЁН' }}
          </div>
          
          <button @click="resetScan" class="btn-new-scan">Scan Another</button>
        </div>
      </div>

      <div class="last-scan" v-if="lastScan">
        <h3>Last Scan</h3>
        <p>{{ lastScan }}</p>
      </div>

      <div class="scan-result" v-if="scanResult">
        <h3>Scan Result</h3>
        <div :class="['result-box', scanResult.status]">
          <p><strong>Status:</strong> {{ scanResult.status }}</p>
          <p v-if="scanResult.guest_name"><strong>Guest:</strong> {{ scanResult.guest_name }}</p>
          <p v-if="scanResult.message"><strong>Message:</strong> {{ scanResult.message }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import jsQR from 'jsqr'
import { apiClient } from '../services/api'

const videoElement = ref(null)
const canvasElement = ref(null)
const manualQrCode = ref('')
const lastScan = ref('')
const scanResult = ref(null)
const currentUser = ref(null)
const isScanning = ref(false)
let scanningInterval = null

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token') && !!currentUser.value
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString()
}

const checkAuth = () => {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  
  if (token && user) {
    try {
      currentUser.value = JSON.parse(user)
      console.log('User authenticated:', currentUser.value)
    } catch (e) {
      console.error('Failed to parse user:', e)
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  currentUser.value = null
  stopScanning()
}

const goToLogin = () => {
  window.location.href = '/login'
}

const startScanning = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: 'environment' } 
    })
    
    videoElement.value.srcObject = stream
    videoElement.value.play()
    
    // Start continuous scanning
    scanningInterval = setInterval(() => {
      captureFrame()
    }, 500)
    
    console.log('Camera started')
  } catch (error) {
    console.error('Camera access denied:', error)
    alert('Unable to access camera. Please check permissions.')
  }
}

const stopScanning = () => {
  if (scanningInterval) {
    clearInterval(scanningInterval)
  }
  
  if (videoElement.value?.srcObject) {
    videoElement.value.srcObject.getTracks().forEach(track => track.stop())
  }
  
  console.log('Camera stopped')
}

const captureFrame = () => {
  if (!videoElement.value || !canvasElement.value) return
  
  try {
    const ctx = canvasElement.value.getContext('2d')
    canvasElement.value.width = videoElement.value.videoWidth
    canvasElement.value.height = videoElement.value.videoHeight
    ctx.drawImage(videoElement.value, 0, 0)
    
    // ✨ Сканируем QR
    const imageData = ctx.getImageData(0, 0, canvasElement.value.width, canvasElement.value.height)
    const code = jsQR(imageData.data, imageData.width, imageData.height)
    
    if (code) {
      isScanning.value = true
      console.log('✅ QR найден:', code.data)
      manualQrCode.value = code.data
      lastScan.value = `Scanning: ${code.data}`
      stopScanning()
      submitManualQR()
    }
  } catch (error) {
    console.error('Frame capture error:', error)
  }
}

const submitManualQR = async () => {
  if (!manualQrCode.value.trim()) {
    alert('Please enter a QR code')
    return
  }
  
  lastScan.value = `Scanning: ${manualQrCode.value}`
  
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      alert('Please login first')
      goToLogin()
      return
    }
    
    // Send to backend for verification
    const response = await apiClient.post('/api/scan/verify', 
      {
        qr_code: manualQrCode.value
      },
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )
    
    scanResult.value = response.data
    isScanning.value = false
    console.log('Scan verified:', response.data)
    
    // Clear input
    manualQrCode.value = ''
  } catch (error) {
    console.error('Verification failed:', error)
    
    // Show error details
    if (error.response?.data) {
      scanResult.value = {
        status: 'error',
        message: error.response.data.detail || JSON.stringify(error.response.data)
      }
    } else if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      currentUser.value = null
      alert('Session expired. Please login again.')
      goToLogin()
    } else {
      scanResult.value = {
        status: 'error',
        message: error.message || 'Verification failed'
      }
    }
  }
}

const resetScan = () => {
  scanResult.value = null
  manualQrCode.value = ''
  lastScan.value = ''
  isScanning.value = false
}

onMounted(() => {
  console.log('Scanner view mounted')
  checkAuth()
  
  if (!isAuthenticated.value) {
    goToLogin()
  }
})

onUnmounted(() => {
  stopScanning()
})
</script>

<style scoped>
.scanner-container {
  max-height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
  scroll-behavior: smooth;
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

.scanner-container::-webkit-scrollbar {
  width: 8px;
}

.scanner-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.scanner-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.scanner-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  margin: 0;
  font-size: 24px;
}

.user-info {
  display: flex;
  gap: 10px;
  align-items: center;
}

.user-info span {
  font-size: 14px;
  color: #666;
}

.btn-logout {
  padding: 8px 16px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.btn-logout:hover {
  background: #c82333;
}

.login-prompt {
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

.login-prompt p {
  margin-bottom: 15px;
  color: #856404;
}

.btn-login {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-login:hover {
  background: #0056b3;
}

.scanner-content {
  display: block;
}

.camera-section {
  margin-bottom: 20px;
  background: #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
}

.video-preview {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  background: #000;
}

.scanner-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.btn-start, .btn-stop {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  color: white;
}

.btn-start {
  background: #28a745;
}

.btn-start:hover {
  background: #218838;
}

.btn-stop {
  background: #dc3545;
}

.btn-stop:hover {
  background: #c82333;
}

.manual-scan {
  background: #1a1a1a;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.manual-scan h3 {
  margin-bottom: 15px;
}

.manual-scan input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
  box-sizing: border-box;
  font-family: monospace;
}

.btn-submit {
  width: 100%;
  padding: 12px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-submit:hover {
  background: #0056b3;
}

.last-scan {
  background: #1a1a1a;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.last-scan h3 {
  margin-bottom: 10px;
}

.last-scan p {
  margin: 0;
  word-break: break-all;
  font-family: monospace;
  color: #666;
}

.scan-result {
  background: #191919;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.scan-result h3 {
  margin-bottom: 15px;
}

.result-box {
  padding: 15px;
  border-radius: 4px;
  border-left: 4px solid #007bff;
}

.result-box.success {
  background: #d4edda;
  border-left-color: #28a745;
  color: #155724;
}

.result-box.error {
  background: #f8d7da;
  border-left-color: #dc3545;
  color: #721c24;
}

.result-box.invalid {
  background: #fff3cd;
  border-left-color: #ffc107;
  color: #856404;
}

.result-box p {
  margin: 5px 0;
}

.result-box strong {
  font-weight: 600;
}

.pass-details-card {
  background: #181a1b;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  text-align: center;
  margin-top: 20px;
  animation: slideUp 0.3s ease-out;
}

.pass-header h2 {
  font-size: 28px;
  margin: 0 0 20px 0;
  color: #c8c3bc;
}

.pass-validity {
  margin: 20px 0;
  background: #1e2021;
  padding: 15px;
  border-radius: 8px;
}

.pass-validity p {
  margin: 5px 0;
}

.pass-validity .time {
  font-size: 20px;
  font-weight: 600;
  color: #007bff;
}

.status-badge {
  font-size: 48px;
  font-weight: bold;
  padding: 20px;
  border-radius: 10px;
  margin: 20px 0;
  animation: pulse 0.5s ease-out;
}

.status-badge.valid {
  background: #d4edda;
  color: #155724;
}

.status-badge.expired {
  background: #fff3cd;
  color: #856404;
}

.status-badge.invalid {
  background: #f8d7da;
  color: #721c24;
}

.btn-new-scan {
  padding: 12px 24px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}
</style>
