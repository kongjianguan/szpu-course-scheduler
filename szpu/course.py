import json
from collections import defaultdict

import requests

JWXT_BASE = "https://jwxt.szpu.edu.cn"


def get_course_schedule(session: requests.Session, xh: str, xn: str, xq: int) -> list[dict]:
    payload = {"*order": "+SKXQ,+KSJC,+JSJC", "XNXQDM": f"{xn}-{xq}", "XH": xh}
    resp = session.post(
        f"{JWXT_BASE}/jwapp/sys/kcbcxmdl/KbcxController/queryxskb.do",
        data={"requestParamStr": json.dumps(payload, ensure_ascii=False)},
        headers={
            "X-Requested-With": "XMLHttpRequest",
            "Origin": JWXT_BASE,
            "Referer": f"{JWXT_BASE}/jwapp/sys/kcbcxmdl/*default/index.do",
        },
    )
    resp.raise_for_status()
    rows = resp.json().get("datas", {}).get("queryxskb", {}).get("rows", [])
    if not rows:
        return []
    return _parse_rows(rows)


def _skzc_to_weeks(skzc: str) -> list[int]:
    return [i + 1 for i, c in enumerate(skzc) if c == "1"]


def _parse_rows(rows: list[dict]) -> list[dict]:
    merged = defaultdict(set)
    for r in rows:
        key = (r.get("KCM", ""), r.get("SKXQ"), r.get("KSJC"), r.get("JSJC"), r.get("SKJS", ""), r.get("JASMC", ""))
        for w in _skzc_to_weeks(r.get("SKZC", "")):
            merged[key].add(w)
    result = []
    for (kcm, day, start, end, teacher, place), weeks in sorted(merged.items(), key=lambda x: (x[0][1] or 0, x[0][2] or 0)):
        if day is None or start is None:
            continue
        sw = sorted(weeks)
        ranges = []
        s = e = sw[0]
        for w in sw[1:]:
            if w == e + 1:
                e = w
            else:
                ranges.append((s, e))
                s = e = w
        ranges.append((s, e))
        week_str = "、".join(str(s) if s == e else f"{s}-{e}" for s, e in ranges)
        result.append({"course": kcm, "day": int(day), "start": int(start), "end": int(end), "teacher": teacher, "place": place or "", "week": week_str})
    return result
