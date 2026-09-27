Antes de escrever o `workspace.dsl` preciso resolver um ponto que muda o modelo — não quero chutar. Segue o que já está claro e as perguntas que faltam.

## O que já está classificado (não precisa confirmar, só corrigir se algo estiver errado)

- **Pessoa:** Cliente — usa o app mobile para fazer e acompanhar pedidos.
- **Sistema em foco:** OrderFlow (workspace com `scope softwaresystem`).
  - **Containers:** `criar-pedido`, `listar-pedidos` e `webhook-pagamento` (cada função Lambda é um container — tecnologia "AWS Lambda - Python") e a tabela `orders` (Amazon DynamoDB, estilizada como banco). As três funções leem e escrevem na tabela.
- **Stripe:** sistema externo (caixa fechada, cinza) que chama `webhook-pagamento`.
- **Amazon API Gateway:** como é só roteamento e auth por API key, não entra na view de containers. Ele aparece nas deployment views como `infrastructureNode`, com o roteamento app → gateway → Lambdas feito via `-/>`.
- **Deployment views:**
  - **Development:** Laptop do desenvolvedor → LocalStack → serviços API Gateway, Lambda (3 funções) e DynamoDB (tabela `orders`).
  - **Production:** Amazon Web Services → us-east-1 → Amazon API Gateway, AWS Lambda (3 funções) e Amazon DynamoDB (tabela `orders`).
- **Views:** `SystemContext`, `Containers`, `Deployment-Development`, `Deployment-Production` (contexto e containers são o par sempre recomendado no C4; as duas de deployment são as que você pediu).

## O que preciso que você responda

1. **Quem constrói o app Flutter?** Se é o seu time (mesmo repo/mesmo ciclo de entrega do OrderFlow), ele vira um **container** do OrderFlow ("App Mobile", Flutter) e aparece na view de containers. Se é de outro time ou de outra empresa, vira um **sistema externo** e o OrderFlow o vê como caixa fechada. Isso muda tanto a view de contexto quanto a de containers, por isso não escolhi por você.
2. **Alguma Lambda chama a API do Stripe?** Por exemplo, `criar-pedido` criando o pagamento no Stripe. Você só descreveu o caminho Stripe → webhook; se existir a chamada de saída, eu desenho, senão fica só a entrada.
3. **Em dev, o webhook do Stripe chega no laptop** (ex.: `stripe listen` encaminhando para o LocalStack) **ou não é exercitado localmente?** Define se o Stripe aparece na deployment view de dev ou só na de produção.

Assim que você responder, escrevo o `workspace.dsl` na raiz do repositório, valido com `docker run --rm structurizr/structurizr validate` e te passo o comando para abrir a UI de preview em `http://localhost:8080`.
