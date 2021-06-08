# A sample TODO application

## Requirements

Python > 3.5

## Setup

```sh
pip install -r requriements.txt

python data_definition.py # This creates the db with required tables

python create_admin.py "username" "password" # This step creates an initial Admin user
```

## Running the application

```sh
python main.py
```

This runs the application in http://127.0.0.1:5000.

Only an admin user can create or list users.
