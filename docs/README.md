
# GradeForge

GradeForge converts student data into personalized report cards automatically.

- Generates report cards with your choice of LLM<sup>1</sup>
- Provides a dashboard of previously made reports
- Updates you through text when generation has completed
- Can be managed with a single command

This is a reimplementation of the first report card generator I made in late 2023 for my work at the time. The extension contains code used to scrape the company's admin pages, and I have made that code private due to the potential risk of exposing sensitive details inadvertently.

<sup>1 - It comes packaged with the choice of Anthropic Claude's API or an Ollama model, but the [`TextGen`](../server/src/text_gen.py) interface can easily be extended to add more.</sup>

## Usage
After starting the application by running `./gradeforge [ollama|claude]`, send a post request to `/generate` with the student's data (as a binary string encoded using the protobuf schema). Typically, you would use the extension to automatically scrape the details and form the body for the endpoint, but this can also be emulated using cURL.

This will kick off the generation, then store it in the database, and finally send you a text confirming it has completed.

(screenshot of generated report cards)

## How it works
GradeForge coordinates a number of different services to achieve its goal.

### The backend
As the report generation process itself can take a fair amount of time (especially if using Ollama), this is offloaded to a separate process than the server. This allows the blocking generation process to not hold up the actual server. The server sends 

Communication between the two occurs through a PostgreSQL instance and ensures that users won't have to wait for individual report cards to finish processing before requesting another one.

### The extension

### The ui

### Coordinating the services
uses Docker Compose to manage the different services needed to generate and serve the report cards. The bash script provided will switch between the different Docker Compose build files.



(Add miro architecure diagram here)

### Putting it all together

The bash script allows less technical users easily restart the application in case of errors or malfunction.

## Setup
Setup typically only requires making sure you have Docker Compose installed and that the appropriate environment variables are set. For a detailed explanation of these steps, check out [this guide](setup.md).

## Example
After setting up the project, running the `gradeforge` bash script is all you need to do to start up the application. For a more detailed usage guide, plus an example usage, look [here](usage.md).

## Limitations

As previously mentioned, the extension code has not been included as it contains specific, closed source implementation details for the propriatery software used at my previous work.

The setup has been purposefully made to be as easy as possible. That said, there is no automatic provision of AWS SNS as the initial creation of the service requires your organization to be authorized (at least according to US regulations).