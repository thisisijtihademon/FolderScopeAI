def create_executive_summary(report):
    total = report['content_summary']['total_files']
    size = report['content_summary']['total_size_mb']
    types = report['content_summary']['file_types']
    key_files = [file['name'] for file in report['files'] if 'code_analysis' in file or 'text_analysis' in file]

    summary = f"This folder contains {total} files spanning code, documents, and media."
    summary += f" The total size is {size} MB."
    summary += f" Major file categories include: {', '.join(types.keys())}."
    if key_files:
        summary += f"\n\nKey files analyzed include: {', '.join(key_files[:5])}{' and others' if len(key_files) > 5 else ''}."
    summary += "\n\nThis project appears structured and purpose-driven, demonstrating elements of frontend, backend, and documentation."
    return summary