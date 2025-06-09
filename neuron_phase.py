from groq import Groq
from dotenv import load_dotenv
import base64
load_dotenv()
# image_path="images/acne.jpg"

def load_image_as_base64(image_path):
    """
    Reads an image from the filesystem and returns its base64-encoded string.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def build_groq_messages(query_text, image_base64):
    """
    Constructs the messages payload for Groq chat completion with image input.
    """
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query_text},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
            ],
        }
    ]


def analyze_image_with_groq(image_path, query,model):
    """
    Calls Groq Vision-enabled model with the image and returns the response.
    """
    client = Groq()
    image_base64 = load_image_as_base64(image_path)
    messages = build_groq_messages(query, image_base64)

    model = model

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    return response.choices[0].message.content

