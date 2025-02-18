from docx import Document

def read_docx(file_path):
    doc = Document(file_path)
    
    full_text = []
    
    # Read the table
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                full_text.append(cell.text)
    
    return '\n'.join(full_text)

def main():
    file_path = 'Skript.docx'
    content = read_docx(file_path)
    print(content)

if __name__ == "__main__":
    main()