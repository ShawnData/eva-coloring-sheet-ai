# Eva's Coloring Sheet AI

## Project Goals
- Create an interactive AI to generate coloring sheets for my daugther, Eva.
- Learn more about agentic frameworks
- Learn effective use of Cursor IDE

## Description

## Project Structure

## Features

## Technical Stacks

## Agent Workflow Outline

```mermaid
graph TD
  A[🗣️ Voice Agent<br>“What do you want to draw?”] --> B[📝 Summarizer Agent<br>Requirements Builder]
  B --> C[🎨 Designer Agent<br>Image Generator]
  C --> D[🗣️ Voice Agent<br>“Do you like this?”]
  D --> E[🛠️ Editor Agent<br>Image Updater]
  E -->|Feedback loop| D
```


## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/eva_coloring_sheet_agent/config/agents.yaml` to define your agents
- Modify `src/eva_coloring_sheet_agent/config/tasks.yaml` to define your tasks
- Modify `src/eva_coloring_sheet_agent/crew.py` to add your own logic, tools and specific args
- Modify `src/eva_coloring_sheet_agent/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the eva-coloring-sheet-agent Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The eva-coloring-sheet-agent Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the EvaColoringSheetAgent Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

