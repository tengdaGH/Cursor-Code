#!/usr/bin/env python3
"""
Extract dialogue data from HTML file and generate Python code for audio generation script.
"""

import re
import json
from pathlib import Path

def extract_dialogues(html_path):
    """Extract all dialogue data from HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all QUESTION_SETS blocks
    pattern = r'QUESTION_SETS\s*=\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print("Could not find QUESTION_SETS")
        return {}
    
    questions_data = {}
    
    # Extract R02 and R03 sets
    for set_id in ['R02', 'R03']:
        # More flexible pattern to match the set structure
        set_pattern = rf'{set_id}:\s*\{{[^}}]*questions:\s*\[(.*?)\]\s*\}}\s*\}}'
        set_match = re.search(set_pattern, content, re.DOTALL)
        if not set_match:
            print(f"Could not find {set_id}")
            continue
        
        questions_text = set_match.group(1)
        
        # Extract individual questions - handle escaped quotes
        question_pattern = r'id:\s*[\'"](\w+-\d+)[\'"],.*?dialogue:\s*\{[^}]*speaker1:\s*[\'"]([^\'"]*(?:\\.[^\'"]*)*)[\'"],[^}]*speaker2:\s*[\'"]([^\'"]*(?:\\.[^\'"]*)*)[\'"]'
        questions = re.findall(question_pattern, questions_text, re.DOTALL)
        
        for q_id, speaker1_text, speaker2_text in questions:
            # Determine voice assignment (alternate between male and female)
            # R02: speaker1 starts with female, R03: speaker1 starts with male
            if set_id == 'R02':
                voice1 = 'VOICE_FEMALE' if int(q_id.split('-')[1]) % 2 == 1 else 'VOICE_MALE'
                voice2 = 'VOICE_MALE' if voice1 == 'VOICE_FEMALE' else 'VOICE_FEMALE'
            else:  # R03
                voice1 = 'VOICE_MALE' if int(q_id.split('-')[1]) % 2 == 1 else 'VOICE_FEMALE'
                voice2 = 'VOICE_FEMALE' if voice1 == 'VOICE_MALE' else 'VOICE_MALE'
            
            questions_data[q_id] = {
                'speaker1': speaker1_text.replace("\\'", "'"),
                'speaker2': speaker2_text.replace("\\'", "'"),
                'voice1': voice1,
                'voice2': voice2
            }
    
    return questions_data

def generate_python_code(questions_data):
    """Generate Python dictionary code for audio generation script."""
    lines = []
    for q_id, data in sorted(questions_data.items()):
        lines.append(f'    "{q_id}": {{')
        lines.append(f'        "topic": "Service",  # Update manually if needed')
        lines.append(f'        "dialogue": [')
        lines.append(f'            {{"speaker": "speaker1", "voice": {data["voice1"]}, "text": "{data["speaker1"]}"}},')
        lines.append(f'            {{"speaker": "speaker2", "voice": {data["voice2"]}, "text": "{data["speaker2"]}"}}')
        lines.append(f'        ]')
        lines.append(f'    }},')
    return '\n'.join(lines)

if __name__ == '__main__':
    html_path = Path(__file__).parent.parent / 'toefl-listening-choose-response-practice.html'
    questions_data = extract_dialogues(html_path)
    
    print(f"Extracted {len(questions_data)} questions")
    print("\nPython code to add to generate-choose-response-audio.py:\n")
    print(generate_python_code(questions_data))
