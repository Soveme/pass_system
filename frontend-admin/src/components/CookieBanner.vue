<template>
  <div class="cookie-banner">
    <div class="cookie-content">
      <p>Мы используем файлы cookies для улучшения вашего опыта. Подробнее в <router-link to="/privacy">политике конфиденциальности</router-link>.</p>
      <div class="cookie-buttons">
        <button @click="$emit('accept')" class="btn btn-primary">Принять</button>
        <button @click="reject" class="btn btn-secondary">Отклонить</button>
        <button @click="showSettings" class="btn btn-link">Настройки</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['accept'])

const reject = () => {
  localStorage.setItem('cookies_accepted', 'false')
}

const showSettings = () => {
  // Open cookie settings modal
  console.log('Open cookie settings')
}
</script>

<style scoped>
.cookie-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #2c3e50;
  color: white;
  padding: 1.5rem;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.2);
  z-index: 1000;
}

.cookie-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.cookie-content p {
  flex: 1;
}

.cookie-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.btn-link {
  background: none;
  border: none;
  color: #3498db;
  cursor: pointer;
  text-decoration: underline;
}
</style>
