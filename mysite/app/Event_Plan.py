import os
from .sql_scripts import *

class Event_Plan:
    def __init__(self, name):
        self.settings = {"classes": 'table table-striped table-hover', 'index': False}
        self.button_colors = {"blue": "btn-primary", "green": "btn-success", "red": "btn-warning"}
        self.name = name
        self.filter = f"EVENT_PLAN.NAME = '{self.name}'"
        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]
        self.day_str = "\n".join([f"[{day}]" for day in self.days])

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

    def summary(self, query):
        new_query = f"""
        SELECT START_HOUR,
               SUM(TOTAL_COUNT) FILTER (WHERE X.DAY = 'Monday') AS "Monday",
               SUM(TOTAL_COUNT) FILTER (WHERE X.DAY = 'Tuesday') AS "Tuesday",
               SUM(TOTAL_COUNT) FILTER (WHERE X.DAY = 'Wednesday') AS "Wednesday",
               SUM(TOTAL_COUNT) FILTER (WHERE X.DAY = 'Thursday') AS "Thursday",
               SUM(TOTAL_COUNT) FILTER (WHERE X.DAY = 'Friday') AS "Friday",
               SUM(TOTAL_COUNT) FILTER (WHERE X.DAY = 'Saturday') AS "Saturday",
               SUM(TOTAL_COUNT) FILTER (WHERE X.DAY = 'Sunday') AS "Sunday"
        FROM (
        ------
        SELECT  TIMESPAN,
        COUNT(PERSON) FILTER (WHERE x.AVAILABILITY_TYPE IN ('Primary', 'Secondary'))  AS TOTAL_COUNT,
        DAY,
        START_HOUR,
        HOUR_ORDER
        FROM (
        {query}
        ) AS X
        GROUP BY EVENT_PLAN, TIMESPAN, DAY, START_HOUR, HOUR_ORDER
        ------
        ) AS X
        GROUP BY START_HOUR, HOUR_ORDER
        ORDER BY HOUR_ORDER
        """
        return new_query


    def type_counts(self, query):
        new_query = f"""
        SELECT  EVENT_PLAN,
                TIMESPAN,
                COUNT(PERSON) FILTER (WHERE x.AVAILABILITY_TYPE = 'Primary')  AS PRIMARY_COUNT,
                COUNT(PERSON) FILTER (WHERE X.AVAILABILITY_TYPE = 'Secondary') AS SECONDARY_COUNT
        FROM (
        {query}
        ) AS X
        GROUP BY EVENT_PLAN, TIMESPAN
        ORDER BY PRIMARY_COUNT DESC, 
        SECONDARY_COUNT DESC
        """
        return new_query

    def display(self, query):
        new_query = f"""
        SELECT EVENT_PLAN,
        TIMESPAN,
        PERSON,
        AVAILABILITY_TYPE
        FROM (
        {query}
        )
        WHERE PERSON IS NOT NULL
        ORDER BY DAY_ORDER, HOUR_ORDER, AVAILABILITY_TYPE, PERSON
        """
        return new_query

    def week_data(self, week):
        query = f"""
        SELECT EVENT_PLAN.NAME      AS EVENT_PLAN,
        TIMESPAN.NAME               AS TIMESPAN,
        PEOPLE_FOR_EVENTPLAN.PERSON AS PERSON,
        AVAILABILITY_TYPE,
        DAY,
        START_HOUR,
        DAY_ORDER,
        HOUR_ORDER
        
        FROM EVENT_PLAN
        CROSS JOIN (VALUES (1), (2), (3), (4)) AS WEEKS(ID)
        JOIN TIMESPAN_DURATION AS TIMESPAN ON EVENT_PLAN.DURATION = TIMESPAN.DURATION
        JOIN (
        SELECT AT.TIMESPAN,
               ROW_NUMBER() OVER (PARTITION BY AT.TIMESPAN ORDER BY AT.AVAILABILITYID) AS RANK,
               AC.COLUMNNAME AS DAY,
               AR.ROWNAME AS START_HOUR,
               AC.COLUMNID AS DAY_ORDER,
               AR.ROWID AS HOUR_ORDER 
        FROM availability_timespan AS AT
        JOIN AVAILABILITY AS AV ON AT.availabilityid = AV.ID
        JOIN AVAILABILITY_COLUMN AS AC ON AV.COLUMNID = AC.COLUMNID
        JOIN AVAILABILITY_ROW AS AR ON  AV.ROWID = AR.ROWID
        ) AS TIMESPAN_START ON TIMESPAN.NAME = TIMESPAN_START.TIMESPAN AND RANK = 1
        LEFT JOIN (
        SELECT X.*
        FROM (
        SELECT PERSONID      AS PERSON,
        'Primary'     AS AVAILABILITY_TYPE,
        EVENTPLANID   AS EVENTPLAN,
        WEEK,
        TIMESPAN,
        NULL::VARCHAR AS GAME
        FROM PERSON_EVENTPLAN_TIMESPAN
        UNION ALL
        SELECT PERSON_TIMESPAN.PERSONID AS PERSON,
        'Secondary'              AS AVAILABILITY_TYPE,
        NULL::VARCHAR            AS EVENTPLAN,
        NULL::INT                AS WEEK,
        TIMESPAN,
        GAMESID                  AS GAME
        FROM PERSON_TIMESPAN
        JOIN PERSON_GAMES ON PERSON_TIMESPAN.PERSONID = PERSON_GAMES.PERSONID
        ) AS X 
        JOIN PERSON ON X.PERSON = PERSON.NAME
        WHERE NAME != 'Ian Kessler' AND PERSON.STATUS = 'Active'
        ) AS PEOPLE_FOR_EVENTPLAN
        ON
        (
        AVAILABILITY_TYPE = 'Primary'
            AND EVENTPLAN = EVENT_PLAN.name
            AND WEEK = WEEKS.ID
            AND PEOPLE_FOR_EVENTPLAN.TIMESPAN = TIMESPAN.NAME
        ) OR
        (
        AVAILABILITY_TYPE = 'Secondary'
            AND PEOPLE_FOR_EVENTPLAN.TIMESPAN = TIMESPAN.name
            AND PEOPLE_FOR_EVENTPLAN.GAME = EVENT_PLAN.GAME
            AND NOT EXISTS (SELECT 1
                            FROM PERSON_EVENTPLAN_AVAILABILITY AS PEPA
                            WHERE PEOPLE_FOR_EVENTPLAN.PERSON = PEPA.PERSONID
                            AND PEPA.EVENTPLANID = EVENT_PLAN.NAME)
        )
        WHERE {self.filter}
        AND WEEKS.ID = '{week}'
        ORDER BY TIMESPAN_START.DAY_ORDER, TIMESPAN_START.HOUR_ORDER
        """
        my_funcs = [self.summary, self.type_counts, self.display]
        sum_df, type_df, det_df = [readSQL(f(query)).to_html(**self.settings) for f in my_funcs]
        summary = self.html_data(f"Week {week} Summary", sum_df, "green")
        count_by_type = self.html_data(f"Week {week} Counts by Type", type_df,"green")
        detailed = self.html_data(f"Week {week} Detailed", det_df, "green")
        data = "\n".join([summary, count_by_type, detailed])
        return self.html_data(f"Week {week}", data)

    def allData(self):
        return "\n".join([self.week_data(week) for week in [1, 2, 3, 4]]) if self.name is not None else ""
