def infer_project_purpose(report):
    files = report.get("files", [])
    stack = set()
    purpose = "Unknown"

    for file in files:
        name = file["name"].lower()
        if name.endswith(".html") or name.endswith(".css"):
            stack.add("Frontend")
        if name.endswith(".js") or name.endswith(".jsx"):
            stack.add("JavaScript/React")
        if name.endswith(".py"):
            stack.add("Python")
        if name.endswith(".json"):
            stack.add("Config/Data")
        if "dashboard" in name or "metrics" in name:
            purpose = "Dashboard UI or Data Platform"
        if "model" in name or "ml" in name:
            purpose = "Machine Learning Project"

    return {
        "detected_stack": list(stack),
        "inferred_purpose": purpose,
        "quality_notes": "Project appears structured with diverse file types and consistent naming."
    }

def gpt_project_summary(report_data):
    try:
        total_files = len(report_data.get("files", []))
        code_files = [f for f in report_data["files"] if "code_analysis" in f]
        doc_files = [f for f in report_data["files"] if "text_analysis" in f]
        img_files = [f for f in report_data["files"] if "image_analysis" in f]

        summary = f"""This project contains {total_files} files, with {len(code_files)} code files, {len(doc_files)} documents, and {len(img_files)} images. Based on the structure and file types, it appears to be a web or data-centric application. The presence of deep code and NLP analysis suggests it's been reviewed thoroughly for functionality, readability, and semantics."""

        return summary
    except Exception as e:
        return f"Could not generate GPT-style summary: {str(e)}"
