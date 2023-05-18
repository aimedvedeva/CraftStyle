import openai

openai.api_key = ''


def get_recommendation(image_urls, style_tags):
    prompt = "Given the following images and style tags, please provide a textual recommendation on how to finalize your look:\n"

    # Append the image URLs and style tags to the prompt
    for image_url, style_tag in zip(image_urls, style_tags):
        prompt += f"![Image]({image_url})\nStyle tag: {style_tag}\n"

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )

    recommendation = response.choices[0].text.strip()

    return recommendation


# Example usage
image_urls = [
    'https://drive.google.com/your-image-url1.jpg',
    'https://drive.google.com/your-image-url2.jpg',
    'https://drive.google.com/your-image-url3.jpg'
]
style_tags = ['casual', 'formal', 'sporty']

recommendation = get_recommendation(image_urls, style_tags)
print(recommendation)
