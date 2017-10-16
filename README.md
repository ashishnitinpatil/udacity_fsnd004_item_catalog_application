Project: Item Catalog Application (nd004)
=========================================
This is part of the project submission under the Full Stack Nano Degree program of Udacity, authored by Ashish Nitin Patil. Kindly respect the [Udacity Honor Code](https://udacity.zendesk.com/hc/en-us/articles/210667103-What-is-the-Udacity-Honor-Code-).


Requirements
------------
Python v3.x (tested with 3.6 only) is required  
- Setup a virtualenv
    ```bash
    virtualenv -p python3.6 .venv
    .venv/Scripts/activate.bat
    ```
- install requirements
    ```bash
    pip install -r requirements.txt
    ```

Project brief
-------------
- The application uses Google Login instead of implementing own authentication
- Once logged in, a user can perform CRUD operations on any of the catalog items
- Application provides a JSON API endpoint for the READ operations
- Site is read-only for anonymous / non-logged-in users

Usage
-----
- Activate virtualenv
    ```bash
    .venv\Scripts\activate.bat
    # For linux, execute ".venv/bin/activate" instead
    ```
- Set environment variables for flask
    ```bash
    # For linux, use export instead of set (& you may skip the quotes)
    set "PythonPath=%PythonPath%;E:\Study\Full_Stack_Nano_Degree\projects\4_item_catalog_application"
    set "FLASK_APP=E:\Study\Full_Stack_Nano_Degree\projects\4_item_catalog_application\server.py"
    set "FLASK_DEBUG=1"
    ```
- Initialize db
    ```bash
    flask shell
    ```
    ```python
    >>> from item_catalog_app.models import db
    >>> db.create_all()
    ```
- Secrets
    - Create your own secrets.json, refer to [sample_secrets.json](/sample_secrets.json) for example
    - Change the [CLIENT_ID](/item_catalog_app/settings.py#L26) setting with your own Google cient ID
- Run server
    ```bash
    flask run
    ```

Licensing
---------
Please refer to [LICENSE](/LICENSE)
