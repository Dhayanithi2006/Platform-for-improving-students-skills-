import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { 
  FiUpload, 
  FiFileText, 
  FiPieChart, 
  FiTrendingUp,
  FiClock,
  FiTarget,
  FiCheck,
  FiAlertTriangle
} from 'react-icons/fi';
import { paperAPI } from '../services/api';

const PaperUpload = ({ studentId }) => {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [quickText, setQuickText] = useState('');
  const [activeTab, setActiveTab] = useState('upload'); // 'upload' or 'text'

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === 'application/pdf') {
        setFile(droppedFile);
      } else {
        alert('Please upload a PDF file');
      }
    }
  }, []);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleTextSubmit = async () => {
    if (!quickText.trim()) {
      alert('Please enter paper text');
      return;
    }

    setIsUploading(true);
    try {
      const response = await paperAPI.quickAnalyze({
        paper_text: quickText,
        student_id: studentId
      });
      setAnalysis(response.analysis);
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Analysis failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first');
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('student_id', studentId);

    try {
      const response = await paperAPI.analyzePaper(formData);
      setAnalysis(response.analysis);
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const getDifficultyColor = (level) => {
    switch(level?.toLowerCase()) {
      case 'hard': return 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900/20';
      case 'medium': return 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/20';
      case 'easy': return 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/20';
      default: return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/20';
    }
  };

  const getPriorityColor = (priority) => {
    switch(priority?.toLowerCase()) {
      case 'high': return 'text-red-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Paper Analysis
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Upload question papers to get personalized study recommendations
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Upload/Input */}
        <div className="lg:col-span-1">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="card"
          >
            {/* Tabs */}
            <div className="flex mb-6 border-b border-gray-200 dark:border-gray-700">
              <button
                className={`flex-1 py-3 text-center font-medium ${
                  activeTab === 'upload'
                    ? 'text-blue-600 border-b-2 border-blue-600 dark:text-blue-400 dark:border-blue-400'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'
                }`}
                onClick={() => setActiveTab('upload')}
              >
                <FiUpload className="inline mr-2" />
                Upload PDF
              </button>
              <button
                className={`flex-1 py-3 text-center font-medium ${
                  activeTab === 'text'
                    ? 'text-blue-600 border-b-2 border-blue-600 dark:text-blue-400 dark:border-blue-400'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300'
                }`}
                onClick={() => setActiveTab('text')}
              >
                <FiFileText className="inline mr-2" />
                Paste Text
              </button>
            </div>

            {/* PDF Upload Section */}
            {activeTab === 'upload' && (
              <div>
                <div
                  className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
                    dragActive
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/10'
                      : 'border-gray-300 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500'
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                >
                  <FiUpload className="text-4xl text-gray-400 dark:text-gray-500 mx-auto mb-4" />
                  
                  {file ? (
                    <div className="mb-4">
                      <p className="font-medium text-gray-800 dark:text-white mb-1">
                        {file.name}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  ) : (
                    <>
                      <p className="text-gray-700 dark:text-gray-300 mb-2">
                        Drag & drop your question paper PDF here
                      </p>
                      <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                        or click to browse files
                      </p>
                    </>
                  )}
                  
                  <label className="cursor-pointer">
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                    <span className="inline-block px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-300">
                      Browse Files
                    </span>
                  </label>
                  
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-4">
                    Supports PDF files up to 10MB
                  </p>
                </div>
                
                <button
                  onClick={handleUpload}
                  disabled={!file || isUploading}
                  className="w-full mt-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-300 disabled:opacity-50"
                >
                  {isUploading ? 'Analyzing...' : 'Analyze Paper'}
                </button>
              </div>
            )}

            {/* Text Input Section */}
            {activeTab === 'text' && (
              <div>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Paste Question Paper Text
                  </label>
                  <textarea
                    value={quickText}
                    onChange={(e) => setQuickText(e.target.value)}
                    placeholder="Paste your question paper text here. Include question numbers and marks distribution for better analysis."
                    className="w-full h-64 p-4 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white resize-none"
                    rows={10}
                  />
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                    Tip: Include marks distribution for accurate difficulty analysis
                  </p>
                </div>
                
                <button
                  onClick={handleTextSubmit}
                  disabled={!quickText.trim() || isUploading}
                  className="w-full py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-300 disabled:opacity-50"
                >
                  {isUploading ? 'Analyzing...' : 'Analyze Paper Text'}
                </button>
              </div>
            )}
          </motion.div>
        </div>

        {/* Right Column - Analysis Results */}
        <div className="lg:col-span-2">
          {analysis ? (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-6"
            >
              {/* Overview Card */}
              <div className="card">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-xl font-bold text-gray-800 dark:text-white">
                      Paper Analysis Results
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Based on {analysis.metadata.subject} paper
                    </p>
                  </div>
                  <div className={`px-3 py-1 rounded-full ${getDifficultyColor(analysis.metadata.paper_difficulty_overall)}`}>
                    {analysis.metadata.paper_difficulty_overall} Difficulty
                  </div>
                </div>

                {/* Score Prediction */}
                {analysis.score_prediction.expected_score && (
                  <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/10 dark:to-indigo-900/10 rounded-xl">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-semibold text-gray-800 dark:text-white mb-1">
                          📈 Score Prediction
                        </h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Based on your current mastery
                        </p>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
                          {analysis.score_prediction.expected_score}/100
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          Expected Score
                        </div>
                      </div>
                    </div>
                    <div className="mt-4">
                      <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
                        <span>Score Range</span>
                        <span>
                          {analysis.score_prediction.score_range[0]} - {analysis.score_prediction.score_range[1]}
                        </span>
                      </div>
                      <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-blue-500 to-indigo-600"
                          style={{
                            width: `${analysis.score_prediction.expected_score}%`
                          }}
                        />
                      </div>
                      <div className="flex justify-between text-xs text-gray-500 dark:text-gray-500 mt-2">
                        <span>0</span>
                        <span>Confidence: {Math.round(analysis.score_prediction.confidence * 100)}%</span>
                        <span>100</span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Topic Distribution */}
                <div className="mb-6">
                  <h4 className="font-semibold text-gray-800 dark:text-white mb-4">
                    📊 Topic Distribution
                  </h4>
                  <div className="space-y-3">
                    {Object.entries(analysis.topic_distribution)
                      .sort((a, b) => b[1] - a[1])
                      .slice(0, 5)
                      .map(([topic, weight]) => (
                        <div key={topic} className="flex items-center justify-between">
                          <span className="text-gray-700 dark:text-gray-300">
                            {topic.replace('_', ' ').title()}
                          </span>
                          <div className="flex items-center gap-4">
                            <div className="w-32 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-gradient-to-r from-blue-500 to-indigo-600"
                                style={{ width: `${weight}%` }}
                              />
                            </div>
                            <span className="text-sm font-medium text-gray-800 dark:text-white w-12 text-right">
                              {weight.toFixed(1)}%
                            </span>
                          </div>
                        </div>
                      ))}
                  </div>
                </div>

                {/* Difficulty Analysis */}
                <div>
                  <h4 className="font-semibold text-gray-800 dark:text-white mb-4">
                    🎯 Difficulty Analysis
                  </h4>
                  <div className="grid grid-cols-3 gap-4">
                    {Object.entries(analysis.difficulty_analysis).map(([level, percent]) => (
                      <div key={level} className="text-center p-4 bg-gray-50 dark:bg-gray-800/50 rounded-xl">
                        <div className={`text-2xl font-bold mb-2 ${
                          level === 'hard' ? 'text-red-600 dark:text-red-400' :
                          level === 'medium' ? 'text-yellow-600 dark:text-yellow-400' :
                          'text-green-600 dark:text-green-400'
                        }`}>
                          {percent.toFixed(0)}%
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400 capitalize">
                          {level} Questions
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Recommendations */}
              <div className="card">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-xl font-bold text-gray-800 dark:text-white">
                      📚 Study Recommendations
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Personalized study plan based on analysis
                    </p>
                  </div>
                  <div className="flex items-center gap-2 text-blue-600 dark:text-blue-400">
                    <FiClock />
                    <span className="font-semibold">7-Day Plan</span>
                  </div>
                </div>

                <div className="space-y-4">
                  {analysis.recommendations.slice(0, 3).map((rec, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="p-4 border border-gray-200 dark:border-gray-700 rounded-xl"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <div className="flex items-center gap-3 mb-1">
                            <h4 className="font-semibold text-gray-800 dark:text-white">
                              {rec.topic}
                            </h4>
                            <span className={`px-2 py-1 text-xs rounded-full ${getPriorityColor(rec.priority)}`}>
                              {rec.priority.toUpperCase()} PRIORITY
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            Weight in paper: {rec.weight_in_paper}% • Current mastery: {rec.current_mastery}%
                          </p>
                        </div>
                        <div className="text-right">
                          <div className="text-lg font-bold text-blue-600 dark:text-blue-400">
                            {rec.recommended_time}
                          </div>
                          <div className="text-sm text-gray-500 dark:text-gray-500">
                            Recommended
                          </div>
                        </div>
                      </div>
                      
                      <div className="mb-3">
                        <h5 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Action Items:
                        </h5>
                        <ul className="space-y-1">
                          {rec.action_items.slice(0, 3).map((item, i) => (
                            <li key={i} className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                              <FiCheck className="text-green-500" />
                              {item}
                            </li>
                          ))}
                        </ul>
                      </div>
                      
                      <div>
                        <h5 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Resources:
                        </h5>
                        <div className="flex flex-wrap gap-2">
                          {rec.resources.slice(0, 3).map((resource, i) => (
                            <span
                              key={i}
                              className="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-full"
                            >
                              {resource}
                            </span>
                          ))}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Study Plan */}
              <div className="card">
                <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-6">
                  📅 7-Day Study Plan
                </h3>
                <div className="space-y-4">
                  {analysis.study_plan.schedule.map((day, index) => (
                    <div key={index} className="p-4 bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-800/50 dark:to-blue-900/10 rounded-xl">
                      <div className="flex items-center gap-3 mb-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                          <span className="text-white font-bold">D{index + 1}</span>
                        </div>
                        <div>
                          <h4 className="font-semibold text-gray-800 dark:text-white">
                            {day.day}: {day.focus}
                          </h4>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            Topics: {day.topics.join(', ')}
                          </p>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {day.activities.map((activity, i) => (
                          <span
                            key={i}
                            className="px-3 py-1 text-sm bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 rounded-lg"
                          >
                            {activity}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="card h-full flex flex-col items-center justify-center text-center p-12"
            >
              <div className="w-24 h-24 bg-gradient-to-br from-blue-100 to-indigo-100 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-full flex items-center justify-center mb-6">
                <FiPieChart className="text-4xl text-blue-500 dark:text-blue-400" />
              </div>
              <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-3">
                No Analysis Yet
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md">
                Upload a question paper or paste paper text to get personalized 
                analysis, score predictions, and study recommendations.
              </p>
              <div className="flex items-center gap-3 text-gray-500 dark:text-gray-500">
                <FiTrendingUp />
                <span>Get score predictions</span>
                <FiTarget />
                <span>Identify weak areas</span>
                <FiClock />
                <span>Plan study schedule</span>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PaperUpload;