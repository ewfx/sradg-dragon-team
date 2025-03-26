import os

from jira import JIRA
import dotenv



class JIRATask:
    def __init__(self):
        dotenv.load_dotenv()
        self._jira_server = os.getenv("JIRA_SERVER")
        self._jira_user = os.getenv("JIRA_USER")
        self._jira_password = os.getenv("JIRA_API_KEY")
        self._jira_project = os.getenv("JIRA_PROJECT")


    def __create_jira_client(self):
        return JIRA(server=self._jira_server, basic_auth=(self._jira_user, self._jira_password))

    def create_jira_issue(self,csv_file_path,description = "Anomaly detected refer the attatchment for more details"):
        jira = self.__create_jira_client()
        issue_dict = {
            'project': {'key': self._jira_project},
            'summary': 'Bug in Payment Gateway',
            'description': description,
            'issuetype': {'name': 'Bug'}
        }
        new_issue = jira.create_issue(fields=issue_dict)
        print(f"✅ Issue created successfully! Key: {new_issue.key}")
        with open(csv_file_path, "rb") as attachment:
            jira.add_attachment(issue=new_issue, attachment=attachment)
        print(f"📎 Attachment '{csv_file_path}' added successfully to {new_issue.key}!")

        # Add a comment to the issue
        jira.add_comment(new_issue, "This is a follow-up comment with more information.")
        print("💬 Comment added successfully!")