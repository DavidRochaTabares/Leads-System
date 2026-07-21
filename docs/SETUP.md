# Setup Guide

## Prerequisites

- **Node.js** 20+
- **Python** 3.13+
- **Docker** & Docker Compose
- **Supabase** account

## Initial Setup

### 1. Clone and Install

```bash
git clone <repository-url>
cd spinedev-platform
npm install
cd backend && pip install -r requirements.txt
```

### 2. Configure Supabase

1. Create a new Supabase project at https://supabase.com
2. Go to Project Settings > API
3. Copy your project URL and keys

### 3. Environment Variables

#### Frontend (`apps/web/.env.local`)

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Backend (`backend/.env`)

```env
ENVIRONMENT=development
DEBUG=true
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
JWT_SECRET_KEY=generate_a_secure_random_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
ALLOWED_ORIGINS=http://localhost:3000
```

### 4. Database Setup

Run migrations:

```bash
cd backend
alembic upgrade head
```

### 5. Create First User

In Supabase Dashboard:
1. Go to Authentication > Users
2. Add a new user with email/password
3. The user will be automatically synced to the database on first login

## Development

### Option 1: Local Development

**Terminal 1 - Frontend:**
```bash
cd apps/web
npm run dev
```

**Terminal 2 - Backend:**
```bash
cd backend
uvicorn api.main:app --reload
```

### Option 2: Docker Development

```bash
docker-compose -f docker-compose.dev.yml up
```

Then run frontend locally:
```bash
cd apps/web
npm run dev
```

## Production Deployment

### Using Docker Compose

```bash
docker-compose up -d
```

### Environment Variables

Create a `.env` file in the root with all production values.

## Verification

1. Frontend: http://localhost:3000
2. Backend API: http://localhost:8000
3. API Docs: http://localhost:8000/docs

## Troubleshooting

### Database Connection Issues

- Verify DATABASE_URL is correct
- Check Supabase project is active
- Ensure IP is whitelisted in Supabase

### Authentication Issues

- Verify Supabase keys are correct
- Check CORS settings in backend
- Ensure user exists in Supabase Auth

### Build Issues

- Clear node_modules and reinstall
- Clear Python cache: `find . -type d -name __pycache__ -exec rm -r {} +`
- Rebuild Docker images: `docker-compose build --no-cache`
