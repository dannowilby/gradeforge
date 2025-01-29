
# GradeForge

GradeForge converts student data into personalized report cards automatically.

- Generates report cards with your choice of LLM*
- Provides a dashboard of previously made reports
- Updates you through text when generation has completed
- Can be managed with a single command

This is a reimplementation of the first report card generator I made in late 2023 for my work at the time. The extension contains code used to scrape the company's admin pages, and I have made that code private due to the potential risk of exposing sensitive details inadvertently.

## How it works
GradeForge coordinates a number of different services to achieve its goal.

### Coordinating the services
uses Docker Compose to manage the different services needed to generate and serve the report cards. The bash script provided will switch between the different Docker Compose build files.

### The backend

(Add miro architecure diagram here)

## Setup
Setup typically only requires making sure you have Docker Compose installed and that the appropriate environment variables are set. For a detailed explanation of these steps, check out [this guide](setup.md).

## Usage + Example
After setting up the project, running the `gradeforge` bash script is all you need to do to start up the application. For a more detailed usage guide, plus an example usage, look [here](usage.md).

## Limitations
