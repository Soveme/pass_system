import client from './client'

export const adminApi = {
  async getStatistics() {
    const response = await client.get('/api/admin/statistics')
    return response.data
  },

  async getVisitsLog(filters = {}) {
    const response = await client.get('/api/visits/log', { params: filters })
    return response.data
  }
}
