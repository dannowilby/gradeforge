
# GradeForge

GradeForge converts student data into personalized report cards automatically.

- Generates report cards with your choice of LLM<sup>1</sup>
- Provides a dashboard of previously made reports
- Updates you through text when generation has completed
- Can be managed with a single command

This is a reimplementation of the first report card generator I made in late 2023 for my work at the time. The extension contains code used to scrape the company's admin pages, and I have made that code private due to the potential risk of exposing sensitive details inadvertently.

<sup>1 - It comes packaged with the choice of Anthropic Claude's API or an Ollama model, but the [`TextGen`](../server/src/text_gen.py) interface can easily be extended to add more.</sup>

## Usage
After completing [setup](setup.md) and starting the application by running `./gradeforge [ollama|claude]`, send a post request to the backend's `/generate` endpoint with the student's data (as a binary string encoded using the protobuf schema). Typically, you would use the extension to automatically scrape the details and form the body for the endpoint, but this can also be emulated using cURL.

This will kick off the generation, store it in the database, and finally send you a text confirming it has completed. You can then use the dashboard to see all the reports you've generated.

![screenshot of an example student's report cards](ui-screenshot.png)

## How it works
GradeForge coordinates a number of different services to achieve its goal.

### Architecture

The backend is a pair of Python processes and a PostgreSQL instance. The processes are split so that one process can handle incoming generation and data requests, and then pass the generation requests off to the second to actually carry out the generation itself. The result is stored in the database, which can be written to and read from on both processes.

Report card generation can take an indeterminate amount of time, so handling requests this way allows proper utilization of resources.

### Generation request processing

The generation process starts by using an LLM to generate the text content of the report card. Depending on the options that the application was run with, the process will either query an Ollama model or Anthropic's Claude, storing it in the database after completion. The process then uses Boto3 to send an SMS to notify of the completed generation.

### Orchastrating

The bash script is included to allow an easy way for less technical users to navigate its options. The script also manages a checksum of your environment variables to verify if the containers should be built again, as Docker Compose won't rebuild containers if build-time environment variables change.


![architecture diagram](architecture-diagram.png)


## Setup
Setup typically only requires making sure you have Docker Compose installed and that the appropriate environment variables are set. For a detailed explanation of these steps, check out [this guide](setup.md).

## Example
After setting up the project, running the `gradeforge` bash script is all you need to do to start up the application. For a more detailed usage guide, plus an example usage, look [here](usage.md).

## Limitations

As previously mentioned, the extension code has not been included as it contains specific, closed source implementation details for the propriatery software used at my previous work.

The setup has been purposefully made to be as easy as possible. That said, there is no automatic provision of AWS SNS as the initial creation of the service requires your organization to be authorized (depending on your local regulations).