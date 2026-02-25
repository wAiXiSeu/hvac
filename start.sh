#!/bin/bash

# HVAC 启动脚本
# 启动后端和前端服务

set -e

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== HVAC 系统启动 ===${NC}"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 启动后端
start_backend() {
    echo -e "${YELLOW}启动后端服务...${NC}"
    cd "$SCRIPT_DIR/hvac-backend"
    
    # 检查并安装后端依赖
    if [ ! -d "venv" ] && [ ! -f "requirements.txt" ]; then
        echo "后端依赖未安装"
    fi
    
    # 激活虚拟环境（如果存在）
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    fi
    
    # 启动 FastAPI 服务
    echo -e "${GREEN}后端服务运行在: http://localhost:8000${NC}"
    uvicorn hvac_backend.main:app --host 0.0.0.0 --port 8000 --reload
}

# 启动前端
start_frontend() {
    echo -e "${YELLOW}启动前端服务...${NC}"
    cd "$SCRIPT_DIR/hvac-web"
    
    # 检查并安装前端依赖
    if [ ! -d "node_modules" ]; then
        echo "安装前端依赖..."
        npm install
    fi
    
    # 启动 Vite 开发服务器
    echo -e "${GREEN}前端服务运行在: http://localhost:5173${NC}"
    npm run dev
}

# 检查端口是否被占用
check_port() {
    local port=$1
    if lsof -i:$port > /dev/null 2>&1; then
        echo -e "${YELLOW}警告: 端口 $port 已被占用${NC}"
        return 1
    fi
    return 0
}

# 解析命令行参数
case "${1:-all}" in
    backend)
        start_backend
        ;;
    frontend)
        start_frontend
        ;;
    all|*)
        # 检查依赖并安装
        echo -e "${YELLOW}检查依赖...${NC}"
        
        # 后端依赖
        cd "$SCRIPT_DIR/hvac-backend"
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt -q 2>/dev/null || true
        fi
        
        # 前端依赖
        cd "$SCRIPT_DIR/hvac-web"
        if [ -f "package.json" ] && [ ! -d "node_modules" ]; then
            npm install
        fi
        
        # 后台启动后端
        start_backend &
        BACKEND_PID=$!
        
        # 等待后端启动
        sleep 2
        
        # 前台启动前端
        start_frontend
        
        # 捕获 Ctrl+C 时关闭后端
        trap "kill $BACKEND_PID 2>/dev/null" EXIT
        wait
        ;;
esac