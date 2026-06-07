class ToolValidationService:

    @classmethod
    def validate_tool_result(
        cls,
        tool_name: str,
        result: dict
    ):

        if not result:

            return {
                "valid": False,
                "message":
                (
                    "Tool returned "
                    "empty result."
                )
            }

        if result.get("error"):

            return {
                "valid": False,
                "message":
                result["error"]
            }

        return {
            "valid": True,
            "message": None
        }