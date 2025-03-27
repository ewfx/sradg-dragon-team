from data_processing.process_data import  DataProcessing
from model.autoencoder_model.autoencoder import Autoencoder
from agentic_ai.agent import ask_question
from agentic_ai.catalyst_reconciliation_agent import GeminiCatalystReconciliationAgent, get_gemini_catalyst_agent
import  pandas as pd
import io
import uuid
from jira_access.jira_task import JIRATask

jira = JIRATask()

def train(file_path="data/train_data.csv"):
    pass

def __save_file(csv_string,file_base_path):
    csv_data = io.StringIO(csv_string)
    df = pd.read_csv(csv_data)

    # Generate a random file name
    random_filename = f"{file_base_path}/anomaly_data_{uuid.uuid4().hex[:8]}.csv"

    # Save the CSV file with the random name
    df.to_csv(random_filename, index=False)
    print(f"✅ CSV file '{random_filename}' generated successfully!")
    return random_filename

def __attatch_anomaly_score(data_frame,anomaly_score):
    # buffer = io.StringIO()
    data_frame["Comments"]=None
    key = "ANOMALY"
    data_frame[key] = anomaly_score
    df_filtered =data_frame [data_frame[key] != 0]
    # df_filtered.to_csv(buffer,index=False)
    # buffer.seek(0)
    return df_filtered.to_csv(index=False)

def predict(file_path,key_columns,criteria_columns,historic_columns,date_columns,derived_columns,usecase_id):
    if usecase_id.lower() == "ihub":
        csv_data= predict_ihub(file_path,key_columns,criteria_columns,historic_columns,date_columns,derived_columns)
        csv_file_save =__save_file(csv_data,"data/generated_result")
        jira.create_jira_issue(csv_file_save)
        return csv_data

    else:
        df = pd.read_csv(file_path)
        df = df.drop(columns=["COMMENT","Anomaly"])
        csv_data= __reconcile_catalyst_using_ai_agent(df.to_string(index=False),key_columns,criteria_columns,historic_columns,date_columns,derived_columns)
        csv_file_save =__save_file(csv_data,"data/generated_result")
        jira.create_jira_issue(csv_file_save)
        return csv_data

def predict_ihub(file_path,key_columns,criteria_columns,historic_columns,date_columns,derived_columns):
    data_processing = DataProcessing(file_path)
    df = data_processing.get_data_frame()
    x_test, y_test = data_processing.process_data_cleanup(
        columns=['As of Date', 'Primary Account', 'Secondary Account', 'Comments', 'ANOMALY'])
    model = Autoencoder(model=None)
    anomaly_col = model.predict(x_test, y_test)
    csv_value = __attatch_anomaly_score(df, anomaly_col)
    agentic_csv = __reconcile_using_ai_agent(csv_value, key_columns, criteria_columns, historic_columns, date_columns, derived_columns)
    return agentic_csv

def __reconcile_using_ai_agent(dataset_info,key_columns,criteria_columns,historic_columns,date_columns,derived_columns):
    return ask_question(dataset_info=dataset_info,key_columns=key_columns,criteria_columns=criteria_columns,derived_columns=derived_columns,date_columns=date_columns,historical_columns=historic_columns)

def __reconcile_catalyst_using_ai_agent(dataset_info,key_columns,criteria_columns,historic_columns,date_columns,derived_columns):
    agent = get_gemini_catalyst_agent()
    data = agent.ask_question(dataset_info=dataset_info,key_columns=key_columns,criteria_columns=criteria_columns,derived_columns=derived_columns,date_columns=date_columns,historical_columns=historic_columns)
    return data
