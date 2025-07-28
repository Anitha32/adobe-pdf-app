
import fitz

def extract_outline_from_pdf(file_path):
    doc = fitz.open(file_path)
    outlines = []
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        size = span["size"]
                        if size > 14:
                            outlines.append({
                                "text": span["text"],
                                "page": page_number + 1,
                                "level": "H1" if size > 18 else "H2"
                            })
    title = doc.metadata.get("title", "Untitled")
    return {"title": title, "outline": outlines}
