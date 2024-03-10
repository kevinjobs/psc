import re
from docx import Document


class CaseParty:
    def __init__(self, party_text: str):
        self.parts = party_text.split(r'：')

    @property
    def typ(self) -> str:
        return self.parts[0]

    @property
    def name(self) -> str:
        other_info = self.parts[1]
        parts = other_info.split(r'，')
        return parts[0]


class Judgment:
    def __init__(self, judgment_path):
        self.judgment_path = judgment_path

    def parse(self):
        if self.raw_type == 'docx':
            pass
        if self.raw_type == 'txt':
            pass
        if self.raw_type == 'doc':
            pass

    @property
    def raw_type(self):
        parts = self.judgment_path.split('.')
        return parts[-1]


class JudgmentParser:
    def __init__(self, judgment_path):
        self.judgment_path = judgment_path
    
    @property
    def head(self):
        raise NotImplementedError

    @property
    def parties(self) -> CaseParty:
        raise NotImplementedError


class DocxParser(JudgmentParser):
    def __init__(self, judgment_path):
        super().__init__(judgment_path)
        self.docx = Document(judgment_path)

    @staticmethod
    def is_case_id(text: str):
        pattern = r'(\(|（)\d{4}(\)|）)[\u4e00-\u9fa5]\d{4}[\u4e00-\u9fa5]{1,3}\d{1,5}[\u4e00-\u9fa5]'
        return re.match(pattern, text) is not None

    @staticmethod
    def is_main_content(text: str):
        pattern = r'原告[\s\S]*一案'
        return re.match(pattern, text) is not None

    @staticmethod
    def is_party(text: str):
        text = text.replace(r'，', ',').replace(r'：', ':').replace(r'。', '')

        pattern = r'(原告|被告):([\u4e00-\u9fa5]*),(男|女),(\d{4}年\d{1,2}月\d{1,2}日出?生,)([\u4e00-\u9fa5]*族,)([\u4e00-\u9fa5]*,)?(户籍地[\u4e00-\u9fa5]*,)?(现?住[\u4e00-\u9fa5]*)'
        groups = re.search(pattern, text)
        if groups:
            return {
                'type': '自然人',
                'type_in_case': groups[1],
                'name': groups[2],
                'gender': groups[3],
                'birthday': groups[4],
            }

        pattern = r'(负责人|经营者|法定代表人):([\u4e00-\u9fa5]{2,10}),([\u4e00-\u9fa5]*)'
        groups = re.search(pattern, text)
        if groups:
            return {
                'type': '自然人',
                'type_in_case': groups[1],
                'name': groups[2],
            }

        pattern = r'(委托诉讼代理人):([\u4e00-\u9fa5]{2,10}),([\u4e00-\u9fa5]*)'
        groups = re.search(pattern, text)
        if groups:
            return {
                'type': '自然人',
                'type_in_case': groups[1],
                'name': groups[2],
                'mark': '律师'
            }


    @property
    def parties(self):
        p = []
        for para in self.docx.paragraphs:
            result = self.is_party(para.text)
            if result:
                p.append(result)
        return p


class JudgmentHider:
    def __init__(self, judgment):
        self.judgment = judgment

    def save(self, output_path: str):
        pass

    @property
    def docx(self):
        pass

