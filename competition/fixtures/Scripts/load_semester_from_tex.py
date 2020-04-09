import re
import json
import datetime
#from ..competition.models import Problem, UserSolution



class SemesterManager:
    def __init__(self,free_semester_id=0,free_serie_id=0,free_problem_id=0):
        self._semester_id = free_semester_id
        self._serie_id = free_serie_id
        self._problem_id = free_problem_id
        self._competition_id = 0

    def get_serie_id(self):
        self._serie_id+=1
        return self._serie_id-1
    
    def get_problem_id(self):
        self._problem_id+=1
        return self._problem_id-1

    def get_competition_id(self):
        self._competition_id+=1
        return self._competition_id-1
    
    def get_semester_id(self):
        self._semester_id+=1
        return self._semester_id-1

    @staticmethod
    def django_repr(model_name,pk,fields):
        return {
            "model": model_name,
            "pk": pk,
            "fields": fields
            }
    
    def create_semester(self,comp_id,year,start,end,late_tags,season):
        fields = {
            "competition" : comp_id,
            "year" : year,
            "start": start,
            "end": end,
            "season" : season
        }
        return SemesterManager.django_repr('competition.Semester',self.get_semester_id(),fields)

    def create_serie(self,semester_id,order,deadline):
        fields = {
            "semester" : semester_id,
            "order" : order,
            "deadline": deadline,
            "complete": False,

        }
        return SemesterManager.django_repr('competition.Semester',self.get_serie_id(),fields)

    def create_problem(self,text,serie,order):
        fields = {
            'problem': text,
            'serie': serie,
            'order': order
        }
        return SemesterManager.django_repr('competition.Problem',self.get_problem_id(),fields)

    def create_new_semester_json(self,problems):
        objects = []
        start_sem ='2020-01-01 22:00:00'
        first_term = '2020-03-01 22:00:00'
        end_sem = '2020-06-01 22:00:00'
        semester = self.create_semester(0,44,start_sem,end_sem,None,1)
        semester_id = semester['pk']
        s1 = self.create_serie(semester_id,1,first_term)
        s1_key = s1['pk']
        objects.append(s1)
        s2 = self.create_serie(semester_id,2,end_sem)
        s2_key = s2['pk']
        objects.append(s2)
        for problem_serie, problem_order, problem_text in problems:
            serie_key = s1_key if problem_serie==1 else s2_key
            objects.append(self.create_problem(problem_text,serie_key,problem_order))
        with open('semesters.json','w') as f:
            print(objects)
            json.dump(objects,f,indent=4)

    
manager = SemesterManager()

roman_numerals={
    'I':1,
    'II':2,
    'III':3,
    'IV':4,
    'V':5,
    'VI':6,
}

class SemesterLaTeXLoader():
    def check_latex():
        pass

    def remove_latex_comments(text):
        text = re.sub(r'\\begin\{comment\}.*?\\end\{comment\}','',text, flags=re.S)
        return re.sub(r'^%.*$',r'',text,flags=re.M)

    def create_semester_db():
        pass

    def export_semester_json():
        
        pass

    def load_kricky(file_name,json_file=None):
        with open(file_name, 'r', encoding='utf8') as input_tex:
            text = input_tex.read()
            text = SemesterLaTeXLoader.remove_latex_comments(text)
            problems = re.findall(r'\\newcommand\{\\zad([^\{\}]+)s([^\{\}]+)\}\{(.*?)\}[^\{\}]*(?=\\newcommand|$)',text,flags=re.S)
            return [(roman_numerals[problem_serie],roman_numerals[problem_order],problem_text.strip('\n')) for problem_order, problem_serie, problem_text in problems ]
            

    def load_strom(file_name):
        with open(file_name, 'r', encoding='utf8') as input_tex:
            text = input_tex.read()
            text = SemesterLaTeXLoader.remove_latex_comments(text)
            problems = re.findall(r'(\\ifcase\\numexpr\\value\{uloha\}-1|\\or).*?\{(.*?)\}[^\{\}]*?(?=\\fi|$|\\or)',text,flags=re.S)
            semester = []
            for i,problem in enumerate(problems):
                semester.append(((i//7)+1,(i%6)+1,problem[1].strip('\n')))
            return semester

if __name__=='__main__':
    x = SemesterLaTeXLoader.load_strom('ulohy_strom.tex')
    manager.create_new_semester_json(x)
    
