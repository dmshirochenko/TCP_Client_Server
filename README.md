# TCP Client/Server Key-Value Store

## Overview
This project includes a TCP server and client that collaborate to create a basic key-value store with timestamp support. The server manages data storage and responds to client requests, while the client can both retrieve and store data.

## Server
### Features
- Connection Handling: Manages incoming TCP connections.
- Data Storage: Uses a global dictionary for timestamped key-value storage.
- PUT Command: Stores or updates data.
- GET Command: Retrieves data based on keys.
- Error Handling: Deals with invalid commands.
- Execution: Listens on 127.0.0.1 and port 8888.

### Usage
Run `server.py` to start the server.

## Client
### Features
- Connection Creation: Establishes a TCP connection to the server.
- GET Command: Sends get requests to retrieve data.
- PUT Command: Sends put requests to store or update data.
- Error Handling: Manages various errors including timeouts and socket errors.
- Response Parsing: Parses server responses.

### Usage
Utilize the `Client` class in `client.py` to interact with the server.

## Requirements
- Python 3.x
- `asyncio` library for the server
- `socket` library for the client

## Installation
1. Clone the repository.
2. Make sure the required libraries are installed.

## Running the Project
1. Start the server by running `server.py`.
2. Use the client in `client.py` to interact with the server.

## Contact
For inquiries or support, please contact [Your Name] at [Your Contact Information].

