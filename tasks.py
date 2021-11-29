from invoke import task
from configure import FlaskConfigure
import time, os

def get_system_info():
    if platform == "linux" or platform == "linux2":
        return ("Linux")
    elif platform == "darwin":
        return ("MAC OS")
    elif platform == "win32":
        return ("Windows")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run(c, header, command, footer ):
    print(f"{bcolors.HEADER}->  {header}")
    print(f"{bcolors.OKCYAN}")
    c.run(command)
    print(f"{bcolors.OKGREEN}--  {footer}\n")

@task
def install(c):
    """
    Installs required python packages, and runs initial setup functions.
    """

    # Install required Python packages with PIP
    run(c, "Start install library", "pip3 install -U -r requirements.txt" , "Install done")
    run(c, "Start migrate database", "python manager.py migrate" , "Migrate done")

@task
def migrate(c):
    run(c, "Start migrate database", "python manager.py migrate" , "Migrate done")

@task
def initdb(c):
    run(c, "Init database for dev", "python manager.py init_db" , "Init done")

@task
def yaml(c):
    run(c, "Create yaml example", "python manager.py create_yaml" , "Create file done")

@task
def test(c):
    run(c, "Testing command", "python manager.py test" , "Test done")

@task
def newmodule(c):
    print("Enter module name:")
    moduleName = input()
    examplePath = os.path.dirname(os.path.abspath(__file__)) + "/utils/example"
    print(examplePath)
    

    run(c, "Create module", f"mkdir {moduleName}" , "Test done")

@task
def push(c):
    print("Commit text:")
    cm = input()
    cmd  = f"git commit -m '{cm}'"
    run(c, "Commit data change", cmd , "Commit done")
    run(c, "Pust data to server", "git push" , "Push done")
    import requests, json
    x = requests.get('http://13.229.146.39:5005/updatesoftware')
    ms = json.loads(x.text)
    print("server message: " + ms["message"])

@task
def server(c):
    run(c, f"Start runing server: {FlaskConfigure.HOST}:{FlaskConfigure.PORT}", "python main.py" , "")