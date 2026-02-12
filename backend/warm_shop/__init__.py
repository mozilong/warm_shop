import pymysql
# 将pymysql伪装成MySQLdb，适配Django的MySQL驱动检测
pymysql.install_as_MySQLdb()
