<template>
  <div class="passes-view">
    <h1>Управление пропусками</h1>
    
    <div class="filters-card">
      <input 
        v-model="searchName" 
        type="text" 
        placeholder="Поиск по имени..."
        class="search-input"
      />
      <input 
        v-model="searchCompany" 
        type="text" 
        placeholder="Поиск по компании..."
        class="search-input"
      />
      <button @click="search" class="btn btn-primary">Поиск</button>
    </div>
    
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>ФИО</th>
            <th>Компания</th>
            <th>Статус</th>
            <th>Дата входа</th>
            <th>Дата выхода</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pass in passes" :key="pass.id">
            <td>{{ pass.guest_name }}</td>
            <td>{{ pass.guest_company || '-' }}</td>
            <td>
              <span :class="['status-badge', `status-${pass.status}`]">
                {{ pass.status }}
              </span>
            </td>
            <td>{{ formatDate(pass.valid_from) }}</td>
            <td>{{ formatDate(pass.valid_until) }}</td>
            <td>
              <button @click="editPass(pass)" class="btn btn-sm btn-primary">Редактировать</button>
              <button @click="deletePass(pass.id)" class="btn btn-sm btn-danger">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import dayjs from 'dayjs'

const passes = ref([])
const searchName = ref('')
const searchCompany = ref('')

const formatDate = (date) => {
  return dayjs(date).format('DD.MM.YYYY HH:mm')
}

const search = async () => {
  try {
    const params = {}
    if (searchName.value) params.name = searchName.value
    if (searchCompany.value) params.company = searchCompany.value
    
    const response = await axios.get('/api/admin/passes/search', { params })
    passes.value = response.data
  } catch (error) {
    console.error('Search failed:', error)
  }
}

const editPass = (pass) => {
  console.log('Edit pass:', pass)
}

const deletePass = async (passId) => {
  if (confirm('Вы уверены?')) {
    try {
      await axios.delete(`/api/passes/${passId}`)
      passes.value = passes.value.filter(p => p.id !== passId)
    } catch (error) {
      console.error('Delete failed:', error)
    }
  }
}

onMounted(() => {
  search()
})
</script>

<style scoped>
.passes-view {
  max-width: 1200px;
}

.filters-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.table-container {
  overflow-x: auto;
}

.table {
  width: 100%;
  background-color: white;
  border-collapse: collapse;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-active {
  background-color: #d4edda;
  color: #155724;
}

.status-expired {
  background-color: #f8d7da;
  color: #721c24;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}
</style>
