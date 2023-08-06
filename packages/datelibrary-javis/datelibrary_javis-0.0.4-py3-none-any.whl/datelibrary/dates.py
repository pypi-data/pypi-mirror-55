
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 18:37:06 2019

@author: ginnidahiya
"""



import re
import datetime 
timedelta = datetime.timedelta 
from datetime import datetime,timedelta
from calendar import monthrange

class DateData:
    def __init__(self, query):
        self._dates = {
        1:['January', 'Jan'],
        2:['February', 'Feb'],
        3:['March', 'Mar'],
        4:['April', 'Apr'],
        5:['May'],
        6:['June','Jun' ],
        7:['July', 'Jul'],
        8:['August', 'Aug'],
        9:['September', 'Sept','Sep'],
        10:['October', 'Oct'],
        11:['November', 'Nov'],
         12:['December','Dec']
        }     
        self._ordinals = ['first', 'second', 'third','fourth' ,'fifth',
                          'sixth','seventh','eighth','ninth','tenth']
        self._verbdates = '(\d{1,2})\s?(?:th|nd|st|rd)?\s?(?:of)?\s?(<month>)\s?(?:of)?\s?(\d{2,4})'
        self._monthyear = '(?<!(?:\s\d{1}\w{2})|(?:\d{2}\w{2}))\s(<month>)\s(\d{2,4})'
        self._month = '(?<!(?:\s\d{1}\w{2})|(?:\d{2}\w{2}))(?!<month>\s\d{4})\s(<month>)\s'
        self._datemonth = '(\d{1,2})\s?(?:th|nd|st|rd)?\s?(?:of)?\s?(<month>)\s(?!\d{4})'
        self._onlynumdates = '(\d{1,2})(?:\-|\.|\/)(\d{1,2})(?:\-|\.|\/)?(\d{2,4})?'
        self._query = query.lower().translate(str.maketrans('', '', '.,?'))
        self._query = " " + self._query + " "
        self._monthytd = '\s(<month>)\s'
        self._empty = '\d{1,2}\s<month>'
        
    def get_month_from_str(self, text):
        '''
        
        
        '''
        for key,values in self._dates.items():
            for syn in values:
                if syn.lower() == text.lower():
                    return key
    
    
    @staticmethod
    def sort_dates(tuple_list):
        '''
        --Sort dates in format [(date, month, year),(date, month, year)]
        '''
        datetime_dates = sorted([datetime(tup[2],tup[1],tup[0]) for tup in tuple_list])
        dates = [(date.date().day,date.date().month,date.date().year) for date in datetime_dates]
        return dates
    
    
    @staticmethod
    def infer_format( num_result):
        '''
        Convert all dates to dd, mm ,yyyy or dd, mm from str
        '''
        try:
            for i,date in enumerate(num_result):
                if date[2]=='':
                    num_result[i] = (int(date[0]), int(date[1]), datetime.today().year)
                else:
                    if int(date[0])<12:
                        if int(date[1])<=12:
                            num_result[i] = (int(date[0]), int(date[1]),int(date[2]))
                        else:
                            num_result[i] = (int(date[1]), int(date[0]),int(date[2]))      
            return list(set(num_result))
        except IndexError:
            return []
    
    
    
    @staticmethod       
    def last_day(d, day_name):
        '''
        ---Returns last day_name from d date. For example, if d is today and day_name is 'sunday'
        the function resturns the last sunday.
        
        Inputs:
            -d is datetime obj
            -day_name is ['sunday','monday','tuesday','wednesday',
                            'thursday','friday','saturday']
            
        Return:
            -datetime obj
        '''
        days_of_week = ['sunday','monday','tuesday','wednesday',
                            'thursday','friday','saturday']
        target_day = days_of_week.index(day_name.lower())
        delta_day = target_day - d.isoweekday()
        if delta_day >= 0: delta_day -= 7 # go back 7 days
        return d + timedelta(days=delta_day)  
    
    
    @staticmethod
    def stringify(date_list):
        '''
            To convert [(date(int), month(int), year(int)),(date(int), month(int), year(int)), ...]
            to ["yyyy-mm-dd","yyyy-mm-dd",...]
            
            Input:
                -list > [(date(int), month(int), year(int)),(date(int), month(int), year(int)), ...]
                
            Returns:
                -list > ["yyyy-mm-dd","yyyy-mm-dd",...]
            
        '''
        return [str(date[2]).zfill(2)+"-"+str(date[1]).zfill(2)+"-"+str(date[0]).zfill(2) for date in date_list]

    def empty_from_string(self):
        string = self._query.lower()
        for month, syns in self._dates.items():
            syns = sorted(syns, key =lambda x: len(x), reverse = True)
            for syn in syns:
                pattern = self._empty.replace('<month>',syn.lower())
                sub_obj = re.subn(pattern," ",string)
                if sub_obj[1] > 0:
                    string = sub_obj[0]
                    break
        return string
                    
                    
    
    def only_verbdates(self):
        '''
        --Method to capture dates like d(or dd)(st/nd optional) <month> yy(or yyyy) ONLY
        
        '''
        results_all = []
        for month, syns in self._dates.items():
            for syn in syns:
                pattern = self._verbdates.replace('<month>',syn.lower())
                result = re.findall(pattern, self._query)
                results_all.extend(result)
        results_all = [(int(date[0]),int(self.get_month_from_str(date[1])),int(date[2])) for date in results_all]
        return results_all            
    
    
    def only_monthyear(self):
        '''
        --Method to capture dates like <month> yy(or yyyy) ONLY
        
        '''
        year = datetime.today().year
        results_all = []

        for month, syns in self._dates.items():
            for syn in syns:
                result = re.findall(self._monthyear.replace('<month>',syn.lower()), self._query)
                results_all.extend(result)
                
        results_all = list(set(results_all))
        try:           
            result = sorted(results_all,key=lambda x: len(x[0]), reverse=True)[0]
            if result[1]!='':
                year = int(result[1])
            month = self.get_month_from_str(result[0])
            no_days = monthrange(year, month)[1]
            return [(1,month,year),(no_days,month,year)]
        
        except IndexError:
            return []
        
    def only_datemonth(self):
        '''
        --Method to capture dates like 1(st/nd optional) <month>

        '''
        results_all = []
        month = datetime.today().month
        year = datetime.today().year
        
        for month, syns in self._dates.items():
            for syn in syns:
                pattern = self._datemonth.replace('<month>',syn.lower())
                result = re.findall(pattern, self._query+" ")
                results_all.extend(result)
        try:
            results_all = [(int(date[0]),self.get_month_from_str(date[1]),year) for date in results_all]
            results_all = list(set(results_all))
            return results_all
        except IndexError:
            return []
    
    
    def only_numdates(self):
        '''
        --Method to capture dates like d(or dd)/-.m(or mm)/.-yy(or yyyy)
        '''
        return re.findall(self._onlynumdates, self._query)
    

    def only_month(self):
        '''
        --Method to capture dates with  <month> ONLY. Returns 1st to last date of the month with current year
        '''
        year = datetime.today().year
        results_all = []
        for month, syns in self._dates.items():
            for syn in syns:
                pattern = self._month.replace('<month>',syn.lower())
                result = re.findall(pattern, self._query+" ")
                results_all.extend(result)
        
        try:            
            if results_all[0]!='':
                print(results_all, month)
                result_all = sorted([self.get_month_from_str(month) for month in results_all])
                if len(result_all)>1:
                    start = result_all[0]
                    end = result_all[-1]
                    no_days =  monthrange(year, end)[1] 
                    return [(1,start,year),(no_days, end,year)]
                else:
                    start = result_all[0]
                    no_days =  monthrange(year, start)[1] 
                    return [(1,start,year),(no_days, start,year)]
        except IndexError:
            return []
                        
    
    def only_relativedates(self):
        '''
        --Method to capture relative dates like this month, last year, last week only
        
        '''
        query = self._query.replace('current month','this month')
        query = query.replace('current year','this year')
        month = datetime.today().month
        year = datetime.today().year
        
        
        for timeline in ['last month', 'this month']:
            if timeline in self._query:
                if 'last' in self._query:
                    month = datetime.today().month
                    year = datetime.today().year
                    if month == 1:
                        month = 12
                        year -= 1
                    else:
                        month -= 1
                    
                no_days = monthrange(year, month)[1]                
                return [(1,month,year), (no_days, month, year)]
                
                    
        for timeline in ['last year', 'this year']:
            if timeline in self._query:
                year = datetime.today().year
                if 'last' in timeline:  
                    return [(1,1,year-1), (31,12,year-1)]         
                return [(1,1,year), (1, 12,year)]
            
        for timeline in ['last week']:
            if timeline in self._query:
                last_sunday = self.last_day(datetime.today(), 'sunday')
                last_monday = self.last_day(last_sunday, 'monday')
                date_range = [last_monday, last_sunday]
                date_range = [(date.date().day,date.date().month,date.date().year) for date in date_range]
                return date_range
            
        for timeline in ['today','yesterday']:
            if timeline in self._query:
                if timeline == 'today':
                    date = datetime.today()
                    return [(date.date().day,date.date().month,date.date().year)]
                if timeline == 'yesterday':
                    date = datetime.today() + timedelta(days = -1)
                    return [(date.date().day,date.date().month,date.date().year)]
        
        for timeline in ['lysm']:
            if timeline in self._query:
                month = datetime.today().month
                year = datetime.today().year -1
                no_days = monthrange(year, month)[1]                
                return [(1,month,year), (no_days, month, year)]
            
                
        return []
    
    def only_ytdmtdqtd(self):
        '''
        --Method to capture ytd, mtd, qtd only
        
        '''
        today = (datetime.today().day, datetime.today().month, datetime.today().year)
        if 'ytd' in self._query.lower():    
            return [(1,1,datetime.today().year),today]
            
        if 'mtd' in self._query.lower():
            return [(1,datetime.today().month, datetime.today().year), today]  
        
        if 'qtd' in  self._query.lower():
            if datetime.today().month%3 == 0: 
                quarter = int(datetime.today().month/3)
            else:
                quarter = int(datetime.today().month/3) + 1
            quarter_begin = [1,4,7,10]
            month = quarter_begin[quarter-1]
            return [(1,month, datetime.today().year),today]
        
        return []
    
    def only_lm(self):
        '''
        --Method to capture l2m,l3m only
        '''
        result = re.findall(r'(?:l|p)(\d{1,2})m',self._query)
        month = datetime.today().month
        year = datetime.today().year
        if len(result)>0:
            if len(result[0])>0:
                captured_month = int(result[0])
                if month - captured_month>0:
                    start_month = month - captured_month
                    end_month = month - 1
                else:
                    start_month = month - captured_month + 12
                    end_month = month - 1 + 12
                    year -= 1
        
                no_days = monthrange(year, end_month)[1] 
                return [(1,start_month,year),(no_days,end_month,year)]
        return []
    
    
    def only_monthytd(self):
        '''
        --Method to capture <month> ytd only
        '''
        year = datetime.today().year
        if 'ytd' in self._query.lower():
            for month, syns in self._dates.items():
                for syn in syns:
                    pattern = self._monthytd.replace('<month>',syn.lower())
                    result = re.findall(pattern, " "+self._query+" ")
                    if len(result)==1:
                        if result[0][0] != '':
                            month = self.get_month_from_str(result[0])
                            no_days = monthrange(year, month)[1] 
                            return [(1,1,year),(no_days,month,year)]
        return []
        
    def only_ordverbweek(self):
        '''
        --Method to capture '<ordinal> (first, second, ...) week of <month>
        '''
        master_pattern = '(<ordinal>)\sw(?:ee)?k\s?(?:of)?\s?(<month>)?'
        month = datetime.today().month
        year = datetime.today().year
        NUM_WEEKS = 4
        for i, ordinal in enumerate(self._ordinals[:NUM_WEEKS]):
            pattern = master_pattern.replace('<ordinal>',ordinal.lower())
            match = re.findall(pattern,self._query.lower())
            
            try:
                 if match[0][0]!='':
                    if ordinal == 'first':   
                        for num,_month in self._dates.items():
                            for syn in _month:
                                month_match = re.findall(pattern.replace('<month>',syn.lower()),self._query.lower())
                                if len(month_match)>0:
                                    if syn.lower() == month_match[0][1]:
                                        return [(1,num,year),(7,num,year)]
                        return [(1,month,year),(7,month,year)]
                    else:
                        start_day = i*7
                        for num,_month in self._dates.items():
                            for syn in _month:
                                month_match = re.findall(pattern.replace('<month>',syn.lower()),self._query.lower())
                                if len(month_match)>0:
                                    if syn.lower() == month_match[0][1]:
                                        return [(start_day,num,year),(start_day+7,num,year)]
                    return [(start_day,month,year),(start_day+7,month,year)]
            except IndexError:
                return []

            
    def only_ordnumweek(self):
        ''' 
        --Method to capture '1st(or 2nd, 3rd, ...) week of <month>
        '''
        pattern = '(\d{1,2})\s?(?:th|nd|st|rd)?\sw(?:ee)?k\s?(?:of)?\s?(<month>)?'
        month = datetime.today().month
        year = datetime.today().year
        is_month = None
        week = None
        for num,_month in self._dates.items():
            for syn in _month:
                result = re.findall(pattern.replace('<month>',syn.lower()),self._query.lower())
                if len(result)>0:
                    if result[0][1]!='':
                        is_month = num
                    if result[0][0]!='':
                        week =int(result[0][0])
                
        if is_month and week:
            if week == 1:
                return [(1,is_month,year),(7,is_month,year)]
            if 5>week >1:
                week-=1
                return [(week*7,is_month,year),(week*7+7,is_month,year)]
        elif not is_month and week:
            if week == 1:
                return [(1,month,year),(7,month,year)]
            if 5>week >1:
                week-=1
                return [(week*7,month,year),(week*7+7,month,year)]
        return []
            
    
    def compile_dates(self):
        if len(self.only_monthytd()) > 1:
            result = list(set(self.only_monthytd()))
            result = self.infer_format(result)
            result = self.sort_dates(result)
            result = self.stringify(result)
            return result
        
        if len(self.only_ordnumweek()+self.only_ordverbweek()) >1:
            result = list(set(self.only_ordnumweek()+self.only_ordverbweek()))
            result = self.infer_format(result)
            result = self.sort_dates(result)
            result = self.stringify(result)
            return result
       
        elif len(self.only_relativedates() + self.only_ytdmtdqtd() + self.only_lm())>=1:
            result = list(set(self.only_relativedates() + self.only_ytdmtdqtd()+self.only_lm()))
            result = self.infer_format(result)
            result = self.sort_dates(result)
            result = self.stringify(result)
            return result

            
        elif len(self.only_numdates() + self.only_verbdates())>0:
            result = list(set(self.only_numdates()+self.only_verbdates()))        
            result = self.infer_format(result)
            result = self.sort_dates(result)
            result = self.stringify(result)
            return result

        elif len(self.only_datemonth()+self.only_monthyear())>0:
            result = list(set(self.only_datemonth()+self.only_monthyear()))        
            result = self.infer_format(result)
            result = self.sort_dates(result)
            result = self.stringify(result)
            return result
        
        else:
            result = list(set(self.only_month()))
            result = self.infer_format(result)
            result = self.sort_dates(result)
            result = self.stringify(result)
            return result

        return []
            
            
        
        
if __name__ == '__main__':
    day = datetime.today().day
    month = datetime.today().month
    year = datetime.today().year
    no_days = monthrange(year, month)[1]  
    today = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
    
    pick_dates = DateData("performance of DCOKE 1000 ml from 1st Sept to 2nd of Oct ")
    formatted = pick_dates.compile_dates()
    print(formatted == ['2019-09-01', '2019-10-02'])
  
    # pick_dates = DateData("performance of DCOKE 1000 ml from 1st September 2019 to 2nd Sep 2019 ")
    # formatted = pick_dates.compile_dates()
    # print(formatted == ['2019-09-01', '2019-09-02'])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml from 1/9/2015 to 2/10/2015 ")
    # formatted = pick_dates.compile_dates()
    # print(formatted == ['2015-09-01', '2015-10-02'])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml from 1/9 to 2/10 ")
    # formatted = pick_dates.compile_dates()
    # print(formatted == ['2019-09-01', '2019-10-02'])

    # pick_dates = DateData("performance of DCOKE 1000 ml from 13/12 to 19/12 ")
    # formatted = pick_dates.compile_dates()
    # print(formatted == ['2019-12-13', '2019-12-19'])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml today")
    # formatted = pick_dates.compile_dates()
    # print(formatted )

    # pick_dates = DateData("performance of DCOKE 1000 ml last month ")
    # formatted = pick_dates.compile_dates()
    # print(formatted , [(1, month-1, 2019), (monthrange(year, month-1)[1], month-1, 2019)])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml l3m ")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(1, month-3, 2019), (monthrange(year, month-1)[1] , month-1, 2019)])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml l1m ")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(1, month-1, 2019), (monthrange(year, month-1)[1] , month-1, 2019)])

    # pick_dates = DateData("performance of DCOKE 1000 ml last month ")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(1, month-1, 2019), (monthrange(year, month-1)[1], month-1, 2019)])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml first week ")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(1, month, 2019), (7, month, 2019)])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml fourth week")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(21, month, 2019), (28, month, 2019)])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml 1st week of jan")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(1, 1, 2019), (7, 1, 2019)])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml 2nd week of feb")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(7, 2, 2019), (14, 2, 2019)])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml third week of march")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(14, 3, 2019), (21, 3, 2019)])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml fourth week of dec")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(21, 12, 2019), (28, 12, 2019)])

    # pick_dates = DateData("performance of DCOKE 1000 ml 3rd week of june")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(14, 6, 2019), (21, 6, 2019)])

    # pick_dates = DateData("performance of DCOKE 1000 ml 3rd week of september")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(14, 9, 2019), (21, 9, 2019)])

    # pick_dates = DateData("Performance July 2018 distributor wise")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(1,7,2018),(31,7,2018)])
    
    # pick_dates = DateData("performance of DCOKE 1000 ml in dec ")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(1,12,2019),(31,12,2019)])

    # pick_dates = DateData("Performance from 7th Jul 2018 to 9th Sep 2019 distributor wise ")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(7,7,2018),(9,9,2019)])

    # pick_dates = DateData("performance of DCOKE 1000 ml ")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [])

    # pick_dates = DateData("Performance from 1 August to 3 sept")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(1,8,2019),(3,9,2019)])

    # pick_dates = DateData("My performance this month")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(1,month,2019),(no_days,month,2019)])
    
    # pick_dates = DateData("MMy performance from 27 July to 31 July?")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(27,7,2019),(31,7,2019)])

    # pick_dates = DateData("13 July to 26 July base Vs achievement")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(13,7,2019),(26,7,2019)])

    # pick_dates = DateData("Performance from 28th July 2019 to 23rd August 2019?")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(28,7,2019),(23,8,2019)])

    # pick_dates = DateData("Base from 1 July to 28July by distributor")
    # formatted = pick_dates.compile_dates()
    # print(formatted == [(1,7,2019),(28,7,2019)])

    # pick_dates = DateData("show gurpreet singh secondary performance ytd in the month of nov")
    # formatted = pick_dates.compile_dates()
    # print(formatted )
