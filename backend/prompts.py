PROMPT_VERSION = "v1"


def build_overview_prompt(title: str, synopsis: str) -> str:
    return f"""You are writing a short teaser for the film "{title}".

Here is the official synopsis. It may contain spoilers:
<synopsis>
{synopsis}
</synopsis>

Write a 1-2 sentence teaser that makes someone want to watch it.
Make it human-like, not AI/robotic like.
Don't use complicated words or phrases. Make it easy to read and understand.
ALso, don't use "—"
Rules:
- Do not include any spoilers in your teaser.
- Only say what type of person would want to watch it, and what type of 
experience they will have.
"""