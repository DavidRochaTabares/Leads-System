# Architecture Documentation

## Overview

SpineDev Platform is built as a modular monorepo designed for long-term growth and maintainability.

## Design Principles

1. **Clean Architecture** - Business logic independent of frameworks
2. **Feature-Based Organization** - Code organized by business capability
3. **Separation of Concerns** - Clear boundaries between layers
4. **Scalability First** - Built to handle multiple internal tools
5. **No Over-Engineering** - Pragmatic solutions over theoretical perfection

## Backend Architecture

### Layer Structure

```
backend/
├── api/              # Presentation Layer
│   ├── routes/      # HTTP endpoints
│   ├── schemas.py   # Request/response models
│   └── dependencies.py
├── services/         # Application Layer
│   ├── auth_service.py
│   └── database.py
├── core/            # Domain Layer
│   ├── config.py
│   └── exceptions.py
├── models/          # Data Layer
│   ├── base.py
│   └── user.py
├── repositories/    # Data Access Layer
│   ├── base.py
│   └── user_repository.py
└── workers/         # Background Tasks
    └── base.py
```

### Key Patterns

**Repository Pattern**
- Abstracts data access
- Enables testing without database
- Centralizes query logic

**Dependency Injection**
- FastAPI's dependency system
- Loose coupling between layers
- Easy to mock for testing

**Service Layer**
- Contains business logic
- Orchestrates between repositories
- Independent of HTTP layer

## Frontend Architecture

### Structure

```
apps/web/src/
├── app/                    # Next.js App Router
│   ├── layout.tsx
│   ├── page.tsx
│   ├── login/
│   └── dashboard/
├── features/               # Feature Modules
│   ├── authentication/
│   │   ├── components/
│   │   └── hooks/
│   └── dashboard/
│       └── components/
└── shared/                 # Shared Resources
    ├── components/ui/
    ├── lib/
    └── stores/
```

### Key Patterns

**Feature-Based Organization**
- Each feature is self-contained
- Components, hooks, and logic together
- Easy to add/remove features

**Shared Resources**
- UI components (shadcn/ui)
- Utilities and helpers
- Global state (Zustand)

**Server/Client Separation**
- 'use client' directive for client components
- Server components by default
- Optimized bundle size

## Data Flow

### Authentication Flow

1. User enters credentials in LoginForm
2. Supabase Auth validates credentials
3. JWT token returned to client
4. Token stored and sent with API requests
5. Backend verifies token with Supabase
6. User record synced to local database

### API Request Flow

1. Client makes request via apiClient
2. JWT token included in Authorization header
3. FastAPI dependency validates token
4. Service layer processes request
5. Repository accesses database
6. Response returned through layers

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR,
    is_active BOOLEAN DEFAULT true,
    supabase_user_id VARCHAR UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

### Future Tables

As tools are added:
- prospecting_tasks
- proposals
- seo_audits
- projects
- etc.

## Deployment Architecture

### Docker Containers

- **web**: Next.js frontend (port 3000)
- **api**: FastAPI backend (port 8000)

### External Services

- **Supabase**: PostgreSQL database + Auth
- **Anthropic**: Claude AI API
- **Google**: Gemini AI API

### Networking

- Docker bridge network for container communication
- CORS configured for frontend-backend communication
- Environment-based configuration

## Security

### Authentication

- Supabase Auth handles user management
- JWT tokens for API authentication
- Tokens verified on every request

### Authorization

- User roles in database (future)
- Permission checks in service layer
- Row-level security in Supabase

### Data Protection

- Environment variables for secrets
- HTTPS in production
- SQL injection prevention via ORM

## Scalability Considerations

### Horizontal Scaling

- Stateless API design
- Database connection pooling
- Load balancer ready

### Vertical Scaling

- Async/await patterns
- Background workers for heavy tasks
- Database indexing

### Future Optimizations

- Redis for caching
- Message queue for workers
- CDN for static assets

## Testing Strategy

### Backend Testing

- Unit tests for services
- Integration tests for repositories
- E2E tests for API endpoints

### Frontend Testing

- Component tests with React Testing Library
- Integration tests for features
- E2E tests with Playwright

## Adding New Tools

### Steps

1. Create feature directory in `apps/web/src/features/`
2. Add database models in `backend/models/`
3. Create repositories in `backend/repositories/`
4. Implement services in `backend/services/`
5. Add API routes in `backend/api/routes/`
6. Build UI components in feature directory
7. Create migration for database changes

### Example: Adding Prospecting Engine

```
backend/
├── models/prospecting.py
├── repositories/prospecting_repository.py
├── services/prospecting_service.py
├── workers/prospecting_worker.py
└── api/routes/prospecting.py

apps/web/src/features/prospecting/
├── components/
├── hooks/
└── types/
```

## Maintenance

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Dependency Updates

```bash
# Frontend
npm update

# Backend
pip install -U -r requirements.txt
```

### Monitoring

- Application logs
- Database query performance
- API response times
- Error tracking (future: Sentry)
