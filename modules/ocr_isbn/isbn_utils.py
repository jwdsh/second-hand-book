import re


def normalize_isbn(isbn: str) -> str:
    """清理并验证ISBN格式"""
    # 移除非数字字符（保留X/x作为校验位）
    cleaned = re.sub(r'[^\dXx]', '', isbn)

    # 验证长度
    if len(cleaned) not in (10, 13):
        return ""

    # 转换为大写
    return cleaned.upper()


def extract_isbn_from_text(text: str) -> str:
    """
    从文本中提取可能的ISBN号
    支持10位和13位格式
    """
    # ISBN正则表达式（支持带连字符和不带连字符）
    patterns = [
        r'ISBN[\s-:]*([\d\-Xx]{10,17})',  # 带ISBN前缀
        r'\b(\d{3}[\s-]?\d{1,5}[\s-]?\d{1,7}[\s-]?\d{1,6}[\s-]?[\dXx])\b',  # 13位
        r'\b(\d{1,5}[\s-]?\d{1,7}[\s-]?\d{1,6}[\s-]?[\dXx])\b'  # 10位
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            normalized = normalize_isbn(match)
            if normalized:
                return normalized
    return ""