Install vscode

Android
Install flutter sdk https://docs.flutter.dev/get-started/install/windows
Framework - Flutter
Dart -> programming language
Android Studio -> https://redirector.gvt1.com/edgedl/android/studio/install/2021.3.1.17/android-studio-2021.3.1.17-windows.exe
Open android studio > click more actions > Install the latest sdk with the highest API level
In the Sdk Tools tab install the ff: Android Build Tools, Command-line Tools, SDK platform-tools

Firebase -> used for authentication only, but not needed to be installed

Web
Python 3.9.13 - Programming language  https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe
Checkbox should be checked for Add Python to PATH

Django 4.1.3 - Framework run this command ->  pip install Django

Download and install XAMPP https://sourceforge.net/projects/xampp/files/XAMPP%20Windows/8.2.0/xampp-windows-x64-8.2.0-0-VS16-installer.exe



Setup Web Source code
python --version //To check if the python was properly installed
python -m venv venv //Creates a virtual environment folder,
cd venv/Scripts -> Enter
activate -> Enter
cd ../.. -> Enter
pip install -r requirements.txt //this will install all dependencies

Open xampp 
Start Mysql and Apache
Click Mysql -> Admin
In Browser, Click New (to create a database)
type in database name : clinic$clinic_database
then Click create

In windows start menu type in: environment variables
Click Environment variables
Under System Variables add new
Variable name : DJANGO_ENV
Variable value : LOCAL

python manage.py makemigrations //creates a mapping of python classes into database
python manage.py migrate // this will perform the actual conversion of python classes into mysql database
python manage.py createsuperuser //this will create admin account


python manage.py runserver //This will run the web app


Setup Android Source code

Open vscode source code
Install necessary extensions:
Flutter
Dart

flutter build apk


Running local server for hardware
Server Code Setup


open chrome

in chrome address bar type in : chrome://flags/
in the search box of flags type in : Insecure origins treated as secure
Click Enabled
Then in the textarea, type in : http://www.365gps.com

go to http://www.365gps.com/ and login using 359339077128046 password is 123456

Wait for the wepage to completely load
pressd F12 in chrome
copy and paste ALL the contents of savedb.js in chrome console


In VSCode

python -m venv venv //Creates a virtual environment folder,
cd venv/Scripts -> Enter
activate -> Enter
cd ../.. -> Enter
pip install -r requirements.txt

type in command: python scrape.py


After running the local server
go back to chrome and MAKE SURE that the focus is on the webpage itself
just click anywhere on the webpage

to stop local server press : Ctrl + C