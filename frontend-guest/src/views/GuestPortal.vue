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
          <div class="form-group checkbox-group">
            <label for="privacy">
              <input 
                id="privacy" 
                v-model="formData.agreedToPrivacy" 
                type="checkbox" 
                required
              />
              <span>
                I agree to the processing of my personal data according to the 
                <button type="button" @click.prevent="openPrivacyModal" class="link-btn">
                  Privacy Policy
                </button> *
              </span>
            </label>
          </div>

          <div v-if="error" class="alert alert-error">{{ error }}</div>
          
          <button type="submit" class="btn btn-primary btn-full" :disabled="loading">
            {{ loading ? 'Processing...' : 'Request Pass' }}
          </button>
        </form>

        <div v-if="showPrivacyModal" class="privacy-modal-overlay" @click="closePrivacyModal">
          <div class="privacy-modal" @click.stop>
            <div class="modal-header">
              <h2>Privacy Policy & Data Processing Agreement</h2>
              <button @click="closePrivacyModal" class="btn-close">✕</button>
            </div>
            
            <div class="modal-body">
              <section>
                <h3>1. Data Collection</h3>
                <p>We collect the following personal information:</p>
                <ul>
                  <li>Full Name</li>
                  <li>Email Address</li>
                  <li>Phone Number</li>
                  <li>Company Name</li>
                </ul>
              </section>
              
              <section>
                <h3>2. Purpose of Processing</h3>
                <p>Your data is processed for the following purposes:</p>
                <ul>
                  <li>Issuing access passes</li>
                  <li>Security and access control</li>
                  <li>Communication regarding your pass</li>
                  <li>Compliance with regulations</li>
                </ul>
              </section>
              
              <section>
                <h3>3. Data Storage</h3>
                <p>Your data will be stored for 30 days from the date of pass creation, after which it will be securely deleted.</p>
              </section>
              
              <section>
                <h3>4. Data Security</h3>
                <p>We use industry-standard encryption and security measures to protect your personal data.</p>
              </section>
              
              <section>
                <h3>5. Your Rights</h3>
                <p>You have the right to:</p>
                <ul>
                  <li>Access your personal data</li>
                  <li>Request correction of inaccurate data</li>
                  <li>Request deletion of your data</li>
                  <li>Withdraw your consent at any time</li>
                </ul>
              </section>
              
              <section>
                <h3>6. Contact</h3>
                <p>For privacy questions, contact: privacy@company.com</p>
              </section>
            </div>
            
            <div class="modal-footer">
              <button @click="closePrivacyModal" class="btn btn-secondary">Close</button>
              <button @click="acceptPrivacy" class="btn btn-primary">I Agree & Accept</button>
            </div>
          </div>
        </div>

      </div>
      
      <div v-if="passCreated" class="pass-display">
        <h1>✅ Pass Created!</h1>
        
        <div class="pass-info">
          <p><strong>Name:</strong> {{ formData.guest_name }}</p>
          <p v-if="formData.guest_company"><strong>Company:</strong> {{ formData.guest_company }}</p>
          <p><strong>Phone:</strong> {{ formData.guest_email }}</p>
          <p><strong>Valid for:</strong> {{ duration }} hours</p>
        </div>
        
        <div class="qr-code-container">
          <h2>Your QR Code</h2>
          <canvas ref="qrCanvas" class="qr-code"></canvas>
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
import { ref, nextTick } from 'vue'
import axios from 'axios'
import QRCode from 'qrcode'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const formData = ref({
  guest_name: '',
  guest_company: '',
  guest_phone: '',
  guest_email: '',
  agreedToPrivacy: false
})

const duration = ref(8)
const loading = ref(false)
const error = ref('')
const passCreated = ref(false)
const qrCanvas = ref(null)
const passQRCode = ref('')

const requestPass = async () => {
  if (!formData.value.agreedToPrivacy) {
    error.value = 'You must agree to the Privacy Policy'
    return
  }
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
    await nextTick()
    // Generate QR code
    
    QRCode.toCanvas(qrCanvas.value, passQRCode.value, {
      width: 300,
      errorCorrectionLevel: 'H',
      type: 'image/png'
    })
    
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

const showPrivacyModal = ref(false)

const openPrivacyModal = () => {
  showPrivacyModal.value = true
}

const closePrivacyModal = () => {
  showPrivacyModal.value = false
}

const acceptPrivacy = () => {
  formData.value.agreedToPrivacy = true
  closePrivacyModal()
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

.checkbox-group {
  margin: 1.5rem 0 1rem 0;
  display: flex;
  align-items: flex-start;
}

.checkbox-group label {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  cursor: pointer;
  color: #555;
  font-size: 0.95rem;
  line-height: 1.4;
}

.checkbox-group input[type="checkbox"] {
  margin-top: 0.25rem;
  cursor: pointer;
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.checkbox-group a {
  color: #3498db;
  text-decoration: none;
  border-bottom: 1px solid #3498db;
}

.checkbox-group a:hover {
  color: #2980b9;
}

.privacy-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.privacy-modal {
  background-color: white;
  border-radius: 12px;
  width: 100%;
  max-width: 700px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
}

.btn-close:hover {
  color: #2c3e50;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  color: #555;
  line-height: 1.6;
}

.modal-body section {
  margin-bottom: 1.5rem;
}

.modal-body section h3 {
  color: #2c3e50;
  margin-bottom: 0.75rem;
  font-size: 1.1rem;
}

.modal-body ul {
  margin-left: 1.5rem;
  color: #666;
}

.modal-body li {
  margin-bottom: 0.5rem;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding: 2rem;
  border-top: 1px solid #e0e0e0;
  background-color: #f8f9fa;
}

.link-btn {
  background: none;
  border: none;
  color: #3498db;
  text-decoration: underline;
  cursor: pointer;
  font-size: inherit;
  padding: 0;
  margin: 0;
}

.link-btn:hover {
  color: #2980b9;
}

@media (max-width: 600px) {
  .privacy-modal {
    max-height: 95vh;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1.5rem;
  }
}

</style>
