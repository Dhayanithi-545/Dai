import os

from google import genai


class GeminiService:

    client = None

    @classmethod
    def initialize(cls):

        try:

            os.environ[
                "GOOGLE_APPLICATION_CREDENTIALS"
            ] = (
                "/home/"
                "dhayanithi-anandan/"
                "PD/TICM/"
                "ticm-qa.json"
            )

            cls.client = (
                genai.Client(
                    vertexai=True,
                    project="ticm-qa",
                    location="us-central1"
                )
            )

            print(
                "Gemini Initialized"
            )

        except Exception as e:

            print(
                f"Gemini Init Error: {e}"
            )

    @classmethod
    async def generate_response(
        cls,
        prompt: str
    ):

        try:

            # Safety fallback
            if cls.client is None:

                cls.initialize()

            response = (
                cls.client.models.generate_content(
                    model=
                    "gemini-2.5-flash",

                    contents=
                    prompt
                )
            )

            return (
                response.text
            )

        except Exception as e:

            print(
                f"Gemini Error: {e}"
            )

            return (
                "Dai encountered "
                "an AI issue."
            )

            