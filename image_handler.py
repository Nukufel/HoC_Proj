import base64
from openai import OpenAI


class ImageHandler:
    """Handles vision-based extraction of structured data from images."""

    VISION_MODEL = "gpt-4o-mini"

    def __init__(self):
        self._client = OpenAI()

    def extract(self, image_bytes: bytes, user_hint: str = "") -> str:
        """
        Send *image_bytes* to the vision model and return the extracted text.

        Args:
            image_bytes: Raw image bytes (JPEG or PNG).
            user_hint:   Optional caption / note the user attached to the image.

        Returns:
            A structured string with labelled categories (EVENTS, TASKS, etc.).
        """
        b64_image = base64.b64encode(image_bytes).decode("utf-8")

        hint_suffix = (
            f"\n\nThe user added this note with the image: \"{user_hint}\""
            if user_hint
            else ""
        )

        prompt = (
            "You are a data-extraction assistant. Carefully read the image and extract "
            "every piece of actionable information. Return a structured list with "
            "clearly labelled categories:\n"
            "- EVENTS: date, time, title, location (if visible)\n"
            "- TASKS / TO-DOs: exact wording of each task\n"
            "- GROCERY ITEMS: each item with quantity if shown\n"
            "- NOTES / REMINDERS: verbatim text\n"
            "If a category has no items, omit it. "
            "Preserve original language. Be precise — do not paraphrase."
            + hint_suffix
        )

        response = self._client.chat.completions.create(
            model=self.VISION_MODEL,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}",
                            "detail": "high",
                        },
                    },
                ],
            }],
        )

        return response.choices[0].message.content
