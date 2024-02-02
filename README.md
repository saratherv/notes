# Notes Backend Flask APP
- This serves as backend to Notes APP, built using flask and also stores changelog of notes.


### Built With
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [SqlAlchemy](https://www.sqlalchemy.org/)
* [Docker](https://www.docker.com/)


## Getting Started

This project build with dockers and can be installed using minmal commands.

### Prerequisites
* [docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/saratherv/notes.git
   ```
2. Change directory
    ```sh
    cd notes
    ```
3. Run Script (This will build container and open the shell)
   ```sh
   ./local_run.sh --clean
   ```
4. Run Command in shell
   ```sh
   flask db upgrade
   ```
4. Start Server
   ```sh
   python3 app.py
   ```
   
## Usage

- Visit http://localhost:9000/api/v1/ui to see swagger of APIs.
- Visit http://localhost:9000/core/authentication/ui to see swagger of Core Endpoints.

### Assumptions and Considerations
- Haven't added volumes, so data is not persistent yet.

