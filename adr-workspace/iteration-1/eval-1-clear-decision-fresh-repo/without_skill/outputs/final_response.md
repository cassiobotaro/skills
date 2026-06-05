Criei o primeiro ADR do repositório documentando a decisão de usar PostgreSQL no lugar de MongoDB no serviço de pedidos.

## O que foi feito

Como o repositório ainda não tinha nenhum ADR, criei a estrutura padrão de diretórios e o ADR numerado a partir de 0001, usando o formato Michael Nygard (o mais difundido para ADRs):

- `docs/adr/0001-use-postgresql-instead-of-mongodb-for-the-orders-service.md`

## Conteúdo do ADR

- **Status:** Accepted
- **Context:** descreve que o fluxo de criação de pedido atualiza estoque, pagamento e pedido de forma conjunta e precisa ser atômico, o que exige transação ACID multi-registro. Compara MongoDB x PostgreSQL e registra os fatores adicionais: experiência do time com Postgres e o uso já existente (e já pago) do RDS.
- **Decision:** usar PostgreSQL (no Amazon RDS) como datastore principal, com o fluxo de criação de pedido envolvido em uma única transação ACID.
- **Consequences:**
  - Positivas: garantias ACID no fluxo multi-escrita, reuso da experiência do time, reuso da infraestrutura RDS já paga.
  - Negativas: schema mais rígido e migrações como passo explícito de deploy.

## Observações

- A data usada no ADR foi 2026-06-04.
- O título do arquivo segue a convenção `NNNN-titulo-em-kebab-case.md`, começando em `0001` por ser o primeiro ADR.
- Caso você já use alguma ferramenta de ADR (como `adr-tools`) ou prefira outro formato/idioma para os ADRs, posso ajustar o template.
