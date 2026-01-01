# SkillTwin - Student Skill Improvement Platform

A comprehensive web application for improving student skills through adaptive learning, performance prediction, and personalized learning paths.

## 🚀 Features

- **Adaptive Testing**: AI-powered tests that adjust difficulty based on student performance
- **Performance Prediction**: Machine learning models to predict student outcomes
- **Personalized Dashboard**: Real-time analytics and progress tracking
- **Paper Analysis**: Upload and analyze exam papers for improvement insights
- **Learning Feed**: Curated educational content recommendations

## 🛠 Technology Stack

### Backend
- **Flask** (Python web framework)
- **SQLite** (Database)
- **SQLAlchemy** (ORM)
- **Machine Learning** (Custom prediction engine)

### Frontend
- **React** (UI framework)
- **Tailwind CSS** (Styling)
- **Framer Motion** (Animations)
- **React Router** (Navigation)

## 📦 Installation & Setup

### Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- Git

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🌐 Deployment Options

### Option 1: Vercel (Recommended for Frontend)
1. Push code to GitHub
2. Connect repository to [Vercel](https://vercel.com)
3. Auto-deployment on every push

### Option 2: Netlify (Frontend)
1. Build frontend: `npm run build`
2. Upload `build/` folder to [Netlify](https://netlify.com)

### Option 3: Heroku (Full Stack)
1. Install Heroku CLI
2. Create `Procfile` for backend
3. Deploy both frontend and backend

### Option 4: Railway (Full Stack)
1. Connect GitHub repository to [Railway](https://railway.app)
2. Auto-detects and deploys both services

## 🔧 Environment Variables

Create `.env` file in backend:
```
FLASK_APP=app.py
FLASK_ENV=production
DATABASE_URL=sqlite:///skilltwin.db
SECRET_KEY=your-secret-key-here
```

## 📱 Demo Credentials

- **Email**: demo@skilltwin.com
- **Password**: demo123

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

## 📄 License

MIT License - feel free to use this project for learning and development.

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Contact the development team

---

**Built with ❤️ for educational empowerment**
