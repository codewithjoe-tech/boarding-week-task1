


# Django Docker Compose Project

This repository contains a Django project configured to run with Docker and Docker Compose for easy local development and testing.

---

## 📑 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Stopping the Project](#stopping-the-project)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## ✅ Prerequisites

Ensure the following tools are installed on your system:

- **Docker** (v20.10 or later)
- **Docker Compose** (v1.29 or later)

### Install Docker

- **Windows/Mac:** Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop).
- **Linux:**

```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
````

### Install Docker Compose (Linux)

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
-o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

* **Verify installations:**

```bash
docker --version
docker-compose --version
```

---

## 🚀 Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Start the Application

```bash
docker-compose up --build
```

This command will:

* Build the Docker images.
* Start all the services (Django, database, etc.).
* Automatically apply migrations and start the server.

### 3. Access the Application

Once the services are up, open your browser and visit:

```
http://localhost:8000
```

---

## 🛑 Stopping the Project

To stop the application, press `Ctrl+C` in the terminal where it's running.

To stop and remove containers, networks, and volumes:

```bash
docker-compose down
```

---

## 🛠️ Troubleshooting

* **Port already in use:** Make sure port `8000` or others aren't already occupied.
* **Docker not running:** Ensure Docker is active (`docker info`).
* **Permission errors:** Try running with `sudo`, or add your user to the `docker` group:

```bash
sudo usermod -aG docker $USER
```

Then restart your terminal.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

```

Let me know if you'd like to include `.env` setup, custom database instructions, or initial migration/seed steps!
```
