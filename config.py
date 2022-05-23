import os

# 是否开启debug模式
DEBUG = True  # 开发
# DEBUG = False

# 读取数据库环境变量
# 本地-开发
# username = os.environ.get("MYSQL_USERNAME", 'root')
# password = os.environ.get("MYSQL_PASSWORD", 'root')
# db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')

# 微信云外网
# username = os.environ.get("MYSQL_USERNAME", 'root')
# password = os.environ.get("MYSQL_PASSWORD", 'SJ1964swwhj')
# db_address = os.environ.get(
#     "MYSQL_ADDRESS", 'sh-cynosdbmysql-grp-n8ldyi7o.sql.tencentcdb.com:28135')

# 微信云内网
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'SJ1964swwhj')
db_address = os.environ.get("MYSQL_ADDRESS", '10.0.224.7:3306')
