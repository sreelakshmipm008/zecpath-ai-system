import os

from extractors.pdf_reader import extract_pdf_text
from extractors.docx_reader import extract_docx_text
from preprocess.text_cleaner import clean_text

# Input and output folders
input_folder = "data/resumes"
output_folder = "data/cleaned_text"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process all resume files
for file in os.listdir(input_folder):

    file_path = os.path.join(input_folder, file)

    if file.endswith(".pdf"):
        text = extract_pdf_text(file_path)

    elif file.endswith(".docx"):
        text = extract_docx_text(file_path)

    else:
        continue


    # Clean the extracted text
    cleaned_text = clean_text(text)


    # -------------------------------
    # Save cleaned text
    # -------------------------------
    output_file = os.path.join(
        output_folder,
        os.path.splitext(file)[0] + ".txt"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

print("\n✅ Resume text extraction completed successfully!")