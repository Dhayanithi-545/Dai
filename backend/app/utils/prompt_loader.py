from pathlib import Path


def load_prompt(
    filename: str,
    **kwargs
):

    prompt_path = (
        Path(__file__)
        .parent.parent
        / "mcp"
        / "prompts"
        / filename
    )

    with open(
        prompt_path,
        "r",
        encoding="utf-8"
    ) as file:

        prompt = file.read()

    return prompt.format(
        **kwargs
    )