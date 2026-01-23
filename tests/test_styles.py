from agents.content_refiner import ContentRefiner
from agents.content_generator import generate_content

def test_generate_content():
    # Sample article text
    article_text = (
        "OpenAI released a new agent framework that allows autonomous task execution."
    )

    platforms = ["twitter", "medium", "youtube"]

    for platform in platforms:
        print(f"\n--- Testing platform: {platform.upper()} ---")
        refined_output = generate_content(article_text, platform)
        print(refined_output)
        print("\n" + "="*50)

if __name__ == "__main__":
    test_generate_content()
