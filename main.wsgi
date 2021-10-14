import sys
sys.path.insert(0,'/home/sree_mbru/vwise_training_public')

activate_this='/home/sree_mbru/.local/share/virtualenvs/vwise_training_public$
    with open(activate_this) as file_:
        exec(file_.read(),dict(__file__=activate_this))

from main import app as application