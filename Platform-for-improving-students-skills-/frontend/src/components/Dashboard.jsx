import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  FiTrendingUp, 
  FiTarget, 
  FiClock,
  FiBarChart2,
  FiBookOpen,
  FiAward,
  FiActivity,
  FiUser
} from 'react-icons/fi';
import PredictionCard from './PredictionCard';
import AdaptiveTest from './AdaptiveTest';
import { performanceAPI } from '../services/api';
import { formatPercentage, timeAgo } from '../utils/helpers';

const Dashboard = ({ user }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchDashboardData();
  }, [user?.id]);

  const fetchDashboardData = async () => {
    setIsLoading(true);
    try {
      console.log('🔍 Fetching dashboard data for user:', user);
      console.log('🆔 User ID:', user?.id || user?.student_id);
      
      // Always use student_id field for API calls
      const userId = user?.student_id || 'student_001';
      
      console.log('📍 Using student_id for API call:', userId);
      
      const data = await performanceAPI.getDashboard(userId);
      const predictionData = await performanceAPI.getPrediction(userId);
      
      console.log('📊 Dashboard data:', data);
      console.log('🔮 Prediction data:', predictionData);
      
      // Handle the wrapped response structure
      setDashboardData(data.dashboard || data);
      setPrediction(predictionData);
    } catch (error) {
      console.error('❌ Failed to fetch dashboard data:', error);
      console.error('📍 Error details:', error.response?.data || error.message);
      // Try fallback to student_001 if current ID fails
      if (user?.id && user?.id !== 'student_001') {
        console.log('🔄 Trying fallback with student_001...');
        try {
          const fallbackData = await performanceAPI.getDashboard('student_001');
          const fallbackPrediction = await performanceAPI.getPrediction('student_001');
          setDashboardData(fallbackData.dashboard || fallbackData);
          setPrediction(fallbackPrediction);
          console.log('✅ Fallback successful with student_001');
        } catch (fallbackError) {
          console.error('❌ Fallback also failed:', fallbackError);
        }
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4 md:p-6">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse space-y-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-48 bg-gray-200 dark:bg-gray-800 rounded-xl" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800 p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2">
                Welcome back, <span className="text-blue-600 dark:text-blue-400">{user?.name}</span>
              </h1>
              <p className="text-gray-600 dark:text-gray-400">
                Your personalized learning dashboard • {user?.class_level}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 rounded-xl">
                <FiActivity className="text-green-500" />
                <span className="font-semibold text-gray-700 dark:text-gray-300">
                  Day {dashboardData?.stats?.streak_days || 0}
                </span>
              </div>
              <button className="p-2 bg-white dark:bg-gray-800 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                <FiUser className="text-xl text-gray-600 dark:text-gray-400" />
              </button>
            </div>
          </div>
        </motion.header>

        {/* Stats Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8"
        >
          {[
            {
              icon: FiTrendingUp,
              title: 'Overall Mastery',
              value: formatPercentage(dashboardData?.stats.overall_mastery || 0),
              color: 'from-blue-500 to-indigo-600',
              change: '+2.5%',
            },
            {
              icon: FiTarget,
              title: 'Weekly Goal',
              value: formatPercentage(dashboardData?.stats.weekly_goal_progress || 0),
              color: 'from-emerald-500 to-teal-600',
              change: 'On track',
            },
            {
              icon: FiBarChart2,
              title: 'Accuracy Rate',
              value: formatPercentage(dashboardData?.stats.accuracy_rate || 0),
              color: 'from-purple-500 to-pink-600',
              change: '+1.8%',
            },
            {
              icon: FiBookOpen,
              title: 'Questions Attempted',
              value: dashboardData?.stats.questions_attempted || 0,
              color: 'from-orange-500 to-red-600',
              change: 'Today: 24',
            },
          ].map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              className="card hover-lift"
            >
              <div className={`h-1 w-full mb-4 rounded-full bg-gradient-to-r ${stat.color}`} />
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-800 dark:text-white mt-1">
                    {stat.value}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">{stat.change}</p>
                </div>
                <div className={`p-3 rounded-xl bg-gradient-to-br ${stat.color} bg-opacity-10`}>
                  <stat.icon className="text-2xl text-gray-700 dark:text-gray-300" />
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Left Column - Prediction Card */}
          <div className="lg:col-span-2">
            <PredictionCard
              prediction={prediction?.prediction}
              riskLevel={prediction?.risk_level}
              weakTopics={prediction?.weak_topics}
            />
          </div>

          {/* Right Column - Quick Actions & Upcoming */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="card"
            >
              <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">
                Quick Actions
              </h3>
              <div className="space-y-3">
                {dashboardData?.quick_actions?.map((action, index) => (
                  <button
                    key={index}
                    className="w-full flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-xl">{action.icon}</span>
                      <span className="font-medium text-gray-700 dark:text-gray-300">
                        {action.action}
                      </span>
                    </div>
                    <span className="text-gray-500 dark:text-gray-400">→</span>
                  </button>
                ))}
              </div>
            </motion.div>

            {/* Upcoming Exams */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="card"
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-gray-800 dark:text-white">
                  Upcoming Exams
                </h3>
                <FiClock className="text-gray-500 dark:text-gray-400" />
              </div>
              <div className="space-y-4">
                {dashboardData?.upcoming_exams?.map((exam, index) => (
                  <div key={index} className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold text-gray-800 dark:text-white">
                        {exam.subject}
                      </span>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        exam.preparedness >= 70 ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300' :
                        exam.preparedness >= 50 ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300' :
                        'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300'
                      }`}>
                        {formatPercentage(exam.preparedness)} ready
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      {exam.topic}
                    </p>
                    <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-500">
                      <span>{exam.date}</span>
                      <span>{exam.days_left} days left</span>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>

        {/* Adaptive Test Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Adaptive Learning
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                Take a test that adapts to your skill level
              </p>
            </div>
            <div className="flex gap-2">
              {['Physics', 'Mathematics', 'Chemistry'].map((subject) => (
                <button
                  key={subject}
                  className="px-3 py-1 text-sm rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                >
                  {subject}
                </button>
              ))}
            </div>
          </div>
          <AdaptiveTest studentId={user.id} subject="Physics" />
        </motion.div>

        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="card"
        >
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-xl font-bold text-gray-800 dark:text-white">
                Recent Activity
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Your learning journey
              </p>
            </div>
            <button className="px-4 py-2 text-sm bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
              View All
            </button>
          </div>
          <div className="space-y-4">
            {dashboardData?.recent_activities?.map((activity, index) => (
              <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                    <FiAward className="text-blue-600 dark:text-blue-400" />
                  </div>
                  <div>
                    <div className="font-medium text-gray-800 dark:text-white">
                      {activity.title}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Score: {activity.score}/100 • {timeAgo(activity.date)}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                    {activity.score >= 70 ? 'Excellent' : activity.score >= 50 ? 'Good' : 'Needs Practice'}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-500">
                    {activity.type}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;