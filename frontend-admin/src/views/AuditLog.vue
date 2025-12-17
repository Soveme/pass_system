<template>
  <div class="audit-container">
    <h1>Audit Log</h1>
    
    <div class="filter-bar">
      <select v-model="filterType" @change="loadAuditLog" class="filter-select">
        <option value="">All Events</option>
        <option value="login">Login</option>
        <option value="pass_created">Pass Created</option>
        <option value="pass_deleted">Pass Deleted</option>
        <option value="scan">Scan</option>
      </select>
      <button @click="loadAuditLog" class="btn-refresh">Refresh</button>
    </div>

    <table class="audit-table">
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>User</th>
          <th>Action</th>
          <th>Details</th>
          <th>IP Address</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in auditLogs" :key="log.id">
          <td>{{ formatDate(log.timestamp) }}</td>
          <td>{{ log.user_id }}</td>
          <td><span class="badge" :class="log.action">{{ log.action }}</span></td>
          <td>{{ log.details }}</td>
          <td>{{ log.ip_address }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '../services/api'

const auditLogs = ref([])
const filterType = ref('')

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString()
}

const loadAuditLog = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      console.warn('No token found')
      return
    }
    
    const params = {}
    if (filterType.value) {
      params.action = filterType.value
    }
    
    const response = await apiClient.get('/api/admin/audit-log', {
      params,
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    auditLogs.value = response.data
    console.log('Audit logs loaded:', auditLogs.value)
  } catch (error) {
    console.error('Failed to load audit logs:', error)
  }
}

onMounted(() => {
  loadAuditLog()
})
</script>

<style scoped>
.audit-container {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.filter-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.filter-select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex: 1;
  max-width: 200px;
}

.btn-refresh {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-refresh:hover {
  background: #0056b3;
}

.audit-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

.audit-table th {
  background: #f8f9fa;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
}

.audit-table td {
  padding: 15px;
  border-bottom: 1px solid #dee2e6;
  word-break: break-word;
}

.audit-table tbody tr:hover {
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

.badge.login {
  background: #28a745;
}

.badge.pass_created {
  background: #17a2b8;
}

.badge.pass_deleted {
  background: #dc3545;
}

.badge.scan {
  background: #ffc107;
  color: #333;
}
</style>
