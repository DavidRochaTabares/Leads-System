# PowerShell setup script for Windows

Write-Host "🚀 Setting up SpineDev Platform..." -ForegroundColor Green

# Check prerequisites
$nodeInstalled = Get-Command node -ErrorAction SilentlyContinue
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
$dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue

if (-not $nodeInstalled) {
    Write-Host "❌ Node.js is required but not installed." -ForegroundColor Red
    exit 1
}

if (-not $pythonInstalled) {
    Write-Host "❌ Python is required but not installed." -ForegroundColor Red
    exit 1
}

if (-not $dockerInstalled) {
    Write-Host "❌ Docker is required but not installed." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Prerequisites check passed" -ForegroundColor Green

# Install frontend dependencies
Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Cyan
npm install
Set-Location apps/web
npm install
Set-Location ../..

# Install backend dependencies
Write-Host "📦 Installing backend dependencies..." -ForegroundColor Cyan
Set-Location backend
pip install -r requirements.txt
Set-Location ..

# Copy environment files
Write-Host "📝 Setting up environment files..." -ForegroundColor Cyan
if (-not (Test-Path "apps/web/.env.local")) {
    Copy-Item "apps/web/.env.example" "apps/web/.env.local"
    Write-Host "⚠️  Please configure apps/web/.env.local with your Supabase credentials" -ForegroundColor Yellow
}

if (-not (Test-Path "backend/.env")) {
    Copy-Item "backend/.env.example" "backend/.env"
    Write-Host "⚠️  Please configure backend/.env with your credentials" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Configure environment variables in apps/web/.env.local and backend/.env"
Write-Host "2. Run database migrations: cd backend && alembic upgrade head"
Write-Host "3. Start development: npm run dev"
Write-Host ""
Write-Host "📚 See docs/SETUP.md for detailed instructions" -ForegroundColor Cyan
