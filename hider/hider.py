import re
from pprint import pprint
from docx import Document
import cpca


class Hider:
    def __init__(self, doc_path: str):
        self.doc_path = doc_path
        self.doc = Document(doc_path)
        self.paras = self.doc.paragraphs

    @property
    def text(self):
        t = ''
        for para in self.paras:
            t += para.text + '\n'
        return t

    @property
    def head(self):
        heads = []
        for para in self.paras:
            text = para.text
            if re.match(r'原告[\s\S]*一案', text):
                return heads
            else:
                heads.append(para)
        return heads

    @property
    def parties(self):
        parties = []
        for para in self.head:
            text = para.text

            splits = text.split('：')

            if len(splits) > 1:
                # print(text)
                identity = splits[0]
                splits2 = splits[1].split('，')
                name = splits2[0]

                info = {
                    'identity': identity,
                    'name': name,
                }

                if len(splits2) > 1:
                    gender = splits2[1]
                    if gender == '男' or gender == '女':
                        info['gender'] = gender

                parties.append(info)

        return parties

    @property
    def hides(self):
        hides = []

        idens = [
            "原告",
            "被告",
            "第三人",
            "法定代表人",
            "委托诉讼代理人"
        ]

        for party in self.parties:
            party['type'] = ''
            party['need_hidden'] = True

            identity = party['identity']

            if identity == '原告' or identity == '被告' or identity == '第三人':
                if party.get('gender'):
                    party['type'] = 'natural person'
                else:
                    party['type'] = 'law person'

            if identity == '法定代表人' or identity == '负责人':
                party['type'] = 'natural person'

            if identity == '委托诉讼代理人':
                party['type'] = 'natural person'
                if party.get('gender'):
                    party['need_hidden'] = True
                else:
                    party['need_hidden'] = False

            hides.append(party)

        names = []
        for hide in hides:
            name = hide
            origin_name = hide['name']
            hide_name = ''
            
            if hide['type'] == 'natural person':                
                hide_name = hide['name'][0] + '某'
                counts = find_duplicated_names(names, hide_name)
                if counts > 0:
                    hide_name = hide_name + str(counts + 1)

            if hide['type'] == 'law person':
                patterns = [
                    '有限公司',
                    '有限责任公司',
                    '股份有限公司',
                    '股份公司',
                    '人民政府',
                ]
                for pattern in patterns:
                    if re.match(r'[\s\S]*' + pattern, origin_name):
                        hide_name = '某' + pattern
                        counts = find_duplicated_names(names, hide_name)
                        if counts > 0:
                            hide_name = hide_name + str(counts + 1)

            name['origin_name'] = origin_name
            name['hide_name'] = hide_name if hide['need_hidden'] else origin_name
            names.append(name)

        return hides

    def replace_all(self, save_path):
        for hide in self.hides:
            origin_name = hide['origin_name']
            hide_name = hide['hide_name']
            for para in self.paras[3:]:
                para.text = para.text.replace(origin_name, hide_name)
        
        for para in self.paras:
            text = para.text
            result = re.search(r'(住所地|户籍地|现住|住)([\s\S]*)(。|，)', text)

            if result:
                origin_address = result.group(1) + result.group(2)
                result = re.search(r'(住所地|户籍地|现住|住)([\u4e00-\u9fa5]{0,100})市', text)
                
                city = None
                district = None
                address_flage = None

                if result:
                    address_flage = result.group(1)
                    city = result.group(2)

                result = re.search(r'(市)([\u4e00-\u9fa5]{0,100})(县|区)', text)
                if result:
                    district = result.group(2) + result.group(3)
                
                hidden_address = ''

                if address_flage:
                    hidden_address += address_flage
                if city:
                    hidden_address += city + '市'
                if district:
                    hidden_address += district

                para.text = para.text.replace(origin_address, hidden_address)

        self.doc.save(save_path)


def find_duplicated_names(names, hide_name):
    counts = 0
    for name in names:
        if name['hide_name'] == hide_name:
            counts += 1
    return counts


def includes(arr, key):
    for i in arr:
        if i == key:
            return True
    return False
