import json
import logging
import os
import time
from abc import ABC, abstractmethod

import psycopg

from app.settings import Settings

FILE_PATH = "app/db/sequences.json"
SEND_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


class DBStrategy(ABC):
    @abstractmethod
    def read_sequences(self):
        pass

    @abstractmethod
    def write_sequences(self, sequences):
        pass


class PostgresStrategy(DBStrategy):
    def __init__(self):
        self.host = Settings.DB_HOST
        self.port = Settings.DB_PORT
        self.user = Settings.DB_USER
        self.password = Settings.DB_PASSWORD
        self.db_name = Settings.DB_NAME
        self._prep_db()

    def read_sequences(self):
        read_statement = "select dna from sequences"
        sequences = {"sequences": []}
        with psycopg.connect(
            (
                f"host={self.host} port={self.port} "
                f"dbname={self.db_name} user={self.user} "
                f"password={self.password}"
            ),
            autocommit=True,
        ) as conn:
            rows = conn.execute(read_statement).fetchall()

            for row in rows:
                sequences["sequences"].append(row[0])

        return sequences

    def write_sequences(self, sequences):
        text_data = json.dumps(sequences)
        write_statement = f"INSERT INTO sequences (dna) VALUES ('{text_data}')"

        self._execute_db_statement(write_statement)

    def _prep_db(self):
        create_table_statement = """
            drop table if exists sequences;
            create table sequences(
                id serial primary key,
                dna jsonb not null
            )
        """

        self._execute_db_statement(create_table_statement)

    def _execute_db_statement(self, statement):
        """
        Execute a database statement with retry logic.

        This method attempts to execute a given SQL statement on a PostgreSQL
        database. It includes retry logic to handle transient errors that may
        occur during the execution. The method will retry the execution up to
        a maximum number of retries defined by MAX_RETRIES. If the statement
        cannot be executed successfully after the maximum number of retries,
        a Exception is raised.

        Args:
            statement (str): The SQL statement to be executed.

        Raises:
            Exception: If the statement cannot be executed after
            the maximum number of retries.

        Logs:
            Logs an error message if an error occurs during the execution of
            the statement.
            Logs an info message indicating the retry delay before each retry
            attempt.
            Logs an error message if the statement fails to execute after the
            maximum number of retries.
        """
        retries = 0
        while retries < MAX_RETRIES:
            try:
                with psycopg.connect(
                    (
                        f"host={self.host} port={self.port} "
                        f"dbname={self.db_name} user={self.user} "
                        f"password={self.password}"
                    ),
                    autocommit=True,
                ) as conn:
                    conn.execute(statement)
                return
            except psycopg.Error as e:
                retries += 1
                logging.error(f"Error executing database statement: {e}")
                logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
        else:
            logging.error(
                (
                    f"host={self.host} port={self.port} "
                    f"dbname={self.db_name} user={self.user} "
                    f"password={self.password}"
                )
            )
            logging.error(
                (
                    "Failed to execute database statement after multiple "
                    "retries. Please check the database connection and "
                    "configuration."
                )
            )
            raise Exception("Failed to execute database statement")


class JSONStrategy(DBStrategy):
    def read_sequences(self):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as file:
                return json.load(file)
        else:
            os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

        return {"sequences": []}

    def write_sequences(self, sequences):
        data = self.read_sequences()
        data["sequences"] += [sequences]
        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)


class DBGateway:
    def __init__(self):
        if Settings.DB_SOURCE == "postgres":
            self.strategy = PostgresStrategy()
        elif Settings.DB_SOURCE == "json":
            self.strategy = JSONStrategy()
        else:
            raise Exception(
                f"Invalid DB source: {Settings.DB_SOURCE}. "
                "Please set the DB_SOURCE environment variable to 'postgres' "
                "or 'json'."
            )

    def read_sequences(self):
        return self.strategy.read_sequences()

    def write_sequences(self, sequences):
        return self.strategy.write_sequences(sequences)
