<template>
  <div class="dashboard">
    <h1>Панель управления</h1>
    
    <div class="stats-grid">
      <div class="stat-card">
        <h3>Активные пропуска</h3>
        <p class="stat-value">{{ stats.active_passes }}</p>
      </div>
      <div class="stat-card">
        <h3>Всего пропусков</h3>
        <p class="stat-value">{{ stats.total_passes }}</p>
      </div>
      <div class="stat-card">
        <h3>Посещений сегодня</h3>
        <p class="stat-value">{{ stats.today_visits }}</p>
      </div>
      <div class="stat-card">
        <h3>Всего посещений</h3>
        <p class="stat-value">{{ stats.total_visits }}</p>
      </div>
    </div>
    
    <div class="quick-actions">
      <h2>Быстрые действия</h2>
      <div class="action-buttons">
        <button @click="goTo('/passes')" class="btn btn-primary">Управление пропусками</button>
        <button @click="goTo('/users')" class="btn btn-primary">Сотрудники</button>
        <button @click="goTo('/audit')" class="btn btn-primary">Журнал аудита</button>
        <button @click="createPass" class="btn btn-primary">Создать пропуск</button>
        <button @click="createGuard" class="btn btn-primary">Добавить охранника</button>
      </div>
    </div>

    <!-- Create Pass Modal -->
    <div v-if="creatingPass" class="modal-overlay" @click="closeCreatePassModal">
      <div class="modal-content" @click.stop>
        <h2>Create Pass</h2>
        <form @submit.prevent="createdPass">
          <div class="form-group">
            <label>Guest Name</label>
            <input v-model="creatingPass.guest_name" type="text">
          </div>
          <div class="form-group">
            <label>Company</label>
            <input v-model="creatingPass.guest_company" type="text">
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input v-model="creatingPass.guest_phone" type="text">
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="creatingPass.guest_email" type="text">
          </div>
          <div class="form-group">
            <label>Valid Until</label>
            <input v-model="creatingPass.valid_until" type="datetime-local">
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-primary">Create</button>
            <button type="button" @click="closeCreatePassModal" class="btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Create User Modal -->
    <div v-if="creatingUser" class="modal-overlay" @click="closeCreateUserModal">
      <div class="modal-content" @click.stop>
        <h2>Добавить охранника</h2>
        <form @submit.prevent="createdUser">
          <div class="form-group">
            <label>Username</label>
            <input v-model="creatingUser.username" type="text" required>
          </div>
          <div class="form-group">
            <label>Full Name</label>
            <input v-model="creatingUser.full_name" type="text" required>
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="creatingUser.email" type="text" required>
          </div>
          <div class="form-group">
            <label>Phone</label>
            <input v-model="creatingUser.phone" type="text" required>
          </div>
          <div class="form-group">
            <label>Password</label>
            <input v-model="creatingUser.password" type="text" required>
          </div>
          <div class="form-group">
            <label>Role</label>
            <select v-model="creatingUser.role">
              <option value="guard">Guard</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn-primary">Create</button>
            <button type="button" @click="closeCreateUserModal" class="btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { apiClient } from '../services/api'

const router = useRouter()
const stats = ref({
  active_passes: 0,
  total_passes: 0,
  today_visits: 0,
  total_visits: 0
})
const creatingPass = ref({
  guest_name: '',
  guest_company: '',
  guest_phone: '',
  guest_email: '',
  valid_until: ''
})
const creatingUser = ref({
  username: '',
  full_name: '',
  email: '',
  phone: '',
  password: '',
  role: 'guard'
})

// Функция открытия модали
const createGuard = () => {
  creatingUser.value = {
    username: '',
    full_name: '',
    email: '',
    phone: '',
    password: '',
    role: 'guard'
  }
}

const loadStats = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/admin/statistics', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    stats.value = response.data
  } catch (error) {
    console.error('Failed to load statistics:', error)
  }
}

const goTo = (path) => {
  router.push(path)
}

const createPass = (pass) => {
  creatingPass.value = { ...pass }
  console.log('Create pass:', creatingPass.value)
}

const closeCreatePassModal = () => {
  creatingPass.value = null
}

const createdPass = async () => {
  try {
    const token = localStorage.getItem('token')
    const now = new Date()
    if (!token) return
    
    const response = await apiClient.post(`/api/passes/create`, {
      ...creatingPass.value, valid_from: now.toISOString()
    }, 
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    console.log('Pass created:', response.data)
    closeCreatePassModal()
  } catch (error) {
    console.error('Create failed:', error)
    alert('Failed to create pass: ' + (error.response?.data?.detail || error.message))
  }
}

const closeCreateUserModal = () => {
  creatingUser.value = null
}

const createdUser = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    
    const response = await apiClient.post('/api/auth/register', 
      {
        ...creatingUser.value
      },
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    )
    
    console.log('User created:', response.data)
    closeCreateUserModal()
  } catch (error) {
    console.error('Create failed:', error)
    alert('Failed to create user: ' + (error.response?.data?.detail || error.message))
  }
}

onMounted(() => {
  loadStats()
  closeCreatePassModal()
  closeCreateUserModal()
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

.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-group select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

</style>
