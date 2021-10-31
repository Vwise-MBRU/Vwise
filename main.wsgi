import sys
sys.path.insert(0,'/home/rasaadmin/Vwise')

activate_this='/home/rasaadmin/.local/share/virtualenvs/Vwise-vqgfxjry/bin/activate_this.py'
with open(activate_this) as file_:
        exec(file_.read(),dict(__file__=activate_this))

from main import app as application
