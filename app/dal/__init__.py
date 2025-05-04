"""
The `dal` (Data Access Layer) directory is intended to separate data access concerns from business logic.

This layer provides a clean interface between the application's core logic and the database operations, but is limited to interacting through model interfaces.

- `/models`: Defines ORM models and handles direct interaction with the database.
- `/schemas`: Defines data validation and serialization logic for API input/output using Pydantic.
"""
