import os
import json
from pydoc import text
import re
from rapidfuzz import fuzz

# Common resume section headings
SECTION_HEADERS = {

    "summary": [
        "summary",
        "professional summary",
        "career summary",
        "career profile",
        "professional profile",
        "profile",
        "career objective",
        "objective"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical skill set",
        "skill set",
        "technical expertise",
        "professional expertise",
        "core competencies",
        "key skills"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "employment details",
        "career history"
    ],

    "education": [
        "education",
        "academic qualifications",
        "academic qualification",
        "qualification",
        "educational background"
    ],

    "projects": [
        "project",
        "projects",
        "academic projects",
        "personal projects",
        "project experience"
    ],

    "certifications": [
        "certification",
        "certifications",
        "certificate",
        "certificates",
        "licenses",
        "license"
    ],

    "achievements": [
        "achievements",
        "achievement",
        "awards",
        "honors",
        "accomplishments"
    ],

    "languages": [
        "language",
        "languages",
        "language proficiency"
    ]
}

# Keywords used for detecting sections without headings

SKILL_KEYWORDS = {
    "python", "java", "c", "c++", "sql", "mysql",
    "excel", "power bi", "tableau", "pandas",
    "numpy", "matplotlib", "seaborn", "tensorflow",
    "django", "flask", "html", "css", "javascript",
    "git", "linux", "aws", "azure", "docker",
    "figma",
    "adobe xd",
    "photoshop",
    "wireframing",
    "terraform",
    "google analytics",
    "google ads",
    "seo",
    "sem",
    "content marketing"
}

EDUCATION_KEYWORDS = {
    "b.tech", "btech", "b.e", "be",
    "mca", "bca", "mba",
    "m.tech", "mtech",
    "b.sc", "msc",
    "phd", "diploma",
    "degree",
    "university",
    "college",
    "cgpa",
    "percentage"
}

CERTIFICATION_KEYWORDS = {
    "certified",
    "certificate",
    "certification",
    "aws",
    "google",
    "microsoft",
    "oracle",
    "ibm",
    "cisco",
    "comptia",
    "professional certificate"
}

EXPERIENCE_KEYWORDS = {
    "pvt ltd",
    "private limited",
    "software engineer",
    "developer",
    "intern",
    "analyst",
    "engineer",
    "consultant",
    "manager",
    "company",
    "technologies",
    "worked",
    "experience"
}

TABLE_HEADERS = {
    "skill",
    "skills",
    "level",
    "degree",
    "college",
    "university",
    "institution",
    "year",
    "cgpa",
    "percentage",
    "marks",
    "grade"
}

def normalize_heading(text):
    text=text.strip().lower()
    text=re.sub(r'[^a-z0-9\s]','',text)
    text=' '.join(text.split())
    for section,heads in SECTION_HEADERS.items():
        if text in heads:
            return section
    # Avoid fuzzy matching full sentences as section headings
    if len(text.split()) > 4:
        return None
    best=None
    score_best=0
    for section,heads in SECTION_HEADERS.items():
        for h in heads:
            score=max(fuzz.ratio(text,h),fuzz.partial_ratio(text,h),fuzz.token_sort_ratio(text,h))
            if score>score_best:
                score_best=score
                best=section
    return best if score_best>=85 else None


def preprocess_layout(text):
    """
    Normalize resume layout before section parsing.

    Supports:
    - Pipe tables
    - Tab tables
    - Two-column resume layouts
    - Normal sequential text

    Requires:
        import re
        normalize_heading()
    """

    processed = []

    table_headers = {
        "skill","skills","level","degree","college","university",
        "institution","cgpa","percentage","year","marks","grade"
    }

    current_section = None

    column_mode = False
    left_heading = None
    right_heading = None
    left_items = []
    right_items = []

    def flush_columns():
        nonlocal column_mode,left_heading,right_heading
        nonlocal left_items,right_items

        if not column_mode:
            return

        if left_heading:
            processed.append(left_heading)
            processed.extend(left_items)

        processed.append("")

        if right_heading:
            processed.append(right_heading)
            processed.extend(right_items)

        processed.append("")

        column_mode = False
        left_heading = None
        right_heading = None
        left_items = []
        right_items = []

    for raw in text.splitlines():

        line = raw.rstrip()

        if not line.strip():
            flush_columns()
            processed.append("")
            continue

        if "|" in line:
            flush_columns()

            cells=[c.strip() for c in line.split("|") if c.strip()]

            if cells and all(c.lower() in table_headers for c in cells):
                continue

            if current_section=="skills":
                processed.append(cells[0])

            elif current_section=="education":
                if len(cells)>=2:
                    processed.append(f"{cells[0]} - {cells[1]}")
                elif cells:
                    processed.append(cells[0])

            else:
                processed.extend(cells)

            continue

        if "\t" in line:
            flush_columns()

            cells=[c.strip() for c in line.split("\t") if c.strip()]

            if cells and all(c.lower() in table_headers for c in cells):
                continue

            if current_section=="skills":
                processed.append(cells[0])

            elif current_section=="education":
                if len(cells)>=2:
                    processed.append(f"{cells[0]} - {cells[1]}")
                elif cells:
                    processed.append(cells[0])

            else:
                processed.extend(cells)

            continue

        if re.search(r"\s{2,}", line):

            cells=[c.strip() for c in re.split(r"\s{2,}", line) if c.strip()]

            if len(cells)==2:
                lh=normalize_heading(cells[0])
                rh=normalize_heading(cells[1])

                if lh and rh:
                    flush_columns()
                    column_mode=True
                    left_heading=cells[0]
                    right_heading=cells[1]
                    left_items=[]
                    right_items=[]
                    continue

            if column_mode and len(cells)==2:
                left_items.append(cells[0])
                right_items.append(cells[1])
                continue

            flush_columns()

        heading=normalize_heading(line.strip())

        if heading:
            current_section=heading

        processed.append(line.strip())

    flush_columns()

    return "\n".join(processed)


def segment_resume(text):
    text = preprocess_layout(text)

    sections = {"header": []}
    current = "header"
    header_lines = 0

    project_keywords = [
    "project",
    "management system",
    "dashboard",
    "analysis",
    "prediction",
    "application",
    "website",
    "portal",
    "inventory",
    "system",
    "classifier",
    "chatbot",
    "tracking",
    "monitoring"
]

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        heading = normalize_heading(line)
        if heading:
            current = heading
            sections.setdefault(current, [])
            continue

        clean = re.sub(r'^[•*\-\u2022]+\s*', '', line)
        lower_line = clean.lower()

        # Ignore common table headers
        if lower_line in TABLE_HEADERS:
            continue

        # Keep only the first two lines as header
        if current == "header" and header_lines < 2:
            sections["header"].append(clean)
            header_lines += 1
            continue
                # Continue the currently detected section
        if current in {"summary", "skills", "experience", "education", "certifications", "projects"}:
            if current == "skills":
                sections[current].extend(
                    [s.strip() for s in re.split(r",|/|;", clean) if s.strip()]
                )
            else:
                sections[current].append(clean)
            continue
        # Detect Education
        if any(
            re.search(rf"\b{re.escape(edu)}\b", lower_line)
            for edu in EDUCATION_KEYWORDS
        ): 
            current = "education"
            sections.setdefault(current, [])
            sections[current].append(clean)
            continue

        # Detect Certifications
        if any(cert in lower_line for cert in CERTIFICATION_KEYWORDS):
            current = "certifications"
            sections.setdefault(current, [])
            sections[current].append(clean)
            continue
            # Detect Experience
        if any(exp in lower_line for exp in EXPERIENCE_KEYWORDS):
            current = "experience"
            sections.setdefault(current, [])
            sections[current].append(clean)
            continue
        # Detect Projects
        if any(word in lower_line for word in project_keywords):
            current = "projects"
            sections.setdefault(current, [])
            sections[current].append(clean)
            continue

        # Detect Skills
        if any(skill in lower_line for skill in SKILL_KEYWORDS):
            current = "skills"
            sections.setdefault(current, [])
            sections[current].extend(
                [s.strip() for s in re.split(r",|/|;", clean) if s.strip()]
            )
            continue

    # Continue current section
    sections.setdefault(current, [])
    sections[current].append(clean)

    return sections

def process_resumes():
    input_folder='data/cleaned_text'
    output_folder='data/segmented_resumes'
    os.makedirs(output_folder,exist_ok=True)
    files=sorted([f for f in os.listdir(input_folder) if f.endswith('.txt')])
    print('='*60)
    print('Resume Section Segmentation Started')
    print('='*60)
    for filename in files:
        with open(os.path.join(input_folder,filename),'r',encoding='utf-8') as f:
            text=f.read()
        sections=segment_resume(text)
        out=os.path.join(output_folder,filename.replace('.txt','.json'))
        with open(out,'w',encoding='utf-8') as f:
            json.dump(sections,f,indent=4)
        print(f'Processed : {filename}')
        print(f'Saved     : {os.path.basename(out)}')
        print('-'*60)
    print(f'\nSuccessfully processed {len(files)} resumes.')
    print(f'Output Folder : {output_folder}')

if __name__=='__main__':
    process_resumes()
