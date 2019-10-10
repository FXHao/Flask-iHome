# -*- coding:utf8 -*-


# 图片验证码的redis有效期，单位：秒
IMAGE_CODE_REDIS_EXPIRES = 3*60

# 短信验证码的redis有效期，单位：秒
SMS_CODE_REDIS_EXPIRES = 5*60

# 发送短信验证码的间隔
SEND_SMS_CODE_INTERAVL = 60

# 登陆错误尝试次数
LOGIN_ERROR_MAX_TIMES = 5

# 登陆错误限制时间 单位：秒
LOGIN_ERROR_FORBID_TIME = 10*60

# 七牛的域名
QINIU_URL_DOMAIN = "http://pysxg6c5p.bkt.clouddn.com/"

# 城区信息的缓存时间 单位：秒
AREA_INFO_REDIS_CAHAE_EXPIRES = 2*60*60

# 主页房屋显示最大条数
HOME_PAGE_MAX_HOUSES = 5

# 主页房屋图片redis缓存时间 单位：秒
HOME_PAGE_DATA_REDIS_EXPIRES = 2*60*60

# 房屋详情页面数据Redis缓存时间，单位：秒
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 2*60*60

# 房屋列表页面页数缓存时间，单位秒
HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES = 2*60*60

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋列表页面每页数据容量
HOUSE_LIST_PAGE_CAPACITY = 2