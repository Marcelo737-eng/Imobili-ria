# Análise cadastral e de crédito para locação — análise do projeto e plano

Documento escrito **antes** de programar, conforme pedido. Ele responde aos 15 pontos de
diagnóstico do item 21 e propõe o plano de implementação.

---

## 1. Diagnóstico do que já existe

### 1.1 Tecnologias

| Camada | O que é usado |
|---|---|
| Backend | Python 3.9+ apenas com a biblioteca padrão (`http.server`, `sqlite3`, `hashlib`, `zlib`) |
| Banco | SQLite, arquivo único em `dados/imobiliaria.db` |
| Frontend | SPA em JavaScript puro (módulos ES), sem framework nem build |
| PDF | Gerador próprio (`app/pdf.py`) — sem ReportLab |
| Dependências externas | **nenhuma** |

Isso é uma restrição real do ambiente: `pip` e `npm` não funcionam aqui. Toda solução
precisa caber na biblioteca padrão — o que afeta diretamente as decisões sobre OCR,
criptografia e consulta a bureaus (seções 4 e 5).

### 1.2 Banco de dados: 51 tabelas

Grupos existentes: cadastros (`clientes`, `imoveis`, `corretores`, `usuarios`), captação,
negociação (`negociacoes`, `negociacao_partes`, `pagamento_condicoes`,
`pagamento_parcelas`), contratos (`contratos`, `contrato_partes`, `contrato_versoes`,
`contrato_assinaturas`), locação (`locacoes`, `locacao_reajustes`), vistoria
(`vistorias`, `vistoria_ambientes`, `vistoria_itens`, `vistoria_fotos`,
`vistoria_comparacoes`), financeiro (`lancamentos`, `comissoes`, `comissao_rateio`),
rotina (`compromissos`, `tarefas`, `checklist_documentos`), apoio (`documentos`, `fotos`,
`auditoria`, `configuracoes`, `ceps_cache`).

### 1.3 Módulos existentes e em funcionamento

26 módulos de API, 25 páginas, 200 rotas, 46 permissões, 6 papéis. Todos validados:
captação, imóveis, clientes, compradores com cruzamento, corretores com controle de CRECI,
visitas, propostas, atendimentos, negociações, contratos com versões e assinatura,
modelos de documento com 110 variáveis, locações com cobranças e reajuste, **vistorias com
laudo em PDF e comparação entrada × saída**, financeiro, comissões com rateio, agenda,
tarefas, auditoria, usuários e permissões, site público, busca de CEP.

### 1.4 O módulo de vistoria

Existe e está completo: `vistorias` + `vistoria_ambientes` + `vistoria_itens` +
`vistoria_fotos` + `vistoria_comparacoes`, com 25 rotas, execução mobile-first ambiente por
ambiente, laudo em PDF gerado pelo sistema e comparação item a item entre entrada e saída
apontando dano, responsabilidade e custo estimado. **Não será tocado** — apenas referenciado
pela análise.

### 1.5 Cadastro de clientes — 44 campos

**Boa notícia: a maior parte do que o item 1 pede já existe.**

| Pedido no item 1 | Situação |
|---|---|
| Nome completo, CPF, RG/CNH | `nome`, `cpf_cnpj`, `rg_ie` ✅ |
| Data de nascimento, estado civil, profissão | `data_nascimento`, `estado_civil`, `profissao` ✅ |
| Telefone, e-mail, endereço atual | `telefone`, `telefone2`, `email`, `email2`, `cep`, `endereco`, `numero`, `complemento`, `bairro`, `cidade`, `estado` ✅ |
| Dados do cônjuge | `nome_conjuge`, `cpf_conjuge`, `rg_conjuge`, `profissao_conjuge`, `nacionalidade_conjuge`, `regime_bens` ✅ |
| Dados bancários | `banco`, `agencia`, `conta`, `tipo_conta`, `pix`, `titular_conta` ✅ |
| **Renda mensal** | ❌ falta |
| **Empresa onde trabalha, cargo, admissão** | ❌ falta |
| **Tempo de residência, tipo de moradia** | ❌ falta |
| **Dependentes** | ❌ falta |

Conclusão: **o cliente não será cadastrado de novo** (item 13/19). Bastam 7 colunas novas
em `clientes`, e o resto dos dados da análise fica na tabela da própria análise — porque
renda e composição mudam a cada pretensão, e congelar o valor analisado é o correto.

### 1.6 `checklist_documentos` — já existe e serve

```
id, entidade, entidade_id, negociacao_id, documento_tipo, descricao,
obrigatorio, status, documento_id, observacoes, conferido_por, conferido_em, criado_em
```

Os status já são exatamente os pedidos no item 2 (`pendente`, `recebido`, `em_analise`,
`aprovado`, `recusado`, `dispensado`), com anexo (`documento_id`), responsável
(`conferido_por`), data e observações. Em `catalogos.py` já existe `CHECKLIST_SUGERIDO` com
listas prontas para `locatario` e `fiador`.

**Reaproveitamento:** acrescento uma coluna `analise_id` e o status
`solicitar_novo` (pedido no item 2). Nada é duplicado.

### 1.7 Documentos e anexos

`documentos` já guarda arquivo com nome aleatório, mime, tamanho, validade e marcação
`confidencial`. O upload valida extensão e tamanho. Os arquivos ficam em `dados/uploads/`,
**fora** da pasta servida como estático, e só saem por endpoint autenticado.

**Falta para a LGPD (item 12/16):** registro de **quem visualizou** cada documento. Hoje o
download não é auditado.

### 1.8 Auditoria

`app/auditoria.py` tem `registrar / criacao / exclusao / diferenca / historico` e a tabela
grava entidade, ação, campo, valor anterior, valor novo, usuário e data. O domínio de ações
já inclui `acesso` — só não é usado ainda. Serve inteiramente para o item 16.

### 1.9 Autenticação e permissões

Senha com PBKDF2-SHA256 (210.000 iterações), sessão em cookie HttpOnly com expiração,
permissão por papel + exceções individuais por usuário, filtragem de campos no servidor.

Papéis atuais e o mapeamento pedido no item 12:

| Pedido | Papel existente |
|---|---|
| Diretor/Administrador | `administrador` |
| Gerente | `gerente` |
| Administrativo | `assistente` |
| Corretor | `corretor` (e `captador`) |

Não preciso criar papéis — preciso criar o grupo de permissões `analise.*` e distribuí-lo.

### 1.10 Gerador de PDF

`app/pdf.py` já tem `titulo`, `subtitulo`, `paragrafo` justificado, `campos`, `tabela`,
`galeria`, `assinaturas`, `caixa_destaque`, `aviso` e paginação automática. O relatório do
item 10 sai direto disso, sem nada novo.

### 1.11 Fluxo de locação já encadeado

```
captacoes → imoveis → visitas → propostas → negociacoes → contratos → locacoes
                                                                    → vistorias
```

As chaves estrangeiras existem. A análise entra **entre a proposta e o contrato**, sem
alterar o encadeamento atual.

### 1.12 PWA

Não existe. Hoje há apenas `<meta name="viewport">`. Faltam `manifest.json`,
service worker, ícones e os metadados de instalação.

---

## 2. Três pontos que dependem de decisão — e o que proponho

### 2.1 Consulta a bureau de crédito (itens 4, 5 e 18)

**Não existe API pública de Serasa/Boa Vista/SPC.** Todas exigem contrato comercial,
credenciais e, na maioria dos casos, certificado digital. Você foi claro: *"não criar uma
falsa consulta nem simular resultados"* — concordo integralmente.

Proposta em duas camadas:

1. **Registro manual da consulta (funciona hoje).** O analista consulta no portal que a
   imobiliária já assina, e registra no sistema: provedor, data e hora, CPF consultado,
   score retornado, faixa informada pelo provedor, restrições, pendências, protocolo e
   anexo do relatório em PDF. Fica tudo no histórico, auditado, com o **consentimento do
   titular** registrado antes. Nada é inventado — o sistema guarda o que veio da fonte.
2. **Arquitetura plugável (para quando houver contrato).** Um módulo `app/bureau.py` com
   interface única (`consultar(cpf, consentimento) -> resultado`) e provedores registráveis.
   Sem credencial configurada, o sistema **diz** que não há integração ativa e oferece o
   registro manual. Quando você fechar contrato, entra um provedor novo sem mexer no resto.

Para ativar uma integração real, no futuro, será necessário: contrato com o bureau,
credenciais (usuário/senha ou token), URL do ambiente, e possivelmente certificado digital
A1. Vou documentar isso no código.

### 2.2 Inteligência artificial e leitura de documentos (item 14)

Testei o que é possível neste ambiente:

| Tarefa | Viável sem dependência? |
|---|---|
| Extrair texto de PDF **com camada de texto** (holerite de sistema, extrato baixado do banco, IR) | ✅ sim — `zlib` + parser próprio |
| Extrair texto de **PDF escaneado ou foto** (RG fotografado, holerite no scanner) | ❌ não — exige OCR (Tesseract ou API de visão) |
| Conferências determinísticas: CPF válido, nome divergente, data inconsistente, soma de renda, comprometimento, documento vencido, arquivo ilegível por tamanho | ✅ sim — e é aqui que está o ganho real |
| Resumo da análise em texto | ✅ sim — descrevendo o que os dados mostram, sem inventar |
| Decidir aprovação | ❌ **não farei** — você pediu, e é o correto |

Na prática da imobiliária a maioria dos documentos chega como **foto**, então extração
automática cobriria só parte dos casos. Por isso proponho inverter a prioridade: entregar
primeiro as **conferências automáticas** (que funcionam sempre, são explicáveis e apontam o
que o analista precisa olhar) e a extração de texto como auxílio onde o arquivo permitir,
sempre com confirmação humana antes de gravar qualquer campo.

Se depois você quiser OCR de fotos, é possível com uma dependência (`pytesseract`) ou uma
API de visão — aí eu explico o que muda.

### 2.3 Criptografia dos documentos (item 17)

Não existe AES na biblioteca padrão do Python. Implementar uma cifra caseira daria uma
**falsa sensação de segurança** — não vou fazer isso.

O que entrego de verdade: arquivos fora do diretório público, nome aleatório de 16 dígitos
hexadecimais, download só por endpoint autenticado com checagem de permissão, marcação de
confidencialidade, **registro de todo acesso** (quem, quando, qual documento) e proteção
contra travessia de diretório. Para cifra em repouso, o caminho honesto é a criptografia de
disco do sistema operacional (BitLocker no Windows, FileVault no macOS, LUKS no Linux) —
vou documentar isso.

---

## 3. Plano de implementação

Tudo aditivo: `CREATE TABLE IF NOT EXISTS` e `ALTER TABLE ADD COLUMN`, como na evolução
anterior. Nenhuma tabela, rota ou tela existente é removida ou reescrita.

### Fase 1 — Modelo de dados

Tabelas novas:

| Tabela | Para quê |
|---|---|
| `analises_locacao` | a análise em si: pretendente, imóvel, valores, status, parecer |
| `analise_rendas` | composição de renda (titular, cônjuge, terceiros), com origem e comprovação |
| `analise_garantias` | uma linha por garantia avaliada (fiador, seguro, caução, título) |
| `analise_fiadores` | dados e imóvel do fiador, com análise própria |
| `analise_consultas` | consultas a bureau: provedor, score, restrições, protocolo, anexo |
| `analise_conferencias` | conferência documento a documento: legível, nome confere, CPF confere, divergências |
| `analise_pareceres` | histórico de pareceres, com justificativa obrigatória |
| `acessos_documento` | quem visualizou/baixou cada documento (LGPD) |
| `consentimentos` | consentimento do titular: finalidade, data, forma, validade |
| `criterios_locacao` | critérios configuráveis da imobiliária |

Colunas novas em `clientes`: `renda_mensal`, `empresa`, `cargo`, `admissao`,
`tempo_residencia_meses`, `tipo_moradia`, `dependentes`.
Coluna nova em `checklist_documentos`: `analise_id`.
Coluna nova em `locacoes`: `analise_id`.

### Fase 2 — Regras e cálculos (`app/analise.py`)

Comprometimento de renda conforme item 6, considerando o que a imobiliária configurar
(aluguel, condomínio, IPTU, outras despesas) sobre a renda **comprovada**; soma da
composição de renda; avaliação contra os critérios configurados; lista de pendências;
detecção de divergências. Tudo determinístico e explicável — cada número mostra de onde veio.

### Fase 3 — Conferência e leitura de documentos

`app/extrator.py`: texto de PDF quando houver camada de texto; validação de CPF; comparação
de nomes com normalização (acentos, abreviações); conferência de datas e validade. Resultado
sempre como **sugestão** para o analista confirmar.

### Fase 4 — Bureau de crédito (`app/bureau.py`)

Interface de provedor, registro manual completo e o aviso claro quando não há integração
ativa. Consentimento obrigatório antes de registrar consulta.

### Fase 5 — API (`app/api/analises.py`)

CRUD da análise, checklist, conferência, rendas, garantias, fiador, consultas, parecer,
relatório em PDF, histórico por cliente. Permissões novas: `analise.ver`,
`analise.editar`, `analise.documentos`, `analise.consultar`, `analise.parecer`,
`analise.excluir`, mais `criterios.editar`.

### Fase 6 — Relatório em PDF

Usando `app/pdf.py`, com todos os itens da seção 10, incluindo o aviso de que a decisão é
da imobiliária e a identificação do responsável.

### Fase 7 — Telas

`analises.js`: lista com filtros e indicadores; ficha com abas (pretendente, renda,
documentos, conferência, consultas, garantia, parecer, histórico). Integração: botão na
proposta de locação, aba no cliente, aba no imóvel, botão na locação. Critérios em
Configurações.

### Fase 8 — LGPD e auditoria

Registro de acesso a documento, consentimento, controle por papel, e a política de retenção.

### Fase 9 — PWA

`manifest.json`, ícones gerados pelo próprio sistema, service worker com cache da casca do
aplicativo, metadados de instalação e tela cheia. Instalável no celular, tablet e desktop.

### Fase 10 — Demonstração, documentação e regressão

Duas análises de exemplo (uma aprovada, uma com ressalvas), atualização do README e bateria
completa de regressão de todas as telas e endpoints.

---

## 4. O que muda no que já existe

| Arquivo | Mudança |
|---|---|
| `app/schema_v2.sql` | tabelas novas (aditivo) |
| `app/migracao.py` | colunas novas, permissões novas, critérios padrão |
| `app/catalogos.py` | domínios novos (status da análise, tipos de renda, resultado de conferência) |
| `app/api/documentos.py` | registro de acesso no download |
| `app/api/propostas.py` | botão "abrir análise de locação" |
| `app/api/locacoes.py` | vínculo com a análise aprovada |
| `app/api/dashboard.py` | indicadores e pendências da análise |
| `app/rotas.py` | registro do módulo novo |
| `web/index.html` | manifest e service worker |
| `web/js/app.js` | menu e rota |
| `web/js/paginas/{propostas,cliente-detalhe,imovel-detalhe,locacoes,configuracoes}.js` | pontos de entrada |

Nada é reescrito. As alterações nos arquivos existentes são acréscimos pontuais.

---

## 5. Pergunta em aberto

**Prazo de retenção dos dados de crédito.** A LGPD exige finalidade e prazo definidos. Para
análises **não aprovadas**, quanto tempo a imobiliária quer guardar os documentos e o
resultado da consulta? Sugestão: 12 meses, configurável, com expurgo assistido (o sistema
lista o que passou do prazo e o administrador confirma a exclusão). Nada é apagado
automaticamente sem confirmação.
