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
        <tr v-for="pass in passes" :key="pass.id">
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
            <label>Valid Until</label>
            <input v-model="editingPass.valid_until" type="datetime-local">
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-primary">Save</button>
            <button type="button" @click="closeEditModal" class="btn-secondary">Cancel</button>
          </div>
        </form>
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

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString()
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
    
    const response = await apiClient.get('/api/admin/passes/search', {
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
  editingPass.value = { ...pass }
  console.log('Edit pass:', editingPass.value)
}

const closeEditModal = () => {
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
  }
}

const deletePass = async (passId) => {
  if (!confirm('Are you sure you want to delete this pass?')) {
    return
  }
  
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

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
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
</style>
