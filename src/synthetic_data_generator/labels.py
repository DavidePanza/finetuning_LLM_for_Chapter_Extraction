def format_labels(chapter_number, chapter_title, start_page, end_page):
    """Formats the chapter labels in a consistent JSON-like structure."""
    return (
        f'{{"chapter_number": "{chapter_number}", '
        f'"chapter_title": "{chapter_title}", '
        f'"start_page": {start_page}, '
        f'"end_page": {end_page}}},\n'
    )