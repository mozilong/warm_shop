#!/bin/bash
# Django项目权限配置脚本 - 适配warm_shop项目
# 使用说明：修改下方数据库密码后，执行 sh grant_permissions.sh

# ========== 配置项（根据你的实际情况修改） ==========
DB_USER="root"          # MySQL用户名
DB_PASS="123456"  # MySQL密码
DB_NAME="warm_shop"     # 数据库名
MYSQL_CMD="mysql -u${DB_USER} -p${DB_PASS} -N -e"

# ========== 开始执行权限配置 ==========
echo "===== 1. 检查数据库连接 ====="
${MYSQL_CMD} "USE ${DB_NAME};"
if [ $? -ne 0 ]; then
    echo "数据库连接失败！请检查用户名/密码/数据库名是否正确"
    exit 1
fi

echo -e "\n===== 2. 创建缺失的权限（users/goods应用） ====="
${MYSQL_CMD} "
USE ${DB_NAME};

-- 新增查看权限
INSERT INTO auth_permission (name, content_type_id, codename)
SELECT 
    CONCAT('Can view ', c.model),
    c.id,
    CONCAT('view_', c.model)
FROM django_content_type c
WHERE c.app_label IN ('users', 'goods')
  AND NOT EXISTS (
      SELECT 1 FROM auth_permission p 
      WHERE p.content_type_id = c.id 
        AND p.codename = CONCAT('view_', c.model)
  );

-- 新增添加权限
INSERT INTO auth_permission (name, content_type_id, codename)
SELECT 
    CONCAT('Can add ', c.model),
    c.id,
    CONCAT('add_', c.model)
FROM django_content_type c
WHERE c.app_label IN ('users', 'goods')
  AND NOT EXISTS (
      SELECT 1 FROM auth_permission p 
      WHERE p.content_type_id = c.id 
        AND p.codename = CONCAT('add_', c.model)
  );

-- 新增修改权限
INSERT INTO auth_permission (name, content_type_id, codename)
SELECT 
    CONCAT('Can change ', c.model),
    c.id,
    CONCAT('change_', c.model)
FROM django_content_type c
WHERE c.app_label IN ('users', 'goods')
  AND NOT EXISTS (
      SELECT 1 FROM auth_permission p 
      WHERE p.content_type_id = c.id 
        AND p.codename = CONCAT('change_', c.model)
  );

-- 新增删除权限
INSERT INTO auth_permission (name, content_type_id, codename)
SELECT 
    CONCAT('Can delete ', c.model),
    c.id,
    CONCAT('delete_', c.model)
FROM django_content_type c
WHERE c.app_label IN ('users', 'goods')
  AND NOT EXISTS (
      SELECT 1 FROM auth_permission p 
      WHERE p.content_type_id = c.id 
        AND p.codename = CONCAT('delete_', c.model)
  );
"

echo -e "\n===== 3. 为普通管理员分配权限 ====="
${MYSQL_CMD} "
USE ${DB_NAME};

INSERT INTO tb_users_user_permissions (user_id, permission_id)
SELECT 
    u.id, 
    p.id
FROM tb_users u
JOIN auth_permission p ON p.content_type_id IN (
    SELECT id FROM django_content_type WHERE app_label IN ('users', 'goods')
)
WHERE u.role = 'admin'
  AND NOT EXISTS (
      SELECT 1 FROM tb_users_user_permissions up 
      WHERE up.user_id = u.id 
        AND up.permission_id = p.id
  );
"

echo -e "\n===== 4. 为商户分配权限 ====="
${MYSQL_CMD} "
USE ${DB_NAME};

INSERT INTO tb_users_user_permissions (user_id, permission_id)
SELECT 
    u.id, 
    p.id
FROM tb_users u
JOIN auth_permission p ON p.content_type_id = (
    SELECT id FROM django_content_type WHERE app_label = 'goods' AND model = 'goods'
)
WHERE u.role = 'merchant'
  AND NOT EXISTS (
      SELECT 1 FROM tb_users_user_permissions up 
      WHERE up.user_id = u.id 
        AND up.permission_id = p.id
  );
"

echo -e "\n===== 5. 验证权限配置结果 ====="
echo "普通管理员权限数量："
${MYSQL_CMD} "
USE ${DB_NAME};
SELECT COUNT(*) FROM tb_users_user_permissions up
JOIN tb_users u ON up.user_id = u.id
WHERE u.role = 'admin';
"

echo -e "\n商户权限数量："
${MYSQL_CMD} "
USE ${DB_NAME};
SELECT COUNT(*) FROM tb_users_user_permissions up
JOIN tb_users u ON up.user_id = u.id
WHERE u.role = 'merchant';
"

echo -e "\n===== 权限配置完成！====="
echo "请重启Django服务：python manage.py runserver 0.0.0.0:8000"
