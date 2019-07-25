# coding:utf-8

import os


base_dir = os.path.dirname(os.path.dirname(__file__))

# Application配置参数

settings = {
    "static_path": os.path.join(base_dir, "static"),
    "template_path": os.path.join(base_dir, "template"),
    "cookie_secret":"kb8LwR4MSASQzT+HWLqy4YWnN1DJcEKJrjblnr77uSw=",
    "xsrf_cookies":True,
    "debug":True,
}

# mysql
mysql_options = dict(
    host="127.0.0.1",
    database="ihome",
    user="root",
    password="mysql"
)

# redis
redis_options = dict(
    host="127.0.0.1",
    port=6379 
)

log_file = os.path.join(base_dir, "logs/log.log")
log_level = "debug"

session_expires = 86400 # session数据有效期，秒

passwd_hash_key = "ihome@$^*" # 密码加密salt 

image_url_prefix = "http://oh6t1ds5l.bkt.clouddn.com/" # 七牛图片的域名