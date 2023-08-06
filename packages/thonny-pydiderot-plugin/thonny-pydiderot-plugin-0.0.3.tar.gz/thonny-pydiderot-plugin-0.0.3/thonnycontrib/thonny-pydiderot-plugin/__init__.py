import os

def load_plugin():
    """
    Cette fonction sera appellée au lancement de thonny.
    On peut donc y faire les configurations que l'on veut.

    Todo:
    - changer le dossier de travail par %HOMESHARE%/python/
    - ajouter le dossier partager en écriture contenant les libs maisons au sys.path
    """
    dossier = os.path.join(
        'S:',
        '_LOGICIELS',
        'MATH',
        'Python',
        'libs'
    )
    if os.path.isdir(dossier):
        os.environ['PYTHONPATH'] = dossier
