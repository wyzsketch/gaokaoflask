# -*- coding: utf-8 -*-
"""
全局工具函数
复用原有Global.py中的通用函数
"""
import hashlib


def djb2_hash(input_str):
    """djb2哈希算法"""
    hash_value = 5381
    for char in input_str:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return hash_value & 0xFFFFFFFF  # 保证32位输出


def calculate_md5(text: str) -> str:
    """计算MD5"""
    text_bytes = text.encode('utf-8')
    md5 = hashlib.md5()
    md5.update(text_bytes)
    return md5.hexdigest()


def parseInt(s):
    """安全转换整数"""
    try:
        return int(s)
    except (ValueError, TypeError):
        return 0


def extract_first_bracket(s: str, max_len: int) -> str:
    """提取第一个括号内的内容"""
    left = s.find("（")
    right = s.find("）", left)
    if left == -1 or right == -1:
        return ""
    inner = s[left + 1:right]
    if "色盲" in inner or "色弱" in inner:
        return ""
    if "班" in inner:
        max_len = max_len + 2
    if len(inner) <= max_len:
        return s[left:right + 1]
    else:
        return ""
