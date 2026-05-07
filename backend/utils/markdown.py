from datetime import datetime


def format_report_header(title: str, query: str, date: str | None = None) -> str:
    """生成报告头部"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    return f"""# {title}

> **研究主题:** {query}
> **生成日期:** {date}
> **生成方式:** OSINT 多智能体自动化分析

---

"""


def format_sources_section(sources: list[dict]) -> str:
    """生成数据来源附录"""
    if not sources:
        return ""
    lines = ["\n---\n\n## 数据来源\n"]
    for i, s in enumerate(sources, 1):
        title = s.get("title", "未知标题")
        url = s.get("url", "")
        date = s.get("date", "")
        lines.append(f"{i}. [{title}]({url}) — {date}\n")
    return "".join(lines)
