# Spark with features system

> Ecossistema Apache e seus componentes (Livy e Zeppelin)

Nesse projeto será apresentado uma estrutura base para levantar um sistema (em containers ou clusters) baseado nos serviços da Apache: Spark, Livy e Zeppelin. Com os containers levantados, você poderá realizar extrações, processamentos, tudo em base do [pyspark](https://spark.apache.org/docs/latest/api/python/index.html), obtendo os benefícios de processamentos em diferentes nós.

# Conteúdos

- [1. Clonando projeto localmente](#1-clonando-projeto-localmente)
- [2. Iniciando as aplicações com Docker](#2-iniciando-as-aplicações-com-docker)
    - [2.1 Iniciando apenas o Spark com o Docker](#21-iniciando-apenas-o-spark-com-o-docker)
    - [2.2 Iniciando Spark e Apache Livy com o Docker](#22-iniciando-spark-e-apache-livy-com-o-docker)
    - [2.3 Deploy com Apache Zeppelin e Livy no Docker](#23-deploy-com-apache-zeppelin-e-livy-no-docker)
    - [2.4 Inicializando as funções utilizando spark-submit](#24-inicializando-as-funções-utilizando-spark-submit)
- [3. Comandos Úteis Docker](#3-comandos-úteis-docker)
- [Tecnologias](#tecnologias)

## 1. Clonando projeto localmente

Link do [Projeto](#).

- Clone o projeto na pasta desejada utilizando o comando

```
    git clone #
```

- Ou clone direto pelo Visual Studio Code
  - Segue o [tutorial](https://learn.microsoft.com/en-us/azure/developer/javascript/how-to/with-visual-studio-code/clone-github-repository?tabs=create-repo-command-palette%2Cinitialize-repo-activity-bar%2Ccreate-branch-command-palette%2Ccommit-changes-command-palette%2Cpush-command-palette) de como clonar direto pelo VS Code.

## 2. Iniciando as aplicações com Docker

O projeto deverá ser inicializado em um terminal do WSL (ou outro terminal), caso precise configurar o terminal, clique neste [link](https://learn.microsoft.com/pt-br/windows/wsl/install). Este terminal precisa ter acesso ao Docker, que pode ser via [Docker Desktop](https://docs.docker.com/desktop/wsl/) ou [Rancher Desktop](https://docs.rancherdesktop.io/ui/preferences/wsl/). Para o processamento, as seguintes variáveis de ambiente são necessárias:

### 2.1 Iniciando apenas o Spark com o Docker

- Vá até a raiz do projeto em um terminal e rode o seguinte comando para fazer o build da imagem do projeto

```
    docker-compose build
```

Será gerada uma imagem **ecossistema-apache**. Para o build da imagem, há o Dockerfile que basicamente usará a imagem [docker.io/bitnami/spark:3.5](https://hub.docker.com/r/bitnami/spark) como base, irá copiar o arquivo **requirements.txt** que possui as bibliotecas necessárias do python, os arquivos dentro da pasta **jars** que são os jars necessários para o pyspark acessar um banco de dados MongoDB ou Oracle.

- Após isso, precisamos rodar a imagem com o seguinte comando

```
    docker-compose up
```

Será criado um container chamado **spark-master** e **spark-worker-1**

- Se tudo estiver certo, a UI do Spark estará rodando em **http://localhost:8080** (caso queira alterar a porta, tem como alterar a relação de portas do docker-compose também). **Importante:** assim que levantar o container, no terminal irá aparecer a url exata do spark-master, assim como na UI do Spark, caso necessário.

### 2.2 Iniciando Spark e Apache Livy com o Docker

- Entre na pasta **deploy-livy** e rode o bash download_archives.sh, irá baixar os arquivos do apache-livy e o spark nas versões corretas
- Ainda na pasta **deploy-livy** rode o seguinte comando:

```
    docker build -t apache-livy-docker -f ./Dockerfile .
```

Será gerada a imagem **apache-livy-docker**, instalando o Python 3.11 e as bibliotecas necessárias em seu código Python. Além de copiar os arquivos jars necessários para conectar ao MongoDB e o Oracle.

- Rodar o seguinte comando para levantar os containers utilizando o docker compose:

```
    docker-compose up
```

- Após isso, nas URLs localhost:8080 e localhost:8998 estarão hospedadas respectivamente as UIs do Spark e do Livy.

- Pode ser enviado um comando de trigger para o processamento de batch enviando um POST para localhost:8998/batches com o seguinte body:

```JSON
    {
    "file": "/opt/main.py",
    "args": ["-f", "funcaoDesejada"]
    }
```

### 2.3 Deploy com Apache Zeppelin e Livy no Docker

- Faça o build da imagem do Livy seguindo os passos de [2.2 Iniciando Spark e Apache Livy com o Docker](#22-iniciando-spark-e-apache-livy-com-o-docker).

- Por último, para dar o deploy da aplicação com o Docker, gerando containers separados, rode o seguinte comando a partir da pasta **deploy-zeppelin** do projeto também:

```
    docker-compose up
```

- Após isso, nas URLs localhost:8080, localhost:8998 e localhost:8081 estarão hospedadas respectivamente as UIs do Spark, do Livy e do Zeppelin

- Você precisará definir a URL certa para o interpretador do Zeppelin. Em **localhost:8081**, na UI do Apache Zeppelin, no canto superior direito, clique em **"anonymous"** e em **Interpreter**.

- Procure as configurações do livy (CTRL+F e procure por livy)

- Configure **zeppelin.livy.url** para **http://livy:8998** e salve

- Após isso, você conseguirá rodar um notebook direto no livy, em uma sessão compartilhada, e consequentemente, rodando no container Spark. Abrindo um Notebook no Zeppelin no interpretador do Livy e rodando o seguinte código de teste, você terá acesso ao livy:
```python
%pyspark
import pyspark
from pyspark.sql import SparkSession
import time
import socket

sparkSession: SparkSession = SparkSession.builder 
        
sparkSession = sparkSession\
    .config("spark.mongodb.input.sampleSize", 50000) \
    .config("spark.driver.host", socket.gethostbyname(socket.gethostname()))\
    .appName("ExtratorInformacoes") \
    .enableHiveSupport() \
    .getOrCreate()

#Setting log level in spark
#sparkSession.sparkContext.setLogLevel('WARN')

init_time = time.time()


print(f"Tempo corrido: {time.time() - init_time}")
sparkSession.stop()
```

### 2.4 Inicializando as funções utilizando spark-submit

Essa instância de docker está habilitada a receber requisições de aplicações a serem rodadas via **spark-submit**, seria como uma API do Spark. É feita da seguinte forma:

- No terminal digite o seguinte padrão:

```sh
    docker exec spark-master spark-submit --master spark://spark-master:7077 --class com.mongodb.spark.sql.DefaultSource main.py -h
```

E ele retornará as funções presentes que podem ser inicializadas e os segmentos que as funções podem ser destinadas. Mas abaixo segue a explicação de cada uma das funções

# 3. Comandos Úteis Docker

Segue abaixo alguns comandos que podem ser utilizados no Docker.

```sh
  docker images  -  Lista as Imagens criadas.
  docker ps  -  Lista os Containers criados.
  docker volume ls  -  Lista os Volumes criados.
  docker container inspect <container name>  -  Inspeciona as configurações de Container.
  docker kill <container name>  -  Da Poweroff no Container.
  docker rm  <container name>  -  Remove o Container.
  docker rmi <image name>  -  Remove a Imagem.
  docker stop <container name>  -  Para um Container que esteja rodando.
  docker start <container name>  -  Inicia um Container que esteja parado.
  docker rm $(docker ps -a -f status=exited -q) - Exclui containers que estão parados
  docker cp -L ./spark/src/teste.py spark-master:/opt/bitnami/teste.py - Copiar arquivo do computador para dentro do container
```

# Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

- [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)
- [Rancher Desktop](https://docs.rancherdesktop.io/getting-started/installation)
- [MongoDB](https://www.mongodb.com/docs/manual/installation/)
- [Apache Spark](https://spark.apache.org/docs/latest/api/python/index.html)
- [Apache Livy](https://livy.apache.org/)
- [Kubernetes](https://kubernetes.io/pt-br/)
