# room_booking_backend

## Installation

### 1. With pipenv
- run below command to install all dependencies with pipenv
```
pipenv install
```

### 2. Without pipenv
- run below command to install all dependencies with only pip
```
pip install -r requirements.txt
```

## update dependencies for requirement.txt
### 1. With pipenv
```
pipenv lock -r > requirements.txt
```
### 2. Without pipenv
```
pip freeze > requirements.txt
```