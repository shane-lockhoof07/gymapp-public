# 💪 GymApp - AI-Powered Workout Tracker

A full-stack fitness tracking application with AI-powered workout analysis and personalized recommendations.

![Tech Stack](https://img.shields.io/badge/Vue.js-3.x-green) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-blue) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue) ![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 🎯 Features

- **Workout Tracking**: Log exercises, sets, reps, and weights with an intuitive interface
- **AI Analysis**: Get personalized workout recommendations powered by Claude AI
- **Progress Visualization**: Track your fitness journey with interactive charts and heatmaps
- **Workout Planning**: Create and save workout templates for quick access
- **Exercise Database**: Comprehensive exercise library with muscle group targeting
- **User Profiles**: Personalized fitness goals and progress tracking

## 🛠️ Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vuetify 3** - Material Design component framework
- **Pinia** - State management
- **Axios** - HTTP client
- **Vite** - Build tool

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL databases with Python objects
- **PostgreSQL** - Relational database
- **Anthropic Claude API** - AI-powered analysis
- **Docker** - Containerization

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL 15+
- Docker (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gymapp.git
   cd gymapp
   ```

2. **Backend Setup**
   ```bash
   cd gymapp_website/gymapp-api
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your configuration
   
   # Run migrations
   python migrations/migration.py
   
   # Start the server
   python main.py
   ```

3. **Frontend Setup**
   ```bash
   cd gymapp_website/gymapp-ui
   
   # Install dependencies
   npm install
   
   # Start development server
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:7777
   - API Documentation: http://localhost:7778/docs

### Docker Setup (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📱 Usage

### Creating an Account
1. Navigate to the homepage
2. Click "Sign Up" and fill in your details
3. Set your fitness goals and experience level

### Logging Workouts
1. Go to the Workouts page
2. Click "Start Workout"
3. Add exercises and log your sets
4. Save your workout with notes

### AI Analysis
1. Navigate to the Analysis tab
2. Choose from:
   - Analyze recent workouts
   - Get a personalized workout plan
   - Create a long-term program
3. Chat with the AI coach for specific questions

## 🏗️ Architecture

```
gymapp/
├── gymapp_website/
│   ├── gymapp-ui/          # Vue.js frontend
│   │   ├── src/
│   │   │   ├── components/ # Reusable Vue components
│   │   │   ├── pages/      # Route pages
│   │   │   ├── stores/     # Pinia state management
│   │   │   └── api/        # API integration
│   │   └── ...
│   │
│   └── gymapp-api/         # FastAPI backend
│       ├── routers/        # API endpoints
│       ├── models/         # Database models
│       ├── utils/          # Utility functions
│       └── migrations/     # Database migrations
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/gymapp

# AI Configuration (Optional)
ANTHROPIC_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-3-haiku-20240307
CLAUDE_MAX_TOKENS=1500
CLAUDE_TEMPERATURE=0.7
```

## 📊 API Documentation

The API documentation is automatically generated and available at:
- Swagger UI: http://localhost:7778/docs
- ReDoc: http://localhost:7778/redoc

### Key Endpoints

- `POST /create` - Create new user
- `POST /login` - User authentication
- `GET /workouts` - Get user's workouts
- `POST /workouts` - Create new workout
- `GET /exercises` - Get exercise database
- `POST /analysis/chat` - AI workout analysis

## 🧪 Development

### Code Style
- Frontend: ESLint with Vue.js recommended rules
- Backend: Follow PEP 8 guidelines

### Adding New Features
1. Create feature branch: `git checkout -b feature/your-feature`
2. Implement changes with clear commits
3. Test thoroughly
4. Submit pull request

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Vue.js and Vuetify communities
- FastAPI documentation and examples
- Anthropic for Claude AI API
- All open-source contributors

---

Built with ❤️ by [Your Name]