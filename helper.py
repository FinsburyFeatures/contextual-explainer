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

  Then, open the Secrets Tool and add OPENAI_API_KEY as a secret.
  """)
  exit(1)


def mine_document(pdf_file) -> str:
  """
    Function to process legal case files.
    This function reads a pdf case file, processes it with an AI model, 
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
  text = "\n".join([page.extract_text() for page in reader.pages])

  
  # Construct the prompt for the AI model, including the text of the case file
  # and a request for the AI to extract key details from the text.
  extract = " here's a case file extract in <case> tags <case>{text}</case>"
  key_pieces = " understand then present the key pieces such as case ID, date, Plaintiff, Appellent, \
                what is the case type, jurisdiction, a short summary, sentiment and its impact on business, \
                and adverse findings, and outcome and put them in separate xml tags."
  
  prompt = (
      f"{anthropic.HUMAN_PROMPT}{extract}\n{anthropic.HUMAN_PROMPT}{key_pieces}\n\n{anthropic.AI_PROMPT}\n\ncase:"
  )

  # Calculate the number of tokens in the text.
  no_tokens = anthropic.count_tokens(text)

  # Print the number of tokens.
  print(f"Number of tokens in text: {no_tokens}")

  # If the number of tokens is more than 100,000, raise an error.
  if no_tokens > 100000:
    raise ValueError(f"Text is too long {no_tokens}.")


  # Make a call to the AI model, using the constructed prompt and a specified model,
  # and limit the result to 1000 tokens.
  res = anthropic_client.completion(prompt=prompt,
                                    model="claude-v1.3-100k",
                                    max_tokens_to_sample=1000)

  # Return the result from the AI model, which contains the extracted case details in XML format.
  return res["completion"]
