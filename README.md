# SZPU Course Schedule → CSV

## Install

```bash
pip install requests pycryptodome
```

## Usage

```bash
# Cookie mode
python3 main.py <student_id> --cookie 'EMAP_LANG=zh; JSESSIONID=...' --xn 2025-2026 --xq 2 -o schedule.csv

# Password login
python3 main.py <student_id> -p 'password' --xn 2025-2026 --xq 2 -o schedule.csv
```

## Arguments

| Arg | Description |
|-----|-------------|
| `xh` | Student ID |
| `-p / --password` | CAS password |
| `--cookie` | Cookie string (skip login) |
| `--xn` | Academic year, e.g. `2025-2026` |
| `--xq` | Semester: `1`=fall `2`=spring `3`=summer |
| `-o / --output` | Output CSV path (default: stdout) |

## CSV Fields

`课程名称,星期,开始节数,结束节数,老师,地点,周数`

## Structure

```
├── main.py
├── requirements.txt
└── szpu/
    ├── encrypt.py     # AES-128-CBC
    ├── login.py       # CAS / cookie login
    ├── course.py      # API query & SKZC parser
    └── csv_writer.py  # CSV export
```

## License

GPL v3
