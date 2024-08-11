import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel

class InstagramSlides(BaseModel):
    slide_1: str
    slide_2: str
    slide_3: str
    slide_4: str
    slide_5: str


def generate_instagram_slides(article_title: str, html_content: str) -> dict:
    """
    Generates Instagram slide texts based on the article's HTML content and title.

    Args:
        article_title (str): The title of the article.
        html_content (str): The HTML content of the article.

    Returns:
        dict: A dictionary with slide numbers and corresponding texts in JSON format.
    """
    # Configure Ollama with the Mistral model
    ollama_llm = OllamaLLM(model="llama3.1")

    # Define the prompt template
    template = """
        Using the following HTML content: {html_content}\n\n
        Use the news article related to the {title}. \n
        Summarize the article and 5 eye-catching consecutive slides for an Instagram carousel that present the news in an eye-catching way. **Each slide should be writing in no more than 30 words**. \n
        **Avoid using hashtags, emojis or links**.\n
        Return the result only as a JSON array with each object containing the keys 'slide_number' and 'text' as values and a 'description' key for the description post using emojis. No other text or explanations should be included
        Example:
        {{
            "slide_1": "Summary of the first key point of the article.",
            "slide_2": "Summary of the second key point.",
            "slide_3": "Summary of the third key point.",
            "slide_4": "Summary of the fourth key point.",
            "slide_5": "Summary of the fifth key point.",
            "description": "Post description."        
        }}
    """
    
    
    # """
    #     Article HTML content: {html_content}\n\n
    #     Using the HTML content related to {title}, generate 5 short texts summarizing the news of the article for consecutive Instagram slides.
    #     The result should be in JSON format with the slides numbered.\n\n
    #     Use a catchy and provocative style, but **do not include any hashtags, emojis, or special characters**.\n\n
    #     Return only the JSON with 'slide_number' and 'text' keys.
    # """


    # Create the prompt template
    prompt = ChatPromptTemplate.from_template(template)

    parser = JsonOutputParser(pydantic_object=InstagramSlides)
 
    chain = prompt | ollama_llm |  parser

    # Generate the response
    response = chain.invoke({"title": article_title, "html_content": html_content})

    # Parse and return the JSON response
    return response
