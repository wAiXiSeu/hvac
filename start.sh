#!/bin/bash

# HVAC 启动脚本
# 启动后端和前端服务

set -e

# 定义颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 默认端口配置
DEFAULT_BACKEND_PORT=8000
DEFAULT_FRONTEND_PORT=5173

# 端口变量（可通过环境变量或命令行参数覆盖）
BACKEND_PORT=${BACKEND_PORT:-$DEFAULT_BACKEND_PORT}
FRONTEND_PORT=${FRONTEND_PORT:-$DEFAULT_FRONTEND_PORT}

# 显示帮助信息
show_help() {
    echo -e "${GREEN}HVAC 系统启动脚本${NC}"
    echo ""
    echo "用法: $0 [选项] [命令]"
    echo ""
    echo "命令:"
    echo "  all              启动后端和前端服务（默认）"
    echo "  backend          仅启动后端服务"
    echo "  frontend         仅启动前端服务"
    echo "  stop             停止所有服务"
    echo "  help             显示此帮助信息"
    echo ""
    echo "选项:"
    echo "  --backend-port PORT   指定后端端口（默认: $DEFAULT_BACKEND_PORT）"
    echo "  --frontend-port PORT  指定前端端口（默认: $DEFAULT_FRONTEND_PORT）"
    echo "  -h, --help            显示此帮助信息"
    echo ""
    echo "环境变量:"
    echo "  BACKEND_PORT    后端端口"
    echo "  FRONTEND_PORT   前端端口"
    echo ""
    echo "示例:"
    echo "  $0                                    # 使用默认端口启动所有服务"
    echo "  $0 --backend-port 8080                # 后端使用 8080 端口"
    echo "  $0 --frontend-port 3000               # 前端使用 3000 端口"
    echo "  $0 --backend-port 8080 --frontend-port 3000  # 自定义两个端口"
    echo "  BACKEND_PORT=8080 $0                  # 通过环境变量指定后端端口"
    echo "  $0 backend                            # 仅启动后端"
    echo "  $0 stop                               # 停止所有服务"
}

# 停止所有服务
stop_services() {
    echo -e "${YELLOW}停止所有服务...${NC}"
    
    # 停止后端
    if lsof -i:$BACKEND_PORT > /dev/null 2>&1; then
        echo -e "${YELLOW}停止后端服务（端口 $BACKEND_PORT）...${NC}"
        lsof -ti:$BACKEND_PORT | xargs kill -9 2>/dev/null || true
    fi
    
    # 停止前端
    if lsof -i:$FRONTEND_PORT > /dev/null 2>&1; then
        echo -e "${YELLOW}停止前端服务（端口 $FRONTEND_PORT）...${NC}"
        lsof -ti:$FRONTEND_PORT | xargs kill -9 2>/dev/null || true
    fi
    
    echo -e "${GREEN}所有服务已停止${NC}"
}

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 解析命令行参数
COMMAND="all"
while [[ $# -gt 0 ]]; do
    case $1 in
        --backend-port)
            BACKEND_PORT="$2"
            shift 2
            ;;
        --frontend-port)
            FRONTEND_PORT="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        backend|frontend|all|stop|help)
            COMMAND="$1"
            shift
            ;;
        *)
            echo -e "${RED}未知参数: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 处理 help 命令
if [ "$COMMAND" = "help" ]; then
    show_help
    exit 0
fi

# 处理 stop 命令
if [ "$COMMAND" = "stop" ]; then
    stop_services
    exit 0
fi

echo -e "${GREEN}=== HVAC 系统启动 ===${NC}"
echo -e "${GREEN}后端端口: $BACKEND_PORT${NC}"
echo -e "${GREEN}前端端口: $FRONTEND_PORT${NC}"

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
    echo -e "${GREEN}后端服务运行在: http://localhost:$BACKEND_PORT${NC}"
    uvicorn hvac_backend.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload
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
    
    # 创建或更新 .env 文件以配置 API 地址
    cat > .env.local << EOF
VITE_API_BASE_URL=http://localhost:$BACKEND_PORT
EOF
    
    # 启动 Vite 开发服务器
    echo -e "${GREEN}前端服务运行在: http://localhost:$FRONTEND_PORT${NC}"
    npm run dev -- --port $FRONTEND_PORT
}

# 检查端口是否被占用
check_port() {
    local port=$1
    local service=$2
    if lsof -i:$port > /dev/null 2>&1; then
        echo -e "${RED}错误: $service 端口 $port 已被占用${NC}"
        echo -e "${YELLOW}提示: 使用 '$0 stop' 停止现有服务，或使用其他端口${NC}"
        return 1
    fi
    return 0
}

# 执行命令
case "$COMMAND" in
    backend)
        check_port $BACKEND_PORT "后端" || exit 1
        start_backend
        ;;
    frontend)
        check_port $FRONTEND_PORT "前端" || exit 1
        start_frontend
        ;;
    all|*)
        # 检查端口
        check_port $BACKEND_PORT "后端" || exit 1
        check_port $FRONTEND_PORT "前端" || exit 1
        
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
