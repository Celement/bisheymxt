import csv
import json
import sys

def read_csv(path):
    encs = ("utf-8-sig", "utf-8", "gb18030", "gbk")
    last = None
    for enc in encs:
        try:
            with open(path, "r", encoding=enc, newline="") as f:
                return list(csv.reader(f))
        except Exception as e:
            last = e
            continue
    raise last

def to_items(rows):
    items = []
    for i, row in enumerate(rows):
        if not row:
            continue
        cell = row[0].strip()
        if i == 0 and cell.lower() == "filename":
            continue
        if cell:
            items.append(cell)
    return items

def write_js(items, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("window.FILENAMES = [\n")
        for i, name in enumerate(items):
            s = json.dumps(name, ensure_ascii=False)
            if i < len(items) - 1:
                f.write(f"{s},\n")
            else:
                f.write(f"{s}\n")
        f.write("]\n")

def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "filenames (1).csv"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "data.js"
    rows = read_csv(csv_path)
    items = to_items(rows)
    write_js(items, out_path)

if __name__ == "__main__":
    main()
