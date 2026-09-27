Antes de escrever o `workspace.dsl`, preciso fechar um ponto que muda a estrutura de todas as views — não quero chutar. Segue como classifiquei o que já está claro e as perguntas que faltam.

## O que já está claro (classificação C4)

| Elemento | Classificação | Motivo |
|---|---|---|
| Cliente | `person` | Humano que usa o sistema pelo app |
| OrderFlow | `softwareSystem` (escopo do workspace) | A API serverless de pedidos que vocês constroem |
| criar-pedido, listar-pedidos, webhook-pagamento | 3 `container` (AWS Lambda - Python) | Cada função serverless é uma unidade que roda sozinha |
| Tabela DynamoDB `orders` | `container` (Amazon DynamoDB, tag `Database`) | Data store; as três Lambdas leem e escrevem nela |
| Stripe | `softwareSystem` externo | SaaS de terceiro que chama o webhook |
| Amazon API Gateway | `infrastructureNode` nas deployment views | Só roteamento e auth por API key, nada custom — é infraestrutura, não aparece na view de containers |
| Dev | `deploymentEnvironment` "Development": laptop do dev → LocalStack → Lambdas e DynamoDB | Como você descreveu |
| Produção | `deploymentEnvironment` "Production": AWS → us-east-1 → API Gateway, AWS Lambda, Amazon DynamoDB | Como você descreveu |

Views: System Context (recomendada sempre), Containers, `Deployment-Development` e `Deployment-Production`.

## O que decide o resto — preciso de você

1. **Quem constrói o app Flutter?** Se é o seu time (mesmo repo/ciclo de vida do OrderFlow), ele entra como um `container` dentro do OrderFlow, aparece na view de containers e ganha uma instância no "smartphone do cliente" na deployment view de produção. Se é outro time ou fornecedor, ele vira um `softwareSystem` externo (caixa fechada) que consome a API. Essa é a diferença entre as duas versões do arquivo.
2. **Em dev, o que roda de fato no LocalStack?** Só as Lambdas e o DynamoDB, ou também a emulação do API Gateway (os devs chamam as funções pelo gateway emulado ou direto)?
3. **Em dev, o app e o Stripe participam?** Por exemplo, app no emulador apontando pro LocalStack e Stripe CLI encaminhando webhooks pro laptop — ou a deployment view de dev deve mostrar só o backend?

Com essas três respostas eu escrevo o `workspace.dsl` completo e valido com `docker run ... structurizr/structurizr validate` antes de entregar.
