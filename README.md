# SpineDev Platform

Internal operating platform for SpineDev business operations.

## Architecture

This is a monorepo built with:

- **Frontend**: Next.js 15, TypeScript, TailwindCSS, shadcn/ui
- **Backend**: FastAPI, Python 3.13, Clean Architecture
- **Database**: Supabase PostgreSQL
- **Deployment**: Docker, Docker Compose

## Structure

```
spinedev-platform/
├── apps/web/              # Next.js frontend
├── backend/               # FastAPI backend
│   ├── api/              # API endpoints
│   ├── workers/          # Background workers
│   ├── core/             # Domain logic
│   ├── services/         # Application services
│   ├── models/           # Data models
│   └── repositories/     # Data access
├── packages/             # Shared packages
├── docker/               # Docker configurations
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.13+
- Docker & Docker Compose
- Supabase account

### Setup

1. Clone the repository
2. Copy environment files:
   ```bash
   cp apps/web/.env.example apps/web/.env.local
   cp backend/.env.example backend/.env
   ```
3. Install dependencies:
   ```bash
   npm install
   cd backend && pip install -r requirements.txt
   ```
4. Start development:
   ```bash
   docker-compose up
   ```

## Development

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## License

Proprietary - SpineDev Internal Use Only
