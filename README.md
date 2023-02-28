## Common troubles
- In case of error occurred while installing mysqlclient:
    ```bash
    sudo apt-get install python3.8-dev libmysqlclient-dev
    ```

- In case of error like this:
"OperationalError: (2002, "Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)")"
    ```bash
    [.env file]
    DB_HOST=localhost ---> DB_HOST=127.0.0.1
    ```