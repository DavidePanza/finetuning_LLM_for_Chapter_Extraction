import re
from collections import OrderedDict


def parse_structured_toc(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    books = []
    
    current_book = None
    current_chapter = None
    
    # Regex patterns
    book_title_re = re.compile(r"^(\d+)\.\s+(.+)", re.IGNORECASE)
    chapter_re = chapter_re = re.compile(r"^[•\*]?\s*Chapter\s+(\d+):\s+(.+)$", re.IGNORECASE)
    subchapter_re = re.compile(r"^(\d+)\.(\d+)\s+(.+)$")

    for line in lines:
        # Check if this is a new book title
        if (match := book_title_re.match(line)):
            # Save previous book if exists
            if current_book:
                books.append(current_book)
            
            # Start new book
            current_book = OrderedDict()
            current_book["id"] = int(match.group(1))
            current_book["name"] = match.group(2).strip()
            current_book["chapters_counts"] = 0
            current_book["chapters"] = []
            current_chapter = None

        # Check if this is a chapter
        elif (match := chapter_re.match(line)) and current_book:
            number = int(match.group(1))
            title = match.group(2).strip()
            current_chapter = {
                "number": number,
                "title": title,
                "subchapter_count": 0,
                "subchapters": []
            }
            current_book["chapters_counts"] = len(current_book["chapters"])
            current_book["chapters"].append(current_chapter)

        # Check if this is a subchapter
        elif (match := subchapter_re.match(line)) and current_chapter:
            sub_number = f"{match.group(1)}.{match.group(2)}"
            title = match.group(3).strip()
            current_chapter["subchapters"].append({
                "number": sub_number,
                "title": title
            })
            # Update subchapter count
            current_chapter["subchapter_count"] = len(current_chapter["subchapters"])
    # Don't forget to add the last book
    if current_book:
        books.append(current_book)

    # If only one book, return it directly (maintains backward compatibility)
    if len(books) == 1:
        return books[0]
    
    # If multiple books, return list
    return books