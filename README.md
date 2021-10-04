# Bedrock Server Backup

#### 1. Description
​		**Linux Minecraft Bedrock Server** (Local/Docker) **backup** *every 5 minutes, every day, every month*

#### 2. Key Feature
- Provides logging, configuration management for running Python projects on the server
- Automaticly saving backups
- RESTful APIs provide an interface to project information

- Periodically execute the module, executing /Core/main.py on a regular basis based on the start and end time
- Message notification module, send email or cooperate with Mirai framework to send QQ messages
- Server API
- Program information and system status can be queried through the built-in API
- Customizable simple API
- Custom web templates

#### 3. Basic Modules

- Archive
  - archive - Archive base type information class
  - handler - Encapsulates the file manipulation API
  - lock - Lock the corresponding backup
  - manager - File List Management
- Core
  - core - Entry to program execution
- Config
  - config.ini - Fill in the basic configuration information
  - settings - Read and initialize data in config.ini
- Logger
  - logger - Outputs log messages to the console, log file, and Server module
- Scheduler
  - scheduler - Scheduled execution of the /Core/main.py module. Once opened and set in config.ini, the /Core/main.py module is scheduled to be executed
- Server
  - handler - Contains the main HTTP request handling and API
  - server - Used to configure and start the server thread
- Static
- Web page view log
- RESTful APIs provide an interface to project information

#### 4. Operation Environment

- [Python 3](https://www.python.org/)

#### 5. Installation Tutorial

1. ```shell
   git clone https://github.com/louisyoungx/bedrock-server-backup.git
   ```

2. ```sh
   cd bedrock-server-backup
   ```

1. ```shell
   python3 runserver.py
   ```

#### 6. Usage

1. Edit the configuration items in /Config/config.ini file according to the comment requirements

   ```ini
   [Archive]
   # insert Docker or Local
   MODE = "Docker"
   # Docker container id
   DOCKER_ID = "c2684040eb11"
   # the absolute /worlds path in your linux or docker container
   ArchiveFilePath = "/worlds"
   # your minecraft archive file name
   ArchiveFileName = "louis-world"
   ```

   

2. Make sure you are in /bedrock-server-backup and enter

   ```sh
   python3 runserver.py
   ```

#### 7. TODO

- Web API Docs ( *It's now available, You can preview it at  /Server/postman_api.json* )

- Web UI 
- Command Line

#### 8. Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request
