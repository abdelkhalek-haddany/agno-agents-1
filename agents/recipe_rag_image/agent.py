from pathlib import Path
from agno.agent import Agent
from agno.embedder.cohere import CohereEmbedder
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.groq import Groq
from agno.tools.openai import OpenAITools
from agno.utils.media import download_image
from agno.vectordb.chroma import ChromaDb
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from config.settings import Settings

# Verify the env variables
settings = Settings()
settings.validate()

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=ChromaDb(
        collection="thai_recipes_collection",
        path="./chroma_db",
        embedder=CohereEmbedder(
            id="embed-v4.0",
        ),
    ),
)

knowledge_base.load()

agent = Agent(
    name="EmbedVisionRAGAgent",
    # model=OpenAIChat(id="gpt-4o-min", api_key=settings.openai_api_key),
    model=Gemini(id="gemini-2.0-flash", api_key=settings.gemini_api_key),
    tools=[OpenAITools()],
    knowledge=knowledge_base,
    instructions=[
        "You are a specialized recipe assistant.",
        "When asked for a recipe:",
        "1. Search the knowledge base to retrieve the relevant recipe details.",
        "2. Analyze the retrieved recipe steps carefully.",
        "3. Use the `generate_image` tool to create a visual, step-by-step image manual for the recipe.",
        "4. Present the recipe text clearly and mention that you have generated an accompanying image manual. Add instructions while generating the image.",
    ],
    markdown=True,
    debug_mode=True,
)

agent.print_response(
    "What is the recipe for a Thai curry?",
)

response = agent.run_response

# Create the tmp directory if it doesn't exist
tmp_dir = Path("tmp")
tmp_dir.mkdir(exist_ok=True)

# Add proper error handling and validation
if response.images:
    print(f"Number of images generated: {len(response.images)}")
    
    for i, image in enumerate(response.images):
        print(f"Image {i+1}: {image}")
        
        # Check if the image URL is valid
        if image.url:
            try:
                download_image(image.url, Path(f"tmp/recipe_image_{i+1}.png"))
                print(f"Successfully downloaded image {i+1} to tmp/recipe_image_{i+1}.png")
            except Exception as e:
                print(f"Failed to download image {i+1}: {e}")
        else:
            print(f"Image {i+1} URL is None or empty")
            
            # Try to access image content directly if URL is None
            if hasattr(image, 'content') and image.content:
                try:
                    import base64
                    import re
                    
                    content = image.content
                    
                    # Handle different content types
                    if isinstance(content, bytes):
                        # If it's already bytes, try to decode as base64 first
                        try:
                            content = content.decode('utf-8')
                        except:
                            # If it's already binary image data, save directly
                            with open(f"tmp/recipe_image_{i+1}.png", "wb") as f:
                                f.write(content)
                            print(f"Successfully saved binary image {i+1} to tmp/recipe_image_{i+1}.png")
                            continue
                    
                    # Convert to string if not already
                    content_str = str(content)
                    
                    # Try to extract pure base64 data
                    # Look for data URL format first
                    if content_str.startswith('data:'):
                        # Extract base64 part after comma
                        if ',' in content_str:
                            content_str = content_str.split(',', 1)[1]
                    
                    # Clean up the base64 string - remove any whitespace, newlines, etc.
                    content_str = re.sub(r'\s+', '', content_str)
                    
                    # Try to find PNG signature in base64
                    png_signature_b64 = 'iVBORw0KGgo'  # PNG signature in base64
                    
                    if png_signature_b64 in content_str:
                        # Extract from PNG signature onwards
                        start_idx = content_str.find(png_signature_b64)
                        content_str = content_str[start_idx:]
                        
                        # Find the end of PNG data (look for PNG end marker in base64)
                        png_end_b64 = 'IEND'  # PNG end chunk
                        if png_end_b64 in content_str:
                            # Find the complete end marker
                            end_patterns = ['IEND', 'AElFTkSuQmCC', 'wAAAABJRU5ErkJggg==']
                            for pattern in end_patterns:
                                if pattern in content_str:
                                    end_idx = content_str.find(pattern) + len(pattern)
                                    content_str = content_str[:end_idx]
                                    break
                    
                    # Ensure proper base64 padding
                    missing_padding = len(content_str) % 4
                    if missing_padding:
                        content_str += '=' * (4 - missing_padding)
                    
                    # Decode base64
                    image_data = base64.b64decode(content_str)
                    
                    # Verify it's a valid PNG by checking signature
                    if image_data.startswith(b'\x89PNG\r\n\x1a\n'):
                        with open(f"tmp/recipe_image_{i+1}.png", "wb") as f:
                            f.write(image_data)
                        print(f"Successfully saved PNG image {i+1} to tmp/recipe_image_{i+1}.png")
                        print(f"Image size: {len(image_data)} bytes")
                    else:
                        print(f"Warning: Image {i+1} doesn't appear to be a valid PNG")
                        # Save anyway for debugging
                        with open(f"tmp/recipe_image_{i+1}_raw.bin", "wb") as f:
                            f.write(image_data)
                        print(f"Saved raw data to tmp/recipe_image_{i+1}_raw.bin for debugging")
                        
                except Exception as e:
                    print(f"Failed to save image {i+1} content: {e}")
                    # Save raw content for debugging
                    try:
                        with open(f"tmp/recipe_image_{i+1}_debug.txt", "w") as f:
                            f.write(str(image.content)[:1000] + "..." if len(str(image.content)) > 1000 else str(image.content))
                        print(f"Saved debug content to tmp/recipe_image_{i+1}_debug.txt")
                    except:
                        pass
            else:
                print(f"Image {i+1} has no URL or content available")
else:
    print("No images were generated in the response")
    print("This might be due to:")
    print("1. The image generation tool failed")
    print("2. The API key for OpenAI (image generation) is missing or invalid")
    print("3. The model didn't call the image generation tool")
    
    # Debug: Print the full response structure
    print("\nFull response structure:")
    print(f"Response type: {type(response)}")
    print(f"Response attributes: {dir(response)}")
    
    # Check if there are any tool calls or errors
    if hasattr(response, 'tool_calls'):
        print(f"Tool calls: {response.tool_calls}")
    if hasattr(response, 'errors'):
        print(f"Errors: {response.errors}")