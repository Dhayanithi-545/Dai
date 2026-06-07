class TraceService:

    @classmethod
    def initialize(
        cls
    ):

        return []

    @classmethod
    def add_step(
        cls,
        trace: list,
        step: str,
        details: str
    ):

        trace.append({

            "step":
            step,

            "details":
            details
        })

        return trace