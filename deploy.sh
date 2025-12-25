#!/bin/bash
# =============================================================================
# LABBAIK AI v6.0 - GitHub Deployment Script
# =============================================================================
# Run this script from your local machine after downloading the zip
# 
# Usage:
#   chmod +x deploy.sh
#   ./deploy.sh
# =============================================================================

set -e  # Exit on error

echo "🕋 LABBAIK AI v6.0 - Deployment Script"
echo "======================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if git is available
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed. Please install git first.${NC}"
    exit 1
fi

# Step 1: Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Please run this script from the labbaik-v6 directory${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Found app.py${NC}"

# Step 2: Initialize git if needed
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}📁 Initializing git repository...${NC}"
    git init
    git branch -M main
fi

# Step 3: Add remote (change URL if needed)
REPO_URL="https://github.com/mshadianto/umrah-planner.git"
echo -e "${YELLOW}🔗 Setting remote to: ${REPO_URL}${NC}"

# Remove existing remote if exists
git remote remove origin 2>/dev/null || true
git remote add origin $REPO_URL

# Step 4: Fetch and prepare for merge
echo -e "${YELLOW}📥 Fetching existing repository...${NC}"
git fetch origin main --depth=1 2>/dev/null || echo "Note: Could not fetch (new repo or network issue)"

# Step 5: Stage all files
echo -e "${YELLOW}📝 Staging all files...${NC}"
git add -A

# Step 6: Commit
COMMIT_MSG="🚀 LABBAIK AI v6.0 - Super Boom Edition

Features:
- 🎮 Gamification (10 levels, achievements, daily challenges)
- 🧭 Umrah Mandiri (Virtual Manasik, Budget AI, 20+ Doa)
- 👥 Umrah Bareng (Smart Matching, Trip Management)
- 💰 Cost Simulator (Real-time pricing)
- 🤖 AI Chat Assistant
- 📦 Booking System
- 🎨 BLACK GOLD Premium Theme

By MS Hadianto"

echo -e "${YELLOW}💾 Creating commit...${NC}"
git commit -m "$COMMIT_MSG" 2>/dev/null || echo "Note: Nothing to commit or already committed"

# Step 7: Push
echo -e "${YELLOW}🚀 Pushing to GitHub...${NC}"
echo ""
echo -e "${RED}⚠️  IMPORTANT: You may need to authenticate with GitHub${NC}"
echo "   - Use Personal Access Token (recommended)"
echo "   - Or configure SSH keys"
echo ""

read -p "Press Enter to push, or Ctrl+C to cancel..."

git push -u origin main --force

echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Go to https://share.streamlit.io"
echo "2. Deploy from: mshadianto/umrah-planner"
echo "3. Main file: app.py"
echo "4. Add secrets in App Settings"
echo ""
echo "🕋 LABBAIK - Panggilan-Nya, Langkahmu"
