<template>
  <div class="audit-container">
    <h1>Visits Log</h1>
    
    <div class="filter-bar">
      <input 
        v-model="dateFilter" 
        type="date" 
        class="filter-input"
        @change="loadAuditLog"
      >
      <button @click="loadAuditLog" class="btn-refresh">Refresh</button>
    </div>

    <table class="audit-table">
      <thead>
        <tr>
          <th>Time</th>
          <th>Guest Name</th>
          <th>Guest Company</th>
          <th>Pass ID</th>
          <th>Guard</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in auditLogs" :key="log.id">
          <td>{{ formatDate(log.visit_time) }}</td>
          <td>{{ log.guest_name }}</td>
          <td>{{ log.guest_company }}</td>
          <td class="pass-id">{{ log.pass_uuid }}</td>
          <td>{{ log.guard_username }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="auditLogs.length === 0" class="empty-state">
      <p>No visits recorded yet</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '../services/api'

const auditLogs = ref([])
const dateFilter = ref('')

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
    if (dateFilter.value) {
      params.date = dateFilter.value
    }
    
    const response = await apiClient.get('/api/visits/log', {
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

.filter-input {
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

.pass-id {
  font-family: monospace;
  font-size: 12px;
  color: #666;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-state p {
  margin: 0;
}
</style>
