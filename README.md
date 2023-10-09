# WORKSHOP

## Prerequisites

- Make sure `python` is installed on your computer (version 3.9 or above) using the following command:
    ```bash 
    python -V
    ```
    If Python is not installed you can download python from here: https://www.python.org/downloads/.
- After installing and adding pythin to the PATH, launch the terminal and run:  
    ```bash 
    python -V
    ```
    Expected behavior:
    ```bash
    $ python -V
    Python 3.11.4
    ```
## Set up
### 1. Fork or clone this repository
**Windows:** 
You need to install git using the following link: https://git-scm.com/download/win

**Linux/Mac:** 
you have git installed by default :)

run the following command to clone the repository:
  ```bash
  git clone https://github.com/natasa-plulikova/brainstorm23_BotAI.git
   ```
   
### 2. Create + activate venv
- redirect to the brainstorm23_BotAI directory where the repository was cloned
- launch the terminal in this folder and create a new python environment using the following command:
    ```bash
    python -m venv .venv
    ```
- activate the newly created python environment using this command:

    **Windows:**
    ```bash
    .\.venv\Scripts\activate.bat
    ```
    **Linux/Mac:**
    ```bash
    source .venv/bin/activate
    ```
### 3. Install required dependencies
   ```bash
   pip install -r requirements.txt
   ```
