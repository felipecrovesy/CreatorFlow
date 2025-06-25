<div align="center">
  <h1 align="center">CreatorFlow</h1>

   <div align="left">
    Trata-se de um ecossistema completo de aplicações que vão do backend ao frontend, integrando tecnologias como Python, C#, Node.js e Vue.js.
     
A arquitetura inclui um sistema de filas com RabbitMQ e persistência de dados em MongoDB. A aplicação em Python atua como fornecedora de dados, populando um banco de dados que é consumido por uma aplicação em .NET.

Essa aplicação em .NET, por sua vez, atua como produtora de mensagens, publicando-as em uma fila RabbitMQ. Um consumidor desenvolvido em Node.js consome essas mensagens, processa os dados e os armazena.

Por fim, essa aplicação em Node expõe dois endpoints que são consumidos por uma interface frontend construída em Vue.js, responsável por exibir os dados de forma organizada e interativa.

<img width="3008" alt="Untitled" src="https://github.com/user-attachments/assets/171ab2f3-e71e-4599-91f3-b5015df6de47" />
    </div>
</div>

## 📋 <a name="table">Sumary</a>

1. ⚙️ [Tech Stack](#tech-stack)
2. 🤖 [Como usar](#quick-start)
3. 🤝 [Contribuições](#contributing)
4. 👥 [Autores](#authors)
<br>

## <a name="tech-stack">⚙️ Tech Stack</a>

- Python 3.11
- Dotnet 9.0 (C#)
- Node.js 20
- Vue 3 (Composition API) com Vite e Element Plus
- MongoDb
- RabbitMq
  
<br>

## <a name="quick-start">🤖 Como usar</a>

Para iniciar o projeto, siga os seguintes passos em seu dispositivo:

**00 - Pré-requisitos**

Para usar este projeto você deve ter instalado previamente os seguintes pacotes:

- [dotnet 9.0](https://dotnet.microsoft.com/pt-br/download/dotnet/9.0)
- [python 3.0](https://www.python.org/downloads/release/python-3110/)
- [node 20](https://nodejs.org/pt/blog/release/v20.9.0)
- Docker
  <br/><br/>

**01 - Rodar os projetos**

Após clonar o repositório, abra o terminal e execute o comando abaixo: 

```bash
docker compose up --build -d
```
<br>

**02 - Ingestão dos Dados**

Acesse o [Flasgger](http://localhost:5000/apidocs/#/Creators/post_creators) da aplicação em Python ou via postman usando o curl abaixo:

Valores aceitos para o size:

- small = 500 registros
- medium = 5.000 registros
- large = 10.000 registros

```bash
curl -X POST "http://localhost:5000/creators" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"size\": \"small\"}"
```

obs: Caso opte por colocar diversos registros e sinta lentidão nas consultas,no Flasgger tem um endpoint que configura indexes para facilitar a consulta no banco de dados.
<br>

**03 - Visualização dos Dados**

Acesse o frontend pelo caminho http://localhost:5173/ para visualização dos dados

<br>

**Extra - Endpoints utilizados pelo frontend**
Também é possível visualizar os dados diretamente pelos endpoints da aplicação Node.js. Com os serviços em execução, acesse os links abaixo no navegador:

- Aba Content Type Resume: http://localhost:3000/content-type-resume
- Aba All Creators: http://localhost:3000/all-creators

## <a name="authors">👥 Autores</a>

<table style="border-collapse: collapse; table-layout: auto; text-align: left;">

  <tbody>
    <tr>
      <td style="padding: 10px; border: 1px solid #ddd;">
        <img src="https://avatars.githubusercontent.com/u/60819196?v=4" width="60" style="border-radius: 50%; display: block; margin: 0 auto;">
      </td>
      <td style="padding: 10px; border: 1px solid #ddd;">Felipe Crovesy</td>
      <td style="padding: 10px; border: 1px solid #ddd;">
        <a href="https://www.linkedin.com/in/felipe-crovesy-6a299283/" target="_blank">LinkedIn</a> |
        <a href="https://github.com/felipecrovesy" target="_blank">GitHub</a>
      </td>
    </tr>
  </tbody>
</table>
