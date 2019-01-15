[![Python 3.7.2](https://img.shields.io/badge/python-3.7.2-blue.svg)](https://www.python.org/downloads/release/python-372/) [![Twisted](https://img.shields.io/badge/twisted-18.9.0-blue.svg)]() [![MS](https://img.shields.io/badge/Marko-%C5%A0tumberger-green.svg)](https://github.com/mstumberger)

# Instructions #
The main purpose of the application is to offer contacts autocompletion, as available e.g. in a phone.
The application does not need to persist the contacts, its main purpose is to serve as an in-memory cache
for its clients. You can assume that a separate application will fill "Pozabljivi imenik"’s cache soon 
after startup of "Pozabljivi imenik" (using the "PUT" command, as described below).

 

0. About

    The application should listen on TCP port 4242 for commands.
    The application needs to be able to serve multiple clients simultaneously.
    The clients can send multiple commands over an established TCP connection,
    the time period between subsequent commands is not limited.
    Commands and responses on a single connection cannot interleave
    (i.e., the commands received over an individual connection should be served in FIFO order).

    The commands are sent to the application using the following custom protocol:

    1. Each command is sent as a "message", whose first four bytes (octets), let’s call them "length",
        specify the length, in bytes, of the remainder of that "message" (let’s call that remainder "payload").
    
    2.  "length" is encoded as a zero padded hexadecimal ASCII [0-9a-f].
        Uppercase ASCII letters are not allowed.
        E.g., for a payload of length 42 bytes, the "length" part of the "message" should be "002a",
        while for a payload of length 4242 bytes, it should be "1092".
    
    3.  "payload" contains an utf-8 encoded JSON Object,
        containing at a minimum a key named "command",
        whose value specifies which command "Pozabljivi imenik" should perform,
        as well as all parameters required by that specific command.

    The application should respond to commands with its own "message",
    comprised of "length" and "payload" encoded as described above.
    Its "payload" must contain the following two keys:

    * "success", whose value is Boolean and must be true if command succeeded without errors and false otherwise,
    
    * "result", whose value type is command dependent in case of success and a String describing the error
      in case of errors (when "success" is false).

    The application should support the following commands (the value of "command" key in "payload" Object is specified 
    in quotes, parameter names and their types are specified in parentheses, "result" type is specified after ->):


1. "PUT" (phone=String, name=String, surname=String) -> null

    The application should create or update the association between value of "phone" and the combination
    of "name" and "surname" values. "phone" value is a String, since it can contain non-numerical characters("+" and similar).
    Upon success, the application should return null as a "result".
    
    ```python
    example = {
        "command": "PUT",
        "phone": "112",
        "name": "klic",
        "surname": "v sili",
    }

    response = {
        "success": True,
        "result": None,
    }
    ```


2. "GET" (phone=String) -> Object(name=String, surname=String)

    The application should return an Object containing the "name" and "surname" values associated with phone number "phone".
    If it doesn’t have an association for phone number "phone", it should return an error.
    
    ```python
    example = {
        "command": "GET",
        "phone": "112"
    }
    
    response = {
        "success": True,
        "result": {
            "name": "klic",
            "surname": "v sili"
        }
    }
    ```

 
3. "DELETE" (phone=String) -> null

    The application should delete the association for phone number "phone".
    If it doesn’t have an association for phone number "phone", it should return an error.
    
    ```python
    example = {
        "command": "DELETE",
        "phone": "112"
    }
    
    response = {
        "success": True,
        "result": None,
    }
    ```


4. "FIND" (prefix=String) -> Array(Object(phone=String, name=String, surname=String), …)

    The application should return an array of "contacts"
    (Objects containing "phone", "name" and "surname" keys, as given in the "PUT" command),
    where the value of "name" or "surname" keys starts with the value specified in "prefix".
    The search should be case insensitive (e.g., when searching for prefix "kl",
    contacts with name "Klemen" and "klic" should be returned). 
    
    If the application has no associations whose "name" or "surname" values start with "prefix",
    it should return an empty array. If "prefix" is an empty string,
    the application should return all of its contacts.
    
   ```python
   example = {
        "command": "FIND",
        "prefix": "kl" 
   }
    
   response = {
        "success": True,
        "result": [
            {"phone": "112", "name": "klic", "surname": "v sili"}, 
            {"phone": "424242", "name": "Klemen", "surname": "Klemen"}
        ]
   }
   ```


5. RUN

    virtualenv is a tool to create isolated Python environments.
    
    1. Install virtualenv via pip:
    
        ``` $ pip install virtualenv ```

    2. Test your installation:

        ``` $ virtualenv --version ```

    3. To begin using the virtual environment, it needs to be activated:

        ``` $ source venv/bin/activate ```

        or
        
        ``` PS  \venv\Scripts\activate ```
