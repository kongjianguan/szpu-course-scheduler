import re

import requests

from .encrypt import encrypt_password

CAS_BASE = "https://authserver.szpu.edu.cn"
JWXT_BASE = "https://jwxt.szpu.edu.cn"


def _get_login_page(session: requests.Session) -> dict:
    url = f"{JWXT_BASE}/jwapp/sys/kcbcxmdl/*default/index.do"
    resp = session.get(url, allow_redirects=True)
    login_url = resp.url
    if "authserver" not in login_url:
        return {"skip": True, "session": session, "final_url": resp.url}
    html = resp.text
    execution = re.search(r'name="execution"\s+value="([^"]+)"', html)
    salt = re.search(r'id="pwdEncryptSalt"\s+value="([^"]+)"', html)
    need_captcha = bool(re.search(r'id="captchaImg"', html) or re.search(r'slider-captcha', html))
    return {
        "skip": False,
        "execution": execution.group(1) if execution else "e1s1",
        "salt": salt.group(1) if salt else "arSxEu10mMRZ0gYu",
        "login_url": login_url,
        "need_captcha": need_captcha,
    }


def _accept_tos(session: requests.Session) -> None:
    session.cookies.set("popYhxy", "true", domain="authserver.szpu.edu.cn", path="/")


def _submit_login(session: requests.Session, username: str, password: str, info: dict) -> None:
    data = {
        "username": username,
        "password": encrypt_password(password),
        "_eventId": "submit",
        "cllt": "userNameLogin",
        "dllt": "generalLogin",
        "execution": info["execution"],
        "lt": "",
    }
    resp = session.post(f"{CAS_BASE}/authserver/login", data=data, allow_redirects=False)
    ticket_url = resp.headers.get("Location", "")
    if not ticket_url or "ticket=" not in ticket_url:
        raise RuntimeError(f"登录失败 (HTTP {resp.status_code})")
    session.get(ticket_url, allow_redirects=True)


def login(username: str, password: str) -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/27.0 Safari/605.1.15"})
    info = _get_login_page(session)
    if info.get("skip"):
        return session
    if info["need_captcha"]:
        raise RuntimeError("需要验证码，暂时无法自动登录")
    _accept_tos(session)
    _submit_login(session, username, password, info)
    return session


def login_with_cookies(cookie_str: str) -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/27.0 Safari/605.1.15"})
    for item in cookie_str.split(";"):
        item = item.strip()
        if "=" in item:
            name, value = item.split("=", 1)
            session.cookies.set(name.strip(), value.strip())
    return session
