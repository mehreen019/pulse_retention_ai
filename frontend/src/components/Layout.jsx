import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import {
  HiChartBar,
  HiDocumentText,
  HiMail,
  HiClipboardList,
  HiTrendingUp,
  HiCurrencyDollar,
  HiUser,
  HiLogout,
  HiCreditCard
} from 'react-icons/hi'
import { FiFileText, FiTarget } from 'react-icons/fi'

const Layout = ({ children, activePage }) => {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const [hoveredItem, setHoveredItem] = useState(null)

  // Determine active page from location if not provided
  const currentPage = activePage || (() => {
    const path = location.pathname
    if (path === '/dashboard' || path === '/') return 'dashboard'
    if (path === '/churn-prediction') return 'churn'
    if (path === '/predictions') return 'predictions'
    if (path === '/email-campaign') return 'email'
    if (path === '/email-history') return 'history'
    if (path === '/analytics') return 'analytics'
    if (path === '/roi-dashboard') return 'roi'
    if (path === '/pricing-billing') return 'pricing'
    if (path === '/csv-normalization') return 'csv-normalization'
    return 'dashboard'
  })()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: HiChartBar, path: '/dashboard' },
    { id: 'churn', label: 'Churn Prediction', icon: FiTarget, path: '/churn-prediction' },
    { id: 'predictions', label: 'Predictions', icon: HiClipboardList, path: '/predictions' },
    { id: 'csv-normalization', label: 'CSV Normalization', icon: FiFileText, path: '/csv-normalization' },
    { id: 'email', label: 'Email Campaign', icon: HiMail, path: '/email-campaign' },
    { id: 'history', label: 'Email History', icon: HiDocumentText, path: '/email-history' },
    { id: 'analytics', label: 'Analytics', icon: HiTrendingUp, path: '/analytics' },
    { id: 'roi', label: 'ROI Dashboard', icon: HiCurrencyDollar, path: '/roi-dashboard' },
    { id: 'pricing', label: 'Pricing & Billing', icon: HiCreditCard, path: '/pricing-billing' }
  ]

  const handleMenuClick = (item) => {
    if (item.path) {
      navigate(item.path)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div
        style={{
          background: 'linear-gradient(135deg, #1e293b 0%, #334155 100%)',
          color: 'white',
          padding: '24px 40px',
          borderBottom: '3px solid #667eea',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)'
        }}
      >
        <h1 style={{ margin: 0, fontSize: '28px', fontWeight: 'bold', letterSpacing: '-0.5px' }}>
          Pulse Retention AI
        </h1>
        <p style={{ margin: '6px 0 0 0', color: '#cbd5e1', fontSize: '14px' }}>
          Customer Intelligence & Retention Platform
        </p>
      </div>

      <div style={{ display: 'flex', minHeight: 'calc(100vh - 100px)' }}>
        {/* Sidebar */}
        <div
          style={{
            width: '260px',
            background: 'linear-gradient(180deg, #334155 0%, #1e293b 100%)',
            color: 'white',
            padding: '30px 20px',
            borderRight: '1px solid #475569',
            boxShadow: '2px 0 8px rgba(0, 0, 0, 0.1)'
          }}
        >
          <div style={{ marginBottom: '30px' }}>
            <h3 style={{ 
              margin: '0 0 18px 0', 
              fontSize: '12px', 
              color: '#94a3b8',
              fontWeight: '600',
              letterSpacing: '1px',
              textTransform: 'uppercase'
            }}>
              FEATURES
            </h3>
            {menuItems.map((item) => {
              const isActive = currentPage === item.id
              const IconComponent = item.icon
              return (
                <div
                  key={item.id}
                  onClick={() => handleMenuClick(item)}
                  onMouseEnter={() => setHoveredItem(item.id)}
                  onMouseLeave={() => setHoveredItem(null)}
                  style={{
                    cursor: 'pointer',
                    padding: '12px 12px',
                    marginBottom: '8px',
                    borderRadius: '8px',
                    backgroundColor: isActive ? '#475569' : (hoveredItem === item.id ? '#3f4a57' : 'transparent'),
                    color: isActive ? '#667eea' : 'white',
                    fontWeight: isActive ? '600' : '400',
                    transition: 'all 0.2s ease',
                    borderLeft: isActive ? '3px solid #667eea' : '3px solid transparent',
                    paddingLeft: isActive ? '9px' : '12px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px'
                  }}
                >
                  <IconComponent style={{ fontSize: '18px', flexShrink: 0 }} />
                  <span>{item.label}</span>
                </div>
              )
            })}
          </div>

          <div
            style={{
              marginTop: '40px',
              padding: '18px',
              backgroundColor: '#475569',
              borderRadius: '10px',
              fontSize: '13px',
              border: '1px solid #64748b'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
              <div style={{
                width: '36px',
                height: '36px',
                borderRadius: '50%',
                backgroundColor: '#667eea',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0
              }}>
                <HiUser style={{ fontSize: '18px', color: 'white' }} />
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <p style={{ margin: 0, color: '#e2e8f0', fontWeight: '600', fontSize: '14px' }}>
                  {user?.name || 'User'}
                </p>
                <p style={{ margin: '4px 0 0 0', color: '#cbd5e1', fontSize: '11px', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {user?.email}
                </p>
              </div>
            </div>
            <p style={{ margin: '0 0 12px 0', color: '#cbd5e1', fontSize: '12px', paddingLeft: '46px' }}>
              Role: <strong className="capitalize" style={{ color: '#e2e8f0' }}>{user?.role || 'user'}</strong>
            </p>
            <button
              onClick={handleLogout}
              style={{
                width: '100%',
                marginTop: '8px',
                padding: '10px',
                backgroundColor: '#ef4444',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '13px',
                fontWeight: '600',
                transition: 'all 0.2s',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
              onMouseOver={(e) => {
                e.target.style.backgroundColor = '#dc2626'
                e.target.style.transform = 'translateY(-1px)'
                e.target.style.boxShadow = '0 4px 8px rgba(239, 68, 68, 0.3)'
              }}
              onMouseOut={(e) => {
                e.target.style.backgroundColor = '#ef4444'
                e.target.style.transform = 'translateY(0)'
                e.target.style.boxShadow = 'none'
              }}
            >
              <HiLogout style={{ fontSize: '16px' }} />
              <span>Logout</span>
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-10 overflow-y-auto bg-gray-50 dark:bg-gray-900">
          {children}
        </div>
      </div>

      {/* Footer */}
      <div
        style={{
          backgroundColor: '#1e293b',
          color: '#cbd5e1',
          padding: '20px 40px',
          textAlign: 'center',
          borderTop: '1px solid #334155',
        }}
      >
        <p style={{ margin: 0, fontSize: '13px' }}>
          © 2025 Pulse Retention AI. All rights reserved. | Customer Intelligence Platform
        </p>
      </div>
    </div>
  )
}

export default Layout

