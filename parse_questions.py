#!/usr/bin/env python3
"""Parse the extracted PDF text into structured JSON question data."""

import re
import json

def parse_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Split into single-choice and multi-choice sections
    single_section, multi_section = text.split('二、多选题（共70题）')
    
    # Remove everything before "一、单选题（共72题）"
    single_part = single_section.split('一、单选题（共72题）')[1]
    
    questions = []
    
    # Parse single-choice questions
    singles = parse_section(single_part, 'single')
    questions.extend(singles)
    
    # Parse multi-choice questions
    multis = parse_section(multi_section, 'multiple')
    questions.extend(multis)
    
    return questions

def parse_section(text, qtype):
    """Parse a section of questions."""
    questions = []
    
    # Split by question number at start of line: "1. ", "2. ", etc.
    # We need to find all question starts
    # Pattern: line starts with digits followed by ". "
    lines = text.split('\n')
    
    # First, collapse continuation lines for questions and options
    # Strategy: iterate through lines, detect question/option boundaries
    current_question = None
    current_stage = 'idle'  # idle, in_question, in_options
    current_options = []
    current_option_label = None
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines, page markers, headers
        if not stripped:
            continue
        if stripped.startswith('第') and '页' in stripped:
            continue
        if stripped == '习近平新时代中国特色社会主义思想 - 复习题库':
            continue
        if stripped.startswith('习近平新时代中国特色社会主义思想'):
            continue
        if stripped.startswith('线上学习训练'):
            continue
        if '总题数' in stripped or '生成日期' in stripped:
            continue
        
        # Check if this is a new question start: "N. "
        q_match = re.match(r'^(\d+)\.\s+(.+)', stripped)
        if q_match:
            # Save previous question
            if current_question is not None:
                current_question['options'] = current_options
                questions.append(current_question)
            
            qnum = int(q_match.group(1))
            qtext = q_match.group(2)
            
            current_question = {
                'id': f'{qtype}-{qnum}',
                'type': qtype,
                'sourceOrder': qnum,
                'question': qtext,
                'options': [],
                'answer': ''
            }
            current_stage = 'in_question'
            current_options = []
            current_option_label = None
            continue
        
        # Check for answer line
        ans_match = re.match(r'^正确答案[：:]\s*(.+)', stripped)
        if ans_match:
            answer_str = ans_match.group(1).strip()
            if current_question:
                # For single: just the letter
                # For multiple: letters separated by 、
                current_question['answer'] = answer_str
            # Save the question
            if current_question is not None:
                current_question['options'] = current_options
                questions.append(current_question)
                current_question = None
            current_stage = 'idle'
            current_options = []
            current_option_label = None
            continue
        
        # Check for option start: "A. ", "B. ", "C. ", "D. "
        opt_match = re.match(r'^([A-D])\.\s+(.+)', stripped)
        if opt_match:
            label = opt_match.group(1)
            opt_text = opt_match.group(2)
            current_options.append({'label': label, 'text': opt_text})
            current_option_label = label
            current_stage = 'in_options'
            continue
        
        # Continuation line
        if current_stage == 'in_question' and current_question:
            # Append to question text
            current_question['question'] += stripped
        elif current_stage == 'in_options' and current_options:
            # Append to last option text
            current_options[-1]['text'] += stripped
    
    # Don't forget the last question if no answer line was processed
    # (shouldn't happen since all have answers)
    if current_question is not None:
        current_question['options'] = current_options
        questions.append(current_question)
    
    return questions

def main():
    filepath = '/Users/hatsuyuki/Library/Mobile Documents/com~apple~CloudDocs/ouc/学科资料/大二下/徐金鹏/题库/题库提取.txt'
    questions = parse_questions(filepath)
    
    # Validate
    singles = [q for q in questions if q['type'] == 'single']
    multis = [q for q in questions if q['type'] == 'multiple']
    print(f"Total: {len(questions)}")
    print(f"Single: {len(singles)}")
    print(f"Multiple: {len(multis)}")
    
    # Check for issues
    for q in questions:
        if not q['answer']:
            print(f"WARNING: No answer for {q['id']}")
        if len(q['options']) < 2:
            print(f"WARNING: Only {len(q['options'])} options for {q['id']}")
    
    # Print first single, last single, first multi, multi #14, last multi
    check_ids = ['single-1', 'single-72', 'multiple-1', 'multiple-14', 'multiple-70']
    for cid in check_ids:
        for q in questions:
            if q['id'] == cid:
                print(f"\n=== {q['id']} ===")
                print(f"Q: {q['question'][:100]}...")
                for o in q['options']:
                    print(f"  {o['label']}. {o['text'][:80]}...")
                print(f"A: {q['answer']}")
                break
    
    # Write JSON
    output_path = '/Users/hatsuyuki/Library/Mobile Documents/com~apple~CloudDocs/ouc/学科资料/大二下/徐金鹏/题库/questions.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\nWritten to {output_path}")

if __name__ == '__main__':
    main()
