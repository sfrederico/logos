# **Lógos**

## 📌 Descrição do Projeto

**Lógos** é um projeto focado em **DevOps e automação**, construído com  **Flask, Docker, CI/CD e monitoramento**. Seu objetivo é testar e validar conceitos de deploy contínuo, observabilidade e gerenciamento de logs em um ambiente de produção controlado e totalmente automatizado.

## 📚 Sobre o Projeto

O nome **Lógos** vem do conceito filosófico presente na filosofia grega, especialmente em Heráclito e no estoicismo, onde representa a **razão, ordem e princípio estruturante do cosmos**. Para os gregos, Lógos é a lógica subjacente que governa a natureza, garantindo harmonia e previsibilidade. No contexto do projeto, a escolha do nome reflete a busca por um **ambiente de desenvolvimento e produção estruturado, monitorável e confiável**, onde cada componente opera de maneira integrada, garantindo estabilidade e controle no fluxo de desenvolvimento e deploy.


## 🔧 Arquitetura e Infraestrutura

O projeto atualmente é executado via Docker Compose, que orquestra três serviços principais:

- Flask App – aplicação web principal;
- PostgreSQL – banco de dados relacional para persistência;
- Nginx – atua como proxy reverso, oferecendo roteamento e suporte HTTPS.

## 📁 **Estrutura do Projeto**
```
Logos/
├── app/ # Aplicação Flask principal
│ └── src/
│ └── tests/
│ └── Dockerfile
│ └── entrypoint.sh
│ └── requirements.txt
│ └── ruff.toml
|
├── nginx/ # Proxy reverso
│ └── default.conf
|
├── .env-EXAMPLE # Variáveis de ambiente para configuração
|
├── .gitignore # Arquivos e pastas a serem ignorados pelo Git
|
├── .gitlab-ci.yml # Pipeline de lint/test/deploy
|
├── docker-compose.yml # Orquestração completa
|
├── README.md # Documentação do projeto
|
└── run-dev.sh # Script para rodar ambiente de desenvolvimento local
```

## 🧱 Integração Contínua (CI/CD)

O código-fonte é versionado tanto no GitHub quanto em um GitLab privado, hospedado em uma cloud sob controle próprio.
Neste ambiente privado, o projeto conta com runners dedicados, garantindo independência e controle total sobre o pipeline de CI/CD.
A pipeline já está implementada e inclui as seguintes etapas:

- Lint – verificação de estilo e qualidade de código.
- Test – execução automática de testes unitários.
- (Em breve) Deploy – entrega automatizada do ambiente Docker para a VPS de produção.


## 🌐 Endpoints

 Endpoint   | Objetivo  |
|-----------|-----------|
| `/`       | Renderiza o README.md como página inicial da aplicação. |
| `/health` | Retorna o estado geral da aplicação (usado em scrapes do Prometheus e verificações de CI). |
| `/error`  | Gera um erro 500 intencional para testar logs de exceção e alertas. |
| `/db`     | Executa uma query simples no PostgreSQL para validar conectividade e medir latência. |


## 🧰 Tecnologias Utilizadas

- **Linguagem:** Python (Flask)
- **Banco de Dados:** PostgreSQL
- **Infraestrutura:** Docker, Docker Compose, VPS (Azure)
- **Servidor Web:** Nginx (com suporte a HTTPS via Let’s Encrypt)
- **CI/CD:** Gitlab CI
- **Monitoramento:** Prometheus + Grafana (em breve)
- **Gerenciamento de Logs:** Graylog (em breve)

## ☎️ Contato

- ✉️ E-mail: osamuelfrederico@gmail.com
- 🔗 Github: https://github.com/sfrederico/logos
- 🔗 GitLab: https://gitlab.sfrederico.dev/sfrederico/logos

