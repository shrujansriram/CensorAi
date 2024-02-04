import os
from openai import OpenAI
import pandas as pd

os.environ['OPENAI_API_KEY'] = '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'

client = OpenAI()

# List of file paths for CSV files
file_paths = [
    'C:/Users/srira/Downloads/profanity1.csv',
    'C:/Users/srira/Downloads/profanityreal2.csv',
    'C:/Users/srira/Downloads/profanity3.csv',
    'C:/Users/srira/Downloads/Hindi.csv'
]

# Initialize an empty list to store all profanity words
all_profanity_words = []

# Iterate over each file path
for file_path in file_paths:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Check if 'profanity' column exists in the DataFrame
    if 'text' in df.columns:
        # Convert the 'profanity' column to string type and extract the profanity words
        profanity_words = df['text'].astype(str).tolist()
        # Extend the all_profanity_words list
        all_profanity_words.extend(profanity_words)
    else:
        print(f"Warning: 'profanity' column not found in file '{file_path}'.")

user_input = input("Enter your message: ")  # Get user input as a sentence

# Initialize a variable to track if profanity is found
profanity_found = False

# Split the user input sentence into words
words = user_input.split()

# Check each word for profanity
for word in words:
    # Check if the word is a profanity word
    if any(profanity_word.lower() in word.lower() for profanity_word in all_profanity_words):
        profanity_found = True
        break

response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': user_input},
    ]
)

# Append a message to the completion response based on whether profanity is found
if profanity_found:
    response.choices[0].message.content = "Please refrain from using profanity in your sentence."
else:
    response.choices[0].message.content = "Thank you for not using any profanity!"

print(response.choices[0].message.content)
