#!/bin/bash

echo "🚀 Setting up SpineDev Platform..."

# Check prerequisites
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }

echo "✅ Prerequisites check passed"

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install
cd apps/web && npm install && cd ../..

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend && pip install -r requirements.txt && cd ..

# Copy environment files
echo "📝 Setting up environment files..."
if [ ! -f apps/web/.env.local ]; then
    cp apps/web/.env.example apps/web/.env.local
    echo "⚠️  Please configure apps/web/.env.local with your Supabase credentials"
fi

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "⚠️  Please configure backend/.env with your credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure environment variables in apps/web/.env.local and backend/.env"
echo "2. Run database migrations: cd backend && alembic upgrade head"
echo "3. Start development: npm run dev"
echo ""
echo "📚 See docs/SETUP.md for detailed instructions"
