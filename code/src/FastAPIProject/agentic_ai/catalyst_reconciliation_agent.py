import os
import google.generativeai as genai
from dotenv import load_dotenv


class GeminiCatalystReconciliationAgent:
    _question_template = """
    You are a data analysis assistant. Given the dataset information below:

    {dataset_info}

    {key_columns} are the columns based on which two data source is merged,

    {criteria_columns} are the columns which are matched between two data sources to mark the reconciliations as a Match or Break. These can be 
    exact match or matching with some tolerance/buffer and is typically done by reconciliation rules engine.

    {derived_columns} are the columns created during reconciliation process to facilitate break analysis.

    {historical_columns} columns with  conjunction the {date_columns} to establish historical trends and patterns in the data.

     please carefully co relate the above data and try to find out the anomaly. and if anomaly found please write it to comments column of the dataset and 1 to anomaly column. then output a csv format of the anomaly 
    data only , no explanation needed
    
    !! Alert: Strictly dont write the code to predict, predict at your side and give the result in expected format and no assumptions or warning or **Important Notes:** or
    explanation needed just in csv format.
    """

    def __init__(self,train_data_set):
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        self._model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        
            Context: This is for your context understand the data not need to do any processing or writing code on it
            you are a data analysis assistant. Given the dataset information below:
            {train_data_set}.
            
            read the dataset thoroughly and try to analyze it. and drive the relationship in between the columns
            and the column "ANOMALY" is the column says if this data point is anomalous or not.
            
            please try to drive the relationship in between the columns and the column "ANOMALY". 
        
        """
        self._chat = self._model.start_chat(history=[])
        self._chat.send_message(prompt)

    def ask_question(self,dataset_info, key_columns, criteria_columns, derived_columns, historical_columns, date_columns):
        final_prompt = self._question_template.format(dataset_info=dataset_info, key_columns=key_columns,
                                                criteria_columns=criteria_columns, derived_columns=derived_columns,
                                                historical_columns=historical_columns, date_columns=date_columns)
        response = self._chat.send_message(final_prompt)

        resp = response.text
        cleaned_string = resp.replace("```csv", "").replace("```", "")
        return cleaned_string


gemini_catalyst_rec_agent = GeminiCatalystReconciliationAgent("data/catalyst/extended_anomaly_testcases_catalyst.csv")

def get_gemini_catalyst_agent():
    return gemini_catalyst_rec_agent