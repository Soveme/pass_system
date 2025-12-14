<template>
  <div class="scanner-container">
    <div class="scanner-header">
      <h1>QR Scanner</h1>
      <button @click="logout" class="btn-logout">Logout</button>
    </div>
    
    <div class="scanner-area">
      <div id="reader" class="qr-reader"></div>
      <div v-if="manualMode" class="manual-input">
        <input 
          v-model="manualQRCode" 
          type="text" 
          placeholder="Or enter QR code manually"
          @keyup.enter="submitManualCode"
          class="form-input"
        />
        <button @click="submitManualCode" class="btn btn-primary">Submit</button>
      </div>
    </div>
    
    <div class="scanner-footer">
      <button @click="toggleManualInput" class="btn btn-secondary">
        {{ manualMode ? 'Use Camera' : 'Manual Input' }}
      </button>
      <button @click="switchCamera" class="btn btn-secondary">Switch Camera</button>
    </div>
    
    <div v-if="lastScan" class="last-scan-info">
      <p><strong>Last Scan:</strong> {{ lastScan }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Html5QrcodeScanner } from 'html5-qrcode'

const router = useRouter()
const manualMode = ref(false)
const manualQRCode = ref('')
const lastScan = ref('')
let scanner = null

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const logout = () => {
  localStorage.removeItem('guard_token')
  router.push('/login')
}

const toggleManualInput = () => {
  manualMode.value = !manualMode.value
}

const switchCamera = () => {
  console.log('Switch camera')
}

const submitManualCode = async () => {
  if (!manualQRCode.value) return
  
  await processQRCode(manualQRCode.value)
  manualQRCode.value = ''
}

const processQRCode = async (qrCode) => {
  try {
    lastScan.value = `Scanning: ${qrCode.substring(0, 8)}...`
    
    // Send to API
    const token = localStorage.getItem('guard_token')
    const response = await fetch(`${API_URL}/api/scan/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ qr_code: qrCode })
    })
    
    const data = await response.json()
    
    if (data.is_valid) {
      router.push(`/result/${data.pass_id}`)
    } else {
      console.log('Invalid pass:', data.reason)
    }
  } catch (error) {
    console.error('Scan error:', error)
    lastScan.value = 'Error scanning QR code'
  }
}

const onScanSuccess = (decodedText) => {
  processQRCode(decodedText)
}

const onScanError = (error) => {
  // Ignore errors from scanner
}

onMounted(() => {
  if (!manualMode.value) {
    try {
      scanner = new Html5QrcodeScanner(
        'reader',
        { fps: 10, qrbox: 250 },
        false
      )
      scanner.render(onScanSuccess, onScanError)
    } catch (error) {
      console.error('Failed to initialize scanner:', error)
    }
  }
})

onUnmounted(() => {
  if (scanner) {
    scanner.clear()
  }
})
</script>

<style scoped>
.scanner-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #1a1a1a;
}

.scanner-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #2a2a2a;
  border-bottom: 2px solid #27ae60;
}

.scanner-header h1 {
  font-size: 1.5rem;
}

.btn-logout {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.scanner-area {
  flex: 1;
  position: relative;
  background-color: #000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-reader {
  width: 100%;
  height: 100%;
}

.manual-input {
  position: absolute;
  bottom: 1rem;
  left: 1rem;
  right: 1rem;
  display: flex;
  gap: 0.5rem;
}

.form-input {
  flex: 1;
  padding: 1rem;
  background-color: #2a2a2a;
  border: 2px solid #27ae60;
  color: white;
  border-radius: 8px;
  font-size: 1rem;
}

.scanner-footer {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  background-color: #2a2a2a;
  border-top: 2px solid #27ae60;
}

.btn-secondary {
  flex: 1;
  background-color: #34495e;
  color: white;
}

.last-scan-info {
  padding: 1rem;
  background-color: #2a2a2a;
  border-top: 1px solid #444;
  color: #27ae60;
  font-weight: bold;
  text-align: center;
}
</style>
