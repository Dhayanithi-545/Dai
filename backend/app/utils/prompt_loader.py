from pathlib import Path


PROMPTS_DIR = (
    Path(__file__)
    .resolve()
    .parent.parent
    / "mcp"
    / "prompts"
)


def load_prompt(
    file_name: str,
    **kwargs
):

    file_path = (
        PROMPTS_DIR
        / file_name
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        prompt = (
            file.read()
        )

    return prompt.format(
        **kwargs
    )