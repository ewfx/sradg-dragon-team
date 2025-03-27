import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")
chat=(model.start_chat(history=[]))

question_template = """
You are a data analysis assistant. Given the dataset information below:

{dataset_info}

{key_columns} are the columns based on which two data source is merged,

{criteria_columns} are the columns which are matched between two data sources to mark the reconciliations as a Match or Break. These can be 
exact match or matching with some tolerance/buffer and is typically done by reconciliation rules engine.

{derived_columns} are the columns created during reconciliation process to facilitate break analysis.

{historical_columns} columns with  conjunction the {date_columns} to establish historical trends and patterns in the data.

in the dataset if the ANOMALY column has value 1 that means there is a possibility of anomaly but it is not full proof, please carefully co relate
the above data and try to find out the anomaly. and if anomaly found please write it to comments column of the dataset. then output a csv format of the anomaly 
data only , no explanation needed.
!! Alert: Strictly dont write the code to predict, predict at your side and give the result in expected format and no assumptions or
explanation needed just in csv format.
"""

def ask_question(dataset_info,key_columns,criteria_columns,derived_columns,historical_columns,date_columns):
    final_prompt = question_template.format(dataset_info=dataset_info,key_columns=key_columns,criteria_columns=criteria_columns,derived_columns=derived_columns,historical_columns=historical_columns,date_columns=date_columns)
    response = chat.send_message(final_prompt)

    resp = response.text
    cleaned_string = resp.replace("```csv", "").replace("```", "")
    return cleaned_string

# Space for Second UseCaese catalyst reconciliation

