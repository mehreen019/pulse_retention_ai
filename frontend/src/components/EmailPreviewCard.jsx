import React from 'react'

/**
 * EmailPreviewCard Component
 * Displays email preview with subject and body
 */
const EmailPreviewCard = ({ subject, htmlBody, textBody, onEdit }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Email Preview</h3>
        {onEdit && (
          <button
            onClick={onEdit}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            Edit Template
          </button>
        )}
      </div>

      {/* Subject */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Subject:
        </label>
        <div className="px-4 py-2 bg-gray-50 rounded border border-gray-200">
          <p className="text-gray-900">{subject}</p>
        </div>
      </div>

      {/* HTML Body Preview */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Email Body:
        </label>
        <div className="border border-gray-200 rounded overflow-hidden">
          <div className="bg-gray-50 px-4 py-2 border-b border-gray-200">
            <span className="text-xs text-gray-600">HTML Preview</span>
          </div>
          <div 
            className="p-4 bg-white max-h-96 overflow-y-auto"
            dangerouslySetInnerHTML={{ __html: htmlBody }}
          />
        </div>
      </div>

      {/* Text Body (optional) */}
      {textBody && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Plain Text Version:
          </label>
          <div className="px-4 py-2 bg-gray-50 rounded border border-gray-200">
            <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans">
              {textBody}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}

export default EmailPreviewCard
