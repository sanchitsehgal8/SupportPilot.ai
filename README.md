# SupportPilot

**SupportPilot** — Smart Customer Support Automation System built with Flask, React, Supabase, and AI/ML.

A complete end-to-end production-ready customer support platform featuring:
- 🔐 JWT authentication + Supabase integration
- 🎫 Smart ticket management with ML-powered assignment
- 📊 Real-time analytics and dashboards
- 🤖 Sentiment analysis and priority prediction
- 💬 Comments and collaboration
- 👥 Multi-role support (Admin, Agent, Customer)

## Quick Start

### Prerequisites
- Python 3.10+
- Node 18+ and npm
- Supabase account (optional, demo mode works without it)

### Backend Setup

1. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r backend/requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials (or leave blank for demo mode)
   ```

3. **Run Flask server:**
   ```bash
   python backend/app.py
   ```
   Server runs at `http://localhost:5001`

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm start
   ```
   App opens at `http://localhost:3000`

### Database Setup (Supabase)

To use persistent database features:

1. Create a Supabase project at [https://supabase.com](https://supabase.com)
2. Copy your project URL and API key to `.env`
3. Run the SQL migration in Supabase dashboard:
   ```sql
   -- Copy contents from docs/supabase_migration.sql
   -- Run in Supabase > SQL Editor
   ```
4. Restart the Flask server

## Project Structure

```
SupportPilot/
├── backend/
│   ├── models/              # OOP data models (7 classes)
│   ├── services/            # Business logic services (6 classes)
│   ├── controllers/         # API endpoint handlers
│   ├── ml/                  # ML models and utilities
│   ├── utils/               # Supabase, JWT, validation helpers
│   ├── tests/               # Pytest unit tests
│   ├── app.py              # Flask application
│   ├── config.py           # Configuration management
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── pages/          # React pages (5 pages)
│   │   ├── components/     # Reusable components
│   │   ├── api/            # Axios API client
│   │   ├── App.js          # Main app component
│   │   └── styles.css      # Global styles
│   ├── package.json        # Node dependencies
│   └── public/
│
├── docs/
│   ├── supabase_migration.sql  # Database schema
│   ├── API_DOCS.md             # API reference
│   ├── ER_diagram.txt          # Database diagram
│   └── CLASS_DIAGRAM.txt       # Class structure
│
└── README.md
```

## API Documentation

### Authentication
- `POST /api/auth/register` — Create account
- `POST /api/auth/login` — Login and get JWT token
- `GET /api/auth/validate` — Validate token (requires auth)
- `POST /api/auth/refresh` — Refresh expired token

### Tickets
- `POST /api/tickets` — Create ticket (customer)
- `GET /api/tickets` — List tickets (filtered by role)
- `GET /api/tickets/<id>` — Get ticket details
- `PUT /api/tickets/<id>/status` — Update status (agent/admin)
- `POST /api/tickets/<id>/assign` — Assign to agent (admin)

### Comments
- `POST /api/tickets/<id>/comments` — Add comment
- `GET /api/tickets/<id>/comments` — List comments

### Analytics
- `GET /api/analytics/dashboard` — Dashboard stats (admin/agent)
- `GET /api/analytics/agents` — All agents performance (admin)
- `GET /api/analytics/agents/<id>` — Agent details

For complete API docs, see `docs/API_DOCS.md`.

## Features

### User Roles
- **Admin**: Full system control, user management, analytics
- **Agent**: Handle tickets, respond to customers, see dashboards
- **Customer**: Create tickets, track status, communicate

### AI/ML Features
- **Sentiment Analysis**: Classifies ticket tone (positive/neutral/negative)
- **Priority Prediction**: Automatically suggests priority level
- **Keyword Extraction**: Extracts key topics from tickets
- **Smart Assignment**: Routes tickets to best available agent

### Dashboard & Analytics
- Ticket metrics (total, open, in-progress, resolved)
- Sentiment distribution
- Agent performance tracking
- Response time analytics
- Category breakdown

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## ML Models

Optional: Train ML models for better predictions
```bash
python backend/ml/train_models.py
```

This creates pickled models in `backend/ml/` for sentiment and priority prediction.

## Environment Variables

Copy `.env.example` to `.env`:

| Variable | Description | Required |
|----------|-------------|----------|
| `FLASK_ENV` | `development` or `production` | No (default: development) |
| `SECRET_KEY` | Flask secret key | No (auto-generated) |
| `JWT_SECRET_KEY` | JWT signing secret | Yes |
| `SUPABASE_URL` | Your Supabase project URL | No (demo mode) |
| `SUPABASE_KEY` | Supabase service role key | No (demo mode) |
| `REACT_APP_API_URL` | Backend API URL | No (default: http://localhost:5001/api) |

## Deployment

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use a strong `JWT_SECRET_KEY`
- [ ] Configure Supabase RLS policies
- [ ] Use HTTPS
- [ ] Set secure CORS origins
- [ ] Use environment secrets (not `.env` file)
- [ ] Enable database backups
- [ ] Set up monitoring/logging

## Architecture

The project follows **clean architecture** with:
- **Models**: Pure data classes
- **Services**: Business logic and database operations
- **Controllers**: API request/response handling
- **Utils**: Shared helpers (JWT, validation, error handling)
- **ML**: Standalone ML utilities

**17+ OOP Classes** across all layers for maintainability and testability.

## License

MIT

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

Built with ❤️ using Flask, React, and Supabase

