import client from './client'

/**
 * Email History API
 * Functions for retrieving email sending history and statistics
 */

export const getEmailHistory = async (params = {}) => {
  const { skip = 0, limit = 50, status, segment_id, customer_email } = params
  
  const queryParams = new URLSearchParams({
    skip: skip.toString(),
    limit: limit.toString(),
  })
  
  if (status) queryParams.append('status', status)
  if (segment_id) queryParams.append('segment_id', segment_id)
  if (customer_email) queryParams.append('customer_email', customer_email)
  
  const response = await client.get(`/email-history/history?${queryParams}`)
  return response.data
}

export const getEmailStats = async (days = 30) => {
  const response = await client.get(`/email-history/stats?days=${days}`)
  return response.data
}

export const getCustomerEmailHistory = async (customerId, params = {}) => {
  const { skip = 0, limit = 20 } = params
  
  const queryParams = new URLSearchParams({
    skip: skip.toString(),
    limit: limit.toString(),
  })
  
  const response = await client.get(`/email-history/customer/${customerId}?${queryParams}`)
  return response.data
}
