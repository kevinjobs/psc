from hider.judgment import DocxParser
from pprint import pprint


if __name__ == '__main__':
    text = '(2023)苏0106民初15903号'
    dp = DocxParser(r"C:\Users\kevin\Downloads\DocxCases\(2023)苏0106民初15903号.docx")
    pprint(dp.parties)
