import re
import json
import os
from dotenv import load_dotenv

load_dotenv(os.path.expanduser(".env"))

latex_file = os.getenv("RESUME_PATH")
js_file = os.getenv("WORKDATA_FILE")


def extract_curly_braces_content(text):
    stack = []  # Stack to keep track of opening braces
    contents = []  # List to store content extracted from lowest-level curly braces

    i = 0
    while i < len(text):
        if text[i] == "{" and (i == 0 or text[i - 1] != "\\"):
            # Start of a new curly brace section
            if stack:
                # If there's already an open brace, this is a nested brace
                # Mark the parent level as having nested braces
                stack[-1][1] = False
            # Push index and flag indicating it's a valid (non-nested) section
            stack.append([i, True])
        elif text[i] == "}" and (i == 0 or text[i - 1] != "\\"):
            # End of a curly brace section
            if stack:
                start, is_lowest = stack.pop()
                if is_lowest:
                    # Extract content between the braces
                    content = text[start + 1 : i]
                    # Add to list only if it's a lowest-level section
                    contents.append(content)
        i += 1

    return contents


def extract_jobs_from_section(content, section_name):
    section_pattern = re.compile(
        rf"\\section{{\s*{section_name}\s*}}\s*\\resumeSubHeadingListStart(.*?)\\resumeSubHeadingListEnd",
        re.DOTALL,
    )
    section_content = section_pattern.search(content)

    if not section_content:
        print(f"{section_name} section not found.")
        return []

    section_content = section_content.group(1)

    curly_braces_content = extract_curly_braces_content(section_content)

    jobs = []
    for index, content in enumerate(curly_braces_content, start=1):
        jobs.append(content)

    return jobs


def extract_jobs_from_latex(latex_path):
    with open(latex_path, "r") as file:
        content = file.read()

    work_experience_jobs = extract_jobs_from_section(content, "Work Experience")

    lab_experience_jobs = extract_jobs_from_section(content, "Lab Experience")

    all_jobs = work_experience_jobs + lab_experience_jobs

    return all_jobs


jobs_raw = extract_jobs_from_latex(latex_file)
job_data = [re.sub(r"\\", "", re.sub(r"--", "-", txt)) for txt in jobs_raw]
#  print(job_data)

companies = [
    "Kathalyst",
    "Human Interaction Lab (Tufts)",
    "Tufts Technology Services",
    "Tufts Department of Child Study & Human Development",
    "Tufts Conference & Event Services",
]

jobs = []

curr_job = {"title": None, "date": None, "role": None, "description": []}

i = 0
while i < len(job_data):
    if job_data[i] in companies:
        # save completed previous job
        if curr_job["title"]:
            jobs.append(curr_job)

        date_idx = i + 2 if "202" in job_data[i + 2] else i + 3
        curr_job = {
            "title": job_data[i],
            "date": job_data[date_idx],
            "role": job_data[i + 1],
            "description": [],
        }
        i = date_idx + 1

    else:
        curr_job["description"].append(job_data[i])
        i += 1

if curr_job["title"]:
    jobs.append(curr_job)

# this is the order that the jobs will show up in the webpage
keep = ["Kathalyst", "Human Interaction Lab (Tufts)", "Tufts Technology Services"]
filtered_jobs = []
for company in keep:
    filtered_jobs.append(next((d for d in jobs if d.get("title") == company), None))
json_string = json.dumps(filtered_jobs, indent=2)
print(json_string)


js_content = f"const workEntriesList = {json_string};"

with open(js_file, "w") as f:
    f.write(js_content)
