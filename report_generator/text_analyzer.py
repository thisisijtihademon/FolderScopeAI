from docx import Document
import fitz  # PyMuPDF
import re
from collections import Counter
import spacy
from textblob import TextBlob
import os
from textblob import TextBlob
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([p.text for p in doc.paragraphs])

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    return "\n".join([page.get_text() for page in doc])

def summarize_text(text):
    return text[:500] + "..." if len(text) > 500 else text

def analyze_text_file(file_path):
    if file_path.endswith('.txt'):
        text = extract_text_from_txt(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        text = ""
    return {"text_summary": summarize_text(text)}

def advanced_text_insights(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        words = re.findall(r'\b\w+\b', content.lower())
        word_count = len(words)
        common_words = Counter(words).most_common(10)
        long_words = [w for w in words if len(w) > 7]

        tone = "technical" if any(
            keyword in content.lower()
            for keyword in ["data", "function", "analysis", "return", "class", "model", "project"]
        ) else "casual"

        return {
            "total_words": word_count,
            "top_keywords": common_words,
            "long_word_count": len(long_words),
            "estimated_tone": tone
        }

    except Exception as e:
        return {"error": str(e)}


def perform_ner_and_sentiment(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        sentiment = TextBlob(text).sentiment

        return {
            "entities": entities,
            "sentiment": {
                "polarity": sentiment.polarity,
                "subjectivity": sentiment.subjectivity
            }
        }
    except Exception as e:
        return {"error": str(e)}

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
