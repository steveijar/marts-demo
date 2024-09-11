import os
import re
from openai import OpenAI



val = input("enter api key: ")

client = OpenAI(
    # This is the default and can be omitted
   # api_key=os.getenv("OPENAIKEY"),
     api_key = val
)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

filecontent = read_file('longtown-sheep-test.txt')


# Prompts for OpenAi might need refining for other auctions

firstprompt = 'You are a helpful assistant. The first prompt will be a long text,  and any messages that you get be regarding that. Please answer any questions and requests having in mind the first prompt'
secondprompt = 'from the text find the date , the auction location, type of auction, provide a  RFC8259 compliant JSON response  following this format without deviation [{   "date": "date of auction",  "auction_location": "the name of the town the auction took place",  "auction_type": "the category of animals in the auction " '
thirdprompt =' for each auction type in the json array return the text after the auction type line that contains a list of names and prices as a paragraph and append to json [{"auction_paragraph": "the paragraph of each auction type "'

# Create an empty list to hold the messages
messages = []

# Append each message as a dictionary to the list
messages.append({"role": "system", "content":firstprompt})
messages.append({"role": "user", "content": filecontent})
messages.append({"role": "user", "content": secondprompt})
messages.append({"role": "user", "content": thirdprompt})

# Use the list of messages in the ChatCompletion.create() function
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
)

#clean up the return as it includes some non valid text
def clean_json_string(json_string):
    pattern = r'^```json\s*(.*?)\s*```$'
    cleaned_string = re.sub(pattern, r'\1', json_string, flags=re.DOTALL)
    return cleaned_string.strip()


cleaned = clean_json_string(response.choices[0].message.content)

#  access the clean response save as file for further processing
f = open("longtown-sheep-test.json", "w")
f.write(cleaned)
f.close()




print(cleaned)

input("Press enter to close program")
