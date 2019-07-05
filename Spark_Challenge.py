#Criação do contexto:
from pyspark import SparkContext
sc = SparkContext.getOrCreate()

#Importando os arquivos de log em duas RDDs:
rddJuly = sc.textFile("access_log_Jul95").cache()
rddAugust = sc.textFile("access_log_Aug95").cache()

#1. Número de hosts únicos.
JulyHosts = rddJuly.flatMap(lambda line: line.split(' ')[0]).distinct().count()
print('July Distinct Hosts: %s' % JulyHosts)

AugustHosts = rddAugust.flatMap(lambda line: line.split(' ')[0]).distinct().count()
print('August Distinct Hosts: %s' % AugustHosts)


#2. O total de erros 404.
def check_404(l):
    try:
        if l.split(' ')[-2] == '404':
            return True
    except:
        return False

Error404July = dict(rddJuly.filter(check_404).filter(lambda line: '404' in line).map(lambda x: (x.split( )[-2],1)).reduceByKey(lambda k,v : k+v).collect())
print('Total July Error 404:', Error404July['404'])

Error404August = rddAugust.map(lambda x: x.split( )[-2]).filter(lambda line: "404" in line).countByValue()
print('Total August Error 404:', Error404August['404'])


#3. Os 5 URLs que mais causaram erro 404.
#July
def check_404(l):
    try:
        if l.split(' ')[-2] == '404':
            return True
    except:
        return False

Error404July = rddJuly.filter(check_404).map(lambda x: (x.split( )[6], x.split( )[-2])).filter(lambda line: '404' in line).map(lambda x: (x,1)).reduceByKey(lambda k,v : k+v).map(lambda x: (x[1], x[0])).sortByKey(ascending=False)
print('***** TOP FIVE URL ERRORS 404 JULY *****')
top = dict(Error404July.take(7))
x = 0
for i in top:
    l = list(top.values())[x]
    print('TOP:', x + 1, '- URL:', l[0] , ' - Errors:', list(top.keys())[x])
    x = x + 1
	
#August	
Error404August = rddAugust.map(lambda x: (x.split( )[6], x.split( )[-2])).filter(lambda line: '404' in line).map(lambda x: (x,1)).reduceByKey(lambda k,v : k+v).map(lambda x: (x[1], x[0])).sortByKey(ascending=False)
print('***** TOP FIVE URL ERRORS 404 AUGUST *****')
top = dict(Error404August.take(5))
x = 0
for i in top:
    l = list(top.values())[x]
    print('TOP:', x + 1, '- URL: ', l[0] , ' - Errors: ', list(top.keys())[x])
    x = x + 1
	

#4. Quantidade de erros 404 por dia.
#July
def check_404(l):
    try:
        if l.split(' ')[-2] == '404':
            return True
    except:
        return False

Error404JulyDay = rddJuly.filter(check_404).map(lambda x: (x.split( )[3].split('[')[1].split('/')[0], x.split( )[-2])).filter(lambda line: '404' in line).sortByKey().countByKey()
print('***** Errors 404 per Day (July) *****')
x = 0
for i in Error404JulyDay:
    print('Day:', list(Error404JulyDay.keys())[x], ' - Errors: ', list(Error404JulyDay.values())[x])
    x = x + 1

#August
Error404AugustDay = rddAugust.map(lambda x: (x.split( )[3].split('[')[1].split('/')[0], x.split( )[-2])).filter(lambda line: '404' in line).sortByKey().countByKey()

print('***** Errors 404 per Day (Agosto) *****')
x = 0
for i in Error404AugustDay:
    print('Day:', list(Error404AugustDay.keys())[x], ' - Errors: ', list(Error404AugustDay.values())[x])
    x = x + 1
	
	
#5. O total de bytes retornados.
JulyBytesTotal = rddJuly.map(lambda x: (1,x.split( )[-1])).map(lambda x : x[0]).sum()
print('Total bytes returned in July: ', JulyBytesTotal)

AugustBytesTotal = rddAugust.map(lambda x: (1,x.split( )[-1])).map(lambda x : x[0]).sum()
print('Total bytes returned in August: ', AugustBytesTotal)