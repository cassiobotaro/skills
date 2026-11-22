Escrevi o ADR da decisão e, como o repositório não tinha nenhum ADR, criei também o log em `doc/adr/`. Não rodei `adr list` nem nenhuma ferramenta sobre os arquivos.

- `doc/adr/0001-registrar-decis-es-de-arquitetura.md` é o ADR inicial padrão, que registra que o projeto passa a usar ADRs. Traduzi o título e o corpo para português.
- `doc/adr/0002-usar-postgresql-em-vez-de-mongodb-no-servi-o-de-pedidos.md` é o ADR da sua decisão, com status `Accepted` e data de hoje (2026-11-22).

O ADR 0002 usa só o que você me contou:
- **Contexto:** a criação de pedido atualiza estoque, pagamento e pedido juntos e precisa de transação ACID. O time já tem experiência com PostgreSQL e a empresa já paga o RDS.
- **Decisão:** usar PostgreSQL, no RDS, no serviço de pedidos, em vez de MongoDB.
- **Consequências:** a transação ACID passa a cobrir o fluxo de criação de pedido, e o time usa uma tecnologia que já conhece. Em troca, o schema fica mais rígido e as migrações viram um passo do deploy.

Escrevi a prosa em português, mas mantive em inglês `Date:`, os títulos `## Status`, `## Context`, `## Decision` e `## Consequences` e a palavra `Accepted`. As ferramentas de ADR, como adr-tools e o importador do Structurizr, leem esses termos em inglês. Os nomes dos arquivos perdem as letras acentuadas (`decis-es`, `servi-o`) porque o adr-tools gera o slug só com letras e dígitos ASCII.

Não coloquei alternativas além do MongoDB nem detalhes que você não mencionou. Se houve outras opções na discussão, me conte e eu adiciono. Como o ADR já está aceito, o corpo não deve mais ser editado depois. Uma mudança futura vira um novo ADR que o substitui.
