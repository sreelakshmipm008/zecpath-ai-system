import os


INPUT_FOLDER = "data/resumes"
OUTPUT_FOLDER = "data/cleaned_text"


def test_output_folder_exists():
    """Check if the output folder exists."""
    assert os.path.exists(OUTPUT_FOLDER), "Output folder does not exist."


def test_all_resumes_processed():
    """Check that every input resume has a corresponding output text file."""

    input_files = [
        f for f in os.listdir(INPUT_FOLDER)
        if f.lower().endswith((".pdf", ".docx"))
    ]

    output_files = [
        f for f in os.listdir(OUTPUT_FOLDER)
        if f.lower().endswith(".txt")
        and f.rsplit(".", 1)[0] in {
            os.path.splitext(input_file)[0]
            for input_file in input_files
        }
    ]

    assert len(input_files) == len(output_files), (
        f"Expected {len(input_files)} output files, "
        f"but found {len(output_files)}."
    )


def test_output_files_are_not_empty():
    """Check that every generated text file contains extracted content."""

    txt_files = [
        f for f in os.listdir(OUTPUT_FOLDER)
        if f.lower().endswith(".txt")
    ]

    assert len(txt_files) > 0, "No output text files found."

    for file in txt_files:

        file_path = os.path.join(OUTPUT_FOLDER, file)

        with open(file_path, "r", encoding="utf-8") as f:

            text = f.read().strip()

            assert len(text) > 0, f"{file} is empty."


def test_supported_output_format():
    """Check that all generated files are in .txt format."""

    for file in os.listdir(OUTPUT_FOLDER):

        assert file.lower().endswith(".txt"), (
            f"Unexpected output file found: {file}"
        )