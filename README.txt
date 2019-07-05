##Qual ​o ​objetivo do ​comando ​​cache em Spark? 
O comando cache permite a reutilização de algumas tarefas executadas pelo Spark, por exemplo:
	* Cálculos de RDD com alto custo podem ter o tempo de recuperação reduzido utilizando cache no caso de algum executor falhar.
	* Reutilização de RDDs em aplicativos independentes do Spark.
	* Reutilização de códigos iterativos como no caso de Machine Learning que reutilizam um RDD várias vezes.
Armazenar todos os RDDs gerados em cache pode não ser uma boa estratégia, pois os blocos úteis em cache podem ser despejados bem antes de 
serem reutilizados. Para estes casos, é necessário tempo de computação adicional para reavaliar os blocos RDD despejados do cache.


##O ​mesmo ​código implementado em ​Spark ​é ​normalmente mais rápido que a implementação equivalente em MapReduce. Por ​quê?
Em cada passo de um job MapReduce os dados são gravados em disco, para a execução do próximo passo do job é necessário iniciar uma nova instância
do JVM e fazer leitura destes dados, com isso, aumenta-se a necessidade de leitura e escrita em disco. 
Já no Apache Spark em cada passo do job os dados trafegam em memória, este processo, além de ser de 10x (em disco) até 100x (em memória) mais rápido, 
nos possibilita também fazer o uso do caching de dados em memória.


##Qual ​é ​a ​função ​do ​​SparkContext​?
Um aplicativo Spark deve conter um SparkContext para ser um aplicativo Spark, ele praticamente é o coração da aplicação, é responsável por configurar os 
serviços internos, realizar a alocação de recursos como processador e memória e estabelecer uma conexão com um ambiente de execução do Spark, ele também 
é utilizado para criar RDDs, acumuladores, variáveis e executar jobs.


##Explique ​com ​suas ​palavras ​​​o ​que ​é ​​Resilient ​Distributed ​Datasets​ (RDD).
RDD é uma representação de um conjunto de dados do Spark, dados estes que podem estar distribuídos (Distributed*) em várias máquinas e podem ter como origem 
as mais váriadas fontes de dados, eles são tolerantes a falhas (Resilient*), ou seja, caso uma partição de um RDD for perdida, ele poderá recompila ela
recuperando os dados perdidos de forma rápida, também são imutáveis, ou seja, apenas criando um novo RDD a partir de uma transformação que é possível 
alterá-lo.


##GroupByKey ​​é ​menos ​eficiente ​que ​​reduceByKey ​​em ​grandes ​dataset. ​Por ​quê? 
Isso ocorre porque a função reduceByKey, utilizando uma função lamdba, combina todos os pares de (chave, valor) antes de passar estes para os executores que 
irão realizar a agregação final, isso produz um desempenho muito melhor pois a quantidade de dados que irá trafegar pela rede será muito menor. Por outro
lado, a função groupByKey é utilizada apenas para agrupar seu conjunto de dados com base em uma chave, todos os pares de valores-chave são processados, 
sendo assim, muitos dados desnecessários são transferidos pela rede, no qual, dependendo do volume, pode exceder a quantidade de memória disponível para 
execução, sendo necessário a utilização de cache em disco que ocasionará em uma queda considerável na perfomance.


##Explique ​o ​que ​o ​código ​Scala ​abaixo ​faz.
val​ ​​textFile​ ​​=​ ​​sc​.​textFile​(​"hdfs://..."​)
val​ ​​counts​ ​​=​ ​​textFile​.​flatMap​(​line​ ​​=>​ ​​line​.​split​(​" ​"​))
 		.​map​(​word​ ​​=>​ ​​(​word​,​ ​​1​))
​ 		.​reduceByKey​(​_​ ​​+​ ​​_​) 
counts​.​saveAsTextFile​(​"hdfs://..."​) 
 
No código acima um arquivo de texto é lido do HDFS, em seguida são realizadas algumas transformações para criar um conjunto de dados de pares (Chave, Valor) 
chamados counts e, em seguida, o mesmo é salvo em um arquivo no hdfs.

Linha 1: val​ ​​textFile​ ​​=​ ​​sc​.​textFile​(​"hdfs://..."​) 
Nesta linha o código escala faz a leitura de um arquivo de texto que está no Sistema de Arquivos HDFS e atribui o seu valor em uma variável imutável 
chamada textFile.

Linha 2: val​ ​​counts​ ​​=​ ​​textFile​.​flatMap​(​line​ ​​=>​ ​​line​.​split​(​" ​"​))
Nesta linha a função flatMap está transformando o RDD de linhas em um novo RDD de palavras utilizando uma função (split) que retorna vários elementos 
para este novo RDD.

Linha 3:.​map​(​word​ ​​=>​ ​​(​word​,​ ​​1​))
Nesta linha a função map está realizando um mapeamento de (chave, valor) com cada palavra, transformando o RDD de palavras em um RDD de tuplas, onde valor 
é igual a 1 e a chave é cada palavra.

Linha 4:.​reduceByKey​(​_​ ​​+​ ​​_​)
Nesta linha esta sendo executada a função reduceByKey que faz a agregação por chave somando o campo valor.

Linha 5:counts​.​saveAsTextFile​(​"hdfs://..."​) 
Nesta linha o RDD salva no HDFS o arquivo de texto de contagem das palavras.