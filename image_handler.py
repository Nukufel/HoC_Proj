import base64
from openai import OpenAI


class ImageHandler:
    """Handles image analasyls."""

    def __init__(self):
        self._client = OpenAI()

    def extract(self, image_bytes: bytes, text: str = '') -> str:
        b64_image = base64.b64encode(image_bytes).decode('utf-8')

        hint_suffix = (
            f'\n\nThe user added this note with the image: "{text}"'
            if text
            else ''
        )

        prompt = (
            'You are a calendar extraction assistant. Analyse the image and extract '
            'every calendar event or appointment visible. '
            'For each event return a structured entry with:\n'
            '- Title\n'
            '- Date (in YYYY-MM-DD format if determinable)\n'
            '- Time (HH:MM 24h if visible)\n'
            '- Duration or end time (if visible)\n'
            '- Location (if visible)\n'
            'List only events. Ignore groceries, tasks, notes, or any other content. '
            'If no events are found, reply with "No events found."'
            'Preserve original language. Be precise — do not paraphrase.'
            + hint_suffix
        )

        response = self._client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': prompt},
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:image/jpeg;base64,{b64_image}',
                                'detail': 'high',
                            },
                        },
                    ],
                }
            ],
        )

        return response.choices[0].message.content
