import os

from google import genai
from app.config.settings import settings


class GeminiService:

    client = None

    @classmethod
    def initialize(cls):

        try:
            os.environ[
                "GOOGLE_APPLICATION_CREDENTIALS"
            ] = settings.GOOGLE_APPLICATION_CREDENTIALS

            cls.client = genai.Client(
                vertexai=True,
                project=settings.GOOGLE_PROJECT_ID,
                location=settings.GOOGLE_LOCATION
            )

            print(
                "Gemini Client Initialized Successfully"
            )

        except Exception as e:
            print(
                f"Gemini Initialization Error: {e}"
            )

    @classmethod
    def get_client(cls):
        return cls.client

    @classmethod
    async def generate_response(
        cls,
        user_message: str
    ):

        try:

            response = cls.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_message
            )

            return response.text

        except Exception as e:
            return f"Gemini Error: {str(e)}"