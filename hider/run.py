import os
from win32com import client
from hider import Hider
from pprint import pprint


def transform(file_path, save_path):
    word = client.Dispatch('Word.Application')
    doc = word.Documents.Open(file_path)
    print('save_path: %s' % save_path)
    doc.SaveAs(save_path, 12)
    doc.Close()
    word.Quit()


if __name__ == "__main__":
    '''hider = Hider('./hider/test.docx')
    hider.replace_all()'''

    dir_path = os.path.dirname(os.path.abspath(__file__))

    case_dir = './DownloadCases'
    case_files = []
    for root, dirs, files in os.walk(case_dir):
        case_files = files

    """
    for case_file in case_files:
        # print(case_file)
        origin_path = os.path.join(dir_path, 'DownloadCases', case_file)
        save_path = os.path.join(dir_path, 'DocxCases', case_file + 'x')
        # print(origin_path, save_path)
        transform(origin_path, save_path)
    """
    for case_file in case_files:
        docx_path = os.path.join(dir_path, 'DocxCases', case_file + 'x')
        save_path = os.path.join(dir_path, 'HideCases', case_file + 'x')
        hider = Hider(docx_path)
        # hider.hides
        hider.replace_all(save_path)
