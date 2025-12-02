import React, { useState } from 'react'

/**
 * TemplateEditor Component
 * Allows editing email subject and body with dynamic field insertion
 */
const TemplateEditor = ({ initialSubject, initialHtmlBody, onSave, onCancel }) => {
  const [subject, setSubject] = useState(initialSubject || '')
  const [htmlBody, setHtmlBody] = useState(initialHtmlBody || '')
  const [showPreview, setShowPreview] = useState(false)

  const dynamicFields = [
    { name: 'name', label: 'Customer Name', example: 'Rahim Ahmed' },
    { name: 'email', label: 'Email', example: 'rahim@example.com' },
    { name: 'phone', label: 'Phone', example: '+8801712345678' },
    { name: 'segment', label: 'Segment', example: 'High Value' },
    { name: 'churn_score', label: 'Churn Score', example: '0.15' },
    { name: 'purchase_amount', label: 'Purchase Amount', example: '50000' },
    { name: 'last_purchase', label: 'Last Purchase Date', example: '2025-11-15' },
  ]

  const insertField = (fieldName, target) => {
    const placeholder = `{${fieldName}}`
    if (target === 'subject') {
      setSubject(subject + placeholder)
    } else {
      setHtmlBody(htmlBody + placeholder)
    }
  }

  const handleSave = () => {
    onSave({ subject, html_body: htmlBody })
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Edit Email Template</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setShowPreview(!showPreview)}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
          >
            {showPreview ? 'Hide Preview' : 'Show Preview'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Editor Section */}
        <div className="lg:col-span-3 space-y-4">
          {/* Subject Editor */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Subject
            </label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="Enter email subject..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Body Editor */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Body (HTML)
            </label>
            <textarea
              value={htmlBody}
              onChange={(e) => setHtmlBody(e.target.value)}
              placeholder="Enter email body..."
              rows={20}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
            />
          </div>

          {/* Preview */}
          {showPreview && (
            <div className="border border-gray-300 rounded-lg p-4">
              <h3 className="font-semibold mb-2">Preview:</h3>
              <div className="bg-gray-50 p-4 rounded">
                <div className="mb-4">
                  <strong>Subject:</strong> {subject}
                </div>
                <div dangerouslySetInnerHTML={{ __html: htmlBody }} />
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex gap-3 pt-4">
            <button
              onClick={handleSave}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
            >
              Save Changes
            </button>
            <button
              onClick={onCancel}
              className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 font-medium"
            >
              Cancel
            </button>
          </div>
        </div>

        {/* Dynamic Fields Sidebar */}
        <div className="lg:col-span-1">
          <div className="sticky top-4">
            <h3 className="text-sm font-semibold text-gray-900 mb-3">
              Dynamic Fields
            </h3>
            <p className="text-xs text-gray-600 mb-4">
              Click to insert a field placeholder. It will be replaced with actual customer data.
            </p>
            <div className="space-y-2">
              {dynamicFields.map((field) => (
                <div key={field.name} className="bg-gray-50 rounded-lg p-3">
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-sm font-medium text-gray-900">
                      {field.label}
                    </span>
                  </div>
                  <div className="text-xs text-gray-600 mb-2">
                    Example: {field.example}
                  </div>
                  <div className="flex gap-1">
                    <button
                      onClick={() => insertField(field.name, 'subject')}
                      className="flex-1 px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                    >
                      → Subject
                    </button>
                    <button
                      onClick={() => insertField(field.name, 'body')}
                      className="flex-1 px-2 py-1 text-xs bg-green-100 text-green-700 rounded hover:bg-green-200"
                    >
                      → Body
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TemplateEditor
