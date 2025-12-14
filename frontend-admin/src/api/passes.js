import client from './client'

export const passesApi = {
  async createPass(data) {
    const response = await client.post('/api/passes/create', data)
    return response.data
  },

  async listPasses(skip = 0, limit = 100) {
    const response = await client.get('/api/passes/', { params: { skip, limit } })
    return response.data
  },

  async getPass(passId) {
    const response = await client.get(`/api/passes/${passId}`)
    return response.data
  },

  async updatePass(passId, data) {
    const response = await client.put(`/api/passes/${passId}`, data)
    return response.data
  },

  async searchPasses(filters) {
    const response = await client.get('/api/admin/passes/search', { params: filters })
    return response.data
  }
}
