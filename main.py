### main.py
from report_generator.folder_scanner import scan_folder
from report_generator.code_analyzer import analyze_code_file, deep_code_analysis, run_bandit_scan, analyze_code_complexity
from report_generator.text_analyzer import analyze_text_file, advanced_text_insights, perform_ner_and_sentiment, text_plagiarism_check
from report_generator.image_analyzer import analyze_image_file
from report_generator.summary_writer import generate_report
from report_generator.executive_summary import create_executive_summary
from report_generator.project_inference import infer_project_purpose, gpt_project_summary
from report_generator.pdf_generator import generate_pdf_report, generate_pdf_with_weasyprint
from report_generator.forensic_analyzer import detect_sensitive_data, detect_code_reuse, detect_obfuscated_code
import markdown2
import argparse
from pathlib import Path
import logging
import zipfile
import csv
import json

def main():
    parser = argparse.ArgumentParser(description="FolderScope AI - Analyze and summarize a folder's contents")
    parser.add_argument("folder", type=str, help="Path to the folder to analyze")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF report generation")
    parser.add_argument("--summary-only", action="store_true", help="Only generate the executive summary")
    parser.add_argument("--html", action="store_true", help="Generate HTML version of the report")
    parser.add_argument("--log", action="store_true", help="Generate a .log file of operations")
    parser.add_argument("--zip", action="store_true", help="Zip the reports folder after generation")
    parser.add_argument("--csv", action="store_true", help="Export file analysis to CSV")
    parser.add_argument("--deep", action="store_true", help="Perform deep forensic analysis")
    args = parser.parse_args()

    if args.log:
        logging.basicConfig(filename="reports/folderscope.log", level=logging.INFO, format="%(asctime)s - %(message)s")
        logging.info("Analysis started")

    folder_path = Path(args.folder)
    if not folder_path.exists():
        print("The specified folder does not exist.")
        return

    report_data = scan_folder(folder_path)
    if args.log:
        logging.info(f"Scanned folder: {folder_path}")

    if not args.summary_only:
        for file in report_data["files"]:
            ext = Path(file["path"]).suffix.lower()
            if ext in [".py", ".js", ".java", ".cpp", ".c", ".html", ".css"]:
                file["code_analysis"] = analyze_code_file(file["path"])
                file["deep_code_analysis"] = deep_code_analysis(file["path"])
                file["security_scan"] = run_bandit_scan(file["path"])
                file["code_complexity"] = analyze_code_complexity(file["path"])
                if args.deep:
                    file["code_reuse"] = detect_code_reuse(file["path"])
                    file["obfuscated_code"] = detect_obfuscated_code(file["path"])
                if args.log:
                    logging.info(f"Deep + security analyzed code file: {file['name']}")
            elif ext in [".txt", ".docx", ".pdf"]:
                file["text_analysis"] = analyze_text_file(file["path"])
                file["text_insights"] = advanced_text_insights(file["path"])
                file["nlp_enrichment"] = perform_ner_and_sentiment(file["path"])
                file["plagiarism_check"] = text_plagiarism_check(file["path"])
                if args.deep:
                    file["sensitive_data"] = detect_sensitive_data(file["path"])
                if args.log:
                    logging.info(f"Advanced NLP analyzed text file: {file['name']}")
            elif ext in [".jpg", ".jpeg", ".png"]:
                file["image_analysis"] = analyze_image_file(file["path"])
                if args.log:
                    logging.info(f"Analyzed image file: {file['name']}")

    report_data["executive_summary"] = create_executive_summary(report_data)
    report_data["project_inference"] = infer_project_purpose(report_data)
    report_data["gpt_analysis"] = gpt_project_summary(report_data)

    md_report_path = Path("reports/your_folder_report.md")
    generate_report(report_data, md_report_path)

    if args.log:
        logging.info("Markdown report generated")

    if not args.no_pdf:
        generate_pdf_report(md_report_path, Path("reports/report_reportlab.pdf"))
        try:
            generate_pdf_with_weasyprint(md_report_path, Path("reports/report_weasyprint.pdf"))
        except Exception as e:
            print("[Warning] WeasyPrint PDF generation failed:", e)
            if args.log:
                logging.warning("WeasyPrint PDF generation failed")

    if args.html:
        html_path = Path("reports/your_folder_report.html")
        with open(md_report_path, 'r', encoding='utf-8') as f:
            html_content = markdown2.markdown(f.read())
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML report generated at: {html_path}")
        if args.log:
            logging.info("HTML report generated")

    if args.csv:
        csv_path = Path("reports/file_analysis.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Path", "Type", "Size (KB)", "Last Modified"])
            for file in report_data["files"]:
                writer.writerow([file["name"], file["path"], file["mime_type"], file["size_kb"], file["last_modified"]])
        print(f"CSV report generated at: {csv_path}")
        if args.log:
            logging.info("CSV export generated")

    if args.zip:
        zip_path = Path("reports/reports_archive.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for report_file in Path("reports").glob("*.*"):
                if report_file.name != "reports_archive.zip":
                    zipf.write(report_file, arcname=report_file.name)
        print(f"Reports zipped at: {zip_path}")
        if args.log:
            logging.info("Reports zipped")

    if args.log:
        logging.info("Analysis completed")

if __name__ == "__main__":
    main()
