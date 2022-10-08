from importlib.machinery import all_suffixes
from transformers import BigBirdPegasusForConditionalGeneration, AutoTokenizer

print("Loading Summarizer model")
tokenizer = AutoTokenizer.from_pretrained("google/bigbird-pegasus-large-pubmed")

#feed input list in a single go
# by default encoder-attention is `block_sparse` with num_random_blocks=3, block_size=64
model = BigBirdPegasusForConditionalGeneration.from_pretrained(
    "google/bigbird-pegasus-large-pubmed"
)

limit = 4096


def breakup(input_text):
    """
    This function takes a single string as input and breaks it up into 
    multiple strings each of which has a length less than the limit set. 
    The strings are broken down at full stops 
    closest to the the limit set.

    Args:
        - A single string
    Returns:

        - A list of strings each of which has length less than the limit set after conversion into tokens."""

    # add full stop at the end of the text if not already present to mark end
    if input_text[-1] != ".":
        input_text += "."
    encoded_input = tokenizer(
        input_text
    )  # encode the entire text to get the total token size

    process = []
    to_loop = (
        len(encoded_input["input_ids"]) // limit + 1
    )  # check the number of chunks we can make of 512 token size

    for i in range(to_loop):
        breakup = tokenizer.decode(
            encoded_input["input_ids"][:limit]
        )  # convert first 512 tokens to raw text.

        end_sentence = breakup.rfind(
            "."
        )  # find the last full stop in the text to find the end of the last complete sentence

        if end_sentence != -1:
            process.append(
                breakup[0 : end_sentence + 1]
            )  # break the raw text at the last complete sentence and add it to the list
            input_text = input_text[end_sentence + 1 :]  # take the remaining raw text
            encoded_input = tokenizer(input_text)  # convert it into tokens again
        else:
            process.append(
                breakup
            )  # if full stop not found add the entire text to the list
            input_text = input_text[len(breakup) :]  # take the remaining raw text
            encoded_input = tokenizer(input_text)  # convert it into tokens again

    return process


def run_model(text):
    """
    This function takes a string as input and returns its' summary.

    Args:
        - A single string

    Returns:
        - Summary text
    """
    inputs = tokenizer(text, return_tensors="pt")
    prediction = model.generate(**inputs)
    prediction = tokenizer.batch_decode(prediction)
    return prediction[0]


def summarize(data, pagewise):
    """
    This function is used to summarize text pagewise or for the entire document.

    Args:
        - A dictionary with numbers as keys representing page numbers
         and strings as values representing text in pages.
        - A boolean True or False flag representing wheter to summarize
          pagewise or for the entire document.
    Returns:

        - A json file containing summaries for each page or for the entire document."""
    if pagewise:
        # append all text from all pages
        to_return = {}
        for i, to_summarize in enumerate(data.values()):
            print("Running summarizer for page number: ", i + 1)
            to_return[i] = run_model(to_summarize)
        return to_return
    else:
        to_summarize = " ".join(data.values())
        chunks = breakup(to_summarize)
        print("Running Summarizer for the entire text in pdf")
        all_summaries = [run_model(chunk) for chunk in chunks]
        return {0: " ".join(all_summaries)}
