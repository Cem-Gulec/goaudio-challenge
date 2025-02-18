from docx import Document
import re

def clean_environment_description(text):
    """
    Cleans and formats environment descriptions by:
    1. Removing excess asterisks
    2. Handling bullet points
    3. Preserving line breaks
    4. Removing extra whitespace
    """
    # Remove all asterisks from start and end
    text = text.strip('*').strip()
    
    # Split into lines and clean each line
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Remove leading/trailing whitespace and asterisks
        line = line.strip().strip('*').strip()
        
        # Remove bullet points (both • and - characters) and clean up
        line = re.sub(r'^[•-]\s*', '', line).strip()
        
        # Only add non-empty lines
        if line:  
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

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
                    
                if is_environment_description(cell_text):
                    cleaned_description = clean_environment_description(cell_text)
                    parsed_content.append({
                        'type': 'environment',
                        'content': cleaned_description
                    })
                else:
                    parsed_content.append({
                        'type': 'dialogue',
                        'content': cell_text
                    })
    
    return parsed_content

def main():
    file_path = 'Skript.docx'
    content = read_docx(file_path)
    
    for item in content:
        if item['type'] == 'environment':
            print("\n[Environment Description]:")
            
            for line in item['content'].split('\n'):
                print(f"{line}")
        else:
            print(f"\n[Dialogue]:\n{item['content']}")

if __name__ == "__main__":
    main()