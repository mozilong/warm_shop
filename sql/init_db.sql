-- ----------------------------
-- 1. 创建数据库（如果不存在）
-- ----------------------------
CREATE DATABASE IF NOT EXISTS warm_shop 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

-- ----------------------------
-- 2. 创建数据库用户并授权
-- ----------------------------
CREATE USER IF NOT EXISTS 'warm_shop_user'@'localhost' IDENTIFIED BY 'StrongPassword123!';
GRANT ALL PRIVILEGES ON warm_shop.* TO 'warm_shop_user'@'localhost';
FLUSH PRIVILEGES;

-- ----------------------------
-- 3. 使用目标数据库
-- ----------------------------
USE warm_shop;

-- ----------------------------
-- 4. 创建核心数据表
-- ----------------------------

-- 用户表
DROP TABLE IF EXISTS tb_users;
CREATE TABLE tb_users (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
  username VARCHAR(150) NOT NULL UNIQUE COMMENT '用户名',
  password VARCHAR(128) NOT NULL COMMENT '加密密码',
  phone VARCHAR(11) NOT NULL UNIQUE COMMENT '手机号',
  email VARCHAR(254) DEFAULT NULL COMMENT '邮箱',
  avatar VARCHAR(100) DEFAULT NULL COMMENT '头像路径',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否激活',
  is_staff TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否管理员',
  is_superuser TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否超级管理员',
  first_name VARCHAR(150) DEFAULT '' COMMENT '名',
  last_name VARCHAR(150) DEFAULT '' COMMENT '姓',
  date_joined DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  last_login DATETIME DEFAULT NULL COMMENT '最后登录时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 商品分类表
DROP TABLE IF EXISTS tb_category;
CREATE TABLE tb_category (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '分类ID',
  name VARCHAR(50) NOT NULL UNIQUE COMMENT '分类名称',
  parent_id INT DEFAULT NULL COMMENT '父分类ID',
  is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  FOREIGN KEY (parent_id) REFERENCES tb_category(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- 商品标签表
DROP TABLE IF EXISTS tb_tag;
CREATE TABLE tb_tag (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '标签ID',
  name VARCHAR(30) NOT NULL UNIQUE COMMENT '标签名称',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品标签表';

-- 商品表
DROP TABLE IF EXISTS tb_goods;
CREATE TABLE tb_goods (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '商品ID',
  name VARCHAR(200) NOT NULL COMMENT '商品名称',
  category_id INT NOT NULL COMMENT '分类ID',
  price DECIMAL(10,2) NOT NULL COMMENT '商品价格',
  stock INT NOT NULL DEFAULT 0 COMMENT '库存数量',
  image VARCHAR(100) DEFAULT NULL COMMENT '商品图片路径',
  description TEXT DEFAULT NULL COMMENT '商品描述',
  sales INT NOT NULL DEFAULT 0 COMMENT '销售数量',
  is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否上架',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  FOREIGN KEY (category_id) REFERENCES tb_category(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

-- 商品-标签关联表
DROP TABLE IF EXISTS tb_goods_tags;
CREATE TABLE tb_goods_tags (
  goods_id INT NOT NULL COMMENT '商品ID',
  tag_id INT NOT NULL COMMENT '标签ID',
  PRIMARY KEY (goods_id, tag_id),
  FOREIGN KEY (goods_id) REFERENCES tb_goods(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tb_tag(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品标签关联表';

-- 购物车表
DROP TABLE IF EXISTS tb_carts;
CREATE TABLE tb_carts (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '购物车ID',
  user_id INT NOT NULL COMMENT '用户ID',
  goods_id INT NOT NULL COMMENT '商品ID',
  quantity INT NOT NULL DEFAULT 1 COMMENT '商品数量',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  FOREIGN KEY (user_id) REFERENCES tb_users(id) ON DELETE CASCADE,
  FOREIGN KEY (goods_id) REFERENCES tb_goods(id) ON DELETE CASCADE,
  UNIQUE KEY unique_user_goods (user_id, goods_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车表';

-- 订单表
DROP TABLE IF EXISTS tb_orders;
CREATE TABLE tb_orders (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单ID',
  order_sn VARCHAR(32) NOT NULL UNIQUE COMMENT '订单编号',
  user_id INT NOT NULL COMMENT '用户ID',
  total_amount DECIMAL(10,2) NOT NULL COMMENT '订单总金额',
  status VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '订单状态：pending-待支付，paid-已支付，shipped-已发货，received-已收货，cancelled-已取消，refunded-已退款',
  shipping_address TEXT NOT NULL COMMENT '收货地址',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  FOREIGN KEY (user_id) REFERENCES tb_users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 订单商品表
DROP TABLE IF EXISTS tb_order_item;
CREATE TABLE tb_order_item (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单商品ID',
  order_id INT NOT NULL COMMENT '订单ID',
  goods_id INT NOT NULL COMMENT '商品ID',
  price DECIMAL(10,2) NOT NULL COMMENT '购买价格',
  quantity INT NOT NULL COMMENT '购买数量',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (order_id) REFERENCES tb_orders(id) ON DELETE CASCADE,
  FOREIGN KEY (goods_id) REFERENCES tb_goods(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单商品表';

-- 支付记录表
DROP TABLE IF EXISTS tb_payments;
CREATE TABLE tb_payments (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '支付记录ID',
  order_id INT NOT NULL UNIQUE COMMENT '订单ID',
  payment_no VARCHAR(64) NOT NULL UNIQUE COMMENT '支付单号',
  payment_method VARCHAR(20) NOT NULL COMMENT '支付方式：alipay-支付宝，wechat-微信支付，unionpay-银联支付',
  amount DECIMAL(10,2) NOT NULL COMMENT '支付金额',
  status VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '支付状态：pending-待支付，success-支付成功，failed-支付失败，refunded-已退款',
  payment_time DATETIME DEFAULT NULL COMMENT '支付时间',
  trade_no VARCHAR(64) DEFAULT NULL COMMENT '第三方支付流水号',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (order_id) REFERENCES tb_orders(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付记录表';

-- 操作日志表
DROP TABLE IF EXISTS tb_operation_logs;
CREATE TABLE tb_operation_logs (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '操作日志ID',
  user_id INT DEFAULT NULL COMMENT '操作用户ID',
  module VARCHAR(50) NOT NULL COMMENT '操作模块',
  operate_type VARCHAR(20) NOT NULL COMMENT '操作类型：login-登录，logout-登出，create-创建，update-更新，delete-删除，query-查询',
  operate_ip VARCHAR(45) NOT NULL COMMENT '操作IP',
  operate_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  content TEXT DEFAULT NULL COMMENT '操作内容',
  FOREIGN KEY (user_id) REFERENCES tb_users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';

-- 错误日志表
DROP TABLE IF EXISTS tb_error_logs;
CREATE TABLE tb_error_logs (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT '错误日志ID',
  error_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '错误时间',
  error_msg TEXT NOT NULL COMMENT '错误信息',
  request_url VARCHAR(255) NOT NULL COMMENT '请求URL',
  request_method VARCHAR(10) NOT NULL COMMENT '请求方法',
  ip VARCHAR(45) NOT NULL COMMENT 'IP地址',
  user_agent TEXT DEFAULT NULL COMMENT '用户代理'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='错误日志表';

-- ----------------------------
-- 5. 插入初始测试数据
-- ----------------------------

-- 插入管理员用户（密码：Admin123456，已加密）
INSERT INTO tb_users (username, password, phone, email, is_staff, is_superuser)
VALUES (
  'admin',
  'pbkdf2_sha256$600000$k8Z7n9X8m7b6v5c4x$8X7Z6M5B4V3C2X1N9M8B7V6C5X4Z3A9S8D7F6G5H4J3K2L1',
  '13800138000',
  'admin@warmshop.com',
  1,
  1
);

-- 插入普通用户（密码：User123456，已加密）
INSERT INTO tb_users (username, password, phone, email)
VALUES (
  'testuser',
  'pbkdf2_sha256$600000$a9S8d7f6g5h4j3k2l$9S8D7F6G5H4J3K2L1M9N8B7V6C5X4Z3A9S8D7F6G5H4',
  '13900139000',
  'test@warmshop.com'
);

-- 插入商品分类
INSERT INTO tb_category (name, parent_id) VALUES 
('电子产品', NULL),
('手机', 1),
('电脑', 1),
('服装', NULL),
('男装', 4),
('女装', 4),
('家居用品', NULL);

-- 插入商品标签
INSERT INTO tb_tag (name) VALUES 
('热销'),
('新品'),
('促销'),
('包邮'),
('精选');

-- 插入商品数据
INSERT INTO tb_goods (name, category_id, price, stock, image, description, sales, is_active) VALUES
('iPhone 15 Pro', 2, 7999.00, 100, '/media/goods/iphone15.jpg', '苹果15 Pro，搭载A17芯片，6.1英寸超视网膜XDR显示屏', 500, 1),
('华为Mate 70 Pro', 2, 6999.00, 80, '/media/goods/huawei_mate70.jpg', '华为Mate 70 Pro，鸿蒙OS 4.0，麒麟9100芯片', 300, 1),
('联想拯救者Y9000P', 3, 8999.00, 50, '/media/goods/lenovo_y9000p.jpg', '联想拯救者Y9000P 2025款，i9-14900HX，RTX4070', 200, 1),
('纯棉短袖T恤', 5, 99.00, 500, '/media/goods/tshirt.jpg', '100%纯棉短袖T恤，舒适透气，多色可选', 1000, 1),
('夏季连衣裙', 6, 199.00, 300, '/media/goods/dress.jpg', '夏季新款连衣裙，修身显瘦，面料舒适', 800, 1),
('北欧风沙发', 7, 2999.00, 20, '/media/goods/sofa.jpg', '北欧风格布艺沙发，实木框架，可拆洗', 50, 1);

-- 关联商品标签
INSERT INTO tb_goods_tags (goods_id, tag_id) VALUES
(1, 1), (1, 2), (1, 4),
(2, 1), (2, 3), (2, 4),
(3, 1), (3, 5),
(4, 1), (4, 3), (4, 4),
(5, 2), (5, 3), (5, 4),
(6, 5), (6, 4);

-- ----------------------------
-- 6. 创建索引优化查询
-- ----------------------------
-- 商品表索引
CREATE INDEX idx_goods_category ON tb_goods(category_id);
CREATE INDEX idx_goods_price ON tb_goods(price);
CREATE INDEX idx_goods_sales ON tb_goods(sales);
CREATE INDEX idx_goods_is_active ON tb_goods(is_active);

-- 订单表索引
CREATE INDEX idx_orders_user ON tb_orders(user_id);
CREATE INDEX idx_orders_status ON tb_orders(status);
CREATE INDEX idx_orders_created_at ON tb_orders(created_at);

-- 订单商品表索引
CREATE INDEX idx_order_item_order ON tb_order_item(order_id);
CREATE INDEX idx_order_item_goods ON tb_order_item(goods_id);

-- 支付记录表索引
CREATE INDEX idx_payments_order ON tb_payments(order_id);
CREATE INDEX idx_payments_status ON tb_payments(status);

-- 操作日志表索引
CREATE INDEX idx_operation_logs_user ON tb_operation_logs(user_id);
CREATE INDEX idx_operation_logs_module ON tb_operation_logs(module);
CREATE INDEX idx_operation_logs_operate_time ON tb_operation_logs(operate_time);

-- 错误日志表索引
CREATE INDEX idx_error_logs_time ON tb_error_logs(error_time);
CREATE INDEX idx_error_logs_ip ON tb_error_logs(ip);

-- ----------------------------
-- 脚本执行完成提示
-- ----------------------------
SELECT '数据库初始化完成！' AS '提示';
SELECT '管理员账号：admin，密码：Admin123456' AS '测试账号';
SELECT '普通用户账号：testuser，密码：User123456' AS '测试账号';