import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useScannerStore = defineStore('scanner', () => {
  const scans = ref([])
  const currentScan = ref(null)

  const addScan = (scan) => {
    scans.value.push({
      ...scan,
      timestamp: new Date().toISOString()
    })
  }

  const clearScans = () => {
    scans.value = []
  }

  return {
    scans,
    currentScan,
    addScan,
    clearScans
  }
})
