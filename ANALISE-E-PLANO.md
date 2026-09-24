# Diagnóstico do projeto e plano de evolução

Documento de análise pedido antes de qualquer alteração de código.
Nenhuma linha do sistema foi modificada para produzir este diagnóstico.

---

## ⚠ Ponto crítico levantado na análise: o módulo de vistoria não está neste projeto

Você mencionou que o **módulo de laudo de vistoria já foi desenvolvido neste projeto**.
Procurei em todo o workspace e **ele não existe aqui**. Confirmei por quatro caminhos:

| Verificação | Resultado |
|---|---|
| Tabelas de vistoria, ambiente, item ou laudo no banco | **nenhuma** (25 tabelas, nenhuma delas) |
| Rotas de API de vistoria/laudo | **nenhuma** (das 90 rotas) |
| Telas de vistoria no frontend | **nenhuma** (das 13 páginas) |
| Arquivos com lógica de vistoria | **nenhum** |

As três ocorrências das palavras que encontrei são coincidências de vocabulário, não código:

- `"AUTO DE VISTORIA DO CORPO DE BOMBEIROS"` → texto dentro de um PDF de exemplo (AVCB);
- `("laudo", "Laudo / Avaliação")` → apenas um item na lista de tipos de documento anexável;
- `ambiente` → campo que classifica **foto do imóvel** (fachada, sala, cozinha), usado no
  anúncio. Não é ambiente de vistoria.

### Por que isso aconteceu

Cada sessão do Kiro Web roda em um **sandbox isolado**. Se você desenvolveu a vistoria em
**outra sessão/conversa**, aquele código ficou no sandbox daquela sessão — ele não aparece
aqui. Este workspace contém somente o sistema de gestão que construímos nesta conversa.

### O que preciso de você

Escolha **uma** opção:

1. **Enviar o código da vistoria.** Se você tem os arquivos, publique num repositório
   GitHub e conecte aqui — eu integro preservando o que já funciona, exatamente como você
   pediu. É o caminho ideal, porque respeita a regra "não recriar o que existe".
2. **Recuperar da outra sessão.** Se a vistoria está em outra conversa do Kiro, abra
   aquela sessão e publique o código num repositório de lá; depois conectamos aqui.
3. **Eu construo a vistoria do zero**, seguindo a especificação detalhada dos itens 22 a 27
   da sua mensagem (tipos, ambientes, itens, fotos por celular, laudo em PDF, comparação
   entrada × saída). Nesse caso nada é perdido, mas também nada é reaproveitado — e é
   provável que o seu módulo tenha detalhes que a especificação não cobre.

**Enquanto isso não se resolve, o plano abaixo já está montado para receber a vistoria**
sem retrabalho: o modelo de dados e os pontos de integração estão definidos, e a Fase 5
(vistoria) é independente das fases anteriores.

---

## 1. Diagnóstico do projeto atual

### O que é hoje

Sistema de gestão imobiliária focado em **cadastro, consulta e divulgação**: imóveis,
clientes, captadores, fotos, documentos, compradores com cruzamento automático, visitas,
propostas, atendimentos, fichas de impressão e site público.

### Números reais

| Medida | Valor |
|---|---|
| Backend | 8.546 linhas Python, 30 arquivos |
| Frontend | 6.459 linhas JavaScript, 19 arquivos |
| Estilos | 486 linhas CSS |
| Banco | 25 tabelas, 38 chaves estrangeiras |
| API | 90 rotas |
| Telas | 13 páginas + site público + 3 fichas de impressão |
| Dependências externas | **zero** (só biblioteca padrão do Python) |

### Qualidade e limitações encontradas

**Pontos fortes (a preservar):**

- **Cadastro único já é realidade.** `clientes` + `cliente_papeis` permitem que a mesma
  pessoa seja proprietário, comprador e locatário sem duplicar cadastro. Isso atende
  diretamente à sua regra "não quero duplicidade".
- **Permissões granulares no servidor** (26 permissões, 5 papéis, exceções por usuário).
  Campos restritos não são enviados ao navegador — não é só esconder na tela.
- **Histórico automático** em `imovel_historico` (valor, status, publicação, proposta).
- **Filtragem de dados por contexto**: a mesma função devolve o imóvel completo, sem dados
  internos, ou apenas o público, conforme quem pergunta.
- **Camada HTTP própria e enxuta**, com roteador, upload multipart e validações.

**Limitações reais (que afetam o que você pediu):**

| Limitação | Impacto no novo escopo |
|---|---|
| **Não existe geração de PDF de verdade.** As fichas são HTML impresso pelo navegador (Ctrl+P → Salvar como PDF). O `midia_demo.py` faz PDFs mínimos, só para dados de exemplo. | **Alto.** Laudo de vistoria e contratos exigem PDF profissional com fotos, paginação e cabeçalho. Precisa de um gerador real. |
| `imoveis` tem **102 colunas** numa única tabela | **Médio.** Funciona, mas dificulta manutenção. Novos módulos não devem ampliar essa tabela. |
| Comissão é **campo no imóvel**, não entidade | **Médio.** Comissão precisa virar tabela própria (divisão entre corretores, pagamento, status). |
| Captação é **campo** (`captador_id`, `data_captacao`) | **Médio.** Você pediu módulo com origem, valor pretendido, situação, documentos e histórico. |
| Não há **negociação** como entidade | **Alto.** É o elo entre proposta aceita e contrato — hoje inexistente. |
| Histórico só cobre **imóveis** | **Médio.** Você pediu auditoria de criação/alteração/exclusão em todos os módulos. |
| Servidor **single-process** com SQLite | **Baixo** para escritório (dezenas de usuários); relevante só em escala maior. |
| Sem testes automatizados | **Médio.** Com 20+ módulos integrados, validar manualmente a cada etapa fica caro. |

---

## 2. Arquitetura atual

```
NAVEGADOR (SPA, JavaScript puro, sem framework)
   │  fetch() → JSON
   ▼
app/servidor.py          ThreadingHTTPServer + arquivos estáticos
   │
app/http_core.py         Requisição, Resposta, upload multipart, Roteador
   │
app/rotas.py             registro central (90 rotas)
   │
app/api/*.py             15 módulos: auth, imoveis, clientes, fotos, documentos,
   │                     compradores, visitas, propostas, atendimentos, usuarios,
   │                     dashboard, fichas, publico, catalogo, corretores
   │
app/seguranca.py         PBKDF2, sessões em cookie, resolução de permissões
app/utils.py             validação CPF/CNPJ, conversões, formatação brasileira
   │
app/db.py                SQLite (conexão por thread, transações)
   ▼
dados/imobiliaria.db  +  dados/uploads/{fotos,documentos}
```

**Padrão de cada módulo de API** (será mantido nos novos):

```python
def registrar(r: Roteador) -> None:
    r.adicionar("GET",  "/api/recurso",      _listar)
    r.adicionar("POST", "/api/recurso",      _criar)
```

Cada handler: `req.exige("permissao")` → valida → `db` → devolve dict (vira JSON).

---

## 3. Arquitetura proposta

**Decisão central: evoluir, não reescrever.** A estrutura atual suporta o crescimento.
As mudanças são aditivas.

```
NAVEGADOR (SPA)
   │
   ├── páginas atuais (13)          ← preservadas
   └── páginas novas (11)           ← captações, negociações, locações, contratos,
   │                                   vistorias, laudos, financeiro, comissões,
   ▼                                   agenda, tarefas, modelos de documento
app/servidor.py                     ← inalterado
app/http_core.py                    ← inalterado
app/rotas.py                        ← + registros novos
   │
app/api/*.py  (15 atuais)           ← preservados
app/api/*.py  (11 novos)            ← captacoes, negociacoes, locacoes, contratos,
   │                                   modelos, vistorias, laudos, financeiro,
   │                                   comissoes, agenda, auditoria
   │
   ├── app/pdf.py          ← NOVO: gerador de PDF real (fotos, paginação, tabelas)
   ├── app/modelos.py      ← NOVO: motor de variáveis {{CAMPO}} dos contratos
   ├── app/auditoria.py    ← NOVO: histórico universal de qualquer entidade
   └── app/comparacao.py   ← NOVO: vistoria de entrada × saída
   ▼
SQLite: 25 tabelas atuais + ~22 novas
```

### Três componentes técnicos que precisam ser construídos

**1. Gerador de PDF (`app/pdf.py`)** — o mais crítico. Sem biblioteca externa
disponível, será um gerador próprio com: texto com quebra automática de linha,
negrito/itálico, tabelas, **imagens JPEG/PNG embutidas** (essencial para o laudo),
cabeçalho/rodapé, numeração e blocos de assinatura. É trabalho sério, mas viável —
o PDF é um formato documentado e já provei o conceito no `midia_demo.py`.

**2. Motor de modelos (`app/modelos.py`)** — substitui `{{NOME_COMPRADOR}}` pelos dados
reais. Resolve variáveis a partir de imóvel, partes, negociação e configurações;
formata valores em reais e **valor por extenso** (exigência de contrato); trata partes
múltiplas (dois compradores → "João e Maria"); e lista as variáveis disponíveis para o
usuário inserir no editor.

**3. Auditoria universal (`app/auditoria.py`)** — generaliza o que hoje existe só para
imóveis: uma tabela registra criação/alteração/exclusão de qualquer entidade, com
usuário, data, campo, valor anterior e novo.

---

## 4. Modelo de banco atual

25 tabelas, 38 relacionamentos. Agrupadas:

| Grupo | Tabelas |
|---|---|
| Catálogos | `tipos_imovel`, `caracteristicas`, `atividades`, `origens_cliente` |
| Pessoas | `clientes`, `cliente_papeis`, `corretores` |
| Acesso | `usuarios`, `papel_permissoes`, `usuario_permissoes`, `sessoes` |
| Imóvel | `imoveis` (102 col.), `imovel_comercial`, `imovel_documentacao`, `imovel_caracteristicas`, `imovel_atividades` |
| Arquivos | `fotos`, `documentos` |
| Comercial | `perfis_interesse`, `indicacoes`, `visitas`, `propostas`, `atendimentos` |
| Auditoria | `imovel_historico` |
| Sistema | `configuracoes` |

**O eixo central já está correto:** `imoveis.proprietario_id → clientes.id` e
`clientes ↔ cliente_papeis`. Todos os módulos novos vão se pendurar nesse eixo.

---

## 5. Modelo de banco proposto

**Regra: nenhuma tabela existente perde coluna ou dado.** Só acrescento tabelas e, quando
necessário, colunas novas com valor padrão.

### Captação (item 6)

```sql
captacoes            proprietario_id→clientes, imovel_id→imoveis, corretor_id→corretores,
                     data, origem, finalidade, valor_pretendido, comissao_percentual,
                     situacao, exclusividade, prazo_autorizacao, observacoes
```

### Negociação — o elo que falta (itens 9, 12, 35)

```sql
negociacoes          imovel_id, tipo (venda|locacao), proposta_id, corretor_id,
                     valor_negociado, status (11 estágios de venda / 10 de locação),
                     data_inicio, data_conclusao, observacoes
negociacao_partes    negociacao_id, cliente_id, papel (comprador|vendedor|locatario|
                     locador|fiador|interveniente), percentual, principal
                     ↑ resolve "um ou vários compradores e vendedores" (item 12)
```

### Contratos (itens 11, 12, 13, 19)

```sql
contratos            negociacao_id, imovel_id, tipo (compra_venda|compromisso|locacao|
                     aditivo|distrato|recibo_sinal|termo_quitacao|termo_entrega),
                     numero, modelo_id, versao, status (rascunho|revisao|final|
                     aguardando_assinatura|assinado|cancelado|distratado),
                     conteudo_html, data_contrato, valor_total, contrato_pai_id,
                     assinado_em, criado_por
contrato_versoes     contrato_id, versao, conteudo_html, usuario_id, criado_em, resumo
                     ↑ nunca sobrescreve versão assinada (item 19)
contrato_partes      contrato_id, cliente_id, papel, dados_congelados (JSON)
                     ↑ congela os dados no momento da assinatura
contrato_assinaturas contrato_id, versao, cliente_id, nome, email, status, data,
                     provedor, id_externo
                     ↑ preparado para assinatura digital (item 20)
```

### Condições de pagamento (item 13)

```sql
pagamento_condicoes  negociacao_id, valor_total, sinal, entrada, financiamento, fgts,
                     recursos_proprios, carta_credito, permuta_valor, permuta_descricao,
                     prazo_financiamento, prazo_assinatura, prazo_posse
pagamento_parcelas   condicao_id, numero, descricao, valor, vencimento, tipo,
                     status (previsto|pago|atrasado), pago_em
                     ↑ alimenta a tabela visual do fluxo de pagamento
```

### Modelos de documento (itens 14, 15, 17)

```sql
modelos_documento    nome, tipo, conteudo_html, cabecalho, rodape, ativo, padrao,
                     observacoes, criado_por, atualizado_em
modelo_versoes       modelo_id, versao, conteudo_html, usuario_id, criado_em
```

### Locação (item 10)

```sql
locacoes             contrato_id, imovel_id, locador_id, locatario_id, fiador_id,
                     valor_aluguel, valor_condominio, valor_iptu, dia_vencimento,
                     indice_reajuste, mes_reajuste, data_inicio, data_fim,
                     tipo_garantia, valor_caucao, seguradora, apolice,
                     status, vistoria_entrada_id, vistoria_saida_id
```

### Vistoria (itens 22 a 27) — estrutura preparada

```sql
vistorias            imovel_id, contrato_id, locacao_id, tipo (entrada|saida|
                     intermediaria|manutencao|conferencia), data, responsavel_id,
                     proprietario_id, locatario_id, status (rascunho|em_andamento|
                     concluida|assinada), conclusao, observacoes, laudo_pdf
vistoria_ambientes   vistoria_id, nome, tipo, ordem, conservacao, descricao,
                     observacoes, medidas
vistoria_itens       ambiente_id, tipo (piso|parede|teto|porta|janela|tomada|
                     interruptor|iluminacao|torneira|louca|metal|armario|
                     eletrodomestico|pintura|esquadria|outro), nome, estado,
                     descricao, observacoes, problema, ordem
vistoria_fotos       vistoria_id, ambiente_id, item_id, arquivo, legenda,
                     observacao, ordem
                     ↑ IMÓVEL → VISTORIA → AMBIENTE → ITEM → FOTO (item 25)
vistoria_comparacoes vistoria_entrada_id, vistoria_saida_id, ambiente, item,
                     resultado (sem_alteracao|alteracao|dano|reparo|melhoria),
                     observacoes, foto_entrada_id, foto_saida_id
```

### Financeiro e comissões (itens 28, 29)

```sql
lancamentos          tipo (receita|despesa), categoria (aluguel|condominio|iptu|
                     sinal|parcela|comissao|taxa|repasse|outro), descricao,
                     valor, vencimento, pago_em, valor_pago, status,
                     imovel_id, cliente_id, contrato_id, locacao_id, negociacao_id,
                     parcela_id, forma_pagamento, observacoes
comissoes            negociacao_id, contrato_id, valor_negocio, percentual, valor,
                     status (prevista|aprovada|paga|cancelada), observacoes
comissao_rateio      comissao_id, corretor_id, papel (captador|vendedor|gerente|
                     parceiro), percentual, valor, pago_em, lancamento_id
                     ↑ resolve "divisão" de comissão (item 29)
```

### Agenda, tarefas, checklist e auditoria (itens 21, 31, 34)

```sql
tarefas              titulo, descricao, tipo, prazo, concluida_em, prioridade,
                     responsavel_id, imovel_id, cliente_id, contrato_id,
                     vistoria_id, negociacao_id, criado_por
compromissos         titulo, tipo (visita|vistoria|assinatura|reuniao|prazo|outro),
                     inicio, fim, local, responsavel_id, vinculos..., status
checklist_documentos entidade (comprador|vendedor|proprietario|locatario|imovel),
                     entidade_id, documento_tipo, obrigatorio,
                     status (pendente|recebido|em_analise|aprovado|recusado),
                     documento_id, observacoes, conferido_por, conferido_em
auditoria            entidade, entidade_id, acao (criacao|alteracao|exclusao),
                     campo, valor_anterior, valor_novo, usuario_id, criado_em
```

**Total: ~22 tabelas novas, 47 no final. Nenhuma alteração destrutiva.**

### Pequenas adições a tabelas existentes

| Tabela | Coluna nova | Motivo |
|---|---|---|
| `clientes` | `nacionalidade_conjuge`, `banco`, `agencia`, `conta`, `tipo_conta`, `pix` | dados bancários (item 5) e contrato |
| `propostas` | `negociacao_id` | ligar proposta → negociação |
| `visitas` | `compromisso_id` | unificar na agenda |
| `usuarios` | papel `vistoriador` | item 33 |

---

## 6. Módulos existentes (preservar)

| Módulo | Situação |
|---|---|
| Dashboard | pronto — será **ampliado** com os novos indicadores do item 30 |
| Imóveis | pronto — cadastro único já é o eixo do sistema |
| Proprietários / Clientes / Compradores / Vendedores / Locatários | pronto via `clientes` + papéis |
| Visitas | pronto — entrará também na agenda |
| Propostas | pronto — ganhará "gerar negociação" |
| Documentos | pronto — ganhará checklist por entidade |
| Usuários e permissões | pronto — ganhará papel `vistoriador` e permissões novas |
| Configurações | pronto — ganhará dados para contrato (razão social, CNPJ, CRECI) |
| Fichas de impressão | pronto — migrarão para o gerador de PDF real |
| Site público | pronto — inalterado |

## 7. Módulos a criar

| # | Módulo | Itens da sua especificação |
|---|---|---|
| 1 | Captações | 6 |
| 2 | Negociações | 9, 35 |
| 3 | Contratos (base + versões) | 19 |
| 4 | Modelos de documento + variáveis | 14, 15, 16 |
| 5 | Editor e visualizador de contrato | 17, 18 |
| 6 | Contratos de compra e venda | 12, 13 |
| 7 | Contratos de locação | 11 |
| 8 | Locações | 10 |
| 9 | Vistorias | 22, 23, 24, 25 |
| 10 | Laudos em PDF | 26 |
| 11 | Comparação entrada × saída | 27 |
| 12 | Financeiro | 28 |
| 13 | Comissões com rateio | 29 |
| 14 | Agenda e tarefas | 31 |
| 15 | Checklist de documentação | 21 |
| 16 | Auditoria universal | 34 |
| 17 | Assinatura digital (estrutura) | 20 |

## 8. Pontos de integração

O fluxo que você desenhou, mapeado para o que existe e o que falta:

```
CAPTAÇÃO ........... criar, ligando a imoveis + clientes + corretores  [NOVO]
   ↓
IMÓVEL ............. existe ✔ (eixo central, sem duplicar)
   ↓
PROPRIETÁRIO ....... existe ✔ (clientes + papel)
   ↓
ANÚNCIO ............ existe ✔ (publicação + site)
   ↓
CLIENTE ............ existe ✔ (+ perfis de interesse e cruzamento)
   ↓
VISITA ............. existe ✔
   ↓
PROPOSTA ........... existe ✔ → ganha botão "gerar negociação"
   ↓
NEGOCIAÇÃO ......... criar — elo entre proposta e contrato          [NOVO]
   ↓
VENDA / LOCAÇÃO .... status na negociação + tabela locacoes         [NOVO]
   ↓
CONTRATO ........... gerado do modelo + dados da negociação         [NOVO]
   ↓
DOCUMENTOS ......... existe ✔ → ganha checklist com status
   ↓
VISTORIA ........... integrar o seu módulo (ou criar)               [PENDENTE]
   ↓
LAUDO .............. PDF com fotos por ambiente                     [NOVO]
   ↓
ASSINATURA ......... registro de assinantes e versões               [NOVO]
   ↓
FINANCEIRO ......... lançamentos ligados a contrato/locação         [NOVO]
   ↓
COMISSÃO ........... comissão + rateio entre corretores             [NOVO]
   ↓
HISTÓRICO .......... auditoria universal (hoje só imóvel)           [AMPLIAR]
```

**Regras de integração que vou seguir:**

1. Nenhum módulo novo cria cadastro de pessoa ou imóvel — todos referenciam
   `clientes.id` e `imoveis.id`.
2. Contrato **nunca** copia dados de pessoa por digitação: busca do cadastro e
   **congela** em `contrato_partes.dados_congelados` no momento da assinatura (assim o
   contrato assinado não muda se o cadastro mudar depois).
3. Vistoria referencia imóvel **e** contrato/locação, permitindo entrada e saída do
   mesmo imóvel em locações diferentes.
4. Financeiro nunca duplica valor: lê de `pagamento_parcelas`, `locacoes` e `comissoes`.

## 9. Riscos

| Risco | Gravidade | Como vou tratar |
|---|---|---|
| **Módulo de vistoria não localizado** | **Alta** | Bloqueia a integração pedida. Preciso da sua decisão (3 opções no topo). Fases 1–4 seguem independentes. |
| **PDF sem biblioteca externa** | **Alta** | Gerador próprio, construído e testado incrementalmente: primeiro texto, depois tabelas, depois imagens. Valido cada etapa abrindo o PDF. |
| Quebrar o que funciona | Alta | Só mudanças aditivas no banco; bateria de testes dos módulos antigos após **cada** fase. |
| Escopo muito grande | Alta | 10 fases entregáveis. Cada fase termina funcionando, salvando e consultando de verdade. |
| Editor de texto rico sem biblioteca | Média | `contenteditable` nativo do navegador + barra de ferramentas própria com `document.execCommand`. |
| Valor por extenso em contrato | Média | Implementação própria em português (exigência real de contratos). |
| Migração de dados existentes | Média | Script de migração idempotente; backup automático do banco antes de aplicar. |
| Assinatura digital | Média | **Não** vou inventar validade jurídica. Estrutura de registro pronta e documentada; integração real exige contratar provedor (DocuSign, Clicksign, D4Sign). |
| Contrato "juridicamente adequado" | Média | Modelos entregues como **ponto de partida editável**, com aviso explícito de revisão por advogado — conforme seu item 40. |
| SQLite com muitos usuários | Baixa | Adequado ao escritório. Documento o limite e o caminho para PostgreSQL. |

## 10. Plano de implementação

Cada fase termina com **teste de regressão** dos módulos anteriores.

| Fase | Entrega | O que passa a funcionar de verdade |
|---|---|---|
| **1** | Banco + auditoria universal | ~22 tabelas novas criadas, migração preservando dados, histórico de qualquer entidade |
| **2** | Captações + Negociações | Captar imóvel do proprietário; proposta aceita gera negociação com partes múltiplas; status de venda e locação |
| **3** | **Gerador de PDF** | PDF real com texto, tabelas, imagens, cabeçalho, paginação e assinaturas. Fichas atuais migradas |
| **4** | Modelos + variáveis + editor | Cadastrar modelo, inserir `{{CAMPOS}}`, editar, pré-visualizar, gerar PDF com dados reais |
| **5** | Contratos CV e Locação | Contrato gerado da negociação, versões, partes congeladas, condições e parcelas, aditivo e distrato |
| **6** | Locações | Locação ativa, reajuste, garantia, vencimento, vínculo com vistoria de entrada/saída |
| **7** | **Vistorias + Laudo** | Vistoria por ambiente/item, fotos pelo celular, laudo em PDF, comparação entrada × saída |
| **8** | Financeiro + Comissões | Lançamentos, parcelas, aluguéis, comissão com rateio entre corretores |
| **9** | Agenda + Tarefas + Checklist | Compromissos unificados, tarefas com prazo, checklist de documentos por entidade |
| **10** | Auditoria final | Dashboard ampliado, permissões dos módulos novos, responsividade (vistoria no celular), revisão de segurança e bugs |

### Ordem e dependências

```
Fase 1 (banco) ──┬── Fase 2 (captação/negociação) ──┬── Fase 5 (contratos) ── Fase 6 (locação)
                 │                                   │                            │
                 └── Fase 3 (PDF) ── Fase 4 (modelos)┘                            │
                                          │                                       │
                                          └── Fase 7 (vistoria + laudo) ──────────┤
                                                                                  │
                                              Fase 8 (financeiro) ────────────────┤
                                              Fase 9 (agenda) ───────────────────┤
                                                                      Fase 10 (auditoria)
```

**A Fase 3 (PDF) é pré-requisito de laudo e contrato** — por isso vem cedo, antes dos
módulos que dependem dela.

---

## Antes de começar, preciso de duas decisões suas

**1. Módulo de vistoria** — qual das três opções do topo deste documento?
(enviar o código / recuperar de outra sessão / eu construir do zero)

**2. Onde o código vai ficar?** Recomendo conectar um **repositório GitHub**. São 47
tabelas e ~25 módulos: sem controle de versão, cada alteração fica arriscada e você não
consegue voltar atrás. Também resolve de vez o problema de você baixar o sistema.

Com essas duas respostas, começo pela Fase 1.
