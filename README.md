# AgileFlow — Gestão e acompanhamento de demandas de TI

## 1. Apresentação do projeto

O AgileFlow é um projeto acadêmico de desenvolvimento de software que propõe uma aplicação web para registrar, consultar e acompanhar demandas de Tecnologia da Informação (TI). A proposta surgiu da necessidade de organizar informações relacionadas às solicitações de serviços e às atividades de suporte e desenvolvimento, permitindo que seus registros sejam consultados e acompanhados de maneira mais clara.

Em ambientes nos quais as solicitações são registradas por diferentes meios, como mensagens, anotações ou planilhas, pode haver dificuldade para localizar informações, identificar a situação de cada demanda e acompanhar as atualizações realizadas ao longo do atendimento. A falta de organização também pode dificultar a comunicação entre as pessoas envolvidas e o acompanhamento das atividades pendentes.

Diante desse cenário, o AgileFlow propõe centralizar as informações essenciais de cada demanda em uma aplicação web simples, com funcionalidades direcionadas às necessidades identificadas. O sistema está sendo desenvolvido como um Produto Mínimo Viável (MVP), priorizando os recursos fundamentais antes da inclusão de funcionalidades mais complexas.

## 2. Objetivo geral

Desenvolver uma aplicação web que permita registrar, consultar e acompanhar demandas de TI, mantendo suas informações organizadas e possibilitando o acompanhamento de seu status e de suas atualizações.

### Objetivos específicos

- Disponibilizar um formulário para registrar demandas com título e descrição.
- Permitir a consulta das demandas cadastradas e de seus respectivos status.
- Possibilitar a atualização do status de uma demanda durante seu acompanhamento.
- Registrar comentários relacionados ao andamento das demandas.
- Aplicar testes automatizados para verificar o comportamento das funcionalidades implementadas.
- Utilizar o controle de versão e a integração contínua para organizar as alterações e acompanhar a qualidade do código.

## 3. Público-alvo

O público-alvo previsto compreende equipes de suporte técnico, profissionais de TI e pequenos grupos de trabalho que necessitam registrar solicitações e acompanhar atividades de maneira organizada.

A proposta também considera pessoas responsáveis por solicitar serviços e acompanhar seu andamento. Para o MVP, o foco está na organização e no acompanhamento das informações essenciais, sem pressupor a implementação de recursos avançados de gestão, notificações ou controle de acesso por diferentes perfis.

## 4. Funcionalidades do MVP

O escopo funcional do AgileFlow está organizado em torno do ciclo básico de uma demanda.

- **Cadastro de demandas:** registro do título e da descrição, com validação dos campos obrigatórios.
- **Consulta de demandas:** apresentação das demandas cadastradas, incluindo descrição e status.
- **Atualização de status:** alteração da situação de uma demanda para Aberta, Em andamento ou Concluída.
- **Registro de atualizações:** inclusão de comentários associados a uma demanda, com registro da data.
- **Validação de dados:** verificação de campos obrigatórios e rejeição de valores inválidos em operações previstas pelo sistema.

Essas funcionalidades constituem o núcleo do MVP. Sua implementação e validação devem ser acompanhadas por testes e verificações de funcionamento, considerando também a necessidade de configuração do banco de dados para a execução integrada da aplicação.

## 5. Tecnologias e ferramentas

### Python 3.12

É a linguagem principal prevista para o desenvolvimento da aplicação. Sua utilização permite organizar as regras de negócio, tratar os dados recebidos e implementar as operações necessárias ao funcionamento do sistema.

### Flask

É o framework utilizado para estruturar a aplicação web e definir as rotas responsáveis por receber as solicitações, executar as operações correspondentes e devolver as respostas ao usuário.

### PostgreSQL

É o sistema de gerenciamento de banco de dados previsto para armazenar as demandas e suas atualizações de forma persistente. O código utiliza a biblioteca Psycopg para estabelecer a comunicação com o banco. A conexão depende da disponibilidade de uma instância PostgreSQL e da configuração da variável de ambiente `DATABASE_URL`.

### pytest

É utilizado na criação e execução de testes automatizados. Os testes verificam respostas das rotas, apresentação de páginas e validações de determinadas operações, contribuindo para identificar falhas durante o desenvolvimento.

### Git e GitHub

São utilizados para o controle de versão e a hospedagem do código-fonte. O trabalho com branches e Pull Requests permite organizar mudanças, revisar alterações e manter um histórico das decisões de desenvolvimento.

### GitHub Actions

É utilizado para automatizar a execução dos testes em eventos configurados no repositório. Essa prática permite verificar se as alterações atendem aos testes automatizados antes de serem integradas à branch principal.

## 6. Organização e práticas de desenvolvimento

O projeto utiliza uma estrutura modular para separar responsabilidades. O diretório `aplicacao` reúne os componentes da aplicação, incluindo a definição das rotas, a criação da aplicação Flask e as funções relacionadas à comunicação com o banco de dados. O diretório `testes` reúne os testes automatizados, enquanto o diretório `.github/workflows` contém a configuração do fluxo de integração contínua.

O desenvolvimento utiliza branches para implementar alterações de forma isolada e Pull Requests para apresentar e integrar mudanças à branch principal após a verificação das condições estabelecidas para o projeto.

Essa organização contribui para a rastreabilidade das alterações, facilita a identificação de problemas e permite acompanhar a evolução do software ao longo de seu ciclo de desenvolvimento.

## 7. Qualidade, segurança e validação

A qualidade do AgileFlow é considerada desde a implementação das funcionalidades. Os testes automatizados ajudam a verificar comportamentos esperados e a rejeição de entradas inválidas. Nas operações de banco de dados, o uso de parâmetros nas consultas contribui para reduzir riscos associados à injeção de SQL. O tratamento das informações exibidas também deve impedir que conteúdo fornecido pelo usuário seja interpretado indevidamente como código HTML.

A conexão com o banco de dados utiliza uma variável de ambiente para evitar que a configuração de acesso seja inserida diretamente no código-fonte. A execução completa das operações que dependem de persistência exige, entretanto, que o banco esteja disponível e corretamente configurado.

Além dos testes técnicos, a validação com pessoas representativas do público-alvo é uma etapa importante para verificar se as funcionalidades atendem às necessidades identificadas. Essa avaliação deve considerar a facilidade de uso, a clareza das informações e a capacidade de realizar as tarefas propostas. Os resultados e as melhorias decorrentes da validação devem ser registrados como evidências do processo de desenvolvimento.

## 8. Situação atual e evolução do projeto

O AgileFlow está em desenvolvimento incremental. O repositório contém a estrutura da aplicação Flask, rotas para as funcionalidades centrais, código de integração com PostgreSQL, testes automatizados e um fluxo de integração contínua configurado no GitHub Actions.

As funcionalidades foram organizadas em alterações versionadas e integradas por Pull Requests. A execução efetiva das operações que dependem do PostgreSQL ainda requer a configuração de um banco disponível e da variável `DATABASE_URL`.

As próximas verificações devem considerar a execução integrada da aplicação, a cobertura dos testes, a validação com o público-alvo e o registro das evidências exigidas pela atividade acadêmica. A documentação será atualizada conforme os resultados forem obtidos, mantendo a distinção entre recursos implementados, recursos efetivamente verificados e etapas ainda pendentes.

## 9. Considerações finais

O AgileFlow busca demonstrar como um problema de organização e acompanhamento de demandas pode ser transformado em uma solução de software de escopo controlado. O desenvolvimento do MVP permite aplicar conceitos de programação web, persistência de dados, testes automatizados, controle de versão e integração contínua em um contexto prático.

Mais do que implementar funcionalidades isoladas, o projeto procura estabelecer um processo de desenvolvimento organizado, no qual as alterações possam ser acompanhadas, verificadas e aprimoradas. A avaliação do resultado depende tanto do funcionamento técnico da aplicação quanto da capacidade de atender às necessidades do público para o qual foi proposta.

## 10. Repositório

Código-fonte: https://github.com/crismoraes-ads/AgileFlow
