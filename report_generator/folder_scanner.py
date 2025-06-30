from pathlib import Path
import mimetypes
from datetime import datetime

def scan_folder(folder_path):
    report = {
        "content_summary": {
            "total_files": 0,
            "file_types": {},
            "total_size_mb": 0,
            "last_modified": ""
        },
        "files": []
    }

    all_files = list(Path(folder_path).rglob("*"))
    total_size = 0
    last_modified = 0

    for file in all_files:
        if file.is_file():
            mime_type, _ = mimetypes.guess_type(file)
            file_info = {
                "name": file.name,
                "path": str(file),
                "mime_type": mime_type if mime_type else "Unknown",
                "size_kb": round(file.stat().st_size / 1024, 2),
                "last_modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            }
            report["files"].append(file_info)
            report["content_summary"]["total_files"] += 1
            file_type = mime_type.split('/')[0] if mime_type else "unknown"
            report["content_summary"]["file_types"][file_type] = report["content_summary"]["file_types"].get(file_type, 0) + 1
            total_size += file.stat().st_size
            last_modified = max(last_modified, file.stat().st_mtime)

    report["content_summary"]["total_size_mb"] = round(total_size / (1024 * 1024), 2)
    report["content_summary"]["last_modified"] = datetime.fromtimestamp(last_modified).isoformat()

    return report
