# NASDAQ Stock Agent

AI-powered NASDAQ stock analysis and investment recommendations using Langchain, Anthropic Claude, and real-time market data.

## Project Structure

```
nasdaq-stock-agent/
├── src/
│   ├── models/          # Data models and schemas
│   ├── services/        # Business logic services
│   ├── agents/          # Langchain agent orchestration
│   ├── api/             # FastAPI REST API components
│   └── config/          # Configuration management
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

### 4. Start MongoDB

Ensure MongoDB is running on `mongodb://localhost:27017/`

### 5. Run the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude access
- `MONGODB_URL`: MongoDB connection string (default: mongodb://localhost:27017/)
- `DEBUG`: Enable debug mode (default: false)

## Requirements

- Python 3.8+
- MongoDB
- Anthropic API key