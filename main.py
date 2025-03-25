import time
import webview
import json5
import sys
import os
import asyncio
import httpx
from bs4 import BeautifulSoup
import re
from googletrans import Translator
from pystray import Icon, Menu, MenuItem
from PIL import Image
from notifypy import Notify
import threading
import webbrowser

httpx.Timeout(15)

base_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base_dir, 'config.json5'), 'r') as f:
    config = json5.load(f)

args = sys.argv[1:]

if '--dev-mode' in args:
    current_mode = 'dev'
else:
    current_mode = 'prod'

web_engine = None

try:
    web_engine = config['defaultWebEngine'][sys.platform]
except:
    web_engine = None

for argv in args:
    if argv.startswith('--web-engine='):
        web_engine = argv.split('=')[1]

loadFrom = config['prodModeLoadFrom']

if current_mode == 'dev':
    loadFrom = config['devModeLoadFrom']

dataDirPath = config[('dev' if current_mode == 'dev' else 'prod') + 'ModeDataDirPath'][sys.platform]

for argv in args:
    if argv.startswith('--data-dir='):
        dataDirPath = argv.split('=')[1]

dataDirPath = os.path.expandvars(dataDirPath)

if not os.path.exists(os.path.join(dataDirPath, 'userData.json5')):
    try:
        os.makedirs(dataDirPath)
    except:
        pass
    with open(os.path.join(dataDirPath, 'userData.json5'), 'w') as f:
        json5.dump({}, f)

with open(os.path.join(dataDirPath, 'userData.json5'), 'r+') as f:
    userData = json5.load(f)

def writeToUserData(userData):
    with open(os.path.join(dataDirPath, 'userData.json5'), 'w') as f:
        json5.dump(userData, f)

async def execAfterLoggedIn(bgm_login_window, endBangumiLogin):
    while True:
        await asyncio.sleep(0.5)
        try:
            if ('login' in bgm_login_window.get_current_url()) == False and ('FollowTheRabbit' in bgm_login_window.get_current_url()) == False:
                break
        except:
            break
        log('满足登录完成判定条件，准备检查登录状态')
    try:
        bgm_login_window.hide()
    except:
        pass
    await endBangumiLogin(bgm_login_window);

async def execAfterOauthComplete(bgm_login_window, endBangumiOauth, cookies):
    while True:
        await asyncio.sleep(0.5)
        try:
            if ('https://bgm.tv/oauth/' in bgm_login_window.get_current_url()) == False:
                break
        except:
            break
    try:
        bgm_login_window.hide()
    except:
        pass
    log('满足oauth完成判定条件，准备获取oauth结果')
    await endBangumiOauth(bgm_login_window, cookies);

class Bridge:
    def __init__(self):
        self.loginAttempt = None
        self.userInfoCache = {'cache': None, 'cacheOauthToken': None, 'username': None}
    def getAppName(self):
        return config['appName']
    def getAppVersion(self):
        return config['appVersion']
    def startBangumiLogin(self):
        self.loginAttempt = 'PENDING'
        log('开始尝试登录Bangumi')
        try:
            bgm_login_window = webview.create_window('Bangumi Login', 'https://bgm.tv/login')
            asyncio.run(execAfterLoggedIn(bgm_login_window, self.endBangumiLogin))
        except Exception as e:
            self.loginAttempt = 'FAILED'
            log(e)
    async def startBangumiOauth(self, bgm_login_window, cookies):
        log('开始尝试oauth')
        try:
            bgm_login_window.load_url('https://bgm.tv/oauth/authorize?client_id='+config['bangumiOauthApplication']['app_id']+'&response_type=code')
            bgm_login_window.show()
            await execAfterOauthComplete(bgm_login_window, self.endBangumiOauth, cookies)
        except Exception as e:
            self.loginAttempt = 'FAILED'
            log(e)
    async def endBangumiLogin(self, bgm_login_window):
        try:
            self.loginAttempt = 'OPERATING'
            await asyncio.sleep(8)
            cookies = bgm_login_window.evaluate_js('document.cookie')
            if 'chii_auth' in cookies:
                log('cookies中存在chii_auth，登录成功，准备尝试oauth登录')
                self.loginAttempt = 'OAUTH_PENDING'
                await self.startBangumiOauth(bgm_login_window, cookies)
            else:
                log('cookies中不存在chii_auth，登录失败')
                bgm_login_window.destroy()
                self.loginAttempt = 'FAILED'
        except Exception as e:
            try:
                bgm_login_window.destroy()
            except:
                pass
            self.loginAttempt = 'FAILED'
            log(e)
    async def endBangumiOauth(self, bgm_login_window, cookies):
        global userData
        try:
            self.loginAttempt = 'OPERATING_OAUTH'
            await asyncio.sleep(5)
            current_url = bgm_login_window.get_current_url()
            if current_url.startswith(config['bangumiOauthApplication']['cb']):
                log('已获取到oauth code')
                req = httpx.post('https://bgm.tv/oauth/access_token', data={
                    'client_id': config['bangumiOauthApplication']['app_id'],
                    'client_secret': config['bangumiOauthApplication']['app_secret'],
                    'grant_type': 'authorization_code',
                    'code': current_url.split('=')[1],
                    'redirect_uri': config['bangumiOauthApplication']['cb']
                }, timeout=20)
                if req.status_code == 200 and req.json().get('access_token') != None:
                    log('oauth登录成功')
                    userData['is_logged_in'] = True
                    userData['cookies'] = cookies
                    userData['oauthToken'] = req.json().get('access_token')
                    userData['expireAt'] = time.time() + req.json().get('expires_in')
                    writeToUserData(userData)
                    bgm_login_window.destroy()
                    self.loginAttempt = 'SUCCESS'
                else:
                    log('oauth登录失败')
                    bgm_login_window.destroy()
                    self.loginAttempt = 'FAILED'
            else:
                log('oauth登录失败')
                bgm_login_window.destroy()
                self.loginAttempt = 'FAILED'
                
        except Exception as e:
            try:
                bgm_login_window.destroy()
            except:
                pass
            self.loginAttempt = 'FAILED'
            log(e)
    def refreshToken(self):
        global userData
        req = httpx.post('https://bgm.tv/oauth/access_token', data={
            'client_id': config['bangumiOauthApplication']['app_id'],
            'client_secret': config['bangumiOauthApplication']['app_secret'],
            'grant_type': 'refresh_token',
            'refresh_token': userData['oauthToken'],
            'redirect_uri': config['bangumiOauthApplication']['cb']
        })
        if req.status_code == 200 and req.json().get('access_token') != None:
            userData['oauthToken'] = req.json().get('access_token')
            writeToUserData(userData)
            return True
        else:
            return False
    def queryLoginAttemptStatus(self):
        return self.loginAttempt
    def searchSubjectByKeyword(self, keyword):
        try:
            req = httpx.post('https://api.bgm.tv/v0/search/subjects', json={'keyword': keyword})
            log(req.text)
            if req.status_code == 200:
                return req.json()
        except:
            return None
    def sendGetReqToApiNoRetry(self, url):
        try:
            req = httpx.get(url, headers=self.getApiHeader())
            if req.status_code // 100 == 2:
                return req.json()
            else:
                if req.json()['title'] == 'Unauthorized':
                    self.exitLogin()
                    return {'error': 'Unauthorized'}
                return {'error': req.text}
        except Exception as e:
            return {'error': str(e)}
    def sendGetReqToApi(self, url):
        req = self.sendGetReqToApiNoRetry(url)
        if 'error' in req:
            for i in range(5):
                req = self.sendGetReqToApiNoRetry(url)
                if 'error' not in req:
                    return req
            return req
        else:
            return req
    def sendPostReqToApiNoRetry(self, url, data):
        try:
            req = httpx.post(url, json=data, headers=self.getApiHeader())
            if req.status_code // 100 == 2:
                return req.json()
            else:
                log(req.text)
                return {'error': req.text}
        except Exception as e:
            return {'error': str(e)}
    def sendPostReqToApi(self, url, data):
        req = self.sendPostReqToApiNoRetry(url, data)
        if 'error' in req:
            for i in range(5):
                req = self.sendPostReqToApiNoRetry(url, data)
                if 'error' not in req:
                    return req
            return req
        else:
            return req
    def sendPutReqToApiNoRetry(self, url, data):
        try:
            req = httpx.put(url, json=data, headers=self.getApiHeader())
            if req.status_code // 100 == 2:
                return req.json()
            else:
                log(req.text)
                return {'error': req.text}
        except Exception as e:
            return {'error': str(e)}
    def sendPutReqToApi(self, url, data):
        req = self.sendPutReqToApiNoRetry(url, data)
        if 'error' in req:
            for i in range(5):
                req = self.sendPutReqToApiNoRetry(url, data)
                if 'error' not in req:
                    return req
            return req
        else:
            return req
    def sendPatchReqToApiNoRetry(self, url, data):
        try:
            req = httpx.patch(url, json=data, headers=self.getApiHeader())
            if req.status_code // 100 == 2:
                return req.json()
            else:
                log(req.text)
                return {'error': req.text}
        except Exception as e:
            return {'error': str(e)}
    def sendPatchReqToApi(self, url, data):
        req = self.sendPatchReqToApiNoRetry(url, data)
        if 'error' in req:
            for i in range(5):
                req = self.sendPatchReqToApiNoRetry(url, data)
                if 'error' not in req:
                    return req
            return req
        else:
            return req
    def getCookiesAsObj(self):
        global userData
        cookies = {}
        for cookie in userData['cookies'].split(';'):
            cookie = cookie.split('=')
            cookies[cookie[0]] = cookie[1]
        return cookies
    def reqWebPage(self, url):
        try:
            
            req = httpx.get(url, headers={
                'User-Agent': config['userAgent']
            }, cookies=self.getCookiesAsObj(), timeout=15)
            if req.status_code == 200:
                return req.text
            else:
                return None
        except:
            return None
    def getLogin(self):
        global userData
        try:
            return {
                'is_logged_in': userData['is_logged_in'],
                'cookies': userData['cookies'],
                'oauthToken': userData['oauthToken']
            }
        except:
            return {
                'is_logged_in': False
            }
    def getApiHeader(self):
        global userData
        if userData['oauthToken'] == None:
            return {
                'User-Agent': config['userAgent']
            }
        return {
            'Authorization': 'Bearer ' + userData['oauthToken'],
            'User-Agent': config['userAgent']
        }
    def getUserInfo(self):
        global userData
        if self.userInfoCache['cache'] != None and self.userInfoCache['cacheOauthToken'] == userData['oauthToken']:
            return self.userInfoCache['cache']
        req = self.sendGetReqToApi('https://api.bgm.tv/v0/me')
        if req != None and req.get('error') == None:
            self.userInfoCache['cache'] = req
            self.userInfoCache['username'] = req['username']
            self.userInfoCache['cacheOauthToken'] = userData['oauthToken']
            return req
        else:
            if req.get('error') == 'Unauthorized':
                return {'error': 'Unauthorized'}
            return None
    def createHiddenWindowWithCookies(self, name, url):
        global userData
        window = webview.create_window(name, url)
        window.hide()
        try:
            time.sleep(2)
            for cookie in userData['cookies'].split(';'):
                window.evaluate_js('document.cookie="'+cookie+'"')
            window.evaluate_js('window.location.reload()')
            return window
        except:
            window.destroy()
            return None
    def getIndexTimeline(self, page = 1, auto_trigger = False):
        global userData
        if '=' not in userData['cookies']:
            return None
        html_content = self.reqWebPage('https://bgm.tv/timeline?type=all&page='+str(page))
        soup = BeautifulSoup(html_content, 'html.parser')

        if '所有人的时间胶囊' in soup.select_one('#header').get_text(strip=True):
            self.exitLogin()
            return {'error': 'Unauthorized'}

        verbs = ["看过", "玩过", "听过", "读过", "在看", "在玩", "在听", "在读", "想看", "想玩", "想听", "想读", "完成了", "搁置了", "抛弃了", "收藏了", "收藏了角色", "加为了好友", "添加了新游戏"]

        items = soup.select('.tml_item')
        results = []

        for i in range(len(items)):
            item = items[i].find(class_=['clearit', 'info'])
            if item == None:
                continue
            result = {}
            result['uuid'] = items[i].get('id')
            # 提取用户昵称和用户名
            a_tags = item.find_all('a')
            if a_tags[0].get_text(strip=True) == "":
                user_a = a_tags[1]
            else:
                user_a = a_tags[0]

            result['userNickname'] = user_a.get_text(strip=True) or None
            result['username'] = user_a['href'].split('/')[-1]

            # 提取动词
            item_text = item.get_text()
            for verb in verbs:
                if verb in item_text:
                    result['verb'] = verb
                    break
            else:
                result['verb'] = None

            # 提取目标
            result['target'] = []
            already_added_ids = []
            for link in a_tags:
                href = link.get('href')
                if (href.startswith('https://bgm.tv/subject/') or
                    href.startswith('https://bgm.tv/character/') or
                    href.startswith('https://bgm.tv/user/')):
                    if link.get_text(strip=True) != "":
                        id = href.split('/')[-1]
                        if id not in already_added_ids and ((href.startswith('https://bgm.tv/user/') and id == result['username']) == False):
                            type_ = 'subject' if 'subject' in href else 'character' if 'character' in href else 'user' if 'user' in href else None
                            result['target'].append({
                                'type': type_,
                                'id': id,
                                'name': link.get_text(strip=True)
                            })
                            already_added_ids.append(id)

            # 提取a_of_b
            result['a_of_b'] = None
            if result['verb'] == '完成了' and 'of' in item_text:
                matches = re.findall(r'\d+ of \d+ 话', item_text)
                if matches:
                    result['a_of_b'] = matches[0]
                else:
                    result['a_of_b'] = None
            
            # 提取头像地址
            img_tag = items[i].find(class_='avatarNeue')

            if img_tag:
                style = img_tag.get('style')
                if style:
                    matches = re.findall(r"url\('(.+)'\)", style)
                    if matches:
                        result['avatar'] = matches[0]
                    else:
                        result['avatar'] = None
                else:
                    result['avatar'] = None
            else:
                result['avatar'] = None

            if result['avatar'] == None:
                for beforeResult in results:
                    if beforeResult['username'] == result['username']:
                        result['avatar'] = beforeResult['avatar']
                        break

            result['date'] = None
            date_tag = items[i].find(class_='titleTip')
            if date_tag:
                result['date'] = date_tag.get('title')

            result['cover'] = None
            cover_tag = items[i].find(class_='cover')
            if cover_tag:
                img_cover_tag = cover_tag.find('img')
                if img_cover_tag:
                    result['cover'] = img_cover_tag['src']

            # 提取评论

            if items[i].find(class_='comment') != None:
                comment_tag = items[i].find(class_='comment')
                result['comment'] = comment_tag.get_text(strip=True)
            else:
                result['comment'] = None

            # 提取rating

            if items[i].find(class_='rateInfo') != None:
                items[i].find(class_='rateInfo').decompose()

            if items[i].find(class_='starlight') != None:
                rating_tag = items[i].find(class_='starlight')
                result['rating'] = rating_tag.get('class')[-1].replace("stars", "").replace(" ", "")
            else:
                result['rating'] = None

            results.append(result)
        
        if page == 1:
            if auto_trigger and userData.get('lastPullResult') != items[0].get('id') and userData.get('disableNotifications') != True:
                log('开始尝试发送通知')
                i = 0
                while i < 3 and i < len(results):
                    notify = Notify()
                    notify.title = 'Bangumium 新动态提醒'
                    notify.message = f"{results[i]['userNickname']}: {results[i]['verb']}了{results[i]['target'][0]['name']}"
                    notify.send()
                    if userData.get('lastPullResult') == items[0].get('id'):
                        break
                    i += 1
                log('通知发送完成')
            userData['lastPullResult'] = items[0].get('id')
            writeToUserData(userData)

        return results
    def getSubjectById(self, subject_id):
        return self.sendGetReqToApi('https://api.bgm.tv/v0/subjects/'+str(subject_id))
    def exitLogin(self):
        global userData
        userData['is_logged_in'] = False
        userData['cookies'] = None
        userData['oauthToken'] = None
        writeToUserData(userData)
        # clear cache
        self.userInfoCache['cache'] = None
        self.userInfoCache['cacheOauthToken'] = None
        self.userInfoCache['username'] = None
        return True
    def translateText(self, text):
        return asyncio.run(Translator().translate(text, dest='zh-cn')).text
    def getCollectStatusBySubjectId(self, id):
        return self.sendGetReqToApi('https://api.bgm.tv/v0/users/'+str(self.userInfoCache['username'])+'/collections/'+str(id))
    def saveCollectStatus(self, id, status, rank, tags, comment, isPrivate):
        data = {
            'type': status,
            'rate': rank,
            'tags': tags,
            'comment': comment,
            'private': isPrivate
        }
        log(data)
        result = self.sendPostReqToApi('https://api.bgm.tv/v0/users/-/collections/'+str(id), data)
        return result
    def getEpisodeStatusBySubjectId(self, id):
        return self.sendGetReqToApi('https://api.bgm.tv/v0/users/-/collections/'+str(id)+'/episodes')
    def getUserProgress(self, type):
        return self.sendGetReqToApi('https://api.bgm.tv/v0/users/'+str(self.userInfoCache['username'])+'/collections?subject_type='+str(type)+'&type=3&limit=30&offset=0')
    def getUserInfoByUsername(self, username):
        return self.sendGetReqToApi('https://api.bgm.tv/v0/users/'+str(username))
    def getUserCollectionListByUsername(self, username, type):
        return self.sendGetReqToApi('https://api.bgm.tv/v0/users/'+str(username)+'/collections?subject_type='+str(type)+'&limit=30&offset=0')
    def changeEpisodeStatus(self, epId, type):
        return self.sendPutReqToApi('https://api.bgm.tv/v0/users/-/collections/-/episodes/'+str(epId), {'type': type})
    def completedAllBeforeEp(self, subjectId, epId):
        all_eps = self.getEpisodeStatusBySubjectId(subjectId)['data']
        target_ids = []
        for ep in all_eps:
            if ep['episode']['id'] == epId:
                target_ids.append(ep['episode']['id'])
                break
            if ep['type'] != 2:
                target_ids.append(ep['episode']['id'])
        return self.sendPatchReqToApi('https://api.bgm.tv/v0/users/-/collections/'+str(subjectId)+'/episodes', {'episode_id': target_ids, 'type': 2})
    def getUserData(self):
        return userData
    def disable_notifications(self):
        global userData
        userData['disableNotifications'] = True
        writeToUserData(userData)
        return True
    def enable_notifications(self):
        global userData
        userData['disableNotifications'] = False
        writeToUserData(userData)
        return True
    def clearAllUserData(self):
        global userData
        userData = {}
        writeToUserData(userData)
        self.userInfoCache = {'cache': None, 'cacheOauthToken': None, 'username': None}
        return True
    def clearAllCache(self):
        self.userInfoCache = {'cache': None, 'cacheOauthToken': None, 'username': None}
        self.getUserInfo()
        return True
    def ZeroDivisionError(self):
        return 1/0
    def openUrl(self, url):
        webbrowser.open(url)
    def getCurrentTheme(self):
        return userData.get('theme')
    def setCurrentTheme(self, theme):
        global userData
        userData['theme'] = theme
        writeToUserData(userData)
    def updateVolStatus(self, subject_id, vol_status):
        self.sendPatchReqToApi('https://api.bgm.tv/v0/users/-/collections/' + str(subject_id), {'vol_status': int(vol_status)})

# tray icon

def toggle_window(icon, item):
    global main_window, is_main_window_shown
    if not is_main_window_shown:
        main_window.show()
        is_main_window_shown = True
    else:
        main_window.hide()
        is_main_window_shown = False;

def quit_app(icon, item):
    global main_window
    log('开始尝试销毁窗体')
    main_window.destroy()
    log('尝试关闭图标')
    icon.stop()
    log('尝试调用sys.exit进行退出')
    os._exit(0)
    sys.exit(0)
    exit(0)


def load_image():
    return Image.open(os.path.join(base_dir,"icon.png"))

tray_menu = Menu(
    MenuItem("显示/隐藏窗口", toggle_window),
    MenuItem("退出", quit_app)
)

icon_image = load_image()
tray_icon = Icon("TrayIcon", icon_image, "托盘图标", tray_menu)

tray_icon.run_detached()

# check timeline

def log(text: str):
    if current_mode == 'dev' or sys.platform != 'win32':
        print(text)
        
is_main_window_shown = False

def on_closing():
    global is_main_window_shown
    main_window.hide()
    is_main_window_shown = False
    return False

main_window = webview.create_window(config['appName'], loadFrom, js_api=Bridge())
is_main_window_shown = True
main_window.events.closing += on_closing
webview.start(gui=web_engine, debug = current_mode == 'dev', user_agent=config['userAgent'], private_mode=True)
