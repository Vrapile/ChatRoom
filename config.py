# 默认输入的服务器地址，测试时候使用，避免登录总是输入地址麻烦
default_server = "127.0.0.1:1"

# 定义服务器端口，一个端口一个房间
PORT = range(1, 3)

# 图灵Tuling机器人还是ChatBot聊天机器人选择
BOTS = ["TuLing", "ChatBot", "User"]
BOT = BOTS[2]

# 浏览器请求头文件
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36', }
headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko)Chrome/62.0.3202.94 Safari/537.36'}

# 图灵密匙，自动回复地址，选择的key不同，tuling机器人的回答也各不相同
tuling_app_key = "e5ccc9c7c8834ec3b08940e290ff1559"
tuling_app_key2 = "4bc32d41c10be18627438ae45eb839ac"
tuling_url = "http://www.tuling123.com/openapi/api"

# 语音保存播放开关
VOICE_SWITCH = True

# 百度文本转语音地址和配置 tts地址
baidu_api_url = "http://tts.baidu.com/text2audio"
baidu_api_set = {"idx": 1, "cuid": "baidu_speech_demo", "cod": 2,
                 "lan": "zh", "ctp": 1, "pdt": 1, "spd": 4, "per": 4, "vol": 5, "pit": 5}

# 百度文字转语音 tsn地址
baidu_api_url2 = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
BaiDu_API_Key_GetVoi = "2NagVAULCYCnOnamrc8MNUPc"
BaiDu_Secret_Key_GetVoi = "af4860b64e77d187643db05ccdb060e4"

# 百度语音识别
BaiDu_App_ID = "10623076"
BaiDu_API_Key = "2NagVAULCYCnOnamrc8MNUPc"
BaiDu_Secret_Key = "af4860b64e77d187643db05ccdb060e4"
BaiDu_OpenApi_Url = "https://openapi.baidu.com/oauth/2.0/token" \
                    "?grant_type=client_credentials&client_id=%&client_secret=%"
