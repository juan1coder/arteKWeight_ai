import spacy
import random
import tkinter as tk
from tkinter import messagebox

# Load spaCy language model
nlp = spacy.load("en_core_web_sm")

# List of influential artists (feel free to add more)
artists = [
    "H.R. Giger", "Moebius", "Zdzisław Beksiński", "Salvador Dalí", "Andy Warhol",
    "Jean-Michel Basquiat", "Yoshitaka Amano", "James Jean", "Peter Mohrbacher",
    "Alphonse Mucha", "Kazimir Malevich", "Gustav Klimt", "Frida Kahlo"
]

# Phrases to insert artists naturally
artist_phrases = [
    "by", "inspired by", "infused with the style of", "with details made by",
    "with elements from", "channeling the spirit of", "reminiscent of"
]

def apply_weight(phrase):
    """Randomly applies weight within a range (0.25 - 2.8)."""
    return f"({phrase}:{round(random.uniform(0.25, 2.8), 2)})"

def process_prompt(prompt):
    """Processes the input prompt, applying weights and inserting artist influences."""
    doc = nlp(prompt)  # Run the prompt through spaCy

    weighted_prompt = []  # Stores final weighted components
    seen_phrases = set()  # Tracks processed phrases to prevent repetition

    # **STEP 1: Extract meaningful phrases**
    meaningful_phrases = []
    
    # Extract noun chunks (e.g., "futuristic cityscape", "robotic arms")
    for chunk in doc.noun_chunks:
        meaningful_phrases.append(chunk.text)

    # Extract adjective + noun groups (e.g., "smooth black latex", "organic materials")
    for token in doc:
        if token.pos_ in ["ADJ", "NOUN"] and token.dep_ in ["amod", "attr", "compound"]:
            phrase = " ".join([child.text for child in token.subtree])
            if len(phrase.split()) >= 3:
                meaningful_phrases.append(phrase)

    # **STEP 2: Process comma-separated concepts**
    split_by_commas = [phrase.strip() for phrase in prompt.split(",")]
    
    # **STEP 3: Inject Artists**
    artist_inserted = False  # Ensure we don't add too many artists
    for i, phrase in enumerate(split_by_commas):
        if phrase not in seen_phrases:
            # Apply weight only to meaningful phrases (avoid single words)
            processed_phrase = apply_weight(phrase) if len(phrase.split()) >= 3 else phrase
            weighted_prompt.append(processed_phrase)
            seen_phrases.add(phrase)
            
            # Randomly insert an artist influence once
            if not artist_inserted and random.random() < 0.4:  # 40% chance to add an artist
                artist = random.choice(artists)
                phrase_format = random.choice(artist_phrases)
                weighted_prompt.append(f"({phrase_format} {artist}:2.0)")
                artist_inserted = True  # Prevent multiple artists in one go

    return ", ".join(weighted_prompt)  # Reassemble the weighted prompt

def on_process_prompt():
    """Handles UI input processing."""
    prompt = entry.get("1.0", tk.END).strip()  # Get input
    if prompt:
        weighted_prompt = process_prompt(prompt)  # Process prompt
        result_text.delete("1.0", tk.END)  # Clear previous result
        result_text.insert(tk.END, weighted_prompt)  # Display new result
    else:
        messagebox.showwarning("Input Error", "Please enter a prompt.")

def on_copy_result():
    """Copies the processed prompt to clipboard."""
    result = result_text.get("1.0", tk.END).strip()
    if result:
        root.clipboard_clear()
        root.clipboard_append(result)  # Copy result
        messagebox.showinfo("Success", "Result copied to clipboard!")
    else:
        messagebox.showwarning("No Result", "There's no result to copy.")

# **GUI Setup (Tkinter)**
root = tk.Tk()
root.title("Prompt Weighting Tool")

tk.Label(root, text="Enter your prompt:").pack(pady=5)
entry = tk.Text(root, height=6, width=50)
entry.pack(pady=5)

process_button = tk.Button(root, text="Process Prompt", command=on_process_prompt)
process_button.pack(pady=5)

copy_button = tk.Button(root, text="Copy to Clipboard", command=on_copy_result)
copy_button.pack(pady=5)

tk.Label(root, text="Processed weighted prompt:").pack(pady=5)
result_text = tk.Text(root, height=6, width=50)
result_text.pack(pady=5)

root.mainloop()
