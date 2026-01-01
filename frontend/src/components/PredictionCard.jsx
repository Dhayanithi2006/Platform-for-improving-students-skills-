import React from 'react';
import { motion } from 'framer-motion';
import { 
  FiTrendingUp, 
  FiAlertTriangle, 
  FiCheckCircle,
  FiActivity 
} from 'react-icons/fi';
import { getRiskColor, formatPercentage } from '../utils/helpers';

const PredictionCard = ({ prediction, riskLevel, weakTopics }) => {
  const getRiskIcon = (level) => {
    switch(level?.toLowerCase()) {
      case 'high': return <FiAlertTriangle className="text-red-500" />;
      case 'medium': return <FiActivity className="text-yellow-500" />;
      case 'low': return <FiCheckCircle className="text-green-500" />;
      default: return <FiTrendingUp />;
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="card hover-lift"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-bold text-gray-800 dark:text-white">
            Performance Prediction
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Based on your recent activity
          </p>
        </div>
        <div className={`px-3 py-1 rounded-full flex items-center gap-2 ${getRiskColor(riskLevel)}`}>
          {getRiskIcon(riskLevel)}
          <span className="font-semibold capitalize">{riskLevel} Risk</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        {/* Predicted Score */}
        <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl">
          <div className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">
            {prediction?.predicted_score || '--'}/100
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Predicted Score
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-500 mt-1">
            Confidence: {prediction?.confidence || '--'}%
          </div>
        </div>

        {/* Confidence Interval */}
        <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-xl">
          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mb-2">
            {prediction?.confidence_interval?.[0] || '--'} - {prediction?.confidence_interval?.[1] || '--'}
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Expected Range
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-500 mt-1">
            Based on current performance
          </div>
        </div>

        {/* Improvement Potential */}
        <div className="text-center p-4 bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 rounded-xl">
          <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mb-2">
            +{prediction?.predicted_score ? Math.max(0, 85 - prediction.predicted_score) : '--'}%
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Improvement Potential
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-500 mt-1">
            With focused study
          </div>
        </div>
      </div>

      {/* Weak Topics */}
      <div className="mt-6">
        <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-4">
          Focus Areas
        </h4>
        <div className="space-y-3">
          {weakTopics?.map((topic, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg"
            >
              <div className="flex items-center gap-3">
                <div className={`w-3 h-3 rounded-full ${
                  topic.mastery >= 70 ? 'bg-green-500' :
                  topic.mastery >= 50 ? 'bg-yellow-500' : 'bg-red-500'
                }`} />
                <div>
                  <div className="font-medium text-gray-800 dark:text-gray-200">
                    {topic.topic}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {topic.subject}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <div className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                    {formatPercentage(topic.mastery)}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-500">
                    Mastery
                  </div>
                </div>
                <button className="px-3 py-1 text-sm bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400 rounded-lg hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors">
                  Study
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/10 dark:to-indigo-900/10 rounded-xl">
        <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-2">
          📝 Recommended Actions
        </h4>
        <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
          <li className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
            Complete 30-minute focused study on weak topics
          </li>
          <li className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 bg-purple-500 rounded-full" />
            Take adaptive mock test to identify gaps
          </li>
          <li className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full" />
            Review concept videos for difficult topics
          </li>
        </ul>
      </div>
    </motion.div>
  );
};

export default PredictionCard;