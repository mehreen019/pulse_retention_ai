import client from './client'

export const roiAPI = {
  /**
   * Get key ROI and financial metrics
   */
  getMetrics: async (timeframe = 'monthly') => {
    const response = await client.get('/roi/metrics', {
      params: { timeframe }
    })
    return response.data
  },

  /**
   * Get profit trend over time
   */
  getProfitTrend: async (timeframe = 'monthly') => {
    const response = await client.get('/roi/profit-trend', {
      params: { timeframe }
    })
    return response.data
  },

  /**
   * Get cost breakdown by category
   */
  getCostBreakdown: async (timeframe = 'monthly') => {
    const response = await client.get('/roi/cost-breakdown', {
      params: { timeframe }
    })
    return response.data
  },

  /**
   * Get ROI for each campaign
   */
  getCampaignROI: async (timeframe = 'monthly') => {
    const response = await client.get('/roi/campaign-roi', {
      params: { timeframe }
    })
    return response.data
  },

  /**
   * Get savings from retention by customer segment
   */
  getRetentionSavings: async (timeframe = 'monthly') => {
    const response = await client.get('/roi/retention-savings', {
      params: { timeframe }
    })
    return response.data
  },

  /**
   * Get comprehensive ROI summary
   */
  getSummary: async (timeframe = 'monthly') => {
    const response = await client.get('/roi/summary', {
      params: { timeframe }
    })
    return response.data
  }
}
