import re


def clean_html_text(text: str) -> str:
    """去除 HTML 标签，保留纯文本"""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def truncate_text(text: str, max_bytes: int = 50000) -> str:
    """按字节数截断文本"""
    encoded = text.encode("utf-8")
    if len(encoded) <= max_bytes:
        return text
    truncated = encoded[:max_bytes]
    return truncated.decode("utf-8", errors="ignore")


def deduplicate_findings(findings: list[dict]) -> list[dict]:
    """根据 source_url 去重"""
    seen_urls: set[str] = set()
    unique = []
    for f in findings:
        url = f.get("source_url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(f)
        elif not url:
            unique.append(f)
    return unique
