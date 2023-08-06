import pandas as pd
from bisect import bisect_right
from collections import defaultdict

class eventDict(defaultdict):
        '''An autosorting dictionary of timebased events'''
        def __init__(self, *args, **kw):
                self.default_factory = list
                
        def __repr__(self):
                return(str(self.items()))
        
        def add_event(self,name,time):
                if time in self[name]:
                        print(f'pyEvent error: eventdict["{name}"] already exists at "{time}"')
                else:
                        self[name].append(time)
                        self[name] = sorted(self[name])

        def determine_event_ranges(self,startname,endname):
                startev = []
                endev = []
                sequencedStart = []
                sequencedEnd = []
                for k,v in self.items():
                        if k == startname:
                                for i in self[k]:
                                        startev.append(float(i))
                        if k == endname:
                                for i in self[k]:
                                        endev.append(float(i))

                for j in range(0,len(startev)):
                        if j < len(endev):
                                (a,b) = _find_end(endev, startev[j])
                                sequencedEnd.append(a)
                                sequencedStart.append(b)

                return(sequencedStart,sequencedEnd)

def parse_events(ex_event_dict):
        '''returns a new eventdict from a dict of values'''
        eventdict = eventDict()
        for k,v in ex_event_dict:
                eventdict.add_event(k,v)
        return(eventdict)

def create_cycles(data,eventdict,start,end):
        '''returns a dataframe of cut cycle data based on input events'''
        completeDf = pd.DataFrame(columns=data.columns)
        column_name_import = list(data.reset_index().columns)
        column_name_export = []
        
        (seq_start,seq_end) = eventdict.determine_event_ranges('start','end')

        for i in range(0,len(seq_start)):
                t = column_name_import
                for x in range(0,len(t)):
                        new_name = t[x] + ('_' + str(i+1))
                        column_name_export.append(new_name)

        
        for i in range(0,len(seq_start)):
                cutdf = pd.DataFrame(columns=data.columns)
                cutdf = data[(data.index > seq_start[i]) & (data.index < seq_end[i])].reset_index()
                index_col = data.index.name

                if index_col == None:
                        index_col = 'index'
                #cutdf.drop(columns=index_col,inplace=True)
                if i == 0:
                        completeDf = completeDf.append(cutdf,ignore_index=True,sort=False)[cutdf.columns.tolist()]
                else:
                        completeDf = pd.concat([completeDf,cutdf], axis=1,ignore_index=True)

        completeDf.columns = column_name_export
        return(completeDf)

def _find_end(endList, startEvent):
        pos = bisect_right(endList, startEvent)

        if pos == 0:
                return(endList[0], startEvent)

        if pos == len(endList):
                print("no ends found")
                return

        after = endList[pos]
        return (after,startEvent)
