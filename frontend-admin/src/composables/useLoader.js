import { ref } from 'vue'

export function useLoader() {
  const loading = ref(false)
  const error = ref(null)

  const execute = async (fn) => {
    loading.value = true
    error.value = null
    try {
      return await fn()
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    execute
  }
}
