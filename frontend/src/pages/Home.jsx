import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../stores/authStore'
import Layout from '../components/Layout'

const Home = () => {
  const navigate = useNavigate()
  const { user } = useAuthStore()

  const quickActions = [
    {
      id: 'churn',
      title: 'Churn Prediction',
      description: 'Analyze customer churn risk',
      icon: '🎯',
      path: '/churn-prediction',
      color: 'from-blue-500 to-indigo-600'
    },
    {
      id: 'email',
      title: 'Email Campaign',
      description: 'Send targeted emails',
      icon: '📧',
      path: '/email-campaign',
      color: 'from-purple-500 to-pink-600'
    },
    {
      id: 'analytics',
      title: 'Analytics',
      description: 'View customer insights',
      icon: '📈',
      path: '/analytics',
      color: 'from-green-500 to-teal-600'
    },
    {
      id: 'roi',
      title: 'ROI Dashboard',
      description: 'Track campaign ROI',
      icon: '💰',
      path: '/roi-dashboard',
      color: 'from-yellow-500 to-orange-600'
    }
  ]

  return (
    <Layout activePage="dashboard">
      {/* Welcome Section */}
      <div className="mb-10">
        <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Welcome back, {user?.name || 'User'}! 👋
        </h2>
        <p className="text-gray-600 dark:text-gray-400 text-lg">
          Here's your account summary and quick actions
        </p>
      </div>

      {/* User Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        {/* Account Status Card */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border-l-4 border-blue-500">
          <div className="text-gray-500 dark:text-gray-400 text-sm font-medium mb-2">
            Account Status
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white mb-3">
            {user?.is_active ? 'Active' : 'Inactive'}
          </div>
          <div className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
            user?.is_active
              ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
              : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
          }`}>
            {user?.is_active ? '✓ Account Active' : '⚠ Account Inactive'}
          </div>
        </div>

        {/* Role Card */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border-l-4 border-green-500">
          <div className="text-gray-500 dark:text-gray-400 text-sm font-medium mb-2">
            Role
          </div>
          <div className="text-3xl font-bold text-gray-900 dark:text-white mb-3 capitalize">
            {user?.role || 'User'}
          </div>
          <div className="text-gray-500 dark:text-gray-400 text-sm">
            Administrator Access
          </div>
        </div>

        {/* Email Card */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border-l-4 border-amber-500">
          <div className="text-gray-500 dark:text-gray-400 text-sm font-medium mb-2">
            Contact Email
          </div>
          <div className="text-xl font-bold text-gray-900 dark:text-white mb-3 truncate">
            {user?.email || 'Not Set'}
          </div>
          <div className="text-gray-500 dark:text-gray-400 text-sm">
            Primary Contact
          </div>
        </div>
      </div>

      {/* Quick Actions Section */}
      <div className="mb-10">
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Quick Actions
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickActions.map((action) => (
            <div
              key={action.id}
              onClick={() => navigate(action.path)}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer group overflow-hidden"
            >
              <div className={`h-2 bg-gradient-to-r ${action.color}`}></div>
              <div className="p-6">
                <div className="text-5xl mb-4 group-hover:scale-110 transition-transform duration-300">
                  {action.icon}
                </div>
                <h4 className="text-xl font-bold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                  {action.title}
                </h4>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  {action.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Activity Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Getting Started
        </h3>
        <div className="space-y-4">
          <div className="flex items-start gap-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
            <div className="text-3xl">📊</div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-1">
                Step 1: Upload Customer Data
              </h4>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Navigate to Churn Prediction and upload your customer transaction CSV to get started.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
            <div className="text-3xl">🤖</div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-1">
                Step 2: Train Your Model
              </h4>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Let our AI analyze your data and build a custom churn prediction model.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
            <div className="text-3xl">📧</div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-1">
                Step 3: Launch Campaigns
              </h4>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Use insights to create targeted email campaigns and retain at-risk customers.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-4 bg-amber-50 dark:bg-amber-900/20 rounded-lg border border-amber-200 dark:border-amber-800">
            <div className="text-3xl">💡</div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-1">
                Step 4: Track ROI
              </h4>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Monitor campaign performance and measure your return on investment in real-time.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default Home
