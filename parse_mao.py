#!/usr/bin/env python3
"""Parse 毛泽东思想题库.md into structured JSON."""

import re
import json
import os

def parse_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    questions = []
    
    # Find sections
    sections = re.split(r'\n# (单选题|多选题|判断题)\n', text)
    # sections will be: [before, type1, content1, type2, content2, type3, content3]
    
    type_map = {'单选题': 'single', '多选题': 'multiple', '判断题': 'judge'}
    
    i = 1  # skip preamble
    while i < len(sections) - 1:
        section_type = sections[i]
        section_content = sections[i + 1]
        qtype = type_map.get(section_type, 'unknown')
        
        # Split into individual questions by "## N. "
        q_blocks = re.split(r'\n## \d+\. ', section_content)
        
        n = 1  # question counter within this type
        for block in q_blocks:
            if not block.strip():
                continue
            
            # Extract question text (first line)
            lines = block.strip().split('\n')
            question_text = lines[0].strip()
            
            # Remove markdown formatting
            question_text = re.sub(r'\*\*', '', question_text)
            
            # Find options: lines starting with "- **A**." or "- **B**." etc.
            options = []
            opt_matches = re.findall(r'- \*\*([A-D])\*\*[.．。]\s*(.+?)(?=\n- \*\*[A-E]\*\*|\n\*\*答案|$)', block, re.DOTALL)
            for label, text in opt_matches:
                text = re.sub(r'\*\*', '', text).strip()
                options.append({'label': label, 'text': text})
            
            # Find answer
            ans_match = re.search(r'\*\*答案\*\*[：:]\s*(.+)', block)
            answer = ''
            if ans_match:
                ans_raw = ans_match.group(1).strip()
                # For judge type, convert to True/False
                if qtype == 'judge':
                    if '正确' in ans_raw:
                        answer = '正确'
                    elif '错误' in ans_raw:
                        answer = '错误'
                else:
                    # Convert A, B, C to A、B、C format
                    answer = '、'.join(re.findall(r'[A-D]', ans_raw))
            
            # Skip if no answer or no options (judge questions have no options)
            if not answer:
                continue
            
            question = {
                'id': f'{qtype}-mao-{n}',
                'type': qtype,
                'subject': 'mao',
                'sourceOrder': n,
                'chapter': '',
                'question': question_text,
                'options': options,
                'answer': answer
            }
            
            # Extract chapter info from title
            ch_match = re.search(r'【(.+?)】', question_text)
            if ch_match:
                question['chapter'] = ch_match.group(1)
            
            questions.append(question)
            n += 1
        
        i += 2
    
    return questions

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, '毛泽东思想题库.md')
    questions = parse_md(filepath)
    
    # Count by type
    singles = [q for q in questions if q['type'] == 'single']
    multis = [q for q in questions if q['type'] == 'multiple']
    judges = [q for q in questions if q['type'] == 'judge']
    
    print(f"Total: {len(questions)}")
    print(f"Single: {len(singles)}")
    print(f"Multiple: {len(multis)}")
    print(f"Judge: {len(judges)}")
    
    # Print samples
    for q in questions[:2]:
        print(f"\n{q['id']}: {q['question'][:80]}...")
        for o in q['options'][:2]:
            print(f"  {o['label']}. {o['text'][:60]}")
        print(f"  A: {q['answer']}")
    
    # Write JSON
    output_path = os.path.join(script_dir, 'mao_questions.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"\nWritten to {output_path}")

if __name__ == '__main__':
    main()
