#!/bin/bash

# AAN Site Deployment Script
# Rebuilds the MkDocs site and deploys to GitHub Pages
# Usage: ./deploy.sh [options] "commit message"
# Options:
#   -f, --fast    Skip local review and deploy immediately
#   -h, --help    Show this help message

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_review() {
    echo -e "${CYAN}[REVIEW]${NC} $1"
}

# Function to show help
show_help() {
    echo "AAN Site Deployment Script"
    echo ""
    echo "Usage: $0 [options] \"commit message\""
    echo ""
    echo "Options:"
    echo "  -f, --fast    Skip local review and deploy immediately"
    echo "  -h, --help    Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 \"Add new content\"                    # Deploy with review"
    echo "  $0 -f \"Quick typo fix\"                  # Fast deploy (skip review)"
    echo "  $0 --fast \"Emergency update\"            # Fast deploy (skip review)"
    echo ""
    echo "Default behavior includes local review before deployment."
    echo "Use -f or --fast to skip review for quick updates."
}

# Parse command line arguments
FAST_DEPLOY=false
COMMIT_MSG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--fast)
            FAST_DEPLOY=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            print_error "Unknown option $1"
            show_help
            exit 1
            ;;
        *)
            COMMIT_MSG="$1"
            shift
            ;;
    esac
done

# Set default commit message if none provided
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Rebuild site - $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Check if we're in the right directory
if [ ! -f "aan/mkdocs.yml" ]; then
    print_error "This script must be run from the root of the a-a-n.git.io repository"
    print_error "Expected to find aan/mkdocs.yml but it's not here"
    exit 1
fi

# Check if mkdocs is available
if ! command -v mkdocs &> /dev/null; then
    print_error "MkDocs is not installed or not in PATH"
    print_error "Please install MkDocs: pip install mkdocs mkdocs-material"
    exit 1
fi

print_status "Starting AAN site deployment..."
print_status "Commit message: $COMMIT_MSG"
if [ "$FAST_DEPLOY" = true ]; then
    print_warning "Fast deploy mode: Skipping local review"
fi

# Navigate to MkDocs directory and build
print_status "Building MkDocs site..."
cd aan
if mkdocs build; then
    print_success "MkDocs build completed successfully"
else
    print_error "MkDocs build failed"
    exit 1
fi
cd ..

# Check if there are any changes
print_status "Checking for changes..."
if git diff --quiet && git diff --cached --quiet; then
    print_warning "No changes detected. Nothing to deploy."
    exit 0
fi

# Show what files have changed
print_status "Files changed:"
git status --porcelain

# Local review step (unless fast deploy)
if [ "$FAST_DEPLOY" = false ]; then
    print_review "Starting local review process..."
    
    # Find an available port
    PORT=8000
    while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
        PORT=$((PORT + 1))
    done
    
    print_review "Starting local server on port $PORT..."
    
    # Start MkDocs server in background
    cd aan
    mkdocs serve --dev-addr=127.0.0.1:$PORT > /dev/null 2>&1 &
    SERVER_PID=$!
    cd ..
    
    # Wait a moment for server to start
    sleep 2
    
    # Try to open browser (works on macOS, Linux with xdg-open, Windows with start)
    LOCAL_URL="http://127.0.0.1:$PORT"
    print_review "Opening browser to $LOCAL_URL"
    
    if command -v open &> /dev/null; then
        # macOS
        open "$LOCAL_URL" 2>/dev/null || true
    elif command -v xdg-open &> /dev/null; then
        # Linux
        xdg-open "$LOCAL_URL" 2>/dev/null || true
    elif command -v start &> /dev/null; then
        # Windows
        start "$LOCAL_URL" 2>/dev/null || true
    else
        print_review "Please manually open: $LOCAL_URL"
    fi
    
    print_review "Review your changes in the browser."
    print_review "Check navigation, content, links, and formatting."
    echo ""
    
    # Prompt for confirmation
    while true; do
        echo -n -e "${CYAN}[REVIEW]${NC} Deploy these changes to production? (y/n): "
        read -r yn
        case $yn in
            [Yy]* ) 
                print_success "Proceeding with deployment..."
                break
                ;;
            [Nn]* ) 
                print_warning "Deployment cancelled by user"
                # Kill the server
                kill $SERVER_PID 2>/dev/null || true
                exit 0
                ;;
            * ) 
                echo "Please answer yes (y) or no (n)."
                ;;
        esac
    done
    
    # Kill the local server
    print_review "Stopping local server..."
    kill $SERVER_PID 2>/dev/null || true
    
    # Wait a moment for server to stop
    sleep 1
fi

# Add all changes
print_status "Adding changes to git..."
git add .

# Commit changes
print_status "Committing changes..."
if git commit -m "$COMMIT_MSG"; then
    print_success "Changes committed successfully"
else
    print_error "Git commit failed"
    exit 1
fi

# Push to GitHub
print_status "Pushing to GitHub..."
if git push origin main; then
    print_success "Successfully pushed to GitHub!"
    print_success "Site will be available at: https://alexithymiaawarenessnetwork.org"
    print_status "Note: GitHub Pages may take a few minutes to update"
else
    print_error "Git push failed"
    exit 1
fi

print_success "Deployment completed successfully! 🚀"
