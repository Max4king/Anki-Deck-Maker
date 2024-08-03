import genanki
import json
import sys
import os

# Check if the user provided the JSON file path
if len(sys.argv) != 2:
    print("Usage: python main.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line arguments
json_file_path = sys.argv[1]

# Default to the raw-json folder if the path is not absolute
if not os.path.isabs(json_file_path):
    json_file_path = os.path.join('raw-json', json_file_path)

# Load the JSON data from the file
with open(json_file_path, 'r') as f:
    synonyms_data = json.load(f)

# Create a unique ID for the deck and model
model_id = 1607392319
deck_id = 2059400110

# Define the model
my_model = genanki.Model(
    model_id,
    'Advanced Synonyms Model',
    fields=[
        {'name': 'Word'},
        {'name': 'Synonym'},
        {'name': 'WordExample'},
        {'name': 'SynonymExample'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '''
                <div style="text-align: center; font-size: 50px;">{{Word}}</div>
                <div style="text-align: center; font-size: 24px; margin-top: 10px;">{{WordExample}}</div>
            ''',
            'afmt': '''
                <div style="text-align: center; font-size: 50px;">{{FrontSide}}</div>
                <hr id="answer">
                <div style="text-align: center; font-size: 50px;">{{Synonym}}</div>
                <div style="text-align: center; font-size: 24px; margin-top: 10px;">{{SynonymExample}}</div>
            ''',
        },
    ])

# Create the deck
my_deck = genanki.Deck(
    deck_id,
    'Advanced Synonyms Deck')

# Add notes to the deck
for item in synonyms_data:
    note = genanki.Note(
        model=my_model,
        fields=[
            item['word'], 
            item['synonym'], 
            item['examples']['word_example'], 
            item['examples']['synonym_example']
        ])
    my_deck.add_note(note)

# Prepare the output file path
output_dir = 'output-deck'
os.makedirs(output_dir, exist_ok=True)
output_file_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_file = os.path.join(output_dir, f"{output_file_base}.apkg")

# Check if the file already exists and add a number to avoid overwriting
counter = 1
while os.path.exists(output_file):
    output_file = os.path.join(output_dir, f"{output_file_base}_{counter}.apkg")
    counter += 1

# Write the deck to a file
genanki.Package(my_deck).write_to_file(output_file)

print(f"Anki deck created successfully at {output_file}!")