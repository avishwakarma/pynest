# pynest

A Python framework for buuilding RESTful APIs. Inspired by NestJS, it provides a modular architecture with decorators for defining modules, controllers, and services. It usages FastAPI under the hood for handling HTTP requests and responses.

## Features

- Modular architecture
- Decorators for defining modules, controllers, and services
- Dependency injection

## Installation

Make sure you have `Python 3.8` or higher installed

To check your Python version, run:

```bash
python --version
```

### Setup virtual environment

```bash
python -m venv venv
source venv/bin/activate
# On Windows use 'venv\Scripts\activate'
```

### Install pynest

```bash
pip install pynest
```

## Usage

```python
# app/app_service.py
from pynest import injectable

@injectable()
class AppService:
  def greet(self):
    return {"message": "Hello, World!"}

# app/app_controller.py
from pynest import controller, get

@controller('/api')
class AppController:
  def __init__(self, app: AppService):
    self.app = app

  @get('/hello')
  def hello(self):
    return self.app.greet()

# app/app_module.py
from pynest import module

@module(
  controllers=[AppController],
  providers=[AppService]
)
class AppModule:
  pass

# main.py
from pynest import bootstrap
from app.app_module import AppModule

app = bootstrap(AppModule, {
  "name": "MyApp",
  "version": "1.0.0",
  "description": "A simple API using pynest",
  "docs_url": "/docs",
})

```

## Running the Application

Run the application using Uvicorn:

```bash
uvicorn main:app --reload
# assiming your main file is named main.py
# and it is placed in the root directory of your project
```

# Contribution

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## Local Development Setup

### Clone the repository:

```bash
git clone https://github.com/avishwakarma/pynest.git
cd pynest
```

### Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
# On Windows use 'venv\Scripts\activate'
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
uvicorn example.main:app --reload
```

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details

# Issues

If you find any issues or have feature requests, please open an issue on the [GitHub repository](https://github.com/avishwakarma/pynest/issues).

# Acknowledgements

This project is inspired by NestJS and aims to bring similar modularity and structure to Python web applications. Thanks to the FastAPI team for their excellent framework that powers this project.

# Contact

For any questions or feedback, feel free to reach out via the [GitHub repository](https://github.com/avishwakarma/pynest).
