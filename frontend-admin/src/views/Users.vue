<template>
  <div class="users-container">
    <h1>User Management</h1>
    
    <div class="search-bar">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="Search by username or email"
        @keyup.enter="searchUsers"
      >
      <button @click="searchUsers" class="btn-search">Search</button>
      <button @click="loadUsers" class="btn-refresh">Refresh</button>
    </div>

    <table class="users-table">
      <thead>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Full Name</th>
          <th>Role</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.full_name }}</td>
          <td><span class="badge">{{ user.role }}</span></td>
          <td>
            <span :class="['status', user.is_active ? 'active' : 'inactive']">
              {{ user.is_active ? 'Active' : 'Inactive' }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '../services/api'

const users = ref([])
const searchQuery = ref('')

const loadUsers = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      console.warn('No token found')
      return
    }
    
    const response = await apiClient.get('/api/admin/users', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    users.value = response.data
    console.log('Users loaded:', users.value)
  } catch (error) {
    console.error('Failed to load users:', error)
  }
}

const searchUsers = async () => {
  if (!searchQuery.value) {
    loadUsers()
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    
    const response = await apiClient.get('/api/admin/users/search', {
      params: {
        query: searchQuery.value
      },
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    users.value = response.data
  } catch (error) {
    console.error('Search failed:', error)
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.users-container {
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

.users-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

.users-table th {
  background: #f8f9fa;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
}

.users-table td {
  padding: 15px;
  border-bottom: 1px solid #dee2e6;
}

.users-table tbody tr:hover {
  background: #f8f9fa;
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  background: #007bff;
  color: white;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
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
</style>
