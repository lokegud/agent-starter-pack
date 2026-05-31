#!/usr/bin/env bash
# Forgix installer — one-curl bootstrap
# Usage: curl -fsSL https://raw.githubusercontent.com/lokegud/agent-starter-pack/claude/self-building-ai-agent-d8sBn/forgix/install.sh | bash

set -euo pipefail

REPO="https://github.com/lokegud/agent-starter-pack"
BRANCH="claude/self-building-ai-agent-d8sBn"
FORGIX_DIR="$HOME/.forgix"
INSTALL_DIR="$FORGIX_DIR/src"

# Detect Termux/Android
IS_TERMUX=false
if [ -n "${PREFIX:-}" ] && echo "${PREFIX:-}" | grep -q "com.termux"; then
    IS_TERMUX=true
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

banner() {
cat << 'EOF'
  ___                _
 | __| ___  _ _ __ _(_)_ __
 | _| / _ \| '_/ _` | \ \ /
 |_|  \___/|_| \__, |_/_\_\
               |___/
 The anti-OpenClaw AI agent. Private. Secure. Local.
EOF
}

info()    { echo -e "${CYAN}[info]${NC} $*"; }
success() { echo -e "${GREEN}[ok]${NC}   $*"; }
warn()    { echo -e "${YELLOW}[warn]${NC} $*"; }
error()   { echo -e "${RED}[error]${NC} $*"; exit 1; }

banner
echo ""

# Check Python
if $IS_TERMUX; then
    info "Detected Android/Termux environment"
    PY=python
else
    for py in python3.12 python3.11 python3; do
        if command -v "$py" &>/dev/null; then
            PY="$py"
            break
        fi
    done
fi

command -v "${PY:-python3}" &>/dev/null || error "Python 3.11+ required. Install via: pkg install python (Termux) or https://python.org"

PY_VER=$("$PY" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
info "Python $PY_VER found"

# Check git
command -v git &>/dev/null || {
    if $IS_TERMUX; then
        info "Installing git via pkg..."
        pkg install -y git
    else
        error "git required. Install via your package manager."
    fi
}

# Clone / update
mkdir -p "$INSTALL_DIR"
if [ -d "$INSTALL_DIR/.git" ]; then
    info "Updating existing installation..."
    git -C "$INSTALL_DIR" pull origin "$BRANCH"
else
    info "Cloning Forgix..."
    git clone --depth=1 --branch "$BRANCH" "$REPO" "$INSTALL_DIR"
fi

# Create venv
VENV="$FORGIX_DIR/venv"
if [ ! -d "$VENV" ]; then
    info "Creating Python virtual environment..."
    "$PY" -m venv "$VENV"
fi

source "$VENV/bin/activate"
pip install --quiet --upgrade pip

info "Installing Forgix..."
pip install --quiet -e "$INSTALL_DIR/forgix"

if $IS_TERMUX; then
    info "Installing Android/Termux extras (llama-cpp-python ARM wheels)..."
    CMAKE_ARGS="-DLLAMA_BLAS=OFF" pip install --quiet "llama-cpp-python>=0.3"
    pip install --quiet "huggingface_hub>=0.24" "qrcode[pil]>=7.4"
else
    pip install --quiet "secretstorage" 2>/dev/null || true
fi

# Wrapper script
if $IS_TERMUX; then
    BIN_DIR="$PREFIX/bin"
else
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
fi

cat > "$BIN_DIR/forgix" << SCRIPT
#!/usr/bin/env bash
source "$VENV/bin/activate"
exec forgix "\$@"
SCRIPT
chmod +x "$BIN_DIR/forgix"

success "Forgix installed!"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo "  1. forgix setup"
echo "  2. forgix start"
if $IS_TERMUX; then
    echo ""
    echo -e "${YELLOW}Android tip:${NC} For same-WiFi access from other devices: forgix start --lan"
fi
