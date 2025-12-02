import React from 'react'

/**
 * CustomerTable Component
 * Displays customers with checkbox selection
 */
const CustomerTable = ({ customers, selectedCustomers, onSelectionChange, loading }) => {
  const handleSelectAll = (e) => {
    if (e.target.checked) {
      onSelectionChange(customers.map(c => c.id))
    } else {
      onSelectionChange([])
    }
  }

  const handleSelectOne = (customerId) => {
    if (selectedCustomers.includes(customerId)) {
      onSelectionChange(selectedCustomers.filter(id => id !== customerId))
    } else {
      onSelectionChange([...selectedCustomers, customerId])
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (customers.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>No customers found in this segment</p>
      </div>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left">
              <input
                type="checkbox"
                checked={selectedCustomers.length === customers.length && customers.length > 0}
                onChange={handleSelectAll}
                className="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
              />
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Name
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Email
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Phone
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Churn Score
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Purchase Amount
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {customers.map((customer) => (
            <tr
              key={customer.id}
              className={`hover:bg-gray-50 ${selectedCustomers.includes(customer.id) ? 'bg-blue-50' : ''}`}
            >
              <td className="px-6 py-4">
                <input
                  type="checkbox"
                  checked={selectedCustomers.includes(customer.id)}
                  onChange={() => handleSelectOne(customer.id)}
                  className="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
                />
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {customer.name}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {customer.email}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {customer.phone || 'N/A'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <span className={`px-2 py-1 rounded-full text-xs ${
                  customer.churn_score > 0.7 ? 'bg-red-100 text-red-800' :
                  customer.churn_score > 0.4 ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {(customer.churn_score * 100).toFixed(0)}%
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ৳{customer.custom_fields?.purchase_amount?.toLocaleString() || 'N/A'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="px-6 py-3 bg-gray-50 text-sm text-gray-700">
        {selectedCustomers.length} of {customers.length} customers selected
      </div>
    </div>
  )
}

export default CustomerTable
