#!/bin/bash

# 灵魂伴侣 - 统一启动脚本
# 支持前后端分离启动、自动安装依赖、避免端口冲突

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
BACKEND_PORT=${BACKEND_PORT:-8010}
FRONTEND_PORT=${FRONTEND_PORT:-3008}
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 函数定义
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# 检查端口是否被占用
check_port() {
    local port=$1
    local port_name=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # 端口被占用
    else
        return 1  # 端口空闲
    fi
}

# 查找可用端口
find_available_port() {
    local start_port=$1
    local port=$start_port
    
    while check_port $port; do
        port=$((port + 1))
        if [ $port -gt $((start_port + 100)) ]; then
            echo ""
            return 1
        fi
    done
    
    echo $port
    return 0
}

# 显示使用说明
show_usage() {
    cat << EOF
${BLUE}灵魂伴侣 - 启动脚本${NC}

用法: ./start.sh [选项]

选项:
    ${GREEN}all${NC}         启动前后端（默认）
    ${GREEN}backend${NC}     仅启动后端服务
    ${GREEN}frontend${NC}    仅启动前端服务
    ${GREEN}--help${NC}      显示此帮助信息
    ${GREEN}--backend-port${NC} PORT   指定后端端口（默认8010）
    ${GREEN}--frontend-port${NC} PORT  指定前端端口（默认3008）

示例:
    ./start.sh all                          # 启动前后端
    ./start.sh backend                      # 仅启动后端
    ./start.sh frontend --frontend-port 3009  # 启动前端，指定端口3009

EOF
}

# 检查依赖
check_dependencies() {
    print_header "检查系统依赖"
    
    local missing_deps=0
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安装"
        missing_deps=1
    else
        print_success "Python3 已安装: $(python3 --version)"
    fi
    
    # 检查 Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js 未安装"
        missing_deps=1
    else
        print_success "Node.js 已安装: $(node --version)"
    fi
    
    # 检查 npm
    if ! command -v npm &> /dev/null; then
        print_error "npm 未安装"
        missing_deps=1
    else
        print_success "npm 已安装: $(npm --version)"
    fi
    
    if [ $missing_deps -eq 1 ]; then
        print_error "请先安装缺失的依赖"
        exit 1
    fi
}

# 安装后端依赖
install_backend_deps() {
    print_header "安装后端依赖"
    
    if [ ! -f "$PROJECT_DIR/requirements.txt" ]; then
        print_error "requirements.txt 不存在"
        return 1
    fi
    
    print_info "安装 Python 依赖..."
    cd "$PROJECT_DIR"
    
    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        print_info "创建虚拟环境..."
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 升级 pip
    pip install --upgrade pip setuptools wheel > /dev/null 2>&1
    
    # 安装依赖
    pip install -r requirements.txt > /dev/null 2>&1
    
    print_success "后端依赖安装完成"
}

# 安装前端依赖
install_frontend_deps() {
    print_header "安装前端依赖"
    
    if [ ! -f "$PROJECT_DIR/frontend/package.json" ]; then
        print_error "frontend/package.json 不存在"
        return 1
    fi
    
    print_info "安装 Node 依赖..."
    cd "$PROJECT_DIR/frontend"
    
    # 使用 npm ci 或 npm install
    if [ -f "package-lock.json" ]; then
        npm ci > /dev/null 2>&1
    else
        npm install > /dev/null 2>&1
    fi
    
    print_success "前端依赖安装完成"
}

# 启动后端
start_backend() {
    local port=$1
    
    print_header "启动后端服务"
    
    # 检查端口
    if check_port $port; then
        print_warning "端口 $port 已被占用，尝试查找可用端口..."
        port=$(find_available_port $port)
        if [ -z "$port" ]; then
            print_error "无法找到可用端口"
            return 1
        fi
        print_info "使用端口 $port"
    fi
    
    # 设置环境变量
    export FLASK_PORT=$port
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    
    # 检查 .env 文件
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        print_warning ".env 文件不存在，使用示例配置"
        if [ -f "$PROJECT_DIR/backend/.env.example" ]; then
            cp "$PROJECT_DIR/backend/.env.example" "$PROJECT_DIR/.env"
            print_info "已从 backend/.env.example 创建 .env"
        fi
    fi
    
    cd "$PROJECT_DIR"
    
    # 激活虚拟环境
    source venv/bin/activate
    
    print_info "启动 Flask 服务器..."
    print_success "后端服务运行在 http://localhost:$port"
    print_info "按 Ctrl+C 停止服务"
    echo ""
    
    python backend/app.py
}

# 启动前端
start_frontend() {
    local port=$1
    
    print_header "启动前端服务"
    
    # 检查端口
    if check_port $port; then
        print_warning "端口 $port 已被占用，尝试查找可用端口..."
        port=$(find_available_port $port)
        if [ -z "$port" ]; then
            print_error "无法找到可用端口"
            return 1
        fi
        print_info "使用端口 $port"
    fi
    
    cd "$PROJECT_DIR/frontend"
    
    print_info "启动 Vite 开发服务器..."
    print_success "前端服务运行在 http://localhost:$port"
    print_info "按 Ctrl+C 停止服务"
    echo ""
    
    # 设置环境变量
    export VITE_API_URL=http://localhost:${BACKEND_PORT}
    
    npm run dev -- --port $port
}

# 启动前后端
start_all() {
    print_header "灵魂伴侣 - 启动前后端服务"
    
    # 检查并调整端口
    local backend_port=$BACKEND_PORT
    local frontend_port=$FRONTEND_PORT
    
    if check_port $backend_port; then
        print_warning "后端端口 $backend_port 已被占用"
        backend_port=$(find_available_port $backend_port)
        if [ -z "$backend_port" ]; then
            print_error "无法找到可用的后端端口"
            exit 1
        fi
        print_info "使用后端端口 $backend_port"
    fi
    
    if check_port $frontend_port; then
        print_warning "前端端口 $frontend_port 已被占用"
        frontend_port=$(find_available_port $frontend_port)
        if [ -z "$frontend_port" ]; then
            print_error "无法找到可用的前端端口"
            exit 1
        fi
        print_info "使用前端端口 $frontend_port"
    fi
    
    # 启动后端（后台运行）
    print_info "启动后端服务..."
    (
        export FLASK_PORT=$backend_port
        export FLASK_ENV=development
        export FLASK_DEBUG=1
        cd "$PROJECT_DIR"
        source venv/bin/activate
        python backend/app.py
    ) &
    BACKEND_PID=$!
    
    sleep 2
    
    # 验证后端是否启动成功
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        print_error "后端启动失败"
        exit 1
    fi
    
    print_success "后端服务已启动 (PID: $BACKEND_PID)"
    print_success "后端地址: http://localhost:$backend_port"
    
    # 启动前端
    print_info "启动前端服务..."
    (
        export VITE_API_URL=http://localhost:$backend_port
        cd "$PROJECT_DIR/frontend"
        npm run dev -- --port $frontend_port
    ) &
    FRONTEND_PID=$!
    
    sleep 2
    
    # 验证前端是否启动成功
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        print_error "前端启动失败"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    
    print_success "前端服务已启动 (PID: $FRONTEND_PID)"
    print_success "前端地址: http://localhost:$frontend_port"
    
    echo ""
    print_header "启动完成"
    echo -e "${GREEN}前端地址: http://localhost:$frontend_port${NC}"
    echo -e "${GREEN}后端地址: http://localhost:$backend_port${NC}"
    echo ""
    print_info "按 Ctrl+C 停止所有服务"
    
    # 处理信号
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
    
    # 等待进程
    wait
}

# 主程序
main() {
    local mode="all"
    
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            all)
                mode="all"
                shift
                ;;
            backend)
                mode="backend"
                shift
                ;;
            frontend)
                mode="frontend"
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            --backend-port)
                BACKEND_PORT="$2"
                shift 2
                ;;
            --frontend-port)
                FRONTEND_PORT="$2"
                shift 2
                ;;
            *)
                print_error "未知选项: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # 检查依赖
    check_dependencies
    
    # 根据模式启动
    case $mode in
        all)
            install_backend_deps
            install_frontend_deps
            start_all
            ;;
        backend)
            install_backend_deps
            start_backend $BACKEND_PORT
            ;;
        frontend)
            install_frontend_deps
            start_frontend $FRONTEND_PORT
            ;;
        *)
            print_error "未知模式: $mode"
            show_usage
            exit 1
            ;;
    esac
}

# 运行主程序
main "$@"
