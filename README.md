# TDD Project - Store API com FastAPI

Este repositório documenta o desenvolvimento de uma API REST, a `Store API`, utilizando Python, FastAPI e MongoDB. O diferencial deste projeto é a aplicação rigorosa da metodologia **TDD (Test-Driven Development)**, que guiou cada passo da implementação.

Mais do que um simples projeto, este `README` serve como um diário de bordo, detalhando não apenas os sucessos, mas também os desafios e as soluções encontradas durante o ciclo de desenvolvimento.

## 🎯 O Desafio Proposto

O objetivo inicial era desenvolver os endpoints de um CRUD (Create, Read, Update, Delete) para produtos, seguindo os princípios do TDD. Isso incluía:
- Implementar exceções customizadas para erros de inserção e busca.
- Garantir que o campo `updated_at` fosse atualizado automaticamente.
- Criar filtros de busca por faixa de preço.

## 🚀 A Jornada do Desenvolvimento: Um Guia de Solução de Problemas

O caminho para fazer todos os testes passarem foi repleto de aprendizados. Abaixo estão os principais obstáculos enfrentados e como foram superados — um guia prático para futuros desenvolvedores.

#### 1. ⚙️ Configuração do Ambiente (`poetry` e `pyenv`)
- **Problema:** O comando `poetry` não era reconhecido no terminal (`CommandNotFoundException`).
- **Causa:** O diretório de scripts do Poetry não estava na variável de ambiente `PATH` do sistema, um problema comum no Windows.
- **Solução:** Adicionar manualmente o caminho do Poetry ao `PATH` da sessão do terminal com o comando:
  ```powershell
  $env:Path += ";$env:APPDATA\Python\Scripts"
  ```

#### 2. 🦀 A Compilação do `pydantic-core` com Rust
- **Problema:** A instalação falhava com um erro ao tentar construir o pacote `pydantic-core`.
- **Causa:** `pydantic-core` usa código em Rust para otimizar a performance e precisava do compilador Rust (`cargo.exe`), que não estava instalado.
- **Solução:** Instalar o ambiente de desenvolvimento Rust através do **[rustup](https://rustup.rs/)**.

#### 3. 🐍 Incompatibilidade de Versões (Python 3.13)
- **Problema:** `TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'`.
- **Causa:** O arquivo `poetry.lock` continha uma versão do `pydantic-core` incompatível com o Python 3.13.
- **Solução:** Executar `poetry update` para forçar a busca por versões mais novas e compatíveis das dependências.

#### 4. 🔗 A Falha Final dos Testes: UUID e MongoDB
- **Problema:** `ValueError: cannot encode native uuid.UUID with UuidRepresentation.UNSPECIFIED`.
- **Causa:** O driver do MongoDB (`motor`) não sabia como serializar os objetos `UUID` do Python para o formato BSON do banco.
- **Solução:** Configurar explicitamente a representação de UUID na conexão com o banco, adicionando o parâmetro `uuidRepresentation="standard"` ao criar o `AsyncIOMotorClient`.
  ```python
  # store/db/mongo.py
  self.client: AsyncIOMotorClient = AsyncIOMotorClient(
      settings.DATABASE_URL, uuidRepresentation="standard"
  )
  ```

#### 5. 🔧 Ajustes Finais nos Testes
- **Problema:** `AssertionError` nos testes devido a mensagens de erro que mudaram após a atualização das bibliotecas.
- **Solução:** Padronizar e atualizar as mensagens de exceção esperadas nos testes para refletir as novas versões.

## ✅ Conclusão da Jornada

Após todos os ajustes, o resultado foi alcançado: **20 testes passando**, validando toda a lógica de negócio da aplicação.

```
================= 20 passed, 3 warnings in 1.05s =================
```

Esta jornada reforça as **vantagens do TDD**:
- **Segurança:** Os testes deram confiança para refatorar o código e atualizar dependências.
- **Qualidade:** Os erros foram descobertos e corrigidos de forma incremental.
- **Documentação Viva:** Os próprios testes servem como uma documentação clara do comportamento da API.

## ▶️ Como Executar o Projeto

#### 1. **📦 Preparar o Ambiente**
   - Certifique-se de ter o **Pyenv** e o **Poetry** instalados.

#### 2. **📥 Instalar as Dependências**
   - Navegue até a pasta `store_api` e execute:
     ```bash
     poetry install
     ```

#### 3. **🧪 Executar os Testes**
   - Para validar se tudo está funcionando corretamente:
     ```bash
     poetry run pytest
     ```

#### 4. **⚡ Rodar a Aplicação**
   - Para iniciar o servidor da API:
     ```bash
     poetry run uvicorn store.main:app --reload
     ```
   - Acesse a documentação interativa em **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.