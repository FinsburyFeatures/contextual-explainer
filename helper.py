import config
from PyPDF2 import PdfReader
import config
import anthropic

# Initialize the anthropic client
try:
    anthropic_client = anthropic.Client(config.ANTHROPIC_API_KEY)

except KeyError:
    sys.stderr.write("""
  You haven't set up your API key yet.
  
  If you don't have an API key yet, set on up on Anthropic.

  Then, open the Secrets Tool and add ANTHROPIC_API_KEY as a secret.
  """)
    exit(1)


def mine_document(pdf_file) -> str:
    """
      Function to process pdf files.
      This function reads a pdf file, processes it with an AI model, 
      and returns the processed results.

      Args:
          pdf_file (pdf): The uploaded pdf file.

      Returns:
          str: Result from the AI model.

      Raises:
          ValueError: If the number of tokens in the text exceeds 100,000.
      """

    # Create a PdfReader object for the file at the given path.
    reader = PdfReader(pdf_file)

    # Extract the text from each page of the pdf file and join them into a single string.
    article_text = "\n".join([page.extract_text() for page in reader.pages])

    # Construct the prompt for the AI model
    explanations_prompt = "From the following text, please extract ten key concepts. Please explain each concept with an example."
    prompt = (
        f"{anthropic.HUMAN_PROMPT}{explanations_prompt}\n{anthropic.HUMAN_PROMPT}{article_text}\n\n{anthropic.AI_PROMPT}"
    )

    # \n\n{anthropic.AI_PROMPT}
    # The above saved here for convenience - do we need/want this in the prompt?

    # Calculate the number of tokens in the text.
    token_count = anthropic.count_tokens(article_text)

    # Print the number of tokens.
    print(f"Number of tokens in text: {token_count}")

    # If the number of tokens is more than 100,000, raise an error.
    if token_count > 100000:
        raise ValueError(f"Text is too long {token_count}.")

    # Make a call to the AI model, using the constructed prompt and a specified model,
    # and limit the result to 1000 tokens.
    explanation_response = anthropic_client.completion(prompt=prompt,
                                                       model="claude-v1.3-100k",
                                                       max_tokens_to_sample=2000)

    methodological_instruction = "From the following text, please extract some methodological concepts that are used in the text. Please explain each methodological concept with an example. For each methodological concept please include some disscusion and different points of view from the wider literature."
    methodological_prompt = (
        f"{anthropic.HUMAN_PROMPT}{methodological_instruction}\n{anthropic.HUMAN_PROMPT}{article_text}\n\n{anthropic.AI_PROMPT}"
    )

    method_response = anthropic_client.completion(prompt=methodological_prompt,
                                                  model="claude-v1.3-100k",
                                                  max_tokens_to_sample=2000)

    # Return the result from the AI model
    return explanation_response["completion"] + "\n\n" + method_response["completion"]
