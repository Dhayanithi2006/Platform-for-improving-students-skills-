import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FiClock, 
  FiBarChart2, 
  FiCheck, 
  FiX,
  FiHelpCircle,
  FiTarget
} from 'react-icons/fi';
import { testAPI } from '../services/api';

const AdaptiveTest = ({ studentId, subject = 'Physics' }) => {
  const [testSession, setTestSession] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [timeLeft, setTimeLeft] = useState(60);
  const [showExplanation, setShowExplanation] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [testCompleted, setTestCompleted] = useState(false);
  const [score, setScore] = useState(null);
  const [difficulty, setDifficulty] = useState('medium');

  useEffect(() => {
    if (testSession) {
      const timer = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            handleTimeUp();
            return 60;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [testSession]);

  const startTest = async () => {
    setIsLoading(true);
    try {
      const response = await testAPI.startAdaptiveTest({
        student_id: studentId,
        subject: subject
      });
      setTestSession(response);
      setCurrentQuestion(response.question);
      setIsLoading(false);
    } catch (error) {
      console.error('Failed to start test:', error);
      setIsLoading(false);
    }
  };

  const handleAnswerSubmit = async () => {
    if (!userAnswer) return;

    setIsLoading(true);
    try {
      const response = await testAPI.submitAnswer({
        test_id: testSession.test_id,
        question_id: currentQuestion.id,
        answer: userAnswer,
        response_time: 60 - timeLeft
      });

      setShowExplanation(true);
      setDifficulty(getDifficultyText(response.ability_estimate));

      if (response.test_completed) {
        setTestCompleted(true);
        // Calculate final score
        const finalScore = calculateFinalScore(response);
        setScore(finalScore);
      } else {
        setTimeout(() => {
          setCurrentQuestion(response.next_question);
          setUserAnswer('');
          setShowExplanation(false);
          setTimeLeft(60);
          setIsLoading(false);
        }, 3000);
      }
    } catch (error) {
      console.error('Failed to submit answer:', error);
      setIsLoading(false);
    }
  };

  const handleTimeUp = () => {
    if (!showExplanation && currentQuestion) {
      handleAnswerSubmit();
    }
  };

  const calculateFinalScore = (response) => {
    // Simple scoring logic
    return Math.round(response.ability_estimate * 100);
  };

  const getDifficultyText = (ability) => {
    if (ability < 0.3) return 'Easy';
    if (ability < 0.7) return 'Medium';
    return 'Hard';
  };

  const getDifficultyColor = (level) => {
    switch(level?.toLowerCase()) {
      case 'easy': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300';
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300';
      case 'hard': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
    }
  };

  if (testCompleted) {
    return (
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="card text-center"
      >
        <div className="mb-6">
          <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-green-400 to-emerald-600 rounded-full flex items-center justify-center">
            <FiCheck className="text-white text-3xl" />
          </div>
          <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">
            Test Completed!
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Great job completing the adaptive test
          </p>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl">
            <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
              {score}/100
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Final Score
            </div>
          </div>
          <div className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-xl">
            <div className="text-xl font-bold text-purple-600 dark:text-purple-400">
              {difficulty}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Final Difficulty
            </div>
          </div>
        </div>

        <button
          onClick={startTest}
          className="w-full py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-300"
        >
          Start New Test
        </button>
      </motion.div>
    );
  }

  if (!testSession) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="card text-center"
      >
        <div className="mb-8">
          <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-blue-400 to-indigo-600 rounded-full flex items-center justify-center">
            <FiTarget className="text-white text-2xl" />
          </div>
          <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">
            Adaptive Test
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Questions adapt to your skill level in real-time
          </p>
          <div className="flex items-center justify-center gap-2 text-sm text-gray-500 dark:text-gray-400">
            <FiBarChart2 />
            <span>10 questions • AI-powered difficulty</span>
          </div>
        </div>

        <button
          onClick={startTest}
          disabled={isLoading}
          className="w-full py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-300 disabled:opacity-50"
        >
          {isLoading ? 'Starting Test...' : 'Start Test'}
        </button>
      </motion.div>
    );
  }

  return (
    <motion.div
      key={currentQuestion?.id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="card"
    >
      {/* Test Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-bold text-gray-800 dark:text-white">
            Adaptive Test
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Question {testSession.question_number} of {testSession.total_questions}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className={`px-3 py-1 rounded-full ${getDifficultyColor(difficulty)}`}>
            {difficulty}
          </div>
          <div className="flex items-center gap-2 text-orange-600 dark:text-orange-400">
            <FiClock />
            <span className="font-mono font-bold">{timeLeft}s</span>
          </div>
        </div>
      </div>

      {/* Question */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-4">
          <FiHelpCircle className="text-blue-500" />
          <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
            {currentQuestion?.subject} • {currentQuestion?.topic}
          </span>
        </div>
        <p className="text-lg text-gray-800 dark:text-gray-200 mb-6">
          {currentQuestion?.question_text}
        </p>

        {/* Options */}
        <div className="space-y-3">
          {currentQuestion?.options?.map((option, index) => (
            <motion.div
              key={index}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <label className={`flex items-center p-4 border rounded-xl cursor-pointer transition-all duration-200 ${
                userAnswer === String.fromCharCode(65 + index)
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-700'
              }`}>
                <input
                  type="radio"
                  name="answer"
                  value={String.fromCharCode(65 + index)}
                  checked={userAnswer === String.fromCharCode(65 + index)}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  className="mr-3 h-5 w-5 text-blue-600"
                />
                <span className="text-gray-800 dark:text-gray-200">
                  {option}
                </span>
              </label>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Explanation */}
      <AnimatePresence>
        {showExplanation && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-6 p-4 bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/10 dark:to-teal-900/10 rounded-xl"
          >
            <h4 className="font-semibold text-emerald-700 dark:text-emerald-400 mb-2">
              Explanation
            </h4>
            <p className="text-gray-700 dark:text-gray-300">
              {currentQuestion?.explanation}
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Action Buttons */}
      <div className="flex gap-3 mt-6">
        <button
          onClick={handleAnswerSubmit}
          disabled={!userAnswer || isLoading}
          className="flex-1 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-300 disabled:opacity-50"
        >
          {isLoading ? 'Checking...' : 'Submit Answer'}
        </button>
      </div>

      {/* Progress Indicator */}
      <div className="mt-6">
        <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
          <span>Test Progress</span>
          <span>{testSession.question_number}/{testSession.total_questions}</span>
        </div>
        <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-blue-500 to-indigo-600"
            initial={{ width: 0 }}
            animate={{ width: `${(testSession.question_number / testSession.total_questions) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>
    </motion.div>
  );
};

export default AdaptiveTest;