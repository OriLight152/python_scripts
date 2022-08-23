import requests, re, json, os

NETEASE_API = 'https://music.163.com/api/pc/package/download/latest'
URL_PATTERN = 'NeteaseCloudMusic_Music_official_(.*).exe'
BARK_URL = 'https://push.amarea.cn/device_key/'

is_use_bark = False
print('[信息]脚本开始执行。')
if os.environ.get('BARK_DEVICE_KEY') is not None:
    is_use_bark = True
    BARK_URL = BARK_URL.replace('device_key', os.environ.get('BARK_DEVICE_KEY'))
    print(f'[信息]启用Bark推送，Bark URL：{BARK_URL}')
try:
    res = requests.get(url=NETEASE_API, allow_redirects=False)
    if res.ok and res.status_code == 302:
        version = re.findall(URL_PATTERN, res.headers['Location'])[0]
        version = version.rsplit('.', 1)
        version_name = version[0]
        version_build = int(version[1])
        with open('config.json', 'r') as f:
            data = f.read()
        version_local = json.loads(data)
        if version_local['build'] < version_build:
            print(f'[信息]检测到新版本 {version_name}[{version_build}]。')
            if is_use_bark:
                data = {
                    'title': '网易云版本',
                    'body': f'检测到新版本: {version_name} [{version_build}]'
                }
                response = requests.post(url=BARK_URL, data=data)
            version_local['name'] = version_name
            version_local['build'] = version_build
            with open('config.json', 'w') as f:
                f.write(json.dumps(version_local))
        else:
            print('[信息]未检测到新版本。')
except Exception as e:
    print('[错误]获取新版本错误，请检查配置。')
    print(e)
    if is_use_bark:
        data = {'title': '网易云版本', 'body': '获取新版本错误，请检查配置。'}
        response = requests.post(url=BARK_URL, data=data)
print('[信息]脚本执行完毕。')
