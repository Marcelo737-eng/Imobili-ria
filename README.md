# Sistema de Gestão Imobiliária

Plataforma única e integrada para **captar, cadastrar, divulgar, negociar, contratar,
vistoriar, administrar e cobrar** imóveis de venda e locação.

Cada pessoa é cadastrada **uma única vez** e passa a carregar consigo todos os seus imóveis,
documentos, propostas, contratos, locações, vistorias e lançamentos financeiros. Nada é
digitado duas vezes: a captação alimenta o imóvel, o imóvel alimenta a negociação, a
negociação gera o contrato, o contrato gera a locação, a locação gera as cobranças e as
vistorias, e tudo desemboca no financeiro e nas comissões.

**Não requer instalação de nenhuma biblioteca.** Usa apenas Python (biblioteca padrão) e
SQLite. O frontend é HTML, CSS e JavaScript puros. Inclusive o gerador de PDF dos laudos e
contratos foi escrito dentro do projeto.

---

## Como executar

```bash
cd imobiliaria
python3 run.py
```

Depois abra **http://localhost:8000** no navegador.

No primeiro acesso o sistema cria o administrador padrão e mostra as credenciais no terminal:

| E-mail | Senha |
|---|---|
| `admin@imobiliaria.com.br` | `admin123` |

> Altere essa senha no primeiro acesso pelo menu do usuário → *Alterar minha senha*.

### Opções de execução

```bash
python3 run.py --porta 9000     # outra porta
python3 run.py --demo           # cria dados de demonstração e inicia
python3 run.py --somente-demo   # apenas cria os dados de demonstração
python3 run.py --reset          # apaga tudo (pede confirmação)
```

### Dados de demonstração

`python3 run.py --demo` monta uma imobiliária fictícia completa, com o ciclo inteiro
percorrido de ponta a ponta — não apenas cadastros soltos:

| O que vem pronto | Quantidade |
|---|---|
| Imóveis de todos os tipos, com fotos e documentos | 10 imóveis, 70 fotos, 42 PDFs |
| Clientes (proprietários, compradores, locatários, fiadores) | 10 |
| Corretores e captadores | 6 |
| Perfis de compradores com cruzamento automático | 6 |
| Visitas, propostas e atendimentos | 12 / 5 / 7 |
| Captações em várias situações (da prospecção à publicada) | 7 |
| Negociações: uma venda em andamento e uma locação concluída | 2 |
| Contratos gerados de modelo e **assinados** | 2 |
| Locações: uma vigente com reajuste aplicado e uma encerrada | 2 |
| Vistorias com laudo em PDF, incluindo entrada × saída comparadas | 4 (21 ambientes, 97 itens) |
| Comparações item a item apontando danos e responsabilidade | 18 linhas |
| Lançamentos financeiros (aluguéis, repasses, taxas, sinal, entrada) | 53 |
| Comissões apuradas e rateadas entre captador, corretor e imobiliária | 2 |
| Checklist de documentos da negociação | 12 itens |
| **Análises de locação**: uma aprovada e uma aprovada com ressalvas | 2 (31 documentos exigidos, 12 conferências) |
| Documentos pessoais do pretendente, com nome e CPF, para a conferência ler | 14 PDFs |
| Consultas de crédito registradas (uma sem apontamento, uma com restrição) | 2 |
| Consentimentos do titular para tratamento de dados e consulta | 2 |
| Compromissos na agenda e tarefas da equipe | 6 / 8 |
| Modelos de documento prontos para editar | 7 |

As fotos e os PDFs de demonstração são **gerados pelo próprio sistema** (sem arquivos
externos). Usuários de teste criados, um por papel:

| E-mail | Senha | Papel |
|---|---|---|
| `admin@imobiliaria.com.br` | `admin123` | Administrador — acesso total |
| `gerente@imobiliaria.com.br` | `gerente123` | Gerente — tudo, exceto usuários e configurações |
| `corretor@imobiliaria.com.br` | `corretor123` | Corretor — vê valores e informações internas |
| `captador@imobiliaria.com.br` | `captador123` | Captador — cadastra, mas não vê dados internos |
| `assistente@imobiliaria.com.br` | `assistente123` | Assistente — só consulta e agenda |
| `vistoriador@imobiliaria.com.br` | `vistoria123` | Vistoriador — faz vistorias no celular |

Entre com usuários diferentes para ver as permissões em ação: os campos restritos
simplesmente não são enviados pelo servidor, e os módulos sem permissão respondem
"acesso restrito" mesmo se o endereço for digitado à mão.

---

## O fluxo que o sistema cobre

```
CAPTAÇÃO → IMÓVEL → DIVULGAÇÃO → VISITA → PROPOSTA → NEGOCIAÇÃO → CONTRATO
    → (venda: parcelas e escritura)        → COMISSÃO → FINANCEIRO
    → (locação: ANÁLISE DE CRÉDITO → LOCAÇÃO → VISTORIA DE ENTRADA
                        → COBRANÇAS → REAJUSTE
                        → VISTORIA DE SAÍDA → COMPARAÇÃO → ENCERRAMENTO)
```

Cada seta é um botão dentro do sistema. Nenhuma etapa exige redigitar dados da anterior.

---

## Módulos

### Captações
Registra a entrada do imóvel na carteira: proprietário, captador, origem, finalidade,
valor pretendido e valor avaliado, comissão acordada, **exclusividade**, prazo de validade
da autorização e situação (em captação → documentação → aprovada → publicada, ou recusada
/ cancelada / encerrada). A ficha mostra a trilha de etapas, a documentação anexada ao
imóvel e o histórico de alterações. Um botão abre a negociação diretamente da captação.

O painel avisa quando uma **autorização está vencendo**, para renovar com o proprietário.

### Clientes — cadastro único
Nome completo ou razão social, CPF ou CNPJ (**validados**, sem duplicidade), RG/inscrição
estadual, telefone, WhatsApp, e-mail, endereço completo, estado civil, regime de bens, nome
e CPF do cônjuge, profissão, nacionalidade, dados bancários para repasse, origem do cliente,
corretor responsável e observações.

Um mesmo cliente pode ter vários papéis ao mesmo tempo: **proprietário, comprador,
vendedor, locador, locatário, fiador ou interessado**. Cada proprietário pode ter quantos
imóveis quiser, sem repetir seus dados.

### Corretores e captadores
Nome, CRECI, telefone, WhatsApp, e-mail, comissão padrão e observações. A ficha mostra
quantos imóveis o profissional captou, de quantos é responsável, clientes, visitas,
propostas, negócios fechados e comissões a receber.

**Controle do registro profissional (CRECI).** O número é padronizado sozinho: digite
`128455f sp`, `SP-128455-F` ou `creci sp 128.455 f` e o sistema grava
`CRECI-SP 128.455-F`, identificando a UF do conselho e se é registro de pessoa física ou
jurídica. Se o número já estiver cadastrado, o sistema **avisa de quem é** e oferece copiar
os dados — evita o corretor duplicado, que é o erro mais comum nesse cadastro.

Cada corretor tem **situação do registro** (ativo, provisório, vencido, suspenso,
cancelado, não verificado), **validade da inscrição** e a **data da última conferência**.
Uma inscrição marcada como ativa mas com validade no passado é tratada como vencida
automaticamente — justamente o caso que costuma passar batido. O painel avisa quando há
CRECI vencido, vencendo em 60 dias, nunca conferido ou corretor ativo sem CRECI, e cada
aviso leva para a lista já filtrada.

> **Por que a conferência não é automática.** Não existe API pública oficial de consulta
> de CRECI. O registro é estadual: são 27 conselhos regionais, cada um com seu site, vários
> com CAPTCHA, e nenhum com integração documentada. O COFECI mantém o cadastro nacional
> (e-CNCI), também sem API aberta. Há sites privados que agregam esses dados por raspagem,
> mas eles próprios avisam que não garantem precisão nem atualidade — base insuficiente
> para o sistema decidir se alguém pode assinar um contrato.
>
> Então o sistema faz o que é confiável: valida o formato, impede número repetido, controla
> validade e situação, avisa quando vence e abre o site do conselho com um clique para a
> conferência — que fica registrada com data e autor na auditoria. A checagem continua
> humana, mas deixa de ser esquecida.

Em **Configurações → Conselho regional** ficam a **UF do seu conselho** e, opcionalmente, o
**endereço da página de consulta**. Quando a UF não é informada, o sistema usa o **estado da
própria imobiliária** — então normalmente não é preciso configurar nada.

Já vêm cadastrados os endereços oficiais de 17 conselhos (SP, RJ, MG, RS, PR, SC, ES, GO,
DF, CE, PE, PA, PB, RN, MT, RO e RR). Para **São Paulo**, o link vai direto para a
[busca por corretores do CRECI-SP](https://www.crecisp.gov.br/cidadao/buscaporcorretores),
que pesquisa por CRECI, CPF, nome, município ou situação cadastral. Para o **Rio de
Janeiro** e **Goiás** também há link direto para a consulta. As demais UFs abrem o COFECI,
que lista todos os regionais.

O endereço personalizado vale apenas para o conselho da sua UF — corretores de outros
estados continuam abrindo o conselho deles. Isso importa quando você trabalha com parceiros
de fora do estado.

### Endereço preenchido pelo CEP
Nos cadastros de **imóvel**, de **cliente** e nas **configurações da imobiliária**, digitar
o CEP preenche tipo de via, rua, bairro, cidade e UF, e o cursor pula para o número. A
busca acontece em cascata:

1. **cache local** — CEP já consultado antes, resposta imediata e **sem internet**
   (os dados de demonstração já vêm com os CEPs dos imóveis em cache);
2. **base própria** — algum imóvel ou cliente já cadastrado com aquele CEP (resolve o caso
   de vários imóveis na mesma rua, também offline);
3. **ViaCEP** — serviço público e gratuito, sem cadastro nem chave;
4. **BrasilAPI** — reserva, se o ViaCEP não responder.

O que vem da internet é guardado, então o segundo uso do mesmo CEP não depende mais da
conexão. Sem internet e sem o CEP no cache, o sistema apenas avisa e libera a digitação
manual — o formulário nunca trava.

Campos já preenchidos **não são sobrescritos**: se o CEP trouxer algo diferente do que você
digitou, aparece um botão para você decidir se quer substituir.

### Imóveis
Código interno único gerado automaticamente (`IM0001`, `IM0002`…), vinculado ao
proprietário e ao captador. O cadastro é organizado em abas:

| Aba | Conteúdo |
|---|---|
| **Identificação** | Finalidade (venda/locação/ambos/procura), categoria, tipo, status, ocupação, conservação, exclusividade, autorização de venda |
| **Localização** | CEP, tipo de via, rua, número, complemento, quadra, lote, bairro, cidade, estado, região, **condomínio**, **distrito industrial**, referência, coordenadas |
| **Medidas** | Terreno, área construída, útil e total, frente, fundos, laterais, testada, topografia, formato |
| **Composição** | Dormitórios, suítes, banheiros, lavabos, salas, cozinhas, vagas, andar, ano de construção, mobiliado |
| **Características** | 120 características agrupadas por ambientes, lazer, conforto, segurança, condomínio, industrial e rural |
| **Comercial / Industrial** | Ver abaixo |
| **Documentação** | Ver abaixo |
| **Valores** | Ver abaixo |
| **Informações internas** | Observações internas, motivo da venda, local das chaves, forma de acesso, contato para visita |
| **Divulgação** | Título, descrição comercial, características, localização, diferenciais, condomínio, infraestrutura, palavras-chave, vídeo e tour virtual |

A ficha do imóvel tem ainda a aba **Negociações, contratos e vistorias**, que reúne num só
lugar a captação, todas as negociações, contratos, locações, vistorias (com link direto
para o laudo em PDF) e a movimentação financeira daquele imóvel.

**Classificação:** residencial, comercial, industrial, rural, terreno ou outro — com 48
tipos detalhados: casa, casa em condomínio, sobrado, apartamento, cobertura, flat, kitnet,
chácara, sítio, fazenda, sala comercial, loja, salão comercial, prédio comercial, galpão,
barracão, área industrial, prédio industrial, condomínio industrial, escritório,
consultório, terreno, lote, área, galpão logístico, oficina e outros.

### Área específica para imóveis comerciais e industriais
**50 atividades** que podem ser exercidas no imóvel (comércio, varejo, atacado, loja,
restaurante, clínica, consultório, academia, escola, depósito, logística, centro de
distribuição, distribuidora, transportadora, armazenamento, indústria leve, média e pesada,
metalúrgica, oficina, serralheria, reciclagem, frigorífico e mais).

Mais: zoneamento, uso permitido, restrito e proibido, alvará de funcionamento, habite-se,
AVCB com validade, licença ambiental, carga e descarga, docas, doca nivelada, entrada para
caminhão, acesso para carreta, pátio de manobra, pé-direito total e útil, tipo e
resistência do piso, estrutura, cobertura, energia disponível, rede trifásica, capacidade
elétrica, subestação, gerador, abastecimento de água, poço artesiano, esgoto, gás, ar
comprimido, ponte rolante e capacidade, escritórios, vestiários, refeitório,
estacionamento, frente de vitrine, fluxo de pessoas, acesso e distância da rodovia e
infraestrutura existente.

### Documentação do imóvel
Matrícula e livro, cartório e comarca, inscrição municipal, número e valor do IPTU,
situação e isenção, concessionária e número da ligação de água, concessionária e número da
instalação de energia, condomínio com valor, administradora e contato, escritura, habite-se,
planta aprovada, alvarás, certidões, certidão negativa, ônus e gravames, financiamento com
banco e saldo devedor, inventário, usucapião e, para imóveis rurais, georreferenciamento,
CCIR/INCRA, ITR e CAR.

**Anexos:** PDF, imagens, Word, Excel, DWG e outros formatos, classificados por tipo
(matrícula, escritura, IPTU, planta, alvará, habite-se, AVCB, licença, certidão, contrato,
autorização, documento pessoal, laudo), com validade e marcação de confidencialidade.

### Valores e negociação
Valor de venda, de locação, de condomínio, de IPTU com periodicidade, **valor mínimo para
negociação** (interno), valor de avaliação, comissão em % e em R$, condições de pagamento e
observações. Marcações para **financiamento, FGTS, permuta, veículo, parcelamento e
consórcio**, com campo livre para descrever o que o proprietário aceita em permuta.

O campo *Mostrar valor no site* permite anunciar o imóvel com "valor sob consulta".

### Fotos
Upload de várias fotos ao mesmo tempo (arrastar e soltar), ordenação, escolha da **foto
principal**, legenda, classificação por ambiente e marcação de **quais fotos podem ser
usadas na divulgação** e quais são somente para arquivo interno. As fotos internas nunca
são servidas publicamente.

### Compradores e interessados
Perfil de busca com finalidade, categorias, tipos desejados, cidades, bairros, condomínios,
faixa de valor, áreas mínimas e máximas, dormitórios, suítes, banheiros, vagas,
características desejadas, atividades pretendidas, forma de pagamento, necessidade de
financiamento, valor de entrada, imóvel que possui para vender, prazo e prioridade.

**Cruzamento automático:** o sistema calcula um percentual de compatibilidade entre cada
perfil e os imóveis disponíveis, mostrando exatamente **o que atende e o que não atende**.
Funciona nos dois sentidos. É possível registrar a indicação e acompanhar sua situação
(sugerido, enviado, visitou, gostou, descartado).

### Visitas, propostas e atendimentos
- **Visitas:** data e hora, cliente, corretor, situação, nível de interesse e feedback.
- **Propostas:** valor proposto, entrada, forma de pagamento, condições, validade e
  situação, com cálculo automático da diferença em relação ao valor pedido. Ao aceitar uma
  proposta, aparece o botão **Gerar negociação**, que já leva imóvel, proponente, valor
  aceito e condições de pagamento.
- **Atendimentos:** ligações, WhatsApp, e-mail, contato presencial, com assunto, descrição
  e **próximo contato programado** — que aparece na lista de retornos da visão geral.

### Negociações
O centro do processo. Cada negociação de venda ou locação reúne, em abas:

- **Partes:** comprador, vendedor, locador, locatário, fiador, interveniente, anuente e
  procurador — com percentual de participação e indicação do titular principal.
- **Pagamento:** composição do preço (sinal, entrada, financiamento, FGTS, recursos
  próprios, carta de crédito, permuta), banco, prazos de sinal, entrada, financiamento,
  assinatura e posse, responsabilidades sobre ITBI, escritura e certidões. O sistema avisa
  quando a composição **não fecha** com o valor total.
- **Cronograma de parcelas:** gerado automaticamente a partir das condições, ou editado
  linha a linha, com distribuição do valor restante e baixa individual de cada parcela.
- **Documentos:** checklist gerado conforme o tipo de negociação e as partes envolvidas,
  com situação por documento (pendente, recebido, em análise, aprovado, recusado,
  dispensado) e barra de progresso.
- **Contratos:** todos os documentos gerados para aquela negociação.
- **Comissões:** apuração com um clique, usando o percentual do imóvel.
- **Histórico:** tudo o que aconteceu, com autor e data.

Mudar o status da negociação **reflete automaticamente no imóvel** (em negociação →
vendido/alugado → de volta a disponível em caso de cancelamento).

### Modelos de documento
Biblioteca de textos-base com um editor de texto formatado (negrito, itálico, títulos,
listas, tabelas) e **mais de 110 variáveis** que o sistema preenche sozinho:

```
{{NOME_COMPRADOR}}  {{CPF_VENDEDOR}}  {{QUALIFICACAO_COMPRADOR}}
{{ENDERECO_IMOVEL}} {{MATRICULA}}     {{DESCRICAO_IMOVEL}}
{{VALOR_TOTAL}}     {{VALOR_TOTAL_EXTENSO}}  {{TABELA_PARCELAS}}
{{DATA_HOJE_EXTENSO}}  {{IMOBILIARIA_CRECI}}  ...
```

Os valores por extenso são escritos pelo próprio sistema em português correto
(*"oitocentos e cinquenta e cinco mil reais"*), inclusive para percentuais e datas.

Acompanham **7 modelos prontos**: compromisso de compra e venda, contrato de locação
residencial, recibo de sinal, termo de entrega de chaves, termo aditivo, distrato e
autorização de venda e divulgação.

> Os modelos são um **ponto de partida editável**. Revise as cláusulas com seu advogado e
> ajuste à sua prática e à legislação vigente antes de usar em negócios reais.

### Contratos
Gerados a partir de um modelo, já com as variáveis resolvidas. Cada contrato tem:

- **Editor próprio** com barra de formatação e um botão para inserir variáveis, mostrando
  o valor atual de cada uma. Um aviso lista as variáveis **sem valor**, indicando o que
  falta completar no cadastro.
- **Prévia preenchida** e **PDF** gerado pelo sistema, com cabeçalho da imobiliária,
  texto justificado, tabela de parcelas e campos de assinatura.
- **Controle de versão:** cada alteração relevante vira uma versão, com resumo do que
  mudou, autor e data — e pode ser restaurada.
- **Partes congeladas:** os dados das pessoas são copiados no momento da geração. Alterar o
  cadastro do cliente depois **não muda** o contrato assinado.
- **Assinaturas:** por assinante, com situação (pendente, enviado, visualizado, assinado,
  recusado, expirado), meio de assinatura e data. Quando todos assinam, o contrato é
  marcado como assinado e a versão é congelada — daí em diante o texto não é mais editável,
  só aditado.
- **Aditivos e distratos** vinculados ao contrato original.

### Locações
Contrato em vigor com locador, locatário, fiador, corretor, aluguel, condomínio, IPTU e de
quem é a responsabilidade de cada encargo, dia de vencimento, índice e periodicidade de
reajuste, vigência com cálculo automático do término, tipo de garantia (fiador, caução,
seguro-fiança, título), taxa de administração e responsabilidades acordadas.

- **Cobranças:** geração dos lançamentos mensais de aluguel, condomínio e IPTU por período
  escolhido, sem duplicar competências já geradas. Baixa e estorno por título.
- **Reajuste:** aplicado por percentual ou por novo valor (um calcula o outro na tela),
  com índice, data de vigência e histórico completo.
- **Vistorias:** entrada, saída, intermediária e manutenção, com link direto para o laudo.
- **Encerramento:** normal ou distrato, com motivo, data e devolução do imóvel para
  disponível.

O painel avisa sobre **locações vencendo em 90 dias**, **reajustes vencidos** conforme a
periodicidade do contrato e **locações sem vistoria de entrada**.

### Análise cadastral e de crédito para locação
Fica entre a proposta e o contrato: reúne renda, documentos, garantia e crédito do
pretendente num processo único, com **parecer registrado por uma pessoa**.

- **Pretensão congelada:** aluguel e encargos ficam gravados na análise, porque renda e
  pretensão mudam a cada tentativa de locação. Ao abrir a análise a partir do imóvel, o
  sistema traz os valores do cadastro e **converte o IPTU anual em mensal**.
- **Composição de renda:** titular, cônjuge, fiador e terceiros, cada fonte com valor
  declarado e valor comprovado. **Só a renda com comprovante entra no cálculo.**
- **Indicadores explicados:** comprometimento de renda (custo mensal ÷ renda comprovada) e
  renda sobre o aluguel, cada um mostrando a conta e o critério cadastrado. Nenhum número
  aparece sozinho.
- **Documentos exigidos:** lista gerada a partir dos critérios por perfil (pessoa física,
  pessoa jurídica, cônjuge, fiador), configuráveis em Configurações. Anexar marca como
  *recebido* — nunca como aprovado.
- **Conferência com apoio de leitura automática:** o sistema lê PDFs com camada de texto,
  valida CPF pelos dígitos, compara o nome tolerando acentos e abreviaturas e confere
  prazos. O resultado é **sugestão**: quem aprova é o analista.
- **Garantia:** fiador (com o imóvel dado em garantia), caução, seguro-fiança ou título,
  cada modalidade conferida contra o critério configurado.
- **Crédito:** registro da consulta feita no portal do provedor, com fonte, data,
  protocolo e o PDF em anexo. **Consulta exige consentimento do titular.**
- **Parecer:** aprovado, aprovado com ressalvas, necessita complementação ou não aprovado
  — sempre com justificativa escrita, autor, data e validade. Análise decidida trava para
  edição; reabrir exige motivo e preserva o parecer anterior no histórico.
- **Relatório em PDF** com tudo o que foi apurado, as contas, as pendências e o parecer.

**O que o sistema não faz, e por quê.** Ele não gera score nem consulta bureau
automaticamente: Serasa, Boa Vista, SPC e Quod não têm API pública, e inventar um número
para preencher a tela seria pior do que não ter. A arquitetura está pronta para ligar uma
integração real (ver `app/bureau.py`); até então, a consulta é feita no portal do provedor
e registrada aqui, com a fonte identificada. E o sistema **não decide**: ele confere,
calcula, aponta pendências e explica cada número — a aprovação é de quem assina o parecer.

#### LGPD
Consentimento do titular registrado com forma, data, validade e autorização específica
para consulta de crédito; revogação a qualquer momento. Toda visualização e todo download
de documento ficam registrados (quem, quando, qual arquivo), e documento pessoal nunca vai
para o cache do navegador. O prazo de guarda é configurável (12 meses por padrão) e o
**expurgo é assistido**: o sistema aponta o que venceu o prazo ou teve o consentimento
revogado, mostra exatamente o que será apagado e o que será mantido, e espera confirmação
de uma pessoa — nada é apagado automaticamente. Depois do expurgo permanecem o código, o
vínculo, o parecer e a auditoria; os dados pessoais e financeiros, não.

### Aplicativo instalável (PWA)
O sistema pode ser instalado na tela inicial do celular: abre com um toque, em tela cheia,
com o ícone e o nome da imobiliária. Os ícones são **gerados pelo próprio sistema** (mesmo
desenho do favicon, em PNG escrito à mão) e o manifesto é montado pelo servidor para
carregar o nome configurado.

O aplicativo guarda apenas o **casco** — HTML, CSS, JavaScript e ícones — para abrir rápido
e mostrar um aviso decente quando falta conexão. **Nenhuma resposta da API e nenhum
documento são guardados no aparelho**, e o servidor reforça isso enviando `no-store` nos
documentos pessoais. Um celular perdido não vira um vazamento de ficha cadastral. Como
consequência, o sistema não funciona offline: os dados ficam no servidor.

A instalação automática pelo navegador só acontece em `https://` ou `localhost` — por
endereço de rede local, use "Adicionar à tela inicial", que tem o mesmo efeito prático.
Ver `COMO-EXECUTAR.md`.

### Vistorias e laudos
Módulo pensado para ser usado **no celular, dentro do imóvel**.

Ao criar a vistoria, o sistema **sugere os ambientes** conforme a categoria do imóvel e os
dormitórios, suítes, banheiros e vagas cadastrados — e, em cada ambiente, os **itens de
conferência** típicos (piso, parede, teto, porta, janela, tomada, iluminação, torneira,
louça, metais, armário, bancada, box, esquadria, pintura, tubulação, elétrica…).

A execução é ambiente por ambiente: a lista lateral mostra o que já foi vistoriado, cada
item abre uma ficha com estado de conservação (novo, ótimo, bom, regular, ruim, danificado),
material, cor, quantidade, funcionamento, descrição e **ressalva**. Um botão salva o item e
abre a câmera para fotografar. Itens com problema ficam destacados em vermelho.

- **Medidores e chaves:** leitura de água, energia e gás e relação de chaves entregues.
- **Fotos:** por ambiente ou por item, com legenda, e todas entram no laudo.
- **Conclusão:** ao concluir, a vistoria fica somente leitura (pode ser reaberta) e o
  **laudo em PDF** passa a ser gerado — com identificação completa, medidores, tabela de
  itens por ambiente com estado e observações, galeria de fotos e campos de assinatura.
- **Comparação entrada × saída:** com um clique, o sistema confronta item a item as duas
  vistorias e classifica cada linha como sem alteração, alteração, dano, reparo, melhoria
  ou faltante. Você ajusta a **responsabilidade** (locatário, locador, desgaste natural) e
  o **custo estimado** do reparo, e o total serve de base para o desconto na caução.

### Financeiro
Contas a receber e a pagar com tipo, categoria (aluguel, condomínio, IPTU, sinal, entrada,
parcela, financiamento, comissão, taxa de administração, repasse, seguro, manutenção,
reforma, multa, juros), valor, vencimento, competência e vínculo com imóvel, cliente,
corretor, contrato, locação ou negociação.

- Lançamento avulso com **repetição mensal** automática.
- **Baixa** com valor, data e forma de pagamento; pagamento parcial vira situação
  "parcial"; **estorno** desfaz a baixa.
- Títulos vencidos são marcados como atrasados automaticamente.
- Resumo do mês, total a receber e a pagar, atrasados, **receita recorrente** dos aluguéis
  vigentes, vencimentos dos próximos dias e distribuição por categoria.

### Comissões
Apuração sobre o valor do negócio, com percentual vindo do imóvel, e **rateio** entre
captador, vendedor, gerência, parceiro, indicação e imobiliária — por percentual ou por
valor, com distribuição automática e aviso quando a soma não fecha 100%.

O pagamento de cada parte gera a **despesa correspondente no financeiro**, e a comissão
passa a parcial ou paga conforme os rateios são liquidados.

### Agenda e tarefas
- **Agenda:** calendário mensal e lista por período, com visitas, vistorias, assinaturas,
  reuniões, prazos, entregas de chaves e pagamentos. Cada compromisso pode estar ligado a
  cliente, imóvel, corretor, contrato, vistoria ou visita. Clique duplo num dia agenda ali.
- **Tarefas:** o que precisa ser feito, com tipo, prioridade, prazo, responsável e vínculo.
  Marcar como concluída é um clique. Atrasadas aparecem destacadas e no painel.

### Auditoria
Trilha de **quem fez o quê, quando e o que mudou** em todo o sistema: criações, alterações
(com valor anterior e novo), exclusões, mudanças de situação e acessos. Filtros por
cadastro, ação, período, número do registro e usuário, com detalhe de cada evento, link
para o registro afetado e exportação da página em CSV.

### Histórico do imóvel
Registra automaticamente: cadastro, alterações de valor (de → para), mudanças de status,
troca de proprietário, publicação e retirada do anúncio, propostas recebidas, visitas,
fotos e documentos adicionados. Também aceita anotações manuais.

### Pesquisa e filtros
**Imóveis:** código, proprietário, captador, corretor, cidade, bairro, condomínio, distrito
industrial, tipo, categoria, finalidade, status, faixa de valor, área construída, área útil,
área do terreno, dormitórios, suítes, banheiros, vagas, ano de construção, situação de
ocupação, características, atividades, pé-direito mínimo, número de docas, acesso para
carreta, rede trifásica, com ou sem fotos, publicados, em destaque, exclusivos e formas de
negociação aceitas.

**Clientes:** nome, CPF/CNPJ, telefone, WhatsApp, e-mail, cidade, tipo de pessoa, papel,
origem, corretor responsável e se possui imóveis.

Cada módulo novo tem seus próprios filtros (situação da captação, status da negociação,
tipo e status de contrato, locações vencendo, vistorias em aberto, categoria e situação
financeira, prioridade da tarefa…).

Há também uma **busca rápida no topo** (atalho `/`) que procura em imóveis e clientes ao
mesmo tempo.

### Visão geral
Além dos indicadores de carteira (imóveis disponíveis, em negociação, vendidos, alugados,
publicados, clientes, compradores, visitas, propostas, valor da carteira), o painel traz um
bloco de **negociação, contratos, locação e financeiro**: captações em andamento,
negociações ativas com valor em jogo, fechamentos do mês, contratos a assinar, locações
vigentes e a vencer, vistorias em aberto, a receber, em atraso, comissões a pagar,
compromissos de hoje e tarefas abertas.

Listas de acompanhamento: contratos aguardando conclusão, títulos em aberto, locações a
vencer, próximos compromissos, tarefas a fazer, vistorias em andamento com barra de
progresso, últimos imóveis, próximas visitas, retornos a fazer e atividade recente.

E um bloco de **pontos de atenção** que junta tudo o que está travando o processo: imóveis
sem foto, visitas atrasadas, imóveis não publicados, títulos vencidos, documentos
obrigatórios pendentes, assinaturas aguardando, locações vencendo, reajustes vencidos,
locações sem vistoria de entrada, autorizações de venda vencendo e tarefas atrasadas.

### Usuários e permissões
Papéis: administrador, gerente, corretor, captador, assistente e **vistoriador**.
**46 permissões granulares** controlam quem pode cadastrar, alterar, excluir, ver
documentos, ver informações internas, ver e alterar valores e comissões, alterar status,
publicar imóveis, editar contratos, assinar, concluir vistorias, mexer no financeiro,
gerenciar modelos e consultar a auditoria.

A matriz de permissões por papel é editável e cada usuário pode ter **exceções
individuais**. As restrições são aplicadas no servidor: dados que o usuário não pode ver
não são enviados ao navegador, e módulos sem permissão respondem "acesso restrito".

### Fichas para impressão e arquivo
- **Ficha completa** (uso interno): todos os dados, documentação, características, valores,
  comissões, informações internas, proprietário, captador, fotos, visitas, propostas e
  histórico.
- **Ficha comercial** (apresentação ao cliente): somente as informações autorizadas para
  divulgação.
- **Ficha do cliente**: dados cadastrais, imóveis, perfis de busca e histórico.
- **Contratos e laudos de vistoria em PDF**, gerados pelo próprio sistema.

### Divulgação e site
O sistema já inclui um **site público pronto** em `/site`, com busca, filtros, cards,
página de detalhe do imóvel, galeria de fotos e botão de WhatsApp. Publica apenas imóveis
com título, descrição e foto liberada.

Para integrar a um site próprio, há uma **API pública em JSON**:

```
GET /api/publico/imoveis          # lista com filtros e paginação
GET /api/publico/imoveis/IM0001   # detalhe por código
GET /api/publico/filtros          # opções disponíveis para montar os filtros
```

Esses endpoints nunca expõem proprietário, captador, valor mínimo, comissão, observações
internas ou documentos.

---

## Estrutura do projeto

```
imobiliaria/
├── run.py                  Ponto de entrada
├── app/
│   ├── schema.sql          Modelo de dados original (25 tabelas)
│   ├── schema_v2.sql       Plataforma integrada + análise de locação (36 tabelas)
│   ├── migracao.py         Migração aditiva e idempotente (com backup)
│   ├── catalogos.py        Tipos, características, atividades, domínios, permissões
│   ├── config.py           Caminhos e parâmetros
│   ├── db.py               Acesso ao SQLite
│   ├── utils.py            Validações (CPF/CNPJ), conversões, formatação
│   ├── seguranca.py        Senhas (PBKDF2), sessões, permissões
│   ├── auditoria.py        Trilha universal de alterações
│   ├── creci.py            Padronização e controle do registro profissional
│   ├── extenso.py          Valores, datas e percentuais por extenso em português
│   ├── modelos.py          Motor de variáveis dos documentos
│   ├── modelos_padrao.py   Os 7 modelos que acompanham o sistema
│   ├── pdf.py              Gerador de PDF próprio (contratos e laudos)
│   ├── analise.py          Cálculos da análise de locação (única fonte dos números)
│   ├── extrator.py         Leitura de PDF e conferência de documentos
│   ├── bureau.py           Registro de consulta de crédito e integração plugável
│   ├── relatorio_analise.py Relatório da análise em PDF
│   ├── pwa.py              Ícones e manifesto do aplicativo instalável
│   ├── http_core.py        Requisição, resposta, upload multipart, roteador
│   ├── servidor.py         Servidor HTTP
│   ├── rotas.py            Registro das 240 rotas
│   ├── html.py             Geração das fichas
│   ├── midia_demo.py       Gerador de PNG e PDF de demonstração
│   ├── demo.py             Dados de demonstração (cadastros)
│   ├── demo_v2.py          Dados de demonstração (ciclo completo)
│   └── api/                Endpoints por módulo — 26 arquivos
├── web/
│   ├── index.html
│   ├── css/app.css
│   └── js/
│       ├── app.js          Roteamento, menu, sessão
│       ├── api.js          Cliente da API
│       ├── ui.js           Componentes e formatação
│       ├── estado.js       Catálogos e permissões
│       ├── icones.js       Ícones SVG
│       ├── cep.js          Preenchimento de endereço pelo CEP
│       ├── instalar.js     Aplicativo instalável e aviso de conexão
│       └── paginas/        26 páginas
├── web/sw.js               Service worker (guarda só o casco, nunca dados)
├── web/icones/             Ícones do aplicativo, gerados pelo sistema
└── dados/                  Criado na primeira execução
    ├── imobiliaria.db
    └── uploads/{fotos,documentos,laudos}
```

**Números:** 61 tabelas, 242 rotas, 53 permissões, 69 domínios de catálogo, ~24.700 linhas
de Python e ~16.200 linhas de JavaScript — sem uma única dependência externa.

### Backup
Copie a pasta `dados/` — contém o banco e todos os arquivos enviados.

Ao atualizar um sistema que **já tinha cadastros**, a migração guarda automaticamente
`dados/imobiliaria-antes-v2.db` como cópia de segurança do banco anterior. Em instalação
nova o arquivo não é criado: não havia nada a preservar, e um banco vazio na pasta só
confundiria quem a abre.

---

## Como acrescentar um módulo

1. Crie a tabela em `app/schema_v2.sql` (sempre `CREATE TABLE IF NOT EXISTS`).
2. Se precisar de colunas novas em tabelas existentes, declare em `COLUNAS_NOVAS`
   (`app/migracao.py`) — a migração é aditiva e nunca apaga dados.
3. Crie o arquivo em `app/api/` e registre em `app/rotas.py`.
4. Acrescente as permissões em `PERMISSOES_V2` e o papel, se houver, em `PAPEIS_V2`.
5. Crie a página em `web/js/paginas/`, registre o `import()` em `web/js/app.js` e
   acrescente a entrada em `DEFINICAO_MENU`.
6. Some os métodos novos em `web/js/api.js`.

---

## Notas técnicas

- **Segurança:** senhas com PBKDF2-SHA256 (210.000 iterações), sessões em cookie HttpOnly
  com expiração, SQL sempre parametrizado, uploads com nome aleatório e extensão
  validada, proteção contra travessia de diretório e filtragem de campos por permissão
  no servidor.
- **Compatibilidade:** Python 3.9 ou superior, sem dependências externas.
- **Internet:** o sistema funciona 100% offline. A única funcionalidade que usa internet é
  a busca de CEP (ViaCEP e BrasilAPI), com tempo limite de 4 segundos por serviço, cache
  em banco e degradação silenciosa — sem conexão, o cadastro continua normal por
  digitação manual. Nenhum dado do sistema é enviado: só o CEP consultado.
- **PDF:** gerador próprio, com as fontes padrão do PDF (Helvetica), texto justificado por
  espaçamento entre palavras, tabelas, imagens JPEG e PNG e paginação automática.
- **Valores em português:** o sistema aceita `R$ 1.250.000,00`, `1.250.000`, `1250000` e
  `150,75` nos campos numéricos.
- **Uploads:** limite de 25 MB por arquivo (ajustável em `IMOB_MAX_UPLOAD_MB`).

### Variáveis de ambiente

| Variável | Padrão | Função |
|---|---|---|
| `IMOB_HOST` | `0.0.0.0` | Endereço de escuta |
| `IMOB_PORT` | `8000` | Porta |
| `IMOB_DATA_DIR` | `dados` | Pasta de dados e uploads |
| `IMOB_SESSION_HORAS` | `12` | Duração da sessão |
| `IMOB_MAX_UPLOAD_MB` | `25` | Tamanho máximo de arquivo |
| `IMOB_ADMIN_EMAIL` | `admin@imobiliaria.com.br` | E-mail do primeiro administrador |
| `IMOB_ADMIN_SENHA` | `admin123` | Senha do primeiro administrador |
