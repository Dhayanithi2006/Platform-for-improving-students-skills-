import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiClock, FiShield, FiEye, FiEyeOff, FiLock, FiCheckCircle, FiAlertCircle } from 'react-icons/fi';

const SecureExam = ({ examConfig, onExamComplete, onExit }) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeRemaining, setTimeRemaining] = useState(examConfig?.duration || 3600);
  const [isFullScreen, setIsFullScreen] = useState(false);
  const [tabSwitches, setTabSwitches] = useState(0);
  const [warnings, setWarnings] = useState([]);
  const [examStarted, setExamStarted] = useState(false);
  const [showConfirmExit, setShowConfirmExit] = useState(false);

  // Mock questions data
  const questions = examConfig?.questions || [
    {
      id: 1,
      question: "What is the primary purpose of adaptive learning systems?",
      options: [
        "To provide one-size-fits-all education",
        "To personalize learning based on individual performance",
        "To reduce teacher workload",
        "To increase standardization"
      ],
      correctAnswer: 1
    },
    {
      id: 2,
      question: "Which algorithm is commonly used in adaptive testing?",
      options: [
        "Linear regression",
        "Decision trees",
        "Item Response Theory (IRT)",
        "K-means clustering"
      ],
      correctAnswer: 2
    },
    {
      id: 3,
      question: "What is a key benefit of personalized learning paths?",
      options: [
        "Faster completion for all students",
        "Improved learning outcomes and engagement",
        "Reduced need for teachers",
        "Lower costs for educational institutions"
      ],
      correctAnswer: 1
    }
  ];

  // Timer effect
  useEffect(() => {
    if (examStarted && timeRemaining > 0) {
      const timer = setTimeout(() => {
        setTimeRemaining(timeRemaining - 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else if (timeRemaining === 0) {
      handleSubmitExam();
    }
  }, [timeRemaining, examStarted]);

  // Full screen monitoring
  useEffect(() => {
    const handleFullScreenChange = () => {
      setIsFullScreen(!!document.fullscreenElement);
      if (!document.fullscreenElement && examStarted) {
        handleTabSwitch();
      }
    };

    const handleVisibilityChange = () => {
      if (document.hidden && examStarted) {
        handleTabSwitch();
      }
    };

    const handleContextMenu = (e) => {
      e.preventDefault();
      addWarning("Right-click is disabled during the exam");
    };

    const handleKeyDown = (e) => {
      if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
        e.preventDefault();
        addWarning("Developer tools are disabled during the exam");
      }
      if (e.ctrlKey && e.key === 'c') {
        e.preventDefault();
        addWarning("Copy is disabled during the exam");
      }
    };

    document.addEventListener('fullscreenchange', handleFullScreenChange);
    document.addEventListener('visibilitychange', handleVisibilityChange);
    document.addEventListener('contextmenu', handleContextMenu);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('fullscreenchange', handleFullScreenChange);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      document.removeEventListener('contextmenu', handleContextMenu);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [examStarted]);

  const handleTabSwitch = () => {
    setTabSwitches(prev => prev + 1);
    addWarning("Tab switching detected! This may be flagged as suspicious activity.");
    
    if (tabSwitches >= 2) {
      addWarning("Multiple tab switches detected. Your exam may be flagged for review.");
    }
  };

  const addWarning = (message) => {
    setWarnings(prev => [...prev, { id: Date.now(), message, timestamp: new Date() }]);
  };

  const startExam = async () => {
    try {
      await document.documentElement.requestFullscreen();
      setExamStarted(true);
    } catch (error) {
      console.log("Full screen not available, starting exam anyway");
      setExamStarted(true);
    }
  };

  const handleAnswerSelect = (questionId, optionIndex) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: optionIndex
    }));
  };

  const handleNextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1);
    }
  };

  const handleSubmitExam = () => {
    const score = calculateScore();
    const results = {
      score,
      totalQuestions: questions.length,
      answers,
      timeSpent: (examConfig?.duration || 3600) - timeRemaining,
      tabSwitches,
      warnings: warnings.length,
      completedAt: new Date()
    };
    
    if (document.fullscreenElement) {
      document.exitFullscreen();
    }
    
    onExamComplete(results);
  };

  const calculateScore = () => {
    let correct = 0;
    questions.forEach(question => {
      if (answers[question.id] === question.correctAnswer) {
        correct++;
      }
    });
    return Math.round((correct / questions.length) * 100);
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (!examStarted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl shadow-xl p-8 max-w-2xl w-full"
        >
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
              <FiShield className="w-8 h-8 text-blue-600" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">Secure Exam Mode</h1>
            <p className="text-gray-600 mb-6">
              This exam will be monitored for academic integrity. Please read the instructions carefully.
            </p>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-blue-900 mb-2">Exam Instructions:</h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Full screen mode is required</li>
              <li>• Tab switching will be monitored and flagged</li>
              <li>• Right-click and developer tools are disabled</li>
              <li>• Copy/paste functionality is disabled</li>
              <li>• Multiple warnings may result in exam review</li>
            </ul>
          </div>

          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-gray-900 mb-2">Exam Details:</h3>
            <div className="text-sm text-gray-600 space-y-1">
              <p>• Duration: {Math.floor((examConfig?.duration || 3600) / 60)} minutes</p>
              <p>• Questions: {questions.length}</p>
              <p>• Format: Multiple choice</p>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={startExam}
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg transition duration-200"
            >
              Start Exam
            </button>
            <button
              onClick={onExit}
              className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-medium py-3 px-4 rounded-lg transition duration-200"
            >
              Exit
            </button>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <FiShield className="w-5 h-5 text-blue-600" />
              <span className="font-semibold text-gray-900">Secure Exam Mode</span>
              {!isFullScreen && (
                <span className="text-red-600 text-sm">⚠️ Full screen required</span>
              )}
            </div>
            
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2">
                <FiClock className="w-4 h-4 text-gray-600" />
                <span className={`font-mono font-semibold ${timeRemaining < 300 ? 'text-red-600' : 'text-gray-900'}`}>
                  {formatTime(timeRemaining)}
                </span>
              </div>
              
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">Question:</span>
                <span className="font-semibold text-gray-900">
                  {currentQuestion + 1} / {questions.length}
                </span>
              </div>
              
              {tabSwitches > 0 && (
                <div className="flex items-center space-x-1 text-red-600">
                  <FiAlertCircle className="w-4 h-4" />
                  <span className="text-sm">{tabSwitches} warnings</span>
                </div>
              )}
              
              <button
                onClick={() => setShowConfirmExit(true)}
                className="text-red-600 hover:text-red-700 font-medium text-sm"
              >
                Exit Exam
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Warnings */}
      {warnings.length > 0 && (
        <div className="bg-red-50 border-b border-red-200">
          <div className="max-w-7xl mx-auto px-4 py-2">
            <div className="flex items-center space-x-2 text-red-800">
              <FiAlertCircle className="w-4 h-4" />
              <span className="text-sm font-medium">
                Latest Warning: {warnings[warnings.length - 1].message}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <motion.div
          key={currentQuestion}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
          className="bg-white rounded-lg shadow-lg p-6"
        >
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Question {currentQuestion + 1}
            </h2>
            <p className="text-lg text-gray-800">
              {questions[currentQuestion].question}
            </p>
          </div>

          <div className="space-y-3 mb-8">
            {questions[currentQuestion].options.map((option, index) => (
              <label
                key={index}
                className={`flex items-center p-4 rounded-lg border-2 cursor-pointer transition-colors ${
                  answers[questions[currentQuestion].id] === index
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <input
                  type="radio"
                  name={`question-${questions[currentQuestion].id}`}
                  checked={answers[questions[currentQuestion].id] === index}
                  onChange={() => handleAnswerSelect(questions[currentQuestion].id, index)}
                  className="mr-3"
                />
                <span className="text-gray-800">{option}</span>
                {answers[questions[currentQuestion].id] === index && (
                  <FiCheckCircle className="w-5 h-5 text-blue-600 ml-auto" />
                )}
              </label>
            ))}
          </div>

          <div className="flex justify-between">
            <button
              onClick={handlePreviousQuestion}
              disabled={currentQuestion === 0}
              className="px-6 py-2 bg-gray-600 hover:bg-gray-700 disabled:bg-gray-400 text-white rounded-lg transition duration-200"
            >
              Previous
            </button>
            
            <div className="flex space-x-2">
              {Array.from({ length: questions.length }, (_, i) => (
                <button
                  key={i}
                  onClick={() => setCurrentQuestion(i)}
                  className={`w-8 h-8 rounded-full text-sm font-medium transition-colors ${
                    i === currentQuestion
                      ? 'bg-blue-600 text-white'
                      : answers[questions[i].id] !== undefined
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-200 text-gray-600'
                  }`}
                >
                  {i + 1}
                </button>
              ))}
            </div>
            
            {currentQuestion === questions.length - 1 ? (
              <button
                onClick={handleSubmitExam}
                className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition duration-200"
              >
                Submit Exam
              </button>
            ) : (
              <button
                onClick={handleNextQuestion}
                className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition duration-200"
              >
                Next
              </button>
            )}
          </div>
        </motion.div>
      </div>

      {/* Exit Confirmation Modal */}
      {showConfirmExit && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Exit Exam Confirmation
            </h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to exit the exam? Your progress will be lost and this action cannot be undone.
            </p>
            <div className="flex gap-4">
              <button
                onClick={() => {
                  setShowConfirmExit(false);
                  if (document.fullscreenElement) {
                    document.exitFullscreen();
                  }
                  onExit();
                }}
                className="flex-1 bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition duration-200"
              >
                Yes, Exit Exam
              </button>
              <button
                onClick={() => setShowConfirmExit(false)}
                className="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-lg transition duration-200"
              >
                Cancel
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default SecureExam;