# DB_editor
<h2> Installation :</h2>
UBUNTU SERVER :<br>

1. Update your system :<br>
#sudo apt-get update<br>
#sudo apt-get upgrade

2. Create a directory :<br>
#mkdir my_app<br>
#cd my_app/

3. Clone project :<br>
#git clone https://github.com/JokerTux/DB_editor.git

4. Install Python Virtual env. :<br>
#sudo apt-get install python3.12-venv<br>
#python3 -m venv .venv<br>
#source .venv/bin/activate<br>
#cd DB_editor/

5. Install Frameworks : <br>
#pip3 install -r requirements.txt

6. Change the IP and the secret key : <br>
#vim main.py <br>
</t>   #? CHANGE ME <br>
</t>   #i
</t>   change the value inside ''<br>
</t>   Press ESC <br>
</t>   #<shift> G <br>
</t>   #i<br>
</t>   change the IP adress and port value if needed<br>
</t>   Press ESC <br>
</t>   #:wq
 
7. Start the website :<br>
#python3 main.py
<br>


<h2> Create your first account :</h2>
<br>
1. Go to instance dir :<br>
#cd instance/<br>
#python3 admin_panel_acc_creation.py<br><br><br>
follow the instructions <br>
example :<br>
</t> login : admin <br>
</t> password : 1234 <br>
</t> if admin press 1; if moderator press 0 : 1 <br>
</t> DONE :) !<br>

GLHF ! 
