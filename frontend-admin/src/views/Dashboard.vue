<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Total Passes</div>
        <div class="stat-value">{{ statistics.total_passes }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Active Passes</div>
        <div class="stat-value">{{ statistics.active_passes }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Today's Visits</div>
        <div class="stat-value">{{ statistics.today_visits }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Total Visits</div>
        <div class="stat-value">{{ statistics.total_visits }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiClient } from '../services/api'

const statistics = ref({
  total_passes: 0,
  active_passes: 0,
  today_visits: 0,
  total_visits: 0
})

const loadStatistics = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      console.warn('No token found')
      return
    }
    
    const response = await apiClient.get('/api/admin/statistics', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    statistics.value = response.data
    console.log('Statistics loaded:', statistics.value)
  } catch (error) {
    console.error('Failed to load statistics:', error)
  }
}

onMounted(() => {
  loadStatistics()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

h1 {
  margin-bottom: 30px;
  font-size: 28px;
  color: #333;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-left: 4px solid #007bff;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
  font-weight: 500;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #007bff;
}
</style>
