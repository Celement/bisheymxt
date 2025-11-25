import csv
import sys
import re
from datetime import datetime

def read_csv(path):
    encs = ("utf-8-sig", "utf-8", "gb18030", "gbk")
    last = None
    for enc in encs:
        try:
            with open(path, "r", encoding=enc, newline="") as f:
                return [r[0].strip() for r in csv.reader(f) if r]
        except Exception as e:
            last = e
            continue
    raise last

def clean_items(rows):
    items = []
    for i, s in enumerate(rows):
        if i == 0 and s.lower() == "filename":
            continue
        if s:
            items.append(s)
    return items

def categorize(name):
    cats = []
    if re.search(r"springboot", name, re.I):
        cats.append(("SpringBoot 🚀", "springboot"))
    if re.search(r"vue", name, re.I):
        cats.append(("Vue 🍃", "vue"))
    if re.search(r"\bssm\b", name, re.I):
        cats.append(("SSM 🧩", "ssm"))
    if re.search(r"小程序", name):
        cats.append(("小程序 📱", "mini"))
    if re.search(r"论文", name):
        cats.append(("论文 📘", "paper"))
    if re.search(r"商城|购物", name):
        cats.append(("商城 🛍️", "shop"))
    if re.search(r"医院|医疗|挂号", name):
        cats.append(("医院 🏥", "med"))
    if re.search(r"校园|高校|学生|教务", name):
        cats.append(("校园 🎓", "edu"))
    if re.search(r"旅游|景区|票务", name):
        cats.append(("旅游 🧭", "travel"))
    if re.search(r"宠物|猫狗", name):
        cats.append(("宠物 🐾", "pet"))
    if re.search(r"系统", name):
        cats.append(("系统 ⚙️", "sys"))
    if re.search(r"平台", name):
        cats.append(("平台 🌐", "plat"))
    if re.search(r"数据|可视化|算法|推荐", name):
        cats.append(("数据 📊", "data"))
    return cats

def anchor(s):
    a = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fa5]+", "-", s)
    a = re.sub(r"-+", "-", a).strip("-")
    return a

def build_md(items):
    total = len(items)
    now = datetime.now().strftime("%Y-%m-%d")
    head = [
        f"# 文件名分页展示 · 项目总览",
        "",
        f"> 数据源：`filenames (1).csv` · 条目数：**{total}** · 更新日期：**{now}**",
        "",
        "---",
        "",
        "## 功能概览",
        "- 纯前端 HTML 展示，支持分页、搜索高亮、标签与响应式布局",
        "- 支持从 `data.js` 加载数据，或从 CSV 转换生成",
        "- 左右侧二维码侧栏，支持文案与图片定制",
        "",
        "## 分类导航",
    ]

    cat_map = {}
    for name in items:
        for ctext, cslug in categorize(name):
            cat_map.setdefault((ctext, cslug), []).append(name)

    nav = []
    for (ctext, cslug), lst in sorted(cat_map.items(), key=lambda x: -len(x[1])):
        nav.append(f"- [{ctext} · {len(lst)}](#{anchor(ctext)})")

    sections = []
    for (ctext, cslug), lst in sorted(cat_map.items(), key=lambda x: -len(x[1])):
        sections.append("")
        sections.append(f"### {ctext}")
        sections.append("")
        sections.append("<details><summary>展开查看</summary>\n")
        for i, n in enumerate(lst, 1):
            sections.append(f"- {n}")
        sections.append("\n</details>")

    full = [
        "",
        "---",
        "",
        "## 全部项目",
        "",
    ]
    for i, n in enumerate(items, 1):
        full.append(f"{i}. {n}")

    lines = head + nav + sections + full
    return "\n".join(lines) + "\n"

def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "filenames (1).csv"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "README.md"
    rows = read_csv(csv_path)
    items = clean_items(rows)
    md = build_md(items)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    main()
