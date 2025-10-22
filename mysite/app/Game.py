import os
from .sql_scripts import *

class Game:
    def __init__(self, name):
        self.name = name
        self.settings = {"classes": 'table table-striped table-hover', 'index': False}
        self.button_colors = {"blue": "btn-primary", "green": "btn-success", "red": "btn-warning"}
        self.filter = f"GAMES.NAME = '{name}'" if self.name is not None else "TRUE"

    def html_data(self, name, data, color="blue"):
        html = f"""
        <div class="container mt-5">
        <button id="{name}_button" class="btn {self.button_colors[color]} mb-3">Show {name}</button>
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

    def availability(self, newbs_only = True):
        query = f"""
        SELECT GAMES.NAME AS GAME,
                PT.TIMESPAN,
                COUNT(DISTINCT PERSON.NAME) AS NUMBER_AVAILABLE
        FROM PERSON 
        JOIN person_timespan AS PT ON PERSON.NAME = PT.PERSONID
        JOIN PERSON_GAMES AS PG ON PT.PERSONID = PG.PERSONID
        JOIN GAMES ON PG.GAMESID = GAMES.NAME
        JOIN TIMESPAN_DURATION AS TD ON PT.TIMESPAN = TD.NAME
        JOIN PERSON_NUMBERPLAYED AS PN ON PT.PERSONID = PN.name
        WHERE {self.filter}
        AND TD.DURATION = GAMES.DURATION
        AND PERSON.STATUS = 'Active' AND PERSON.NAME != 'Ian Kessler'
        and {"PN.numberplayed = '0'" if newbs_only else "True"} 
        GROUP BY GAMES.NAME, PT.TIMESPAN
        ORDER BY GAME, NUMBER_AVAILABLE DESC
        """
        button_label = f"Availability{' (Newbs Only)' if newbs_only else ''}"
        return self.html_data(button_label, readSQL(query).to_html(**self.settings))

    def people_interested(self):
        query = f"""
        SELECT PERSON_GAMES.GAMESID AS GAME,
                PERSON_GAMES.PERSONID AS PERSON
        FROM games 
        JOIN person_games ON GAMES.NAME = PERSON_GAMES.GAMESID
        JOIN PERSON ON PERSONID = PERSON.NAME
        WHERE {self.filter}
        and PERSON.STATUS = 'Active' 
        and PERSON.NAME != 'Ian Kessler'
        ORDER BY GAME, PERSON
        """
        return self.html_data("People Interested", readSQL(query).to_html(**self.settings))

    def allData(self):
        return "\n".join([self.availability(True), self.availability(False), self.people_interested()])


