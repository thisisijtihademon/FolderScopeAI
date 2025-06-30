# 📁 FolderScopeAI - Deep Code & Text Analyzer

A next-gen forensic scanner for folders packed with code, documentation, and more. Analyze, summarize, and report like a digital detective 🕵️‍♂️.

---

## 🚀 How to Use

### 🔧 Basic Command
```bash
python main.py <folder_path>
```

### ⚙️ Available CLI Flags
| Flag       | Description |
|------------|-------------|
| `--html`   | Generate HTML report |
| `--pdf`    | Generate PDF report (WeasyPrint or ReportLab) |
| `--csv`    | Export report to CSV format |
| `--log`    | Save a `.log` file of operations |
| `--zip`    | Auto zip the report directory |
| `--deep`   | Perform forensic scans for code smell, reuse, obfuscation, sensitive data |

---

## 🧠 Modules & Functions

### 📜 Text Analyzer
Located at: `report_generator/text_analyzer.py`

- `analyze_text_file(file_path)`  
  ➤ Returns word count, sentence count, sentiment polarity & subjectivity

- `advanced_text_insights(file_path)`  
  ➤ Adds reading ease score, most common words, and plagiarism matches

- `perform_ner_and_sentiment(file_path)`  
  ➤ Named Entity Recognition + sentiment scan

- `text_plagiarism_check(file_path)`  
  ➤ Uses TF-IDF + cosine similarity to flag reused content in the same folder

---

### 🧬 Code Analyzer
Located at: `report_generator/code_analyzer.py`

- `analyze_code_file(file_path)`  
  ➤ Detects number of functions, classes, language type, and complexity hints

- `deep_code_analysis()`  
  ➤ Hooks into more advanced tools for structural insights

- `run_bandit_scan(file_path)`  
  ➤ Python security audit using Bandit

- `detect_sensitive_data(file_path)`  
  ➤ Flags tokens, API keys, secrets

- `detect_code_reuse(file_path)`  
  ➤ Checks for signs of copied logic from other sources

- `detect_obfuscated_code(file_path)`  
  ➤ Spots minified, encoded, or misleading structures

- `analyze_code_complexity(file_path)`  
  ➤ Measures cyclomatic complexity, nested blocks, and potential technical debt

---

### 🗃️ Output Formats

- `.md`: Full Markdown Summary Report
- `.html`: Stylish HTML version of the above
- `.pdf`: Clean printable report
- `.csv`: Tabular dump of file metrics
- `.log`: Step-by-step operations log
- `.zip`: Compressed report package

---

## 🔩 Requirements
Install dependencies using pip:
```bash
pip install -r requirements.txt
```
Or individually:
```bash
pip install textblob spacy sklearn weasyprint markdown2
python -m textblob.download_corpora
python -m spacy download en_core_web_sm
```

---

## 🌟 Example Usage
```bash
python main.py D:/ProjectPortfolio --html --csv --log --zip --deep
```

This will produce:
- An HTML report
- A CSV table
- A zip file with all results
- Deep scan insights

---

## 📌 Notes
- Currently works best on `.txt`, `.py`, `.js`, `.html`, `.md`, `.json` files
- Plagiarism check compares local `.txt` files only
- Bandit scan requires `bandit` installed (`pip install bandit`)

---

## 🧑‍💻 Made for:
- Researchers 🧪
- Developers 🧑‍💻
- Forensic Analysts 🕵️‍♀️
- AI Workflow Auditors 🤖

> FolderScopeAI isn’t just a tool. It’s a *codebase conscience.*

## 🔧 Features

### 🔍 Text Analysis (text_analyzer.py)
- `analyze_text_file()` → Word count, sentence count, sentiment polarity and subjectivity
- `advanced_text_insights()` → Flesch reading ease, most common words, plagiarism detection
- `perform_ner_and_sentiment()` → Named Entity Recognition (NER) + sentiment analysis
- `text_plagiarism_check()` → Detect similarity between `.txt` files in same folder

### 🧠 Code Analysis (code_analyzer.py)
- `analyze_code_file()` → Line count, class/function count, comments ratio
- `deep_code_analysis()` → Flags long functions, duplicate lines, weird code patterns
- `run_bandit_scan()` → Runs Bandit security scan on Python files
- `analyze_code_complexity()` → Complexity and readability check (NEW!)

### 🕵️ Forensic Insights (forensic_analyzer.py)
- `detect_sensitive_data()` → Finds hardcoded keys, tokens, secrets
- `detect_code_reuse()` → Flags reused logic across files (GitHub-copy style)
- `detect_obfuscated_code()` → Detects encoded or minified suspicious code

## 🚀 CLI Usage

```bash
python main.py <folder_path> [--html] [--csv] [--log] [--zip] [--deep]
```

### Flags
- `--html` → Export full HTML report
- `--csv` → Export insights to CSV
- `--log` → Create scan log file
- `--zip` → Archive the folder with timestamp
- `--deep` → Run forensic scans on top of analysis

## 📦 Installation

Make sure you’re in a virtual environment, then run:

```bash
pip install textblob
pip install spacy
pip install scikit-learn
python -m textblob.download_corpora
python -m spacy download en_core_web_sm
```

## ✅ Output
- Markdown and HTML summaries per file
- Forensic logs (if `--log` enabled)
- CSVs with structured results
- Optional `.zip` backup of the scanned folder

## 💬 Author
Made with ❤️ by Ijtihad Emon — AI-assisted, precision-delivered.

---
Stay curious. Stay skeptical. Scan responsibly.
