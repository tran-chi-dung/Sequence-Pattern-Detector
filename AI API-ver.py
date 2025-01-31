import PyPDF2
import docx
import pytesseract
from PIL import Image
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import language_tool_python  # For grammar checking
import openai  # For AI-powered writing and tone adjustment

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Load spaCy model for advanced NLP
nlp = spacy.load("en_core_web_sm")

# Set up Tesseract OCR (ensure Tesseract is installed on your system)
# For Windows, specify the Tesseract path if needed:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set up OpenAI API (replace with your API key)
openai.api_key = "your_openai_api_key_here"

# Set up LanguageTool for grammar checking
grammar_tool = language_tool_python.LanguageTool('en-US')

def extract_text(file_path):
    """Extract text from a file based on its type."""
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_path.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        # Use OCR for image files
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    else:
        raise ValueError("Unsupported file type")

def preprocess_text(text):
    """Preprocess the text by tokenizing and removing stopwords."""
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    return filtered_words

def word_frequency_analysis(words):
    """Perform word frequency analysis."""
    return Counter(words)

def generate_summary(text, summary_length=3):
    """Generate a summary of the text."""
    sentences = sent_tokenize(text)
    if len(sentences) <= summary_length:
        return ' '.join(sentences)
    else:
        return ' '.join(sentences[:summary_length])

def sentiment_analysis(text):
    """Perform sentiment analysis using NLTK's VADER."""
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    return sentiment_score

def extract_entities(text):
    """Extract named entities using spaCy."""
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def extract_keywords(text, num_keywords=10):
    """Extract keywords based on word frequency."""
    words = preprocess_text(text)
    word_freq = word_frequency_analysis(words)
    return word_freq.most_common(num_keywords)

def grammar_check(text):
    """Check grammar using LanguageTool."""
    matches = grammar_tool.check(text)
    return matches

def find_and_replace(text, find_word, replace_word):
    """Find and replace all occurrences of a word in the text."""
    return text.replace(find_word, replace_word)

def ai_continue_writing(prompt):
    """Use OpenAI to continue writing based on a prompt."""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def ai_change_tone(text, tone):
    """Use OpenAI to change the tone of the text."""
    prompt = f"Rewrite the following text in a {tone} tone:\n\n{text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def analyze_document(file_path):
    """Analyze the document and return the results."""
    text = extract_text(file_path)
    words = preprocess_text(text)
    word_freq = word_frequency_analysis(words)
    summary = generate_summary(text)
    sentiment = sentiment_analysis(text)
    entities = extract_entities(text)
    keywords = extract_keywords(text)
    grammar_issues = grammar_check(text)

    analysis_results = {
        'text': text[:1000] + "..." if len(text) > 1000 else text,  # Show first 1000 chars
        'word_freq': word_freq.most_common(10),
        'summary': summary,
        'sentiment': sentiment,
        'entities': entities,
        'keywords': keywords,
        'grammar_issues': grammar_issues
    }
    return analysis_results

# GUI Application
class DocumentAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Analysis Tool")
        self.root.geometry("1000x800")

        # File selection button
        self.file_button = tk.Button(root, text="Select Document", command=self.select_file)
        self.file_button.pack(pady=10)

        # Text area to display results
        self.result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
        self.result_text.pack(padx=10, pady=10)

        # Buttons for advanced features
        self.find_replace_button = tk.Button(root, text="Find and Replace", command=self.find_replace)
        self.find_replace_button.pack(pady=5)

        self.grammar_check_button = tk.Button(root, text="Check Grammar", command=self.check_grammar)
        self.grammar_check_button.pack(pady=5)

        self.ai_continue_button = tk.Button(root, text="AI Continue Writing", command=self.ai_continue)
        self.ai_continue_button.pack(pady=5)

        self.ai_tone_button = tk.Button(root, text="AI Change Tone", command=self.ai_change_tone)
        self.ai_tone_button.pack(pady=5)

    def select_file(self):
        """Open a file dialog and analyze the selected document."""
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx"), ("Text Files", "*.txt"), 
                       ("Image Files", "*.png *.jpg *.jpeg *.tiff *.bmp *.gif")]
        )
        if file_path:
            try:
                self.file_path = file_path
                results = analyze_document(file_path)
                self.display_results(results)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def display_results(self, results):
        """Display the analysis results in the text area."""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "=== Extracted Text ===\n")
        self.result_text.insert(tk.END, results['text'] + "\n\n")
        self.result_text.insert(tk.END, "=== Word Frequency Analysis ===\n")
        self.result_text.insert(tk.END, str(results['word_freq']) + "\n\n")
        self.result_text.insert(tk.END, "=== Summary ===\n")
        self.result_text.insert(tk.END, results['summary'] + "\n\n")
        self.result_text.insert(tk.END, "=== Sentiment Analysis ===\n")
        self.result_text.insert(tk.END, str(results['sentiment']) + "\n\n")
        self.result_text.insert(tk.END, "=== Named Entities ===\n")
        self.result_text.insert(tk.END, str(results['entities']) + "\n\n")
        self.result_text.insert(tk.END, "=== Keywords ===\n")
        self.result_text.insert(tk.END, str(results['keywords']) + "\n\n")
        self.result_text.insert(tk.END, "=== Grammar Issues ===\n")
        self.result_text.insert(tk.END, str(results['grammar_issues']) + "\n\n")

    def find_replace(self):
        """Find and replace words in the document."""
        find_word = simpledialog.askstring("Find", "Enter the word to find:")
        replace_word = simpledialog.askstring("Replace", "Enter the word to replace with:")
        if find_word and replace_word:
            text = extract_text(self.file_path)
            updated_text = find_and_replace(text, find_word, replace_word)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, updated_text)

    def check_grammar(self):
        """Check grammar in the document."""
        text = extract_text(self.file_path)
        matches = grammar_check(text)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "=== Grammar Issues ===\n")
        self.result_text.insert(tk.END, str(matches) + "\n\n")

    def ai_continue(self):
        """Use AI to continue writing."""
        text = extract_text(self.file_path)
        continuation = ai_continue_writing(text)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "=== AI Continuation ===\n")
        self.result_text.insert(tk.END, continuation + "\n\n")

    def ai_change_tone(self):
        """Use AI to change the tone of the document."""
        tone = simpledialog.askstring("Change Tone", "Enter the desired tone (e.g., formal, casual, persuasive):")
        if tone:
            text = extract_text(self.file_path)
            updated_text = ai_change_tone(text, tone)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"=== AI Tone Change ({tone}) ===\n")
            self.result_text.insert(tk.END, updated_text + "\n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentAnalysisApp(root)
    root.mainloop()