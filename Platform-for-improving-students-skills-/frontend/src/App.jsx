import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import PaperUpload from './components/PaperUpload';
import AdaptiveTest from './components/AdaptiveTest';
import PredictionCard from './components/PredictionCard';
import LearningFeed from './components/LearningFeed';
import Profile from './components/Profile';
import { 
  FiMoon, 
  FiSun, 
  FiMenu, 
  FiX, 
  FiHome, 
  FiBarChart2,
  FiFileText,
  FiTarget,
  FiBookOpen,
  FiSettings,
  FiUser,
  FiLogOut,
  FiBell,
  FiSearch,
  FiHelpCircle,
  FiTrendingUp
} from 'react-icons/fi';
import './styles/global.css';

// Context for theme and user
const ThemeContext = React.createContext();
const UserContext = React.createContext();

// Main App Component
const App = () => {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('skilltwin_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const [darkMode, setDarkMode] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches);
  });
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  useEffect(() => {
    if (user) {
      localStorage.setItem('skilltwin_user', JSON.stringify(user));
      // Load notifications
      loadNotifications();
    } else {
      localStorage.removeItem('skilltwin_user');
    }
  }, [user]);

  const loadNotifications = async () => {
    // Mock notifications
    setNotifications([
      {
        id: 1,
        title: 'Upcoming Physics Test',
        message: 'Unit test on Thermodynamics in 3 days',
        time: '2 hours ago',
        read: false,
        type: 'exam'
      },
      {
        id: 2,
        title: 'Study Recommendation',
        message: 'New practice questions available for Optics',
        time: '1 day ago',
        read: true,
        type: 'study'
      },
      {
        id: 3,
        title: 'Paper Analysis Complete',
        message: 'Your uploaded paper has been analyzed',
        time: '2 days ago',
        read: false,
        type: 'analysis'
      }
    ]);
  };

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
    setSidebarOpen(false);
    setNotifications([]);
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const markNotificationAsRead = (id) => {
    setNotifications(notifications.map(notif => 
      notif.id === id ? { ...notif, read: true } : notif
    ));
  };

  const navigation = [
    { name: 'Dashboard', path: '/', icon: <FiHome />, color: 'text-blue-500' },
    { name: 'Performance', path: '/performance', icon: <FiTrendingUp />, color: 'text-green-500' },
    { name: 'Mock Tests', path: '/tests', icon: <FiTarget />, color: 'text-purple-500' },
    { name: 'Paper Analysis', path: '/paper-analysis', icon: <FiFileText />, color: 'text-orange-500' },
    { name: 'Learning Path', path: '/learning', icon: <FiBookOpen />, color: 'text-pink-500' },
    { name: 'Analytics', path: '/analytics', icon: <FiBarChart2 />, color: 'text-indigo-500' },
    { name: 'Resources', path: '/resources', icon: <FiBookOpen />, color: 'text-teal-500' },
  ];

  const userNavigation = [
    { name: 'Profile', path: '/profile', icon: <FiUser /> },
    { name: 'Settings', path: '/settings', icon: <FiSettings /> },
    { name: 'Help', path: '/help', icon: <FiHelpCircle /> },
  ];

  return (
    <ThemeContext.Provider value={{ darkMode, toggleDarkMode }}>
      <UserContext.Provider value={{ user, setUser }}>
        <Router>
          <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800 transition-colors duration-300">
            {/* Header */}
            <AnimatePresence>
              {user && (
                <motion.header
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800 shadow-sm"
                >
                  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                      {/* Left: Logo and Menu */}
                      <div className="flex items-center">
                        <button
                          onClick={() => setSidebarOpen(true)}
                          className="md:hidden p-2 mr-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                        >
                          <FiMenu className="text-xl text-gray-700 dark:text-gray-300" />
                        </button>
                        <div className="flex items-center gap-2 cursor-pointer">
                          <motion.div 
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center"
                          >
                            <span className="text-white font-bold">ST</span>
                          </motion.div>
                          <motion.span 
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent"
                          >
                            SkillTwin
                          </motion.span>
                        </div>
                        
                        {/* Desktop Navigation */}
                        <nav className="hidden md:flex items-center space-x-1 ml-8">
                          {navigation.slice(0, 4).map((item) => (
                            <Link
                              key={item.name}
                              to={item.path}
                              className="flex items-center gap-2 px-4 py-2 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors font-medium"
                            >
                              <span className={item.color}>{item.icon}</span>
                              {item.name}
                            </Link>
                          ))}
                        </nav>
                      </div>

                      {/* Center: Search Bar */}
                      <div className="hidden lg:flex flex-1 max-w-md mx-4">
                        <div className="relative w-full">
                          <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                          <input
                            type="text"
                            placeholder="Search questions, topics, or resources..."
                            className="w-full pl-10 pr-4 py-2 bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 dark:text-white"
                          />
                        </div>
                      </div>

                      {/* Right: User Actions */}
                      <div className="flex items-center gap-3">
                        {/* Search Button for Mobile */}
                        <button className="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
                          <FiSearch className="text-xl text-gray-700 dark:text-gray-300" />
                        </button>

                        {/* Notifications */}
                        <div className="relative">
                          <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 relative">
                            <FiBell className="text-xl text-gray-700 dark:text-gray-300" />
                            {notifications.filter(n => !n.read).length > 0 && (
                              <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                            )}
                          </button>
                          
                          {/* Notifications Dropdown */}
                          <div className="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 hidden group-hover:block">
                            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                              <h3 className="font-semibold text-gray-800 dark:text-white">Notifications</h3>
                            </div>
                            <div className="max-h-96 overflow-y-auto">
                              {notifications.map(notif => (
                                <div
                                  key={notif.id}
                                  className={`p-4 border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-750 ${!notif.read ? 'bg-blue-50 dark:bg-blue-900/20' : ''}`}
                                  onClick={() => markNotificationAsRead(notif.id)}
                                >
                                  <div className="flex items-start gap-3">
                                    <div className={`p-2 rounded-lg ${notif.type === 'exam' ? 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400' : 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'}`}>
                                      {notif.type === 'exam' ? '📅' : '📚'}
                                    </div>
                                    <div className="flex-1">
                                      <h4 className="font-medium text-gray-800 dark:text-white">{notif.title}</h4>
                                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{notif.message}</p>
                                      <span className="text-xs text-gray-500 dark:text-gray-500 mt-2 block">{notif.time}</span>
                                    </div>
                                    {!notif.read && (
                                      <span className="w-2 h-2 bg-blue-500 rounded-full mt-2"></span>
                                    )}
                                  </div>
                                </div>
                              ))}
                            </div>
                            <div className="p-4 text-center border-t border-gray-200 dark:border-gray-700">
                              <a href="/notifications" className="text-sm text-blue-600 dark:text-blue-400 hover:underline">
                                View all notifications
                              </a>
                            </div>
                          </div>
                        </div>

                        {/* Theme Toggle */}
                        <button
                          onClick={toggleDarkMode}
                          className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                          aria-label="Toggle dark mode"
                        >
                          {darkMode ? (
                            <FiSun className="text-xl text-gray-700 dark:text-gray-300" />
                          ) : (
                            <FiMoon className="text-xl text-gray-700 dark:text-gray-300" />
                          )}
                        </button>

                        {/* User Profile (Desktop) */}
                        <div className="hidden md:flex items-center gap-3">
                          <div className="text-right">
                            <div className="font-semibold text-gray-800 dark:text-white">
                              {user?.name}
                            </div>
                            <div className="text-sm text-gray-600 dark:text-gray-400">
                              {user?.class_level}
                            </div>
                          </div>
                          <div className="relative group">
                            <button className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
                              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center">
                                <span className="text-white text-sm font-bold">
                                  {user?.name?.charAt(0) || 'U'}
                                </span>
                              </div>
                            </button>
                            
                            {/* User Dropdown */}
                            <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 hidden group-hover:block">
                              <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                                <div className="font-semibold text-gray-800 dark:text-white">{user?.name}</div>
                                <div className="text-sm text-gray-600 dark:text-gray-400">{user?.email}</div>
                              </div>
                              <div className="py-2">
                                {userNavigation.map((item) => (
                                  <a
                                    key={item.name}
                                    href={item.path}
                                    className="flex items-center gap-3 px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                                  >
                                    {item.icon}
                                    {item.name}
                                  </a>
                                ))}
                              </div>
                              <div className="border-t border-gray-200 dark:border-gray-700 py-2">
                                <button
                                  onClick={handleLogout}
                                  className="flex items-center gap-3 px-4 py-2 w-full text-left text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                                >
                                  <FiLogOut />
                                  Logout
                                </button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.header>
              )}
            </AnimatePresence>

            {/* Sidebar for Mobile */}
            <AnimatePresence>
              {sidebarOpen && (
                <>
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={() => setSidebarOpen(false)}
                    className="fixed inset-0 bg-black/50 z-40 md:hidden"
                  />
                  <motion.aside
                    initial={{ x: '-100%' }}
                    animate={{ x: 0 }}
                    exit={{ x: '-100%' }}
                    transition={{ type: 'tween' }}
                    className="fixed top-0 left-0 h-full w-64 bg-white dark:bg-gray-900 z-50 shadow-xl md:hidden"
                  >
                    <div className="p-4 border-b border-gray-200 dark:border-gray-800">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                            <span className="text-white font-bold">ST</span>
                          </div>
                          <span className="text-xl font-bold text-gray-800 dark:text-white">
                            SkillTwin
                          </span>
                        </div>
                        <button
                          onClick={() => setSidebarOpen(false)}
                          className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
                        >
                          <FiX className="text-xl text-gray-700 dark:text-gray-300" />
                        </button>
                      </div>
                      <div className="mt-4">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center">
                            <span className="text-white font-bold">
                              {user?.name?.charAt(0) || 'U'}
                            </span>
                          </div>
                          <div>
                            <div className="font-semibold text-gray-800 dark:text-white">
                              {user?.name}
                            </div>
                            <div className="text-sm text-gray-600 dark:text-gray-400">
                              {user?.class_level}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <nav className="p-4 space-y-1">
                      {navigation.map((item) => (
                        <a
                          key={item.name}
                          href={item.path}
                          onClick={() => setSidebarOpen(false)}
                          className="flex items-center gap-3 p-3 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                        >
                          <span className={item.color}>{item.icon}</span>
                          <span className="font-medium">{item.name}</span>
                        </a>
                      ))}
                    </nav>
                    <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 dark:border-gray-800">
                      <div className="space-y-2">
                        {userNavigation.map((item) => (
                          <a
                            key={item.name}
                            href={item.path}
                            onClick={() => setSidebarOpen(false)}
                            className="flex items-center gap-3 p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
                          >
                            {item.icon}
                            {item.name}
                          </a>
                        ))}
                        <button
                          onClick={handleLogout}
                          className="flex items-center gap-3 p-2 w-full text-left text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                        >
                          <FiLogOut />
                          Logout
                        </button>
                      </div>
                    </div>
                  </motion.aside>
                </>
              )}
            </AnimatePresence>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
              <AnimatePresence mode="wait">
                <Routes>
                  <Route
                    path="/login"
                    element={
                      user ? (
                        <Navigate to="/" replace />
                      ) : (
                        <Login onLogin={handleLogin} />
                      )
                    }
                  />
                  <Route
                    path="/"
                    element={
                      user ? (
                        <Dashboard user={user} />
                      ) : (
                        <Navigate to="/login" replace />
                      )
                    }
                  />
                  <Route
                    path="/performance"
                    element={
                      user ? (
                        <PerformancePage user={user} />
                      ) : (
                        <Navigate to="/login" replace />
                      )
                    }
                  />
                  <Route
                    path="/tests"
                    element={
                      user ? (
                        <TestsPage user={user} />
                      ) : (
                        <Navigate to="/login" replace />
                      )
                    }
                  />
                  <Route
                    path="/paper-analysis"
                    element={
                      user ? (
                        <PaperUpload user={user} />
                      ) : (
                        <Navigate to="/login" replace />
                      )
                    }
                  />
                  <Route
                    path="/learning"
                    element={
                      user ? (
                        <LearningPage user={user} />
                      ) : (
                        <Navigate to="/login" replace />
                      )
                    }
                  />
                  <Route
                    path="/analytics"
                    element={
                      user ? (
                        <AnalyticsPage user={user} />
                      ) : (
                        <Navigate to="/login" replace />
                      )
                    }
                  />
                  <Route
                    path="/profile"
                    element={
                      user ? (
                        <Profile user={user} setUser={setUser} />
                      ) : (
                        <Navigate to="/login" replace />
                      )
                    }
                  />
                  <Route
                    path="/settings"
                    element={
                      user ? (
                        <div className="max-w-4xl mx-auto p-6">
                          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
                            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Settings</h1>
                            <p className="text-gray-600 dark:text-gray-400">Settings page coming soon...</p>
                          </div>
                        </div>
                      ) : (
                        <Navigate to="/login" replace />
                      )
                    }
                  />
                  <Route
                    path="/help"
                    element={
                      user ? (
                        <div className="max-w-4xl mx-auto p-6">
                          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
                            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Help Center</h1>
                            <p className="text-gray-600 dark:text-gray-400">Help center coming soon...</p>
                          </div>
                        </div>
                      ) : (
                        <Navigate to="/login" replace />
                      )
                    }
                  />
                  <Route
                    path="*"
                    element={
                      <Navigate to={user ? "/" : "/login"} replace />
                    }
                  />
                </Routes>
              </AnimatePresence>
            </main>

            {/* Footer */}
            <Footer />
          </div>
        </Router>
      </UserContext.Provider>
    </ThemeContext.Provider>
  );
};

// Performance Page Component
const PerformancePage = ({ user }) => {
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch prediction data
    setTimeout(() => {
      setPredictionData({
        predicted_score: 78,
        confidence_interval: [72, 84],
        confidence: 85,
        risk_level: 'medium',
        weak_topics: [
          { topic: 'Thermodynamics', mastery: 45, subject: 'Physics' },
          { topic: 'Optics', mastery: 60, subject: 'Physics' },
          { topic: 'Calculus', mastery: 55, subject: 'Mathematics' }
        ]
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Performance Analytics
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Track your progress and get personalized insights
        </p>
      </div>
      
      <PredictionCard 
        prediction={predictionData}
        riskLevel={predictionData?.risk_level}
        weakTopics={predictionData?.weak_topics}
      />
      
      {/* Additional Performance Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h3 className="font-semibold text-gray-800 dark:text-white mb-4">
            📈 Progress Over Time
          </h3>
          <div className="h-48 flex items-center justify-center text-gray-500 dark:text-gray-400">
            Progress chart will appear here
          </div>
        </div>
        
        <div className="card">
          <h3 className="font-semibold text-gray-800 dark:text-white mb-4">
            🎯 Topic Mastery
          </h3>
          <div className="space-y-4">
            {['Physics', 'Mathematics', 'Chemistry'].map((subject) => (
              <div key={subject} className="flex items-center justify-between">
                <span className="text-gray-700 dark:text-gray-300">{subject}</span>
                <div className="flex items-center gap-3">
                  <div className="w-32 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-blue-500 to-indigo-600"
                      style={{ width: `${Math.random() * 100}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium text-gray-800 dark:text-white w-10">
                    {Math.floor(Math.random() * 30 + 70)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        <div className="card">
          <h3 className="font-semibold text-gray-800 dark:text-white mb-4">
            ⚡ Study Efficiency
          </h3>
          <div className="text-center py-8">
            <div className="text-4xl font-bold text-green-600 dark:text-green-400 mb-2">
              85%
            </div>
            <div className="text-gray-600 dark:text-gray-400">
              Questions Correct per Hour
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// Tests Page Component
const TestsPage = ({ user }) => {
  const [activeTab, setActiveTab] = useState('adaptive');
  const [subjects] = useState(['Physics', 'Mathematics', 'Chemistry', 'All Subjects']);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Mock Tests & Practice
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Take adaptive tests, topic quizzes, and full-length exams
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <div className="flex space-x-4">
          {['adaptive', 'topics', 'full', 'history'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 font-medium capitalize ${
                activeTab === tab
                  ? 'text-blue-600 border-b-2 border-blue-600 dark:text-blue-400 dark:border-blue-400'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'
              }`}
            >
              {tab === 'adaptive' ? 'Adaptive Tests' :
               tab === 'topics' ? 'Topic Quizzes' :
               tab === 'full' ? 'Full Exams' : 'History'}
            </button>
          ))}
        </div>
      </div>

      {/* Content based on active tab */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          {activeTab === 'adaptive' && (
            <AdaptiveTest studentId={user.id} subject="Physics" />
          )}
          
          {activeTab === 'topics' && (
            <div className="card">
              <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">
                Topic-based Quizzes
              </h3>
              <div className="grid grid-cols-2 gap-4">
                {subjects.map((subject) => (
                  <div key={subject} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-blue-300 dark:hover:border-blue-700 transition-colors cursor-pointer">
                    <div className="font-semibold text-gray-800 dark:text-white mb-2">
                      {subject}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      {subject === 'All Subjects' ? 'Mixed questions' : '10 questions'}
                    </div>
                    <button className="mt-3 px-4 py-2 text-sm bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors">
                      Start Quiz
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {activeTab === 'full' && (
            <div className="card">
              <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">
                Full-length Exams
              </h3>
              <div className="space-y-4">
                {[
                  { title: 'Physics Final Exam', duration: '3 hours', questions: 50 },
                  { title: 'Mathematics Board Exam', duration: '3 hours', questions: 60 },
                  { title: 'Chemistry Comprehensive Test', duration: '2.5 hours', questions: 45 }
                ].map((exam, index) => (
                  <div key={index} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-semibold text-gray-800 dark:text-white">
                          {exam.title}
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                          {exam.questions} questions • {exam.duration}
                        </div>
                      </div>
                      <button className="px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-300">
                        Start Exam
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {activeTab === 'history' && (
            <div className="card">
              <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">
                Test History
              </h3>
              <div className="space-y-3">
                {[
                  { test: 'Physics Adaptive Test', score: 85, date: '2024-01-15', time: '15:30' },
                  { test: 'Mathematics Quiz', score: 72, date: '2024-01-14', time: '10:15' },
                  { test: 'Chemistry Practice', score: 90, date: '2024-01-13', time: '14:45' }
                ].map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg">
                    <div>
                      <div className="font-medium text-gray-800 dark:text-white">
                        {item.test}
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        {item.date} • {item.time}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className={`text-lg font-bold ${
                        item.score >= 80 ? 'text-green-600 dark:text-green-400' :
                        item.score >= 60 ? 'text-yellow-600 dark:text-yellow-400' :
                        'text-red-600 dark:text-red-400'
                      }`}>
                        {item.score}/100
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-500">
                        Score
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <div className="card">
            <h3 className="font-semibold text-gray-800 dark:text-white mb-4">
              📊 Test Statistics
            </h3>
            <div className="space-y-3">
              {[
                { label: 'Tests Taken', value: '24' },
                { label: 'Average Score', value: '78%' },
                { label: 'Best Score', value: '95%' },
                { label: 'Improvement', value: '+12%' }
              ].map((stat, index) => (
                <div key={index} className="flex items-center justify-between">
                  <span className="text-gray-600 dark:text-gray-400">{stat.label}</span>
                  <span className="font-semibold text-gray-800 dark:text-white">{stat.value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Test Tips */}
          <div className="card">
            <h3 className="font-semibold text-gray-800 dark:text-white mb-4">
              💡 Test Tips
            </h3>
            <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li className="flex items-start gap-2">
                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-1.5"></div>
                Read questions carefully before answering
              </li>
              <li className="flex items-start gap-2">
                <div className="w-1.5 h-1.5 bg-green-500 rounded-full mt-1.5"></div>
                Manage your time effectively
              </li>
              <li className="flex items-start gap-2">
                <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mt-1.5"></div>
                Review difficult questions at the end
              </li>
              <li className="flex items-start gap-2">
                <div className="w-1.5 h-1.5 bg-orange-500 rounded-full mt-1.5"></div>
                Stay calm and focused throughout
              </li>
            </ul>
          </div>

          {/* Upcoming Tests */}
          <div className="card">
            <h3 className="font-semibold text-gray-800 dark:text-white mb-4">
              📅 Upcoming Tests
            </h3>
            <div className="space-y-3">
              <div className="p-3 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/10 dark:to-indigo-900/10 rounded-lg">
                <div className="font-medium text-gray-800 dark:text-white">
                  Physics Unit Test
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  In 3 days • Thermodynamics
                </div>
              </div>
              <div className="p-3 bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/10 dark:to-teal-900/10 rounded-lg">
                <div className="font-medium text-gray-800 dark:text-white">
                  Mathematics Quiz
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  Tomorrow • Calculus
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// Learning Page Component
const LearningPage = ({ user }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Learning Path
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Personalized learning recommendations and resources
        </p>
      </div>

      <LearningFeed studentId={user.id} />
    </motion.div>
  );
};

// Analytics Page Component
const AnalyticsPage = ({ user }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Detailed Analytics
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          In-depth analysis of your performance and learning patterns
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">
            Study Time Distribution
          </h3>
          <div className="h-64 flex items-center justify-center text-gray-500 dark:text-gray-400">
            Chart: Study time by subject
          </div>
        </div>

        <div className="card">
          <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">
            Performance Trends
          </h3>
          <div className="h-64 flex items-center justify-center text-gray-500 dark:text-gray-400">
            Chart: Score improvement over time
          </div>
        </div>

        <div className="card lg:col-span-2">
          <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">
            Topic-wise Analysis
          </h3>
          <div className="h-80 flex items-center justify-center text-gray-500 dark:text-gray-400">
            Heatmap: Topic mastery vs time spent
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// Footer Component
const Footer = () => {
  return (
    <footer className="mt-12 py-8 border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">ST</span>
              </div>
              <span className="text-xl font-bold text-gray-800 dark:text-white">
                SkillTwin
              </span>
            </div>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Transforming education through proactive evaluation and personalized learning.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-gray-800 dark:text-white mb-4">
              Product
            </h4>
            <ul className="space-y-2">
              {['Features', 'Pricing', 'API', 'Documentation'].map((item) => (
                <li key={item}>
                  <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-gray-800 dark:text-white mb-4">
              Company
            </h4>
            <ul className="space-y-2">
              {['About', 'Blog', 'Careers', 'Press'].map((item) => (
                <li key={item}>
                  <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-gray-800 dark:text-white mb-4">
              Support
            </h4>
            <ul className="space-y-2">
              {['Help Center', 'Contact Us', 'Privacy', 'Terms'].map((item) => (
                <li key={item}>
                  <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-800 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-gray-500 dark:text-gray-500">
            © {new Date().getFullYear()} SkillTwin. All rights reserved.
          </p>
          <div className="flex items-center gap-4">
            <a href="#" className="text-gray-500 dark:text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
              Twitter
            </a>
            <a href="#" className="text-gray-500 dark:text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
              LinkedIn
            </a>
            <a href="#" className="text-gray-500 dark:text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
              GitHub
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default App;