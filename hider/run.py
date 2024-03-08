from hider import Hider
from pprint import pprint


if __name__ == "__main__":
    hider = Hider('./test.docx')
    hider.replace_all()
