from docx import Document
import re

def clean_environment_description(text):
    """
    Cleans and formats environment descriptions by:
    1. Removing excess asterisks
    2. Separating main description from background descriptions
    3. Preserving line breaks
    4. Removing extra whitespace
    """
    # Remove all asterisks from start and end
    text = text.strip('*').strip()
    
    # Split into lines
    lines = text.split('\n')
    main_description = []
    background_descriptions = []
    
    for line in lines:
        # Remove leading/trailing whitespace and asterisks
        line = line.strip().strip('*').strip()
        
        # Check if line is a bullet point (background description)
        if re.match(r'^[•\t]+.*$', line):
            # Remove the bullet point and clean up
            cleaned_line = re.sub(r'^[•\t]+\s*', '', line).strip()
            if cleaned_line:
                background_descriptions.append(cleaned_line)
        else:
            # Remove any remaining bullet points or dashes
            line = re.sub(r'^[•-]\s*', '', line).strip()
            if line:
                main_description.append(line)
    
    return {
        'main': '\n'.join(main_description),
        'background': background_descriptions
    }

def is_environment_description(text):
    """
    Checks if the text is an environment description by looking for:
    1. Text surrounded by multiple asterisks
    2. Text with bullet points and asterisks
    """
    # Remove whitespace and newlines for the initial check
    condensed_text = ''.join(text.split())
    
    # Check for text surrounded by at least one asterisk
    if condensed_text.startswith('*') and condensed_text.endswith('*'):
        return True
    
    # Check for bullet points with asterisks
    if re.search(r'[\*•-]', text) and '*' in text:
        return True
        
    return False

def parse_character_line(line):
    """
    Parses a character line that might include an emotional indication.
    Returns a tuple of (character_name, emotion) or just (character_name, None)
    """
    pattern = r'^(Emma|Leo)(?:\s*\((.*?)\))?$'
    match = re.match(pattern, line)
    
    if match:
        character_name = match.group(1)
        emotion = match.group(2)  # Will be None if no parentheses
        return character_name, emotion
    return None, None

def parse_character_content(text):
    """
    Parses content containing character lines and additional descriptions.
    Returns a list of dictionaries with type and content.
    """
    lines = text.split('\n')
    parsed_lines = []
    current_character = None
    current_emotion = None
    current_dialogue = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for environment descriptions within the content
        if is_environment_description(line):
            if current_character and current_dialogue:
                parsed_lines.append({
                    'type': 'dialogue',
                    'character': current_character,
                    'emotion': current_emotion,
                    'content': '\n'.join(current_dialogue)
                })
                current_character = None
                current_emotion = None
                current_dialogue = []
            
            cleaned_env = clean_environment_description(line)
            if cleaned_env['main']:
                parsed_lines.append({
                    'type': 'environment',
                    'content': cleaned_env['main']
                })
            if cleaned_env['background']:
                parsed_lines.append({
                    'type': 'background',
                    'content': cleaned_env['background']
                })
            continue
            
        # Check for additional descriptions (starting with -)
        if line.startswith('-'):
            if current_character and current_dialogue:
                parsed_lines.append({
                    'type': 'dialogue',
                    'character': current_character,
                    'emotion': current_emotion,
                    'content': '\n'.join(current_dialogue)
                })
                current_character = None
                current_emotion = None
                current_dialogue = []
            parsed_lines.append({
                'type': 'description',
                'content': line[1:].strip()
            })
            continue
            
        character, emotion = parse_character_line(line)
        if character:
            if current_character and current_dialogue:
                parsed_lines.append({
                    'type': 'dialogue',
                    'character': current_character,
                    'emotion': current_emotion,
                    'content': '\n'.join(current_dialogue)
                })
                current_dialogue = []
            current_character = character
            current_emotion = emotion
        else:
            if current_character:
                current_dialogue.append(line)
    
    # Add any remaining dialogue
    if current_character and current_dialogue:
        parsed_lines.append({
            'type': 'dialogue',
            'character': current_character,
            'emotion': current_emotion,
            'content': '\n'.join(current_dialogue)
        })
    
    return parsed_lines

def read_docx(file_path):
    doc = Document(file_path)
    parsed_content = []
    
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                cell_text = cell.text.strip()
                
                # Skip empty cells
                if not cell_text:
                    continue
                
                # Check if the entire cell is an environment description
                if is_environment_description(cell_text) and not any(name in cell_text for name in ['Emma', 'Leo']):
                    cleaned_env = clean_environment_description(cell_text)
                    if cleaned_env['main']:
                        parsed_content.append({
                            'type': 'environment',
                            'content': cleaned_env['main']
                        })
                    if cleaned_env['background']:
                        parsed_content.append({
                            'type': 'background',
                            'content': cleaned_env['background']
                        })
                else:
                    # Parse mixed content (character lines and descriptions)
                    parsed_content.extend(parse_character_content(cell_text))
    
    return parsed_content

def main():
    file_path = 'Skript.docx'
    content = read_docx(file_path)
    
    for item in content:
        if item['type'] == 'environment':
            print("\n[Environment Description]:")
            print(item['content'])
        
        elif item['type'] == 'background':
            print("\n[Background Description]:")
            for line in item['content']:
                print(f"{line}")
        
        elif item['type'] == 'description':
            print(f"\n[Additional Description]:\n{item['content']}")
        
        elif item['type'] == 'dialogue':
            emotion_str = f" ({item['emotion']})" if item['emotion'] else ""
            print(f"\n[{item['character']}{emotion_str}]:")
            print(f"{item['content']}")

if __name__ == "__main__":
    main()