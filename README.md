# Ranking de Nomes do IBGE 📊
Bem-vindo ao projeto Ranking de Nomes do IBGE! Este projeto marca um marco importante na minha jornada de desenvolvimento, onde aplico pela primeira vez, de forma documentada e estruturada, conhecimentos fundamentais em boas práticas, DDD (Domain-Driven Design), testes unitários e princípios de clean code.

Com ele, é possível interagir com a API do IBGE para consultar a frequência e popularidade de nomes no Brasil. Os dados coletados são exibidos diretamente no terminal e também armazenados em um banco de dados PostgreSQL, proporcionando uma base sólida para análises futuras e garantindo a consistência por meio de uma restrição de unicidade que evita duplicações.

O projeto foi estruturado e documentado com foco em organização e clareza, refletindo as boas práticas aprendidas e aplicadas ao longo do desenvolvimento.
## Descrição
Esta aplicação consulta a API do IBGE para obter dados sobre a popularidade de nomes no Brasil. Você pode especificar nomes, localidades, sexo e décadas para personalizar as consultas. Se forem fornecidos nomes, o programa utiliza a API nomes do IBGE com os nomes concatenados; caso contrário, utiliza a API ranking, que retorna os 20 nomes mais populares de acordo com os parâmetros fornecidos. Se nenhum parâmetro for fornecido, retorna o top 20 geral.

## Estrutura do Projeto
- main.py: Ponto de entrada da aplicação.
- IBGE.py: Classe para interagir com a API do IBGE.
- Item.py: Classe que representa cada item (nome) obtido.
- Ranking.py: Classe para gerenciar e exibir o ranking.
- Postgre.py: Classe para interagir com o banco de dados PostgreSQL.
- credenciais.py: Arquivo com as credenciais do banco de dados.
- requirements.txt: Lista de dependências do projeto.
- README.md: Este arquivo.
- tests/: Pasta contendo testes unitários para as funções do projeto.


## Pré-requisitos
- Python 3.6 ou superior
- PostgreSQL instalado e em execução
- Credenciais de acesso ao banco de dados PostgreSQL

## Instalação
Clone o repositório:

- Clone o repositório:
  ```bash
  git clone https://https://github.com/vinilopesc/IBGE.git
  cd ranking-nomes-ibge
  ```
- Crie um ambiente virtual (opcional, mas recomendado):
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # No Windows: venv\Scripts\activate
  ```
- Instale as dependências:
  ```bash
  pip install -r requirements.txt
  ```
- Crie um arquivo chamado credenciais.py na raiz do projeto com o seguinte conteúdo:
  ```
  host = 'seu_host'
  port = 5432
  database = 'seu_banco_de_dados'
  user = 'seu_usuario'
  password = 'sua_senha'
  # Substitua 'seu_host', 'seu_banco_de_dados', 'seu_usuario' e 'sua_senha' pelas suas credenciais do PostgreSQL.
  ```
## Como Usar
Para executar o programa, utilize o seguinte comando no terminal:

  ```bash
python main.py --nomes nome1 nome2 --local UF --sexo M/F/- --decada ano
  ```
### Parâmetros disponíveis:

- --nomes: Lista de nomes para gerar o ranking (opcional).
- --local: Sigla da unidade federativa (por exemplo, SP, RJ) ou BR para Brasil (opcional).
- --sexo: Sexo para filtrar os nomes (M, F ou - para ambos) (opcional).
- --decada: Década para filtrar os nomes (formato YYYY, por exemplo, 1990) (opcional).
Exemplo:

  ```bash
  python main.py --nomes João Maria --local SP RJ --sexo F --decada 1980 1990
  ```
  Este comando irá buscar os nomes "João" e "Maria" nos estados de São Paulo e Rio de Janeiro, sexo feminino, nas décadas de 1980 e 1990.
  ```markdown    
  Nome           Localidade     Sexo           Década         Frequência
  ----------------------------------------------------------------------
  MARIA             35            F            1980            105247
  MARIA             35            F            1990            48185
  MARIA             33            F            1980            27944
  MARIA             33            F            1990            17632
  JOAO              35            F            1990            423
  JOAO              35            F            1980            223
  JOAO              33            F            1990            182
  JOAO              33            F            1980            85
  ```

### Exemplo de Saída
Ao executar o programa sem nenhum parâmetro:

  ```bash
  python main.py
  ```
A saída será semelhante a:

  ```markdown
Nome           Localidade     Sexo           Década         Frequência
----------------------------------------------------------------------
MARIA          BR             -              Geral          11734129
JOSE           BR             -              Geral          5754529
ANA            BR             -              Geral          3089858
JOAO           BR             -              Geral          2984119
ANTONIO        BR             -              Geral          2576348
FRANCISCO      BR             -              Geral          1772197
CARLOS         BR             -              Geral          1489191
PAULO          BR             -              Geral          1423262
PEDRO          BR             -              Geral          1219605
LUCAS          BR             -              Geral          1127310
LUIZ           BR             -              Geral          1107792
MARCOS         BR             -              Geral          1106165
LUIS           BR             -              Geral          935905
GABRIEL        BR             -              Geral          932449
RAFAEL         BR             -              Geral          821638
FRANCISCA      BR             -              Geral          725642
DANIEL         BR             -              Geral          711338
MARCELO        BR             -              Geral          693215
BRUNO          BR             -              Geral          668217
EDUARDO        BR             -              Geral          632664
  ```
### Testes
- O projeto inclui testes unitários para todas as funções, localizados na pasta tests. Para executar os testes, utilize:

  ```bash
  python -m unittest discover tests
  ```
  
## Referências
[- API do IBGE - Nomes: Documentação da API
](https://servicodados.ibge.gov.br/api/docs/nomes?versao=2)

## Observações

- Se nenhum nome for fornecido, o programa retornará os nomes mais populares com base nos outros parâmetros.
- Os dados coletados são armazenados no banco de dados PostgreSQL configurado, evitando duplicatas.
Certifique-se de que o banco de dados PostgreSQL está em execução e as credenciais estão corretas.
