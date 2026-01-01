import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  FiBookOpen, 
  FiVideo, 
  FiFileText, 
  FiClock,
  FiTrendingUp,
  FiPlay,
  FiDownload,
  FiExternalLink
} from 'react-icons/fi';

const LearningFeed = ({ studentId }) => {
  const [feed, setFeed] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mock learning feed data
    const mockFeed = [
      {
        id: 1,
        type: 'video',
        title: 'Introduction to Thermodynamics',
        description: 'Learn the basics of heat and energy transfer',
        duration: '15 min',
        difficulty: 'Medium',
        thumbnail: '🎥',
        url: '#'
      },
      {
        id: 2,
        type: 'article',
        title: 'Calculus Fundamentals',
        description: 'Master derivatives and integrals',
        readTime: '10 min read',
        difficulty: 'Hard',
        thumbnail: '📄',
        url: '#'
      },
      {
        id: 3,
        type: 'practice',
        title: 'Physics Problem Set',
        description: 'Practice mechanics problems',
        questions: 20,
        difficulty: 'Easy',
        thumbnail: '📝',
        url: '#'
      },
      {
        id: 4,
        type: 'video',
        title: 'Organic Chemistry Basics',
        description: 'Understanding carbon compounds',
        duration: '20 min',
        difficulty: 'Medium',
        thumbnail: '🎥',
        url: '#'
      }
    ];

    setTimeout(() => {
      setFeed(mockFeed);
      setLoading(false);
    }, 1000);
  }, [studentId]);

  const getDifficultyColor = (difficulty) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/20';
      case 'medium': return 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/20';
      case 'hard': return 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900/20';
      default: return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/20';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'video': return <FiPlay className="w-4 h-4" />;
      case 'article': return <FiFileText className="w-4 h-4" />;
      case 'practice': return <FiBookOpen className="w-4 h-4" />;
      default: return <FiFileText className="w-4 h-4" />;
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-white dark:bg-gray-800 rounded-lg p-6 animate-pulse">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
              <div className="flex-1">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Learning Feed</h2>
        <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
          <FiTrendingUp className="w-4 h-4" />
          <span>Recommended for you</span>
        </div>
      </div>

      <div className="space-y-4">
        {feed.map((item, index) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 p-6 hover-lift"
          >
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-16 h-16 bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-lg flex items-center justify-center text-2xl">
                {item.thumbnail}
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-2">
                  <span className={`inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(item.difficulty)}`}>
                    {getTypeIcon(item.type)}
                    <span>{item.type}</span>
                  </span>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(item.difficulty)}`}>
                    {item.difficulty}
                  </span>
                </div>
                
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                  {item.title}
                </h3>
                
                <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">
                  {item.description}
                </p>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400">
                    {item.duration && (
                      <span className="flex items-center space-x-1">
                        <FiClock className="w-3 h-3" />
                        <span>{item.duration}</span>
                      </span>
                    )}
                    {item.readTime && (
                      <span className="flex items-center space-x-1">
                        <FiFileText className="w-3 h-3" />
                        <span>{item.readTime}</span>
                      </span>
                    )}
                    {item.questions && (
                      <span className="flex items-center space-x-1">
                        <FiBookOpen className="w-3 h-3" />
                        <span>{item.questions} questions</span>
                      </span>
                    )}
                  </div>
                  
                  <button className="flex items-center space-x-1 text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium">
                    <span>Start</span>
                    <FiExternalLink className="w-3 h-3" />
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {feed.length === 0 && (
        <div className="text-center py-12">
          <FiBookOpen className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No content available</h3>
          <p className="text-gray-500 dark:text-gray-400">
            Check back later for new learning materials.
          </p>
        </div>
      )}
    </div>
  );
};

export default LearningFeed;