# Local Development Guide

## Prerequisites

- pyenv (for Python version management)
- Node.js 20+
- npm or yarn
- OpenAI API key

## Backend Setup with pyenv

### 1. Install Python 3.12

```bash
# Install pyenv if not already installed
brew install pyenv  # macOS
# or follow https://github.com/pyenv/pyenv#installation for Linux

# Install Python 3.12
pyenv install 3.12.0

# Set Python version for this project
pyenv local 3.12.0

# Verify
python --version
```

### 2. Create and Activate Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Or use pyenv-virtualenv
pyenv virtualenv 3.12.0 comic-env
pyenv local comic-env
```

### 3. Install Dependencies

```bash
# After activating venv
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Create .env file from template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

### 5. Run Backend Server

```bash
cd backend
source venv/bin/activate  # if not already activated
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000
API docs available at http://localhost:8000/docs

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
# Create frontend .env file
echo "VITE_API_URL=http://localhost:8000" > frontend/.env
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will be available at http://localhost:5173

## Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## CLI Usage

```bash
cd backend
source venv/bin/activate

# Generate a comic from text
python -m src.cli generate "Your story text here..." -o output.png -f png

# Show version
python -m src.cli version
```

## Troubleshooting

### pyenv Not Found in Shell

Add to your shell configuration (`~/.zshrc` or `~/.bashrc`):

```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Then reload your shell: `source ~/.zshrc`

### Python Version Issues

```bash
# Check current Python version
pyenv version

# Rehash shims
pyenv rehash

# Clear Python cache
pyenv uninstall 3.12.0
pyenv install 3.12.0
```

### Import Errors

Make sure you've activated the virtual environment and installed dependencies:

```bash
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

## Project Structure

```
ai_comic/
├── backend/
│   ├── src/
│   │   ├── cli.py              # CLI entry point
│   │   ├── main.py             # FastAPI app
│   │   ├── config.py           # Settings
│   │   ├── models.py           # Pydantic models
│   │   ├── utils/
│   │   │   └── logger.py       # Logging
│   │   └── services/
│   │       ├── story_processor.py   # Text parsing
│   │       ├── image_generator.py   # DALL-E integration
│   │       ├── comic_composer.py    # Image composition
│   │       └── comic_service.py     # Orchestrator
│   ├── requirements.txt
│   ├── Dockerfile
│   └── venv/                  # Virtual environment (gitignored)
├── frontend/
│   ├── src/
│   │   ├── api/                # API client
│   │   ├── components/         # Vue components
│   │   ├── stores/             # Pinia stores
│   │   ├── views/              # Page views
│   │   └── router/             # Vue Router
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml          # Docker deployment
├── .env.example                # Environment template
└── .gitignore
```

## Development Workflow

1. Make code changes
2. Run tests (`pytest` for backend, `npm test` for frontend)
3. Test locally with dev servers
4. Build Docker images and test (`docker-compose up --build`)
5. Commit changes

## Docker vs Local Development

| Task | Docker | Local (pyenv) |
|------|--------|----------------|
| Initial setup | `./start.sh` | Follow this guide |
| Running services | `docker-compose up` | Manual dev servers |
| Debugging | Container logs | Direct access |
| Hot reload | Limited | Full support |
| Production deploy | Docker only | Not recommended |