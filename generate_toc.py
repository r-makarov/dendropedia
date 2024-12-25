import os
import json
import re

def sort_key(entry):
    # Extract the index from the entry name
    match = re.match(r"(\d+)_+(.*)", entry.name)
    if match:
        index = int(match.group(1))
        title = match.group(2).replace('_', ' ')
    else:
        index = float('inf')  # If no index, place it at the end
        title = entry.name.replace('_', ' ')
    return (index, title)

def generate_pages_json(directory, base_url="pages"):
    pages = []

    entries = sorted(os.scandir(directory), key=sort_key)

    for entry in entries:
        match = re.match(r"(\d+)_+(.*)", entry.name)
        title = match.group(2).replace('_', ' ') if match else entry.name.replace('_', ' ')

        if entry.is_dir():
            # Recursively process subdirectories
            pages.append({
                "title": title,
                "url": None,  # No direct URL for directories
                "children": generate_pages_json(entry.path, f"{base_url}/{entry.name}")
            })
        elif entry.is_file() and entry.name.endswith(".html"):
            # Process HTML files
            pages.append({
                "title": os.path.splitext(title)[0],  # Title is the file name without extension
                "url": f"{base_url}/{entry.name}"
            })

    return pages

def main():
    pages_dir = "pages"  # The folder containing your HTML files
    output_file = "pages.json"

    if not os.path.exists(pages_dir):
        print(f"Error: Directory '{pages_dir}' does not exist.")
        return

    pages = generate_pages_json(pages_dir)
    data = { "pages": pages }

    # Write to pages.json
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"'{output_file}' has been generated successfully.")

if __name__ == "__main__":
    main()
