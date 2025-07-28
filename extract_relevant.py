
import fitz
import os

def extract_relevant_info(file_path, persona):
    doc = fitz.open(file_path)
    matched = []
    keywords = persona['persona'].lower().split() + persona['job_to_be_done'].lower().split()
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        for line in text.split('\n'):
            if any(keyword in line.lower() for keyword in keywords):
                matched.append({
                    "text": line.strip(),
                    "page": page_num + 1
                })
    return {"file_name": os.path.basename(file_path), "matched_content": matched}
