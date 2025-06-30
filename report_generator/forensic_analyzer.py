import re
import hashlib


def detect_sensitive_data(file_path):
    sensitive_patterns = [
        r'AKIA[0-9A-Z]{16}',  # AWS Access Key ID
        r'(?i)api[_-]?key\s*[:=]\s*["\']?[a-z0-9]{32,}',
        r'(?i)secret[_-]?key\s*[:=]\s*["\']?[a-z0-9]{32,}',
        r'(?i)password\s*[:=]\s*["\']?.{6,}',
        r'(?i)token\s*[:=]\s*["\']?[a-z0-9\-]{32,}'
    ]
    matches = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for pattern in sensitive_patterns:
                found = re.findall(pattern, content)
                if found:
                    matches.extend(found)
    except Exception as e:
        return {"error": str(e)}
    return matches if matches else None


def detect_code_reuse(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            hash_digest = hashlib.md5(content.encode()).hexdigest()
            return {"md5_hash": hash_digest}
    except Exception as e:
        return {"error": str(e)}


# This is very basic obfuscation detection based on entropy and minification

def detect_obfuscated_code(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            line_lengths = [len(line) for line in content.splitlines() if line.strip()]
            avg_line_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0

            if avg_line_length > 150:  # Arbitrary threshold
                return {"suspicion": "High average line length; possibly minified or obfuscated"}
    except Exception as e:
        return {"error": str(e)}
    return None
