Criei o design doc em `docs/design/exportacao-relatorios-em-background.md`, em português, no estado Rascunho. Não executei nenhuma verificação nem renderizei o diagrama de containers.

**O que entrou, só com o que você me contou:**
- O problema: o timeout de 30s no gateway, os 12% de falha acima de 50 mil linhas e o ticket semanal do suporte.
- Os objetivos: zerar os timeouts, aguentar 100 mil linhas e ter um caminho único de exportação.
- A solução: API enfileira o job, worker gera CSV/XLSX em streaming, S3 guarda o arquivo e o e-mail leva o link assinado.
- Um diagrama de containers e um diagrama de sequência do fluxo.
- Os trade-offs e as alternativas, com "não fazer nada" incluído, e as preocupações transversais de Plataforma e Segurança.

**O que ficou como questão em aberto, porque você não me deu:**
- O que fica fora de escopo.
- A validade do link assinado, a retenção do arquivo no S3 e quem pode baixar.
- Se o job usa fila própria ou a mesma dos outros times, e se há limite por usuário.
- Retentativa, aviso de falha e duplicidade de pedido.
- Qual serviço envia o e-mail.
- O plano de entrega e rollback, e os testes e alertas.
- Como o usuário acompanha o pedido entre o clique e o e-mail.

Vale olhar estes pontos:
- **Autor e revisores:** pus `cassiobotaro` (do git) como autor e só as áreas Plataforma e Segurança como revisores. Falta você colocar os nomes.
- **Diagrama de containers:** a imagem `diagrams/exportacao-containers.svg` ainda não existe. O código em Structurizr DSL está dobrado logo abaixo do placeholder, para renderizar depois. Deixei sem tecnologia o box do e-mail.
- **Edição de estilo:** passei o `unslop` no texto. Só tirei negritos de ênfase, e não achei travessões nem outros vícios.
- **Commit:** não commitei nada.

Se você me der as respostas das questões de segurança e de infraestrutura, eu passo cada uma para o corpo do doc e tiro da lista de questões em aberto.
