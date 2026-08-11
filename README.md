# 🐳 Docker Compose Three-Tier Web Application

A three-tier web application orchestrated with Docker Compose, consisting of an Nginx reverse proxy, a Python Flask application, and a MySQL database.

This project was built as part of my DevOps learning journey to understand multi-container applications, Docker Compose, service-to-service networking, reverse proxies, environment variables, persistent storage, container lifecycle, and the separation between publicly exposed and internal services.

---

## 📌 Project Overview

This project extends the concepts learned from a single-container Docker application into a multi-container architecture.

Instead of running the entire application in one container, the application is separated into three services:

```text
                    Browser
                       │
                       │ localhost:8080
                       ▼
                ┌─────────────┐
                │    Nginx    │
                │ Presentation │
                └──────┬──────┘
                       │
                       │ app:5000
                       ▼
                ┌─────────────┐
                │   Flask     │
                │ Application │
                └──────┬──────┘
                       │
                       │ database:3306
                       ▼
                ┌─────────────┐
                │    MySQL    │
                │    Data     │
                └──────┬──────┘
                       │
                       ▼
                 mysql_data
                 Named Volume

The three services communicate over a private Docker Compose network.

Only Nginx is exposed to the host machine.

🏗️ Architecture

The application follows a three-tier architecture.

1. Presentation Layer — Nginx

Nginx receives requests from the browser through port 8080 on the host machine.

Host:8080 → Nginx:80

Nginx acts as a reverse proxy and forwards application requests to the Flask service.

2. Application Layer — Python Flask

The Flask application contains the application logic and communicates with the MySQL database.

The Flask service listens internally on port 5000.

It is not exposed directly to the host machine.

3. Data Layer — MySQL

MySQL stores the application data, including the page visit counter.

MySQL listens internally on port 3306.

Port 3306 is intentionally not published to the host, keeping the database inaccessible directly from the host browser.

🛠️ Technologies Used
Python
Flask
MySQL 8.4
Nginx 1.29.1
Docker
Docker Compose
Linux / WSL
Git & GitHub
📂 Project Structure
docker-compose-app/
├── app/
│   ├── Dockerfile
│   └── app.py
├── nginx/
│   └── default.conf
├── images/
│   ├── appfoldercreated.png
│   ├── catapp.py1.png
│   ├── catapp.py2.png
│   ├── curl-database.png
│   ├── curl-localhost.png
│   ├── default.conf-image.png
│   ├── directory-setup.png
│   ├── dockerbuild-app.png
│   ├── dockercompose-downandup.png
│   ├── dockercompose-execweb.png
│   ├── dockercompose-psandvolumels.png
│   ├── dockercompose-upandps.png
│   ├── dockercompose-version.png
│   ├── dockercompose-volumermandls.png
│   ├── dockercomposeappandps.png
│   ├── dockerfile.png
│   ├── dockernetwork-inspect1.png
│   ├── dockernetwork-inspect2.png
│   ├── dockernetwork-list.png
│   ├── failedlocalhost3306-attempt.png
│   ├── localhost8080success.png
│   ├── mounts.png
│   ├── perssistence-volume.png
│   ├── sudocomposepsfinal.png
│   └── webpagesuccess.png
├── .env.example
├── .gitignore
├── compose.yaml
└── README.md
1. Project Setup

The project was created inside my DevOps projects directory.

A dedicated directory was created for the Docker Compose application:

mkdir docker-compose-app
cd docker-compose-app

The initial project directory was empty before the application components were created.

2. Creating the Flask Application

The application layer was implemented using Python and Flask.

The Flask application keeps track of the number of times the webpage has been visited.

The application uses environment variables to obtain database configuration rather than hard-coding credentials.

This allows configuration to be separated from application code.

The application connects to MySQL using the Docker Compose service name:

database

rather than using localhost.

This is because containers communicate with one another through the Docker Compose network.

3. Creating the Python Dockerfile

A Dockerfile was created for the Flask application.

The Dockerfile defines the environment required to run the Python application and installs its dependencies.

The application was then built into a Docker image.

4. Configuring Nginx

Nginx was used as the presentation layer and reverse proxy.

A custom Nginx configuration was created to forward incoming requests to the Flask application.

The important concept here is that the browser does not need to communicate directly with Flask.

Instead:

Browser
   ↓
Nginx
   ↓
Flask

This allows Nginx to act as the public-facing entry point for the application.

5. Creating the Docker Compose Configuration

Docker Compose was used to define and manage the three services.

The final compose.yaml contains:

services:
  web:
    image: nginx:1.29.1
    ports:
      - "8080:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro

  app:
    build: ./app
    environment:
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}

  database:
    image: mysql:8.4
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:

The Compose file defines the complete application stack and allows all three services to be managed together.

6. Environment Variables and Configuration

Database credentials are stored in a .env file rather than directly inside compose.yaml.

Example:

MYSQL_DATABASE=your_database_name
MYSQL_USER=your_database_user
MYSQL_PASSWORD=your_database_password
MYSQL_ROOT_PASSWORD=your_root_password

The .env file is excluded from version control using .gitignore.

A .env.example file is included in the repository to show the required configuration variables without exposing real credentials.

This provides a safer configuration pattern:

.env
   ↓
Actual local credentials
   ↓
Excluded from Git

.env.example
   ↓
Configuration template
   ↓
Safe to publish
7. Docker Compose Services

The project contains three services:

sudo docker compose config --services

The services are:

app
database
web

Docker Compose creates and manages the containers associated with these services.

The application stack can be started with:

sudo docker compose up -d

The -d option runs the containers in detached mode, allowing the terminal to remain available.

The running services can be inspected using:

sudo docker compose ps

8. Docker Compose Networking

Docker Compose automatically creates a private network for the application.

The services can communicate with one another using their Compose service names.

For example:

app → database:3306

The Flask application does not need to know the IP address of the MySQL container.

Docker's internal DNS resolves:

database

to the appropriate MySQL container.

The Docker network can be inspected using:

sudo docker network ls

The network configuration can also be inspected with:

sudo docker network inspect docker-compose-app_default

9. Public Ports vs Internal Ports

One of the key concepts demonstrated by this project is the difference between a container port and a published host port.

Nginx is configured with:

ports:
  - "8080:80"

This means:

Host port 8080
      ↓
Container port 80

Therefore, the application can be accessed from the host using:

http://localhost:8080

However, the Flask application only shows:

5000/tcp

and MySQL shows:

3306/tcp

Neither port is published to the host.

This means they are available to other containers on the Compose network but are not directly exposed to the host.

For example, attempting to access MySQL through the host's localhost:3306 does not work.

This demonstrates the difference between:

Publicly exposed service
        ↓
localhost:8080
        ↓
Nginx

and:

Internal service
        ↓
database:3306
        ↓
MySQL
10. Testing Container-to-Container Communication

The Flask application communicates with MySQL using the Compose service name.

The Docker network allows containers to locate one another without exposing every service to the host.

The network can also be tested from inside the containers.

This helped demonstrate that an internal Docker network is different from a host-published port.

11. Nginx Reverse Proxy

The browser communicates with Nginx rather than directly with Flask.

The request flow is:

Browser
   ↓
localhost:8080
   ↓
Nginx:80
   ↓
app:5000
   ↓
Flask
   ↓
database:3306
   ↓
MySQL

This means Nginx is the only public-facing component of the application.

The successful application response can be tested with:

curl http://localhost:8080

12. Persistent Storage with Docker Volumes

The MySQL data directory is mounted to a named Docker volume:

volumes:
  - mysql_data:/var/lib/mysql

The named volume allows database data to survive container recreation.

The volume can be inspected using:

sudo docker volume ls

The volume configuration was also inspected to understand where Docker stores the persistent data.

13. Testing Data Persistence

One of the most important experiments in this project was testing what happens to database data when the containers are removed.

The application stack was stopped and removed using:

sudo docker compose down

The named volume remained because docker compose down does not remove named volumes by default.

The stack was then recreated:

sudo docker compose up -d

The application was accessed again after the containers were recreated.

The page visit counter continued using the existing database data rather than starting from scratch.

This demonstrated the difference between:

Container lifecycle

and:

Persistent application data

The containers can be destroyed and recreated while the named volume preserves the database state.

14. Final Application Test

The complete three-tier application was tested through the Nginx entry point:

curl http://localhost:8080

The response confirmed that the request successfully passed through the application stack.

The application was also verified through the browser.

🧠 What I Learned

Through this project, I learned:

How Docker Compose manages multiple containers as a single application.
How to define services using compose.yaml.
How containers communicate through a Compose network.
How Docker's internal DNS resolves service names.
Why containers can communicate using service names instead of IP addresses.
The difference between container ports and published host ports.
Why MySQL does not need to expose port 3306 to the host.
How Nginx can act as a reverse proxy.
How a three-tier architecture can be represented using containers.
How to build a custom Python application image.
How to use environment variables for application configuration.
Why secrets should not be hard-coded into source code.
How .env and .env.example serve different purposes.
How .gitignore prevents sensitive configuration from being committed.
How named Docker volumes provide persistent storage.
The difference between anonymous and named volumes.
How docker compose up creates and starts services.
How docker compose down removes containers and networks.
How Docker Compose preserves named volumes unless explicitly removed.
How to inspect Docker networks, volumes, containers, and logs.
How to test connectivity between containers.
How to troubleshoot a multi-container application.
🚀 Key Docker Compose Workflow

The workflow demonstrated in this project is:

Create Application
        ↓
Create Dockerfiles
        ↓
Configure Nginx
        ↓
Create compose.yaml
        ↓
Define Services
        ↓
Configure Environment Variables
        ↓
Create Docker Network
        ↓
Build Images
        ↓
Create Containers
        ↓
Nginx → Flask → MySQL
        ↓
Persist Data with Named Volume
        ↓
Test Application
        ↓
Recreate Containers
        ↓
Verify Persistent Data
🔍 Useful Commands
Start the application
sudo docker compose up -d
Build and start
sudo docker compose up -d --build
View running services
sudo docker compose ps
View all containers
sudo docker compose ps -a
View logs
sudo docker compose logs
View logs for a specific service
sudo docker compose logs app
Stop and remove the application
sudo docker compose down
View Compose projects
sudo docker compose ls
View Docker networks
sudo docker network ls
View Docker volumes
sudo docker volume ls
Validate the Compose configuration
sudo docker compose config
👩🏽‍💻 Author

Benita Adakeja

Computer Science Student | DevOps & Cloud Enthusiast

GitHub: https://github.com/benitaadakeja
