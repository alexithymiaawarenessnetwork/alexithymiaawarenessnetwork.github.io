#!/bin/bash

# AAN Site Deployment Script
# Rebuilds the MkDocs site and deploys to GitHub Pages

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Get commit message from argument or use default
COMMIT_MSG="${1:-"Rebuild site - $(date '+%Y-%m-%d %H:%M:%S')"}"

print_status "Starting AAN site deployment..."
print_status "Commit message: $COMMIT_MSG"

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
