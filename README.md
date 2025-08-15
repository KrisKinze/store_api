# TDD Project - Store API com FastAPI

Este repositório documenta o desenvolvimento de uma API REST, a `Store API`, utilizando Python, FastAPI e MongoDB. O diferencial deste projeto é a aplicação rigorosa da metodologia **TDD (Test-Driven Development)**, que guiou cada passo da implementação.

Mais do que um simples projeto, este `README` serve como um diário de bordo, detalhando não apenas os sucessos, mas também os desafios e as soluções encontradas durante o ciclo de desenvolvimento.

## O Desafio Proposto

O objetivo inicial era desenvolver os endpoints de um CRUD (Create, Read, Update, Delete) para produtos, seguindo os princípios do TDD. Isso incluía:
- Implementar exceções customizadas para erros de inserção e busca.
- Garantir que o campo `updated_at` fosse atualizado automaticamente.
- Criar filtros de busca por faixa de preço.

## A Jornada do Desenvolvimento: Um Guia de Solução de Problemas

O caminho para fazer todos os testes passarem foi repleto de aprendizados. Abaixo estão os principais obstáculos enfrentados e como foram superados — um guia prático para futuros desenvolvedores.

### 1. Configuração do Ambiente (`poetry` e `pyenv`)

O primeiro desafio surgiu na configuração do ambiente.

- **Problema:** O comando `poetry` não era reconhecido no terminal (`CommandNotFoundException`).
- **Causa:** O diretório de scripts do Poetry não estava na variável de ambiente `PATH` do sistema, um problema comum no Windows, especialmente ao alternar entre versões do Python com `pyenv`.
- **Solução:** Adicionar manualmente o caminho do Poetry ao `PATH` da sessão do terminal com o comando:
  ```powershell
  $env:Path += ";$env:APPDATA\Python\Scripts"
  ```

### 2. A Compilação do `pydantic-core`

Com o Poetry funcionando, a instalação das dependências apresentou um novo obstáculo.

- **Problema:** A instalação falhava com um erro de `FileNotFoundError` ao tentar construir o pacote `pydantic-core`.
- **Causa:** `pydantic-core` usa código em Rust para otimizar a performance. O instalador (pip/poetry) precisava do compilador Rust (`cargo.exe`), que não estava instalado no sistema.
- **Solução:** Instalar o ambiente de desenvolvimento Rust através do **[rustup](https://rustup.rs/)**. Após a instalação e o reinício do terminal, o Poetry conseguiu compilar e instalar a dependência com sucesso.

### 3. Incompatibilidade de Versões (Python 3.13)

Mesmo com o Rust instalado, um novo erro de compilação surgiu.

- **Problema:** `TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'`.
- **Causa:** O arquivo `poetry.lock` continha uma versão do `pydantic-core` que era incompatível com a versão mais recente do Python (3.13) utilizada no ambiente. A API interna do Python havia mudado.
- **Solução:** Executar o comando `poetry update`. Isso forçou o Poetry a resolver novamente as dependências, encontrar versões mais novas e compatíveis com o Python 3.13 e atualizar o `poetry.lock`.

### 4. A Falha Final dos Testes: UUID e MongoDB

Com o ambiente finalmente configurado, os testes começaram a rodar, mas falharam em massa.

- **Problema:** Quase todos os testes que interagiam com o banco de dados falhavam com o erro `ValueError: cannot encode native uuid.UUID with UuidRepresentation.UNSPECIFIED`.
- **Causa:** O driver do MongoDB (`motor`) não sabia como serializar os objetos `UUID` do Python para o formato BSON do banco. Por segurança, ele se recusa a "adivinhar" o formato correto.
- **Solução:** Configurar explicitamente a representação de UUID na conexão com o banco de dados. A correção foi feita em `store/db/mongo.py`, adicionando o parâmetro `uuidRepresentation="standard"` ao criar o `AsyncIOMotorClient`.

```python
# store/db/mongo.py
self.client: AsyncIOMotorClient = AsyncIOMotorClient(
    settings.DATABASE_URL, uuidRepresentation="standard"
)
```

### 5. Ajustes Finais nos Testes

Com o erro do UUID resolvido, restaram apenas algumas falhas pontuais.

- **Problema 1:** `AssertionError` em um teste de schema. A URL de erro do Pydantic havia mudado de `.../2.5/v/missing` para `.../2.11/v/missing`.
- **Solução 1:** Atualizar o valor esperado no teste para refletir a nova versão do Pydantic.

- **Problema 2:** `AssertionError` nos testes de `update`. A mensagem de erro para "produto não encontrado" era inconsistente entre os métodos (`Product not found with id:` vs. `Product not found with filter:`).
- **Solução 2:** Padronizar a mensagem de exceção em todos os métodos para garantir a consistência esperada pelos testes.

## Conclusão da Jornada

Após todos os ajustes, o resultado foi alcançado: **20 testes passando**, validando toda a lógica de negócio da aplicação.

```
================= 20 passed, 51 warnings in 0.99s =================
```

Esta jornada reforça as **vantagens do TDD**:
- **Segurança:** Os testes nos deram a confiança para refatorar o código e atualizar dependências, sabendo que a lógica principal estaria protegida.
- **Qualidade:** Os erros foram descobertos e corrigidos de forma incremental e controlada.
- **Documentação Viva:** Os próprios testes servem como uma documentação clara de como a API deve se comportar.

## Como Executar o Projeto

### 1. Preparar o Ambiente
Certifique-se de ter o **Pyenv** e o **Poetry** instalados.

### 2. Instalar as Dependências
Navegue até a pasta `store_api` e execute:
```bash
poetry install
```

### 3. Executar os Testes
Para validar se tudo está funcionando corretamente:
```bash
poetry run pytest
```

### 4. Rodar a Aplicação
Para iniciar o servidor da API:
```bash
poetry run uvicorn store.main:app --reload
```
Acesse a documentação interativa em **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.
```# TDD Project - Store API com FastAPI

Este repositório documenta o desenvolvimento de uma API REST, a `Store API`, utilizando Python, FastAPI e MongoDB. O diferencial deste projeto é a aplicação rigorosa da metodologia **TDD (Test-Driven Development)**, que guiou cada passo da implementação.

Mais do que um simples projeto, este `README` serve como um diário de bordo, detalhando não apenas os sucessos, mas também os desafios e as soluções encontradas durante o ciclo de desenvolvimento.

## O Desafio Proposto

O objetivo inicial era desenvolver os endpoints de um CRUD (Create, Read, Update, Delete) para produtos, seguindo os princípios do TDD. Isso incluía:
- Implementar exceções customizadas para erros de inserção e busca.
- Garantir que o campo `updated_at` fosse atualizado automaticamente.
- Criar filtros de busca por faixa de preço.

## A Jornada do Desenvolvimento: Um Guia de Solução de Problemas

O caminho para fazer todos os testes passarem foi repleto de aprendizados. Abaixo estão os principais obstáculos enfrentados e como foram superados — um guia prático para futuros desenvolvedores.

### 1. Configuração do Ambiente (`poetry` e `pyenv`)

O primeiro desafio surgiu na configuração do ambiente.

- **Problema:** O comando `poetry` não era reconhecido no terminal (`CommandNotFoundException`).
- **Causa:** O diretório de scripts do Poetry não estava na variável de ambiente `PATH` do sistema, um problema comum no Windows, especialmente ao alternar entre versões do Python com `pyenv`.
- **Solução:** Adicionar manualmente o caminho do Poetry ao `PATH` da sessão do terminal com o comando:
  ```powershell
  $env:Path += ";$env:APPDATA\Python\Scripts"
  ```

### 2. A Compilação do `pydantic-core`

Com o Poetry funcionando, a instalação das dependências apresentou um novo obstáculo.

- **Problema:** A instalação falhava com um erro de `FileNotFoundError` ao tentar construir o pacote `pydantic-core`.
- **Causa:** `pydantic-core` usa código em Rust para otimizar a performance. O instalador (pip/poetry) precisava do compilador Rust (`cargo.exe`), que não estava instalado no sistema.
- **Solução:** Instalar o ambiente de desenvolvimento Rust através do **[rustup](https://rustup.rs/)**. Após a instalação e o reinício do terminal, o Poetry conseguiu compilar e instalar a dependência com sucesso.

### 3. Incompatibilidade de Versões (Python 3.13)

Mesmo com o Rust instalado, um novo erro de compilação surgiu.

- **Problema:** `TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'`.
- **Causa:** O arquivo `poetry.lock` continha uma versão do `pydantic-core` que era incompatível com a versão mais recente do Python (3.13) utilizada no ambiente. A API interna do Python havia mudado.
- **Solução:** Executar o comando `poetry update`. Isso forçou o Poetry a resolver novamente as dependências, encontrar versões mais novas e compatíveis com o Python 3.13 e atualizar o `poetry.lock`.

### 4. A Falha Final dos Testes: UUID e MongoDB

Com o ambiente finalmente configurado, os testes começaram a rodar, mas falharam em massa.

- **Problema:** Quase todos os testes que interagiam com o banco de dados falhavam com o erro `ValueError: cannot encode native uuid.UUID with UuidRepresentation.UNSPECIFIED`.
- **Causa:** O driver do MongoDB (`motor`) não sabia como serializar os objetos `UUID` do Python para o formato BSON do banco. Por segurança, ele se recusa a "adivinhar" o formato correto.
- **Solução:** Configurar explicitamente a representação de UUID na conexão com o banco de dados. A correção foi feita em `store/db/mongo.py`, adicionando o parâmetro `uuidRepresentation="standard"` ao criar o `AsyncIOMotorClient`.

```python
# store/db/mongo.py
self.client: AsyncIOMotorClient = AsyncIOMotorClient(
    settings.DATABASE_URL, uuidRepresentation="standard"
)
```

### 5. Ajustes Finais nos Testes

Com o erro do UUID resolvido, restaram apenas algumas falhas pontuais.

- **Problema 1:** `AssertionError` em um teste de schema. A URL de erro do Pydantic havia mudado de `.../2.5/v/missing` para `.../2.11/v/missing`.
- **Solução 1:** Atualizar o valor esperado no teste para refletir a nova versão do Pydantic.

- **Problema 2:** `AssertionError` nos testes de `update`. A mensagem de erro para "produto não encontrado" era inconsistente entre os métodos (`Product not found with id:` vs. `Product not found with filter:`).
- **Solução 2:** Padronizar a mensagem de exceção em todos os métodos para garantir a consistência esperada pelos testes.

## Conclusão da Jornada

Após todos os ajustes, o resultado foi alcançado: **20 testes passando**, validando toda a lógica de negócio da aplicação.

```
================= 20 passed, 51 warnings in 0.99s =================
```

Esta jornada reforça as **vantagens do TDD**:
- **Segurança:** Os testes nos deram a confiança para refatorar o código e atualizar dependências, sabendo que a lógica principal estaria protegida.
- **Qualidade:** Os erros foram descobertos e corrigidos de forma incremental e controlada.
- **Documentação Viva:** Os próprios testes servem como uma documentação clara de como a API deve se comportar.

## Como Executar o Projeto

### 1. Preparar o Ambiente
Certifique-se de ter o **Pyenv** e o **Poetry** instalados.

### 2. Instalar as Dependências
Navegue até a pasta `store_api` e execute:
```bash
poetry install
```

### 3. Executar os Testes
Para validar se tudo está funcionando corretamente:
```bash
poetry run pytest
```

### 4. Rodar a Aplicação
Para iniciar o servidor da API:
```bash
poetry run uvicorn store.main:app --reload
```
Acesse a documentação