
#!/bin/bash

# JARVIS AI Assistant Deployment Script

echo "🤖 Starting JARVIS AI Assistant deployment..."

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

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
        return 0
    else
        print_error "Python 3 not found. Please install Python 3.8 or higher."
        return 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
        return 0
    else
        print_error "pip3 not found. Please install pip."
        return 1
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install requirements
install_requirements() {
    print_status "Installing Python requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Requirements installed"
}

# Create directory structure
create_directories() {
    print_status "Creating directory structure..."
    mkdir -p config
    mkdir -p data
    mkdir -p logs
    mkdir -p assets/audio
    mkdir -p assets/images
    mkdir -p modules
    print_success "Directory structure created"
}

# Set up configuration files
setup_config() {
    print_status "Setting up configuration files..."
    
    # Create default config if it doesn't exist
    if [ ! -f "config/user_preferences.json" ]; then
        cat > config/user_preferences.json << EOF
{
    "voice_enabled": true,
    "wake_word": "jarvis",
    "confidence_threshold": 0.7,
    "response_speed": 1.0,
    "theme": "dark",
    "auto_save_conversations": true,
    "max_conversation_history": 100
}
EOF
        print_success "Default user preferences created"
    fi
    
    # Create Streamlit config
    mkdir -p .streamlit
    if [ ! -f ".streamlit/config.toml" ]; then
        cat > .streamlit/config.toml << EOF
[global]
developmentMode = false

[server]
headless = true
enableCORS = true
port = 8501

[theme]
primaryColor = "#00d4ff"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
font = "sans serif"

[browser]
gatherUsageStats = false
EOF
        print_success "Streamlit config created"
    fi
}

# Check system dependencies
check_system_deps() {
    print_status "Checking system dependencies..."
    
    # Check for audio libraries
    if command -v aplay &> /dev/null || command -v paplay &> /dev/null; then
        print_success "Audio system detected"
    else
        print_warning "Audio system not detected. Voice features may not work."
    fi
    
    # Check for portaudio (required for speech recognition)
    if ldconfig -p | grep -q portaudio; then
        print_success "PortAudio found"
    else
        print_warning "PortAudio not found. Install with: sudo apt-get install portaudio19-dev"
    fi
}

# Run the application
run_app() {
    print_status "Starting JARVIS AI Assistant..."
    print_status "Access the application at: http://localhost:8501"
    print_status "Press Ctrl+C to stop the application"
    streamlit run streamlit_app.py
}

# Main deployment process
main() {
    echo "🤖 JARVIS AI Assistant Deployment"
    echo "=================================="
    
    # Check prerequisites
    check_python || exit 1
    check_pip || exit 1
    
    # Setup environment
    create_venv
    activate_venv
    install_requirements
    
    # Setup application
    create_directories
    setup_config
    check_system_deps
    
    print_success "Deployment completed successfully!"
    echo ""
    print_status "To start JARVIS manually, run:"
    print_status "  source venv/bin/activate"
    print_status "  streamlit run streamlit_app.py"
    echo ""
    
    # Ask if user wants to start now
    read -p "Do you want to start JARVIS now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_app
    fi
}

# Run main function
main "$@"
