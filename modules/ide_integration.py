# programmers_assistant/modules/ide_integration.py

from typing import Optional

# Simulate code being read directly from an IDE
# In a real system, this could interface with VS Code, PyCharm, etc.

def get_open_code() -> Optional[str]:
    try:
        # Placeholder: Pretend this reads from a temp file the IDE syncs to
        with open("programmers_assistant/data/open_code.py", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
