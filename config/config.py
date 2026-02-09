# config/config.py
# 数据库配置（支持MySQL/SQLite，SQLite无需配置账号密码，轻量化首选）
DB_CONFIG = {
    "type": "mysql",  # 可选：mysql/sqlite
    "mysql": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "your_mysql_password",  # 替换为实际密码
        "db": "warm_shop"  # 需提前创建该数据库
    },
    "sqlite": {
        "path": "./warm_shop.db"  # SQLite数据库文件路径
    }
}

# 服务器配置
SERVER_CONFIG = {
    "host": "0.0.0.0",  # 允许外网访问
    "port": 8000,       # 服务端口
    "reload": True      # 开发环境热重载，生产环境设为False
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "path": "./logs",   # 日志存储目录
    "max_size": 1024*1024*50  # 单日志文件最大50MB
}