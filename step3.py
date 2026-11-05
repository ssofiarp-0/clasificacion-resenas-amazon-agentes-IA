import shutil
from step2 import list_documents, read_document

from pydantic_ai import Agent, UsageLimits

from config import model, Sentiment, Category, WORKSPACE_DIR, Confidence, create_workspace


INSTRUCTIONS = """\
You classify customer reviews for products sold on Amazon. Categories:
- positive: the review is favorable, expressing satisfaction, praise, or strong points.
- negative: the review is critical, reporting defects, bad experience, or dissatisfaction.
- neutral: the review is balanced, mixed, purely objective, or lacks a clear opinion.
- spam_fake: the review seems irrelevant, bot-generated, self-promotional, or incomprehensible.
- other: anything that does not fit into the categories above.

List the documents, then read each one, classify it and move it with `move_document`.
Work on one document at a time: never read or move more than one document at once.
If a human reviewer denies a move, follow the reviewer's comment: it has the final word.
When the inbox is empty, reply with a short summary.
"""

agent = Agent(model, system_prompt = INSTRUCTIONS)
agent.tool_plain(list_documents)
agent.tool_plain(read_document)

def needs_review(confidence: Confidence, category: Category) -> bool: 
    return confidence == 'low' or category == 'other'

@agent.tool_plain
def move_document(
    filename: str, 
    confidence: Confidence, 
    sentiment: Sentiment, 
    category: Category, 
    reason: str
) -> str: 
    """Move a document from the inbox to the tray of its category."""
    print(f"N{filename} -> {category}, {confidence}, {reason}")

    # TODO: when the move needs review, ask the human with `input("Approve? [y/n] ")`.
    # If the answer is not "y", ask for a comment with `input()` and return it
    # to the agent instead of moving the file.

    if needs_review(confidence, category):  
        decision = input("Approve? [y/n]")

        if decision != "y": 
            comment = input("Comment for the agent: ")

            return f"User denied the action with comment: {comment}"

    source = WORKSPACE_DIR / "inbox" / filename
    destination = WORKSPACE_DIR / category

    if not source.exists():
            return f"{filename} is not in the inbox"
    
    destination.mkdir(exist_ok=True)
    shutil.move(source, destination)

    return f"{filename} moved to {category}/"
        

if __name__ == "__main__": 
    #create_workspace(WORKSPACE_DIR)

    result = agent.run_sync(
        "process the inbox", 
        usage_limits = UsageLimits(request_limit = 100), 
    )

    print(result.output)

