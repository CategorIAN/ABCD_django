import os
from .sql_scripts import *

class Person:
    def __init__(self, name):
        self.name = name
        self.filter = f"WHERE NAME LIKE '%{self.name}%'" if self.name is not None else ""
        self.settings = {"classes": 'table table-striped table-hover', 'index': False}

    def html_data(self, name, data):
        html = f"""
        <div class="container mt-5">
        <button id="{name}_button" class="btn btn-primary mb-3">Show {name}</button>
        </div>
        
        <div id="{name}" class="container mt-5" style="display: none;">
        {data}
        </div>
        """
        java_script = f"""
        <script>
        document.addEventListener("DOMContentLoaded", function () {{
            const button = document.getElementById("{name}_button");
            const container = document.getElementById("{name}");
                button.addEventListener("click", function () {{
                if (container.style.display === "none") {{
                    container.style.display = "block";
                    button.textContent = "Hide {name}";
                }} else {{
                    container.style.display = "none";
                    button.textContent = "Show {name}";
                }}
            }});
        }});
        </script>
        """
        return html + "\n" + java_script

    def readText(self):
        columns = readSQL("SELECT NAME FROM FORM_QUESTION WHERE FORM = 'ABCD General Survey' AND TYPE = 'Text'")
        query = f"""
        SELECT 
                {sqlColumns(columns["name"])}
        FROM PERSON
        {self.filter}
        """
        return self.html_data("Text", readSQL(query).to_html(**self.settings))

    def readLinScale(self):
        columns = readSQL("SELECT NAME FROM FORM_QUESTION WHERE FORM = 'ABCD General Survey' AND TYPE = 'Linear Scale'")
        query = f"""
        SELECT 
                {sqlColumns(columns["name"])}
        FROM PERSON
        {self.filter}
        """
        return self.html_data("Liner Scale", readSQL(query).to_html(**self.settings))

    def readMultChoice(self):
        columns = readSQL("SELECT NAME FROM FORM_QUESTION WHERE FORM = 'ABCD General Survey' AND TYPE = 'Multiple Choice'")
        query = f"""
        SELECT 
                {sqlColumns(columns["name"])}
        FROM PERSON
        {self.filter}
        """
        return self.html_data("Multiple Choice", readSQL(query).to_html(**self.settings))

    '''
    def readCheckBox(self):
        columns = readSQL("SELECT NAME FROM FORM_QUESTION WHERE FORM = 'ABCD General Survey' AND TYPE = 'CheckBox'")
        field_ = f"""
        SELECT NAME FROM FORM_QUESTION WHERE FORM = 'ABCD General Survey' AND TYPE = 'CheckBox'
        """
    '''



