<template>
  <div class="dashboard">
    <h1>Панель управления</h1>
    
    <div class="stats-grid">
      <div class="stat-card">
        <h3>Активные пропуска</h3>
        <p class="stat-value">{{ stats.activePass }}</p>
      </div>
      <div class="stat-card">
        <h3>Всего пропусков</h3>
        <p class="stat-value">{{ stats.totalPasses }}</p>
      </div>
      <div class="stat-card">
        <h3>Посещений сегодня</h3>
        <p class="stat-value">{{ stats.todayVisits }}</p>
      </div>
      <div class="stat-card">
        <h3>Всего посещений</h3>
        <p class="stat-value">{{ stats.totalVisits }}</p>
      </div>
    </div>
    
    <div class="quick-actions">
      <h2>Быстрые действия</h2>
      <div class="action-buttons">
        <button @click="goTo('/passes')" class="btn btn-primary">Управление пропусками</button>
        <button @click="goTo('/statistics')" class="btn btn-primary">Просмотр статистики</button>
        <button @click="goTo('/audit')" class="btn btn-primary">Журнал аудита</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const stats = ref({
  activePass: 0,
  totalPasses: 0,
  todayVisits: 0,
  totalVisits: 0
})

const loadStats = async () => {
  try {
    const response = await axios.get('/api/admin/statistics')
    stats.value = response.data
  } catch (error) {
    console.error('Failed to load statistics:', error)
  }
}

const goTo = (path) => {
  router.push(path)
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
}

.dashboard h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-card h3 {
  color: #7f8c8d;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  text-transform: uppercase;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3e50;
}

.quick-actions {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.quick-actions h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-buttons .btn {
  flex: 1;
  min-width: 200px;
}
</style>
