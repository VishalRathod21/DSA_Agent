#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Update package lists
echo -e "${GREEN}Updating package lists...${NC}"
sudo apt-get update

# Install system dependencies
echo -e "\n${GREEN}Installing system dependencies...${NC}"
sudo apt-get install -y python3-pip python3-venv

# Create and activate virtual environment
echo -e "\n${GREEN}Setting up virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and setuptools
echo -e "\n${GREEN}Upgrading pip and setuptools...${NC}"
pip install --upgrade pip setuptools wheel

# Install Python dependencies
echo -e "\n${GREEN}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Install development dependencies if requested
if [[ $1 == "--dev" ]]; then
    echo -e "\n${GREEN}Installing development dependencies...${NC}"
    pip install -e ".[dev]"
fi

echo -e "\n${GREEN}✅ Setup complete!${NC}"
echo -e "Activate the virtual environment with: ${GREEN}source venv/bin/activate${NC}"
