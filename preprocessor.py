import pandas as pd 
import re
import datetime as dt

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\D{3}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern,data)


    df = pd.DataFrame({'Messages' : messages, 'Dates' : dates})
    df['Dates'] = pd.to_datetime(df['Dates'], format = '%d/%m/%y, %I:%M %p - ')

    #--------------------------------------------------------------------------------------
    users = []
    message = []

    for msg in df['Messages']:
        entry = re.split('([\w\W]+?):\s', msg)

        if entry[1:]:
           users.append(entry[1])
           message.append(entry[2])

        else:
          users.append('Notification')
          message.append(entry[0])




    df['User'] = users
    df['Message_'] = message

    df.drop(columns = ['Messages'], inplace = True)

    #--------------------------------------------------------------------------------
    df['Year'] = df['Dates'].dt.year
    df['Month'] = df['Dates'].dt.strftime('%B')
    df['Day'] = df['Dates'].dt.day
    df['Day Name'] = df['Dates'].dt.day_name()
  
    df['Hour'] = df['Dates'].dt.hour
    df['Minute'] = df['Dates'].dt.minute
    



    period = []
    for hour in df['Hour']:
       if hour ==23:
          period.append(str(hour)+'-'+str('00'))
       elif hour == 0:
          period.append(str('00')+'-'+str(hour + 1))
       else:
          period.append(str(hour)+'-'+str(hour+1))


    df['Period'] = period

    #----------------------------------------------------------------------------------
    return df




    