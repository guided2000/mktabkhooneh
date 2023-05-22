from datetime import datetime

#datetime.strptime(dto, "%Y-%m-%d")
#2023-05-08 17:41:48+00:00
def diffNowDate(DateStr):
   DateStr=str(DateStr)
   DateStr=DateStr[:-6]
   fmt = '%Y-%m-%d %H:%M:%S'
   d2 = datetime.strptime(str(datetime.now().year)+'-'+str(datetime.now().month)+'-'+str(datetime.now().day)+' '+str(datetime.now().hour)+':'+str(datetime.now().minute)+':'+str(datetime.now().second), fmt)
   d1 = datetime.strptime(DateStr, fmt)
   ago1=str(d2-d1).split(',')
   if len(ago1)<2:
       ago2=ago1[0]
       
   else:    
       ago2=ago1[1][1:]
   ago3=ago2.split(':')
   ago=[]
   for i in ago3:
      ago.append(int(i))
   days =(d2-d1).days
   year= days//365
   month= (days-(year*365))//30
   week= (days-(month*30+year*365))//7
   day=days-(week*7+month*30+year*365)
   hour=ago[0]
   minute=ago[1]
   second=ago[2]
   
   year=str(year)+'سال و'
   month=str(month)+'ماه و'
   week=str(week)+'هفته و'
   day=str(day)+'روز و'
   hour=str(hour)+'ساعت و'
   minute=str(minute)+'دقیقه و'
   second=str(second)+'ثانیه و'
   z=[year,month,day,hour,minute]      

   output=''
   for o in z:
        if o[0] != '0'and len(z)>0:
           output+=o
           output1=output[:-1]+'پیش'
   z=[year,month,day,hour,minute]
   if len(z)<1:
      output1='اکنون'
   
   return output1