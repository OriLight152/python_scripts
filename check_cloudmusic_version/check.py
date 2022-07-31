import requests, re, json

NETEASE_API = 'https://music.163.com/api/pc/package/download/latest'
URL_PATTERN = 'NeteaseCloudMusic_Music_official_(.*).exe'
BARK_URL = 'https://push.amarea.cn/yourkey/'

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
            data = {
                'title': '网易云版本',
                'body': f'检测到新版本: {version_name} [{version_build}]'
            }
            response = requests.post(url=BARK_URL, data=data)
            version_local['name'] = version_name
            version_local['build'] = version_build
            with open('config.json', 'w') as f:
                f.write(json.dumps(version_local))
except Exception as e:
    data = {'title': '网易云版本', 'body': f'获取新版本错误，请检查服务端配置。'}
    response = requests.post(url=BARK_URL, data=data)
