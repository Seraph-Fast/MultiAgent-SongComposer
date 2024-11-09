# MultiAgent Composer

MultiAgent Composer is a Python-based AI application that generates original poetry by orchestrating conversations between multiple AI agents, each contributing uniquely to the final composition. The project simulates collaborative creativity by leveraging sequential communication between specialized agents:

- **Data Assistant**: Provides a poem in the style of a specified poet, serving as the stylistic foundation.
- **Assistant Original Poem**: Writes an original poem in its own unique style, introducing fresh creative elements.
- **Composer Agent**: Synthesizes elements from both poems to produce a new composition that emulates the specified poet's style.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage Guide](#usage-guide)
  - [Interacting with the Agents](#interacting-with-the-agents)
  - [Viewing Logs](#viewing-logs)
- [Sequence Diagram](#sequence-diagram)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Multi-Agent Collaboration**: Simulates interaction between AI agents to create poetry.
- **Customizable Poet Styles**: Users can specify any poet's style for the composition.
- **Dockerized Deployment**: Easy setup and scalability with Docker and Docker Compose.
- **Database Integration**: Logs conversations and generated poems in PostgreSQL for persistence.

---

## Architecture

The application consists of the following components:

- **Agents Module (`agents.py`)**: Defines and initializes the AI agents and manages their interactions.
- **Response Extraction**: Processes agent responses to extract poems using standardized tags.
- **Database (`PostgreSQL`)**: Stores logs of conversations and generated content.
- **API Server (`FastAPI`)**: Provides endpoints for interacting with the agents and retrieving data.

---

## Setup Instructions

### Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- **Git** installed for cloning the repository.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/multiagent-composer.git
   cd multiagent-composer
   ```
   
2. **Create app/.env(for ollama api) and app/db.env(for database connection)**
   
  examples:
  
   app/db.env:
   
   ```makefile
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=1234
    POSTGRES_DB=db
    POSTGRES_HOST=database
    POSTGRES_PORT=5432
   ```
   app/.env:

   ```makefile
    MODEL_NAME="{model available}"
    BASE_URL="http://{api_base}:{port}/v1"
   ```
3. **Build and Run the Application**

    ```bash
    docker-compose up --build
    ```
