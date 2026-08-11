# Tabletop Event Planning Application

A full-stack event-planning system that uses participant survey data to automate scheduling, invitations, reporting, and other workflows for recurring tabletop gaming events.

The system consists of a Python ETL pipeline that transforms Google Forms survey responses into a normalized PostgreSQL database and a Django web application that uses the resulting data for event planning and administration.

## Repositories

The project is divided into two repositories:

* **ETL / Data Processing:** [ABCD](https://github.com/CategorIAN/ABCD)
* **Django Web Application:** [ABCD_django](https://github.com/CategorIAN/ABCD_django)

## Technology Stack

* Python
* Django
* PostgreSQL
* Pandas
* psycopg2
* HTML
* Bootstrap
* JavaScript
* Google Forms

## System Architecture

```text
Google Forms
      ↓
CSV Export
      ↓
Python ETL Pipeline
      ↓
Normalized PostgreSQL Database
      ↓
Django Web Application
      ↓
Event Planning / Invitations / Reports / Analytics
```

## ETL Pipeline

The ETL pipeline imports participant responses exported from Google Forms and transforms them into a normalized relational database.

Major functionality includes:

* Reading Google Forms CSV exports
* Cleaning and standardizing participant data
* Removing duplicate submissions
* Incrementally synchronizing participant information
* Creating and updating lookup tables
* Recording survey submission history
* Mapping survey responses into normalized relational structures

The importer is metadata-driven rather than being hardcoded for individual survey questions. It supports text, linear-scale, multiple-choice, checkbox, and checkbox-grid questions.

## Relational Database

PostgreSQL stores participant and event-planning information in a normalized schema.

Major entities include:

* Participants
* Games
* Meals
* Events
* Event Plans
* Availability
* Invitations
* Form Requests
* Form Submissions
* Time Spans

Multi-value responses such as checkboxes and grids are represented using lookup and bridge tables rather than storing multiple values in individual columns.

## Event Planning and Scheduling

The application converts participant availability into relational scheduling data and generates valid scheduling windows based on an event's required duration.

When planning an event, the system:

1. Retrieves event-specific participant availability when available.
2. Falls back to participants' general availability when necessary.
3. Matches participants with game preferences.
4. Matches participants with valid scheduling windows.
5. Generates reports for evaluating potential event dates and times.

The resulting reports summarize participant availability and help identify suitable times for future events.

## Invitation Management

The application generates invitation recommendations using information such as:

* Previous invitations
* Attendance history
* Survey completion
* Expected attendance
* Invitation frequency
* Participant priority
* Game interest
* Scheduling availability

Invitation records track invited participants, invitation dates, attendance, and additional guests.

This provides a repeatable, data-driven process for managing invitations while balancing participation across recurring events.

## Meal Recommendations

The system also assists with meal planning by combining participant preferences, historical meal usage, and configurable weighting factors.

Historical usage affects recommendation weights so that meal selection can account for both attendee preferences and meal rotation.

## Django Application

The Django application provides administrative interfaces for:

* Participant management
* Survey request tracking
* Invitation management
* Event planning
* Event scheduling
* Participant profiles
* Game analytics
* Meal statistics
* Availability reporting

The application uses unmanaged Django models that map to the PostgreSQL database populated by the ETL pipeline.

## Dynamic Reporting

Reports are dynamically generated from relational data and survey metadata.

Examples include:

* Participant survey responses
* Availability summaries
* Event-planning reports
* Invitation call lists
* Meal statistics
* Game participation reports

Using survey metadata allows the reporting system to adapt to changes in survey questions without requiring separate hardcoded reporting logic for every question.

## Engineering Concepts

This project demonstrates experience with:

* ETL and data pipelines
* Relational database normalization
* Incremental data synchronization
* PostgreSQL
* Django
* Dynamic reporting
* Scheduling algorithms
* Rule-based recommendations
* Workflow automation
* Metadata-driven application design

## Project Status

**Completed**

This was one of my earlier large-scale software engineering projects. It combines data engineering, database design, backend development, reporting, scheduling, and web development into an integrated system.

If redesigning portions of the application today, I would further separate application responsibilities through service and repository layers, move additional presentation logic into Django templates, and centralize reusable frontend assets. The project nevertheless demonstrates the design and implementation of an end-to-end system for transforming survey data into operational event-planning workflows.
