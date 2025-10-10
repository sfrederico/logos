# **Lógos**

## 📌 Descrição do Projeto

**Lógos** é um projeto focado em **DevOps e automação**, utilizando **Flask, Docker, CI/CD e monitoramento** para testar e validar conceitos de **deploy, observabilidade e gerenciamento de logs**. A aplicação será implantada em produção em uma VPS de alguma cloud ainda não definida, e contará com um pipeline automatizado para testes e deploy contínuo.

## 📚 Sobre o Projeto

O nome **Lógos** vem do conceito filosófico presente na filosofia grega, especialmente em Heráclito e no estoicismo, onde representa a **razão, ordem e princípio estruturante do cosmos**. Para os gregos, Lógos é a lógica subjacente que governa a natureza, garantindo harmonia e previsibilidade. No contexto do projeto, a escolha do nome reflete a busca por um **ambiente de desenvolvimento e produção estruturado, monitorável e confiável**, onde cada componente opera de maneira integrada, garantindo estabilidade e controle no fluxo de desenvolvimento e deploy.

## 🌐 Endpoints

1. `/`

Objetivo: Renderizar o README.md como página inicial da aplicação.

2. `/health`

Objetivo: Informar o estado geral da aplicação (saúde e dependências) para scrapes do Prometheus e verificações de CI.

3. `/error`

Objetivo: Provocar um erro 500 intencional para gerar logs de exceção e testar integrações de observabilidade e alertas.

4. `/db`

Objetivo: Executar uma query simples no PostgreSQL e exibir o resultado para validar conectividade e fornecer base para métricas de latência de banco.


## 🧰 Tecnologias Utilizadas

- **Linguagem:** Python (Flask)
- **Banco de Dados:** PostgreSQL
- **Infraestrutura:** Docker, Docker Compose, VPS (a definir)
- **Servidor Web:** Nginx (com suporte a HTTPS via Let’s Encrypt)
- **CI/CD:** Gitlab CI
- **Monitoramento:** Prometheus + Grafana
- **Gerenciamento de Logs:** Graylog

## ☎️ Contato

- ✉️ E-mail: osamuelfrederico@gmail.com
- 🔗 GitLab: https://gitlab.sfrederico.dev/sfrederico/logos

