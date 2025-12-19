<template>
  <div class="passes-container">
    <h1>Pass Management</h1>
    
    <div class="search-bar">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Search by name or ID"
        @keyup.enter="searchPasses"
      >
      <button @click="searchPasses" class="btn-search">Search</button>
      <button @click="loadPasses" class="btn-refresh">Refresh</button>
    </div>

    <table class="passes-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Guest Name</th>
          <th>Company</th>
          <th>Valid From</th>
          <th>Valid Until</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="pass in passes" :key="pass.id" @click="viewPass(pass)">
          <td>{{ pass.uuid }}</td>
          <td>{{ pass.guest_name }}</td>
          <td>{{ pass.guest_company }}</td>
          <td>{{ formatDate(pass.valid_from) }}</td>
          <td>{{ formatDate(pass.valid_until) }}</td>
          <td>
            <span :class="['status', pass.is_active ? 'active' : 'inactive']">
              {{ pass.is_active ? 'Active' : 'Inactive' }}
            </span>
          </td>
          <td>
            <button @click="editPass(pass)" class="btn-edit">Edit</button>
            <button @click="deletePass(pass.id)" class="btn-delete">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- View Modal -->
    <div v-if="viewingPass" class="modal-overlay" @click="closeViewModal">
      <div class="modal-content" @click.stop>
        <h2>Pass Details</h2>
        <p><strong>ID:</strong> {{ viewingPass.uuid }}</p>
        <p><strong>Guest Name:</strong> {{ viewingPass.guest_name }}</p>
        <p><strong>Company:</strong> {{ viewingPass.guest_company }}</p>
        <p><strong>Phone:</strong> {{ viewingPass.guest_phone }}</p>
        <p><strong>Email:</strong> {{ viewingPass.guest_email }}</p>
        <p><strong>Valid from:</strong> {{ formatDate(viewingPass.valid_from) }}</p>
        <p><strong>Valid until:</strong> {{ formatDate(viewingPass.valid_until) }}</p>
        
        <div class="card-actions">
          <button @click="editPass(viewingPass)" class="btn-edit">Edit</button>
          <button @click="deletePass(viewingPass.id)" class="btn-delete">Delete</button>
          <button @click="openEmailModal(viewingPass)" class="btn-email">Send Email</button>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="editingPass" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <h2>Edit Pass</h2>
        <form @submit.prevent="updatePass">
          <div class="form-group">
            <label>Guest Name</label>
            <input v-model="editingPass.guest_name" type="text">
          </div>
          <div class="form-group">
            <label>Company</label>
            <input v-model="editingPass.guest_company" type="text">
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input v-model="editingPass.guest_phone" type="text">
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="editingPass.guest_email" type="text">
          </div>
          <div class="form-group">
            <label>Valid Until</label>
            <input v-model="editingPass.valid_until" type="datetime-local">
          </div>
          <div class="form-group">
            <label class="toggle-label">
              <input v-model="editingPass.is_active" type="checkbox" class="toggle-input">
              <span class="toggle-slider"></span>
              Active
            </label>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-primary">Save</button>
            <button type="button" @click="closeEditModal" class="btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Email Modal -->
    <div v-if="emailPass" class="modal-overlay" @click="closeEmailModal">
      <div class="modal-content" @click.stop>
        <h2>Send Email to {{ emailPass.guest_name }}</h2>
        
        <div class="form-group">
          <label>To:</label>
          <input :value="emailPass.guest_email" type="email" disabled>
        </div>
        
        <div class="form-group">
          <label>Message:</label>
          <textarea 
            v-model="emailMessage" 
            placeholder="Enter your message here..."
            rows="6"
          ></textarea>
        </div>
        
        <div class="form-actions">
          <button 
            @click="sendEmail" 
            class="btn-primary"
            :disabled="emailLoading"
          >
            {{ emailLoading ? 'Sending...' : 'Send Email' }}
          </button>
          <button 
            type="button" 
            @click="closeEmailModal" 
            class="btn-secondary"
            :disabled="emailLoading"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '../services/api'

const passes = ref([])
const searchQuery = ref('')
const editingPass = ref(null)
const viewingPass = ref(null)
const emailPass = ref(null)
const emailMessage = ref('')
const emailLoading = ref(false)

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString()
}

const viewPass = (pass) => {
  viewingPass.value = { ...pass }
}

const closeViewModal = () => {
  viewingPass.value = null
}

const loadPasses = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      console.warn('No token found')
      return
    }
    
    const response = await apiClient.get('/api/passes/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    passes.value = response.data
    console.log('Passes loaded:', passes.value)
  } catch (error) {
    console.error('Failed to load passes:', error)
  }
}

const searchPasses = async () => {
  if (!searchQuery.value) {
    loadPasses()
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    
    const response = await apiClient.get('/api/passes/search', {
      params: {
        name: searchQuery.value,
        skip: 0,
        limit: 100
      },
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    passes.value = response.data
  } catch (error) {
    console.error('Search failed:', error)
  }
}

const editPass = (pass) => {
  closeViewModal()
  editingPass.value = { ...pass }
  console.log('Edit pass:', editingPass.value)
}

const closeEditModal = () => {
  closeViewModal()
  editingPass.value = null
}

const updatePass = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    
    const passId = editingPass.value.id
    const response = await apiClient.put(`/api/passes/${passId}`, editingPass.value, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    console.log('Pass updated:', response.data)
    closeEditModal()
    loadPasses()
  } catch (error) {
    console.error('Update failed:', error)
    alert('Failed to update pass: ' + (error.response?.data?.detail || error.message))
  }
}

const deletePass = async (passId) => {
  if (!confirm('Are you sure you want to delete this pass?')) {
    return
  }
  closeViewModal()
  
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    
    const response = await apiClient.delete(`/api/passes/${passId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    console.log('Pass deleted:', response.data)
    loadPasses()
  } catch (error) {
    console.error('Delete failed:', error)
    alert('Failed to delete pass: ' + (error.response?.data?.detail || error.message))
  }
}

const openEmailModal = (pass) => {
  emailPass.value = pass
  emailMessage.value = ''  // Очистить предыдущее письмо
  closeViewModal()  // Закрыть карточку
}

const closeEmailModal = () => {
  emailPass.value = null
  emailMessage.value = ''
}

const sendEmail = async () => {
  if (!emailMessage.value.trim()) {
    alert('Please enter a message')
    return
  }
  
  try {
    emailLoading.value = true
    const token = localStorage.getItem('token')
    
    const response = await apiClient.post(
      `/api/passes/${emailPass.value.id}/send-email`,
      {
        message: emailMessage.value,
        recipient_email: emailPass.value.guest_email
      },
      {
        headers: { 'Authorization': `Bearer ${token}` }
      }
    )
    
    console.log('Email sent:', response.data)
    alert('Email sent successfully!')
    closeEmailModal()
  } catch (error) {
    console.error('Failed to send email:', error)
    alert('Failed to send email: ' + (error.response?.data?.detail || error.message))
  } finally {
    emailLoading.value = false
  }
}

onMounted(() => {
  loadPasses()
})
</script>

<style scoped>
.passes-container {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.search-bar input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn-search, .btn-refresh {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-search:hover, .btn-refresh:hover {
  background: #0056b3;
}

.passes-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

.passes-table th {
  background: #f8f9fa;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
}

.passes-table td {
  padding: 15px;
  border-bottom: 1px solid #dee2e6;
}

.passes-table tbody tr:hover {
  background: #f8f9fa;
}

.status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status.active {
  background: #d4edda;
  color: #155724;
}

.status.inactive {
  background: #f8d7da;
  color: #721c24;
}

.btn-edit, .btn-delete {
  padding: 6px 12px;
  margin-right: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.btn-edit {
  background: #28a745;
  color: white;
}

.btn-edit:hover {
  background: #218838;
}

.btn-delete {
  background: #dc3545;
  color: white;
}

.btn-delete:hover {
  background: #c82333;
}

.btn-email {
  background: #17a2b8;
  color: white;
  padding: 6px 12px;
  margin-right: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.btn-email:hover {
  background: #138496;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
}

.modal-content h2 {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-group input[type="text"],
.form-group input[type="datetime-local"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;
}

.toggle-input {
  appearance: none;
  -webkit-appearance: none;
  width: 50px;
  height: 26px;
  background: #ccc;
  border: none;
  border-radius: 13px;
  cursor: pointer;
  transition: background 0.3s ease;
  position: relative;
}

.toggle-input::before {
  content: '';
  position: absolute;
  width: 22px;
  height: 22px;
  background: white;
  border-radius: 50%;
  top: 2px;
  left: 2px;
  transition: left 0.3s ease;
}

.toggle-input:checked {
  background: #28a745;
}

.toggle-input:checked::before {
  left: 26px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn-primary, .btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  resize: vertical;
}

.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

</style>
