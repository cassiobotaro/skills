Escrevi o doc em `docs/design/exportacao-de-relatorios-em-background.md`. Você me deu a substância toda — problema com número, solução, alternativas descartadas com o porquê, o custo aceito e os times impactados —, então fui direto para a escrita em vez de te entrevistar.

O que está lá:

- **Contexto e objetivos** com os seus números: 12% de falha acima de 50 mil linhas, timeout de 30s no gateway, ticket semanal no suporte; objetivos medíveis (zerar falhas por timeout, aguentar 100 mil linhas) e o "manter um caminho síncrono para exportações pequenas" escrito como exclusão explícita, já que é justamente o que a decisão abre mão.
- **Arquitetura** como diagrama de containers C4, autorado em Structurizr DSL (validado), renderizado em PNG (`docs/design/diagrams/arquitetura-containers.png`) com a fonte dobrada num `<details>` logo abaixo — quem edita o modelo acha a fonte, quem só lê vê a figura.
- **Fluxo** da exportação como diagrama Mermaid (renderiza direto no GitHub/GitLab), validado — [prévia editável](https://l.mermaid.ai/wQsZ1O). Ele mostra só o caminho feliz, e o doc diz isso na cara: retentativa, falha na geração e e-mail não entregue não foram definidos, então não inventei ramo de erro nenhum.
- **Trade-offs** com os três ✓ e os três ✗, incluindo o custo que vocês aceitaram (fim do download imediato, inclusive para exportação pequena) e dois que decorrem do desenho: mais peças para operar e dado de cliente passando a repousar no S3.
- **Alternativas** numa tabela com as duas que vocês descartaram, mais "não fazer nada" refutado pelos seus próprios números.
- **Preocupações transversais** separadas para Plataforma (fila compartilhada, rajada de exportação longa) e Segurança (link assinado com PII trafegando por e-mail) — é o convite para esses times revisarem cedo.

Deixei em aberto o que não dava para preencher sem inventar, e essas são as perguntas que valem mais a sua resposta:

1. Quem assina como autor, e quem revisa por Plataforma e por Segurança? Deixei os nomes como "a definir" no cabeçalho.
2. Qual a validade do link assinado e por quanto tempo os arquivos ficam no S3? Segurança vai perguntar isso primeiro.
3. O que acontece quando a geração falha no meio — retentativa, fila de mensagens não processadas, aviso ao usuário?
4. O usuário acompanha a exportação em andamento de alguma forma, ou o e-mail é o único sinal?
5. Como vocês pretendem verificar o resultado antes de subir (teste de carga com 100 mil linhas?) e o que vão monitorar em produção para provar que os timeouts foram a zero?

Me responde o que já estiver decidido que eu incorporo no corpo do doc e tiro da lista de questões em aberto.
