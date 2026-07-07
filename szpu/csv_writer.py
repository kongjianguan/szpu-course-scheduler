import csv
import io


def to_csv(slots: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["课程名称", "星期", "开始节数", "结束节数", "老师", "地点", "周数"])
    for s in slots:
        w.writerow([s["course"], s["day"], s["start"], s["end"], s["teacher"], s["place"], s["week"]])
    return buf.getvalue()


def save_csv(slots: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        f.write(to_csv(slots))
