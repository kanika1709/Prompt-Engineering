import streamlit as st
import openai

# Function to mask PII info using OpenAI
def PII_masking_zero_shot(text, api_key):
    # Set OpenAI API key
    openai.api_key = api_key

    # Define the prompt
    prompt = "Mask the PII info from the following Input:\nInput: \"{TEXT}\"\nOutput:"

    # Create completions with the GPT-3.5 Turbo model
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )
    masked_text = completion.choices[0].message['content']
    return masked_text

def PII_masking_few_shot(text, api_key):
  # Set your OpenAI API key
  openai.api_key = api_key

  # Define the prompt

  SYSTEM_PROMPT = "You are a smart and intelligent PII masking system. I will provide you the definition of the PII entities you need to mask, the sentence from where you mask the entities and the output format with examples. Only mask the detected PII entities in the input sentence and keep the rest of the sentence as same."

  USER_PROMPT_1 = "Are you clear about your role?"

  ASSISTANT_PROMPT_1 = "Sure, I'm ready to help you with your NER task. Please provide me with the necessary information to get started."

  GUIDELINES_PROMPT = (
      "Below are the entity type and Entity Definition you need to mask:\n"
      "1. PERSON: Short name or full name of a person from any geographic regions.\n"
      "2. EMAIL ADDRESS: Email address of any individual from any host.\n"
      "3. PHONE_NUMBER: 10 digit Phone number of any individual \n"
      "4. CREDIT CARD: Credit Card details of any individual \n"
      "5. LOC: Name of any geographic location, like cities, countries, continents, districts etc.\n"
      "\n"
      "Examples:\n"
      "\n"
      "1. Example Input Sentence: Jacob lives in Madrid since 12th January 2015.\n"
      "Example Output: ['PERSON'] lives in ['LOC'] since 12th January 2015.\n"
      "\n"
      "2. Example Input Sentence: John's credit card number is 1234-5678-9876-5432 and his email id is johndoe@example.com.\n"
      "Example Output: ['PERSON']'s credit card number is ['CREDIT CARD'] and his email id is ['EMAIL ADDRESS'].\n"
      "\n"
      "3. Example Input Sentence: John's phone number is 1234565431.\n"
      "Example Output: ['PERSON']'s phone number is ['PHONE NUMBER']. \n"
      "\n"
      "4. Example Input Sentence: Akshita is Data Scientist.\n"
      "Example Output: ['PERSON'] is Data Scientist.\n"
      "\n"
      "5. Input Sentence to be masked by PII masking system: {}\n"
      "Masked Output by PII masking system: "
  )
  final_prompt = GUIDELINES_PROMPT.format(text)

  completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                      {"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": USER_PROMPT_1},
                      {"role": "assistant", "content": ASSISTANT_PROMPT_1},
                      {"role": "user", "content": final_prompt}
                  ]
    )

  masked_text = completion.choices[0].message['content']
  return masked_text


# Streamlit app
def main():
    st.title("PII Masking App")
    st.write("Enter the text containing PII (Personally Identifiable Information) to mask:")

    # Input text from user
    input_text = st.text_area("Input Text")

    # Input OpenAI API Key
    api_key = st.text_input("Enter OpenAI API Key")

    if st.button("Mask PII"):
        if not api_key:
            st.error("Please enter your OpenAI API Key")
        elif not input_text:
            st.error("Please enter some text")
        else:
            # Call PII_masking_zero_shot function to mask PII
            masked_text_zero_shot = PII_masking_zero_shot(input_text, api_key)
            st.success("Masked Text Zero shot:")
            st.write(masked_text_zero_shot)

            masked_text_few_shot = PII_masking_few_shot(input_text, api_key)
            st.success("Masked Text Few shot:")
            st.write(masked_text_few_shot)

if __name__ == "__main__":
    main()
