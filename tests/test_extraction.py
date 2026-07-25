import os

def test_cleaned_text_output():
    output_folder = "data/cleaned_text"

    # Check output folder exists
    assert os.path.exists(output_folder)

    # Check text files were created
    txt_files = [f for f in os.listdir(output_folder) if f.endswith(".txt")]
    assert len(txt_files) > 0

    # Check files are not empty
    for file in txt_files:
        with open(os.path.join(output_folder, file), "r", encoding="utf-8") as f:
            assert f.read().strip() != ""