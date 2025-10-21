import psycopg2
from decouple import config
import pandas as pd

def sqlTuple(*fields):
    return ', '.join([f"'{field}'" for field in fields])

def addPerson(name, status = 'Active'):
    command = f"""
    INSERT INTO PERSON (NAME, STATUS) VALUES ({sqlTuple(name, status)})
    """
    return command

def deletePerson(name):
    invites = f"DELETE FROM INVITATION WHERE PERSON = '{name}';"
    form_requests = f"DELETE FROM FORM_REQUESTS WHERE PERSON = '{name}';"
    form_submissions = f"DELETE FROM FORM_SUBMISSIONS WHERE PERSON = '{name}';"
    eventplan_availability = f"DELETE FROM PERSON_EVENTPLAN_AVAILABILITY WHERE PERSONID = '{name}';"
    person = f"DELETE FROM PERSON WHERE NAME = '{name}';"
    delete_stmts = [invites, form_requests, form_submissions, eventplan_availability, person]
    return delete_stmts

def request(person, form, timestamp):
    command = f"""
    INSERT INTO FORM_REQUESTS (PERSON, FORM, TIMESTAMP) VALUES ({sqlTuple(person, form, timestamp)})
    """
    return command

def invite(event, timestamp, person, plus_ones, result):
    command = f"""
    INSERT INTO INVITATION (EVENT, TIMESTAMP, PERSON, PLUS_ONES, RESULT) VALUES
    ({sqlTuple(event, timestamp, person, plus_ones, result)})
    """
    return command

def queried_df(cursor, query):
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    data = [[str(x) for x in tuple(y)] for y in cursor.fetchall()]
    return pd.DataFrame(data=data, columns=columns)

def callList(event_id):
    query = f"""
            Select Person.Name, 
               EXISTS (
                    SELECT 1
                    FROM invitation
                    where invitation.person = person.name
                    and invitation.event = '{event_id}'
               ) AS Invited,
               Redeem, 
               New, 
               CompletedSurvey, 
               ExpectedAttendance, 
               ExpectedInvite
            from Person 
            Left Join Person_Games on Person.name = Person_Games.PersonID
            Left Join Person_Timespan on Person.name = Person_Timespan.personid
            Left Join Person_Redeem on Person.name = Person_Redeem.name
            Left Join Person_CompletedSurvey on Person.name = Person_CompletedSurvey.name
            Left Join Person_Expected on Person.name = Person_Expected.Name
            Left Join Person_Due on Person.name = Person_Due.name
            Left Join Event on Person_Games.gamesid = event.game and Person_Timespan.timespan = event.timespan
            Where (
                    Person_Redeem.Redeem or 
                    (
                    Person_Due.EventDue 
                    and Person_Due.InviteDue
                    )
                    ) 
                and person.name != 'Ian Kessler' 
                and Person.Status = 'Active'
                and (
                    Not Person_Completedsurvey.CompletedSurvey 
                    or Event.EventId = '{event_id}'
                    )
            Order By Invited,
                     Redeem Desc, 
                     New Desc, 
                     CompletedSurvey Desc, 
                     ExpectedAttendance, 
                     ExpectedInvite, 
                     Person.Name
    """
    return query

def plannedCallList(event_id):
    query = f"""
            Select Person.Name, 
                    Submitted_EPA, 
                    Redeem, 
                    ExpectedAttendance, 
                    ExpectedInvite
            from Person
            left join person_games on person.name = person_games.personid
            left join person_timespan on person.name = person_timespan.personid
            left join person_redeem on person.name = person_redeem.name
            left join person_completedepa on person.name = person_completedepa.name
            left join person_expected on person.name = person_expected.name
            left join person_due on person.name = person_due.name
            left join person_eventplan_timespan on person.name = person_eventplan_timespan.personid
            Left Join event as event_general on 
                person_games.gamesid = event_general.game and 
                person_timespan.timespan = event_general.timespan
            left join event as event_planned on person_completedepa.eventplanid = event_planned.event_plan
            where event_planned.eventid = '{event_id}' 
            and (
                    (
                        person_completedepa.submitted_epa
                        and person_eventplan_timespan.eventplanid = event_planned.event_plan
                        and person_eventplan_timespan.timespan = event_planned.timespan
                        and person_eventplan_timespan.week = event_planned.week
                    ) or 
                    (   
                        not person_completedepa.submitted_epa 
                        and event_general.eventid = '{event_id}' 
                        and (redeem or (eventdue and invitedue))
                        and person.name != 'Ian Kessler' 
                        and status = 'Active'
                    )
            ) 
            group by Person.Name, 
                    Submitted_EPA, 
                    Redeem, 
                    ExpectedAttendance, 
                    ExpectedInvite
            order by submitted_epa desc, 
                    redeem desc, 
                    expectedattendance, 
                    expectedinvite, 
                    person.name
    """
    return query

def callListDF(event_id):
    df = readSQL(f"Select event_plan from event where eventid = '{event_id}'")
    event_plan = df['event_plan'].iloc[0]
    return readSQL(callList(event_id)) if event_plan == "None" else readSQL(plannedCallList(event_id))


def executeSQL(*commands):
    try:
        connection = psycopg2.connect(user = config("DB_USER"),
                                      password = config("DB_PASSWORD"),
                                      host = config("DB_HOST"),
                                      port = config("DB_PORT"),
                                      database = config("DB_NAME"))
        cursor = connection.cursor()
        for command in commands:
            command = command.replace("'None'", "NULL").replace("''", "NULL")
            cursor.execute(command)
        connection.commit()

    except psycopg2.Error as e:
        print(e)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")

def readSQL(query):
    try:
        connection = psycopg2.connect(user = config("DB_USER"),
                                      password = config("DB_PASSWORD"),
                                      host = config("DB_HOST"),
                                      port = config("DB_PORT"),
                                      database = config("DB_NAME"))
        cursor = connection.cursor()
        df = queried_df(cursor, query)
        return df

    except psycopg2.Error as e:
        print(e)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")