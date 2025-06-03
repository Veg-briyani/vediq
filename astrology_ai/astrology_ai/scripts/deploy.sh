#!/bin/bash

# Astrology AI - Quick Deploy Script
# Automatically commits and pushes changes to GitHub

echo "🚀 Astrology AI - Quick Deploy to GitHub"
echo "========================================"

# Check if we're in a git repository (check current dir and parent dir)
if [ ! -d ".git" ] && [ ! -d "../.git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Determine the git root directory
if [ -d ".git" ]; then
    GIT_ROOT="."
elif [ -d "../.git" ]; then
    GIT_ROOT=".."
    echo "📁 Git repository found in parent directory"
else
    echo "❌ Error: Git repository not found"
    exit 1
fi

# Change to git root directory
cd "$GIT_ROOT"

# Check for uncommitted changes
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ No changes to commit"
    echo "📡 Checking if remote is up to date..."
    git status
    exit 0
fi

# Add all changes
echo "📁 Adding all changes..."
git add .

# Get current timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Check if a commit message was provided as argument
if [ $# -eq 0 ]; then
    # Default commit message with timestamp
    COMMIT_MSG="🔄 Auto-update: $TIMESTAMP"
else
    # Use provided commit message
    COMMIT_MSG="$1"
fi

# Commit changes
echo "💾 Committing changes..."
git commit -m "$COMMIT_MSG"

# Check if commit was successful
if [ $? -eq 0 ]; then
    echo "✅ Changes committed successfully"
    
    # Push to GitHub
    echo "📡 Pushing to GitHub..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo "🎉 Successfully deployed to GitHub!"
        echo "🔗 Repository: https://github.com/Veg-briyani/vediq.git"
    else
        echo "❌ Failed to push to GitHub"
        exit 1
    fi
else
    echo "❌ Failed to commit changes"
    exit 1
fi

echo ""
echo "📊 Repository Status:"
git status

echo ""
echo "🏷️  Recent Commits:"
git log --oneline -3 