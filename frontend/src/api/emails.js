import apiClient from './client'

/**
 * Email API Client
 * Handles all email-related API calls
 */

/**
 * Get all customer segments
 * @returns {Promise} List of segments
 */
export const getSegments = async () => {
  const response = await apiClient.get('/emails/segments')
  return response.data
}

/**
 * Get customers in a specific segment
 * @param {string} segmentId - Segment ID
 * @returns {Promise} List of customers
 */
export const getSegmentCustomers = async (segmentId) => {
  const response = await apiClient.get(`/emails/segments/${segmentId}/customers`)
  return response.data
}

/**
 * Get all customers
 * @returns {Promise} List of all customers
 */
export const getAllCustomers = async () => {
  const response = await apiClient.get('/emails/customers')
  return response.data
}

/**
 * Generate email preview
 * @param {Object} data - Generation request data
 * @param {string[]} data.customer_ids - Customer IDs (optional)
 * @param {string} data.segment_id - Segment ID (optional)
 * @param {Object} data.extra_params - Extra parameters (optional)
 * @returns {Promise} Generated email template
 */
export const generateEmailPreview = async (data) => {
  const response = await apiClient.post('/emails/emails/generate', data)
  return response.data
}

/**
 * Send emails to customers
 * @param {Object} data - Send request data
 * @param {string} data.subject - Email subject
 * @param {string} data.html_body - HTML email body
 * @param {string} data.text_body - Plain text body (optional)
 * @param {string[]} data.customer_ids - Customer IDs
 * @param {string} data.segment_id - Segment ID (optional)
 * @returns {Promise} Send results
 */
export const sendEmails = async (data) => {
  const response = await apiClient.post('/emails/emails/send', data)
  return response.data
}

/**
 * Send emails to entire segment
 * @param {Object} params - Send parameters
 * @param {string} params.segment_id - Segment ID
 * @param {string} params.subject - Email subject
 * @param {string} params.html_body - HTML email body
 * @param {string} params.text_body - Plain text body (optional)
 * @returns {Promise} Send results
 */
export const sendToSegment = async (params) => {
  const response = await apiClient.post('/emails/emails/send-to-segment', null, { params })
  return response.data
}
