import React from 'react'

/**
 * SegmentSelector Component
 * Dropdown to select customer segment
 */
const SegmentSelector = ({ segments, selectedSegment, onSegmentChange, loading }) => {
  return (
    <div className="w-full">
      <label htmlFor="segment" className="block text-sm font-medium text-gray-700 mb-2">
        Select Customer Segment
      </label>
      <select
        id="segment"
        value={selectedSegment || ''}
        onChange={(e) => onSegmentChange(e.target.value)}
        disabled={loading}
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
      >
        <option value="">-- Select a Segment --</option>
        {segments.map((segment) => (
          <option key={segment.id} value={segment.id}>
            {segment.name} ({segment.customer_count} customers)
          </option>
        ))}
      </select>
      {selectedSegment && (
        <p className="mt-2 text-sm text-gray-600">
          {segments.find(s => s.id === selectedSegment)?.description}
        </p>
      )}
    </div>
  )
}

export default SegmentSelector
