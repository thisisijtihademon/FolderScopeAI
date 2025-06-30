import os
import re
from textblob import TextBlob
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def generate_report(report, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Folder Report\n\n")

        if "executive_summary" in report:
            f.write(f"## Executive Summary\n{report['executive_summary']}\n\n")

        f.write(f"## Content Summary\n")
        for key, value in report["content_summary"].items():
            f.write(f"- {key.replace('_', ' ').title()}: {value}\n")

        f.write(f"\n## File Details\n")
        for file in report["files"]:
            f.write(f"\n### {file['name']}\n")
            f.write(f"- Path: {file['path']}\n")
            f.write(f"- Type: {file['mime_type']}\n")
            f.write(f"- Size: {file['size_kb']} KB\n")
            f.write(f"- Last Modified: {file['last_modified']}\n")

            if "code_analysis" in file:
                ca = file["code_analysis"]
                f.write(f"  - Language: {ca.get('language')}\n")
                f.write(f"  - Lines: {ca.get('line_count')}\n")
                f.write(f"  - Functions: {ca.get('function_count')}\n")
                f.write(f"  - Classes: {ca.get('class_count')}\n")

            if "text_analysis" in file:
                f.write(f"  - Text Summary: {file['text_analysis'].get('text_summary')}\n")

            if "image_analysis" in file:
                f.write(f"  - Image Metadata: {file['image_analysis']}\n")

def analyze_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            blob = TextBlob(content)
            return {
                "word_count": len(blob.words),
                "sentence_count": len(blob.sentences),
                "sentiment_polarity": blob.sentiment.polarity,
                "sentiment_subjectivity": blob.sentiment.subjectivity
            }
    except Exception as e:
        return {"error": str(e)}

def advanced_text_insights(file_path):
    insights = {}
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            insights["reading_ease"] = flesch_reading_ease(content)
            insights["most_common_words"] = get_most_common_words(content)
            insights["plagiarism_matches"] = text_plagiarism_check(file_path)
    except Exception as e:
        insights["error"] = str(e)
    return insights

def flesch_reading_ease(text):
    words = text.split()
    sentences = text.count('.')
    syllables = sum([count_syllables(word) for word in words])
    if len(words) == 0 or sentences == 0:
        return 0
    return 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (syllables / len(words))

def count_syllables(word):
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev_char_was_vowel = False
    for char in word:
        if char in vowels:
            if not prev_char_was_vowel:
                count += 1
                prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False
    if word.endswith("e") and count > 1:
        count -= 1
    return count if count > 0 else 1

def get_most_common_words(text, n=5):
    words = re.findall(r'\w+', text.lower())
    freq = {}
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:n]

def perform_ner_and_sentiment(file_path):
    result = {"entities": [], "sentiment": {}}
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
            doc = nlp(text)
            result["entities"] = [(ent.text, ent.label_) for ent in doc.ents]
            blob = TextBlob(text)
            result["sentiment"] = {
                "polarity": blob.sentiment.polarity,
                "subjectivity": blob.sentiment.subjectivity
            }
    except Exception as e:
        result["error"] = str(e)
    return result

def text_plagiarism_check(file_path):
    try:
        base_path = os.path.dirname(file_path)
        files = [f for f in os.listdir(base_path) if f.endswith('.txt') and os.path.join(base_path, f) != file_path]

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as target_file:
            target_text = target_file.read()

        scores = []
        for other_file in files:
            try:
                with open(os.path.join(base_path, other_file), 'r', encoding='utf-8', errors='ignore') as f:
                    comparison_text = f.read()
                    tfidf = TfidfVectorizer().fit_transform([target_text, comparison_text])
                    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
                    scores.append({"file": other_file, "similarity": round(sim, 4)})
            except:
                continue

        return sorted(scores, key=lambda x: x['similarity'], reverse=True)
    except Exception as e:
        return {"error": str(e)}
