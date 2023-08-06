# cyclist
Event-based data analysis framework
v 0.0.1

Cyclist allows you to split dataframes at predetermined "events". For instance, with an EMG channel measured during exercise you may capture the moment flexion and extension happens via motion capture. You can input the timing of your flexion and extension events into dictionaries and pass that into the create cycles function which will return the EMG cycles cut from first event 1 to stop event 1, and then first event 2 to stop event 2. Or, pass the same event twice, which will split the file into multiple parts from each event. 

Class: eventDict, extends defaultdict

New eventDict:  
x = cyclist.eventDict()  

Explicit event creation:  
eventDict.add_event(name,time)  
  
Parse a dict of events:  
events = cyclist.parse_events(external_event_dict)  
external event dict must be a valid dictionary of form {'x':[1,2,3], 'two':[5.0,51,107]}  

Split data based on cycles:  
cyclist.create_cycles(data,eventDict,start,end)  
Loops over the data and cuts from:  
  Start 1 -> End 1  
  Start 2 -> End 2  
  ...  
  Start n -> End n  
  
  Returns a dataframe with len(data.columns) * n columns, with each column given a _n suffix  