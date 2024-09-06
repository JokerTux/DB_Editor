
# DB_editor

## Installation:

### Ubuntu Server:

1. **Update your system:**

```bash
sudo apt-get update
sudo apt-get upgrade
```

2. **Create a directory:**

```bash
mkdir my_app
cd my_app/
```

3. **Clone the project:**

```bash
git clone https://github.com/JokerTux/DB_editor.git
```

4. **Install Python Virtual Environment:**

```bash
sudo apt-get install python3.12-venv
python3 -m venv .venv
source .venv/bin/activate
cd DB_editor/
```

5. **Install the required frameworks:**

```bash
pip3 install -r requirements.txt
```

6. **Change the IP and secret key (with vim):**

```bash
vim main.py
```

- Search for `? CHANGE ME`
- Press `i` to enter insert mode and change the value inside `''`
- Press `ESC`
- Scroll to the bottom by pressing `G`
- Press `i` again to change the IP address and port if needed
- Press `ESC` and type `:wq` to save and quit

7. **Start the website:**

```bash
python3 main.py
```

## Create your first account:

1. Go to the `instance` directory:

```bash
cd instance/
```

2. Run the register script `admin_panel_acc_creation.py`:

```bash
python3 admin_panel_acc_creation.py
```

- Follow the instructions provided.

Example:

- **Login:** `admin`
- **Password:** `1234`
- If **admin**, press 1; if **moderator**, press 0: `1`

**DONE!** :)
