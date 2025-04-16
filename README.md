# City Skylines

## Description
Introducing City Skylines, a cutting-edge smart city application designed to revolutionize urban planning and management. Our data-driven platform empowers city planners, and analysts to make more accurate and insightful decisions, ensuring sustainable and efficient resource allocation across various urban systems.  City Skylines addresses the challenges of fragmented data sources, time-consuming manual entry, and outdated information by seamlessly integrating diverse datasets into a unified, user-friendly interface.

## Team Members
- Tanmay Demble
- Ganesh Danke
- Simone Kaplunov
- Maya Karintholil

## Technology Stack
- Docker
- MySQL
- Streamlit
- Flask

## Prerequisites
- Docker and Docker Compose installed
- Git (for cloning the repository)

## Getting Started

### Clone the Repository
```bash
git clone [repository-url]
cd [repository-directory]
```

### Environment Setup
1. Create a `.env` file in the root directory with the following content:
```
# Database Configuration
DB_USER=root
DB_PASSWORD=<your_db_password>
DB_NAME=CityPlanner
DB_HOST=db
DB_PORT=3306
```

### Starting the Application
To start all services:
```bash
docker compose -f docker-compose-testing.yaml up
```

This command:
- Builds all necessary Docker images
- Creates and starts containers 
- Executes SQL initialization scripts
- Sets up the network between services

### Accessing the Application
- Main application: [http://localhost:8501]

## Project Demo
[Watch our project demo video](https://drive.google.com/file/d/1BBnLa91mkvAvl9vLtZ3rM94U7DNcAVot/view?usp=sharing)
