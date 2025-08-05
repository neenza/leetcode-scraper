import json
import csv

# Input and output file paths
json_path = 'all_problems.json'
csv_path = 'all_problems.csv'

# Load JSON data
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract stat_status_pairs
stat_status_pairs = data.get('stat_status_pairs', [])

# Define CSV columns
columns = [
    'question_id',
    'question__title',
    'question__title_slug',
    'difficulty',
    'paid_only',
    'status',
    'frequency',
    'is_favor',
    'frontend_question_id',
    'total_acs',
    'total_submitted',
    'question__hide',
    'is_new_question'
]

rows = []
for item in stat_status_pairs:
    stat = item.get('stat', {})
    difficulty = item.get('difficulty', {})
    row = {
        'question_id': stat.get('question_id'),
        'question__title': stat.get('question__title'),
        'question__title_slug': stat.get('question__title_slug'),
        'difficulty': difficulty.get('level'),
        'paid_only': item.get('paid_only'),
        'status': item.get('status'),
        'frequency': item.get('frequency'),
        'is_favor': item.get('is_favor'),
        'frontend_question_id': stat.get('frontend_question_id'),
        'total_acs': stat.get('total_acs'),
        'total_submitted': stat.get('total_submitted'),
        'question__hide': stat.get('question__hide'),
        'is_new_question': item.get('is_new_question'),
    }
    rows.append(row)

# Sort rows by ascending frontend_question_id (convert to int for correct order)
rows.sort(key=lambda r: int(r['frontend_question_id']) if r['frontend_question_id'] is not None else 0)

with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
print(f"CSV file written to {csv_path}")

