# scripts/init_db.py
import pymysql
import os
from config.config import DB_CONFIG

# 适配Docker环境变量（优先读取环境变量）
def get_db_config():
    config = DB_CONFIG.copy()
    if os.getenv("DB_HOST"):
        config["mysql"]["host"] = os.getenv("DB_HOST")
        config["mysql"]["port"] = int(os.getenv("DB_PORT", 3306))
        config["mysql"]["user"] = os.getenv("DB_USER", "root")
        config["mysql"]["password"] = os.getenv("DB_PASSWORD")
        config["mysql"]["db"] = os.getenv("DB_NAME", "warm_shop")
    return config

def init_mysql_db():
    config = get_db_config()
    if config["type"] != "mysql":
        print("当前配置为SQLite，无需初始化MySQL")
        return
    
    # 连接MySQL（先不指定数据库）
    conn = pymysql.connect(
        host=config["mysql"]["host"],
        port=config["mysql"]["port"],
        user=config["mysql"]["user"],
        password=config["mysql"]["password"],
        charset="utf8mb4"
    )
    cursor = conn.cursor()

    try:
        # 创建数据库（若不存在）
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['mysql']['db']} DEFAULT CHARACTER SET utf8mb4")
        conn.select_db(config["mysql"]["db"])

        # 创建核心表（示例：商品表、订单表）
        # 商品表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS goods (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL COMMENT '商品名称',
            price DECIMAL(10,2) NOT NULL COMMENT '商品价格',
            stock INT NOT NULL DEFAULT 0 COMMENT '库存',
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # 订单表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id VARCHAR(32) PRIMARY KEY COMMENT '订单号',
            goods_id INT NOT NULL COMMENT '商品ID',
            num INT NOT NULL COMMENT '购买数量',
            total_price DECIMAL(10,2) NOT NULL COMMENT '订单总价',
            status TINYINT DEFAULT 0 COMMENT '0-待支付 1-已支付 2-已完成 3-已取消',
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
            FOREIGN KEY (goods_id) REFERENCES goods(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        conn.commit()
        print("数据库初始化成功！")
    except Exception as e:
        conn.rollback()
        print(f"数据库初始化失败：{e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_mysql_db()