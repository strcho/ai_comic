# Comic Generation Agent

AI-powered automatic comic generation tool that transforms text stories into visual comics using OpenAI's DALL-E.

## Features

- 📝 **Text to Comic**: Convert story text into multi-panel comics
- 🎨 **AI Image Generation**: Powered by OpenAI DALL-E 3
- 🖼️ **Multiple Formats**: Export as PNG or PDF
- 🌐 **Web Interface**: Modern Vue 3 + TypeScript UI
- 🐳 **Docker Support**: Easy deployment with Docker Compose
- 🔧 **CLI Tool**: Command-line interface for batch processing
- 📊 **Real-time Progress**: Track generation progress in the UI

## Quick Start (Docker)

```bash
# 1. Clone and setup
git clone <repository>
cd ai_comic

# 2. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Start the application
./start.sh

# 4. Open browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

## Quick Start (Local Development with pyenv)

```bash
# 1. Setup environment (installs Python 3.12, creates venv)
./setup-local.sh

# 2. Start development servers
./start-local.sh

# 3. Open browser
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

See [LOCAL_DEV.md](LOCAL_DEV.md) for detailed local development setup.

## Architecture

```
┌─────────────┐
│   Vue 3 UI  │
│ (Frontend)  │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────┐
│  FastAPI    │
│  (Backend)  │
└──────┬──────┘
       │
       ├────────────┬────────────┐
       ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Story    │  │ Image    │  │ Comic    │
│ Parser   │  │ Generator│  │ Composer │
└──────────┘  └──────────┘  └──────────┘
                    │
                    ▼
              ┌──────────┐
              │ OpenAI   │
              │ DALL-E 3 │
              └──────────┘
```

### Backend Components

- **StoryProcessor**: Parses text into 2-5 scenes
- **ImageGenerator**: Creates images using OpenAI DALL-E
- **ComicComposer**: Composes panels into final comic (PNG/PDF)
- **ComicService**: Orchestrates the entire pipeline

### Frontend Components

- **StoryEditor**: Text input with scene preview
- **ConfigPanel**: Generation settings (style, size, format)
- **ProgressDisplay**: Real-time progress tracking
- **ComicPreview**: View and download generated comics

## Usage

### Web UI

1. Open http://localhost:3000 (Docker) or http://localhost:5173 (local)
2. Enter your story text in the editor
3. Configure generation settings (optional)
4. Click "Generate Comic"
5. Preview and download the result

### CLI

```bash
cd backend
source venv/bin/activate

# Generate a comic
python -m src.cli generate "Your story here..." -o comic.png -f png

# Show version
python -m src.cli version
```

### API

```bash
# Generate comic
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your story here...",
    "format": "png",
    "style": "vivid"
  }'

# Get task status
curl http://localhost:8000/api/task/{task_id}

# Download comic
curl -O http://localhost:8000/api/comic/{task_id}
```

## Configuration

Environment variables (see `.env.example`):

- `OPENAI_API_KEY`: Required - Your OpenAI API key
- `OPENAI_IMAGE_MODEL`: DALL-E model (default: dall-e-3)
- `IMAGE_SIZE`: Image size in pixels (default: 1024)
- `IMAGE_QUALITY`: standard or hd (default: standard)
- `CORS_ORIGINS`: Allowed frontend origins
- `LOG_LEVEL`: Logging level (default: INFO)

## Development

### Tech Stack

**Backend**:
- Python 3.12
- FastAPI
- OpenAI API
- Pillow (PIL)
- ReportLab

**Frontend**:
- Vue 3
- TypeScript
- Vite
- Element Plus
- Pinia
- Axios

### Local Development

See [LOCAL_DEV.md](LOCAL_DEV.md) for:
- pyenv setup
- Virtual environment creation
- Running tests
- Debugging tips

### Project Structure

```
ai_comic/
├── backend/              # Python/FastAPI backend
│   ├── src/
│   │   ├── services/    # Core logic
│   │   ├── utils/       # Utilities (logging, etc.)
│   │   ├── cli.py       # CLI entry point
│   │   └── main.py      # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # Vue 3 frontend
│   ├── src/
│   │   ├── components/  # Vue components
│   │   ├── views/       # Page views
│   │   ├── stores/      # Pinia stores
│   │   ├── api/         # API client
│   │   └── router/      # Vue Router
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── LOCAL_DEV.md          # Local dev guide
└── start.sh             # Docker quick start
```

## Deployment

### Docker

```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production

For production deployment:
1. Use environment variables for sensitive data
2. Enable HTTPS
3. Set up proper CORS origins
4. Configure rate limiting
5. Set up monitoring and logging

## Troubleshooting

### Docker build fails

```bash
# Clean and rebuild
docker-compose down
docker system prune -a
docker-compose up --build
```

### Python import errors

```bash
# Reinstall dependencies
cd backend
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Frontend build issues

```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## License

[Your License]

## Contributing

Contributions welcome! Please read our contributing guidelines.

## Support

- 📧 Email: [support email]
- 🐛 Issues: [GitHub issues]
- 📚 Docs: [documentation link]

---

Built with ❤️ using AI-powered image generation.