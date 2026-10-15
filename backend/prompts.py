PROMPT_VERSION = "v1"


def build_overview_prompt(title: str, synopsis: str) -> str:
    return f"""You are writing a short teaser for the film "{title}".

Here is the official synopsis. It may contain spoilers:
<synopsis>
{synopsis}
</synopsis>

Write a 2-3 sentence teaser that makes someone want to watch it.

Rules:
- Use only facts from the synopsis. Do not add anything.
- No spoilers: do not reveal twists, deaths, who wins, or how it ends.
- Describe the set-up only: who the main character is and what they want.
- Plain text only. No headings, lists or quotation marks.
"""