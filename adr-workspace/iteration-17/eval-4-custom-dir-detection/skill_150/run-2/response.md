Escrevi o ADR 3 em `docs/architecture/decisions/0003-version-the-public-api-by-url-path.md`, com status `Accepted` e data 2026-11-22. Foi o único arquivo criado ou alterado.

- **Idioma:** o log existente (ADRs 1 e 2) está em inglês, então o texto do ADR 3 também está em inglês, para o log não ficar misturado. Os rótulos (`Date:`, `## Status` etc.) seguem o padrão do adr-tools.
- **Conteúdo:** o Context traz os três motivos que você deu: SDKs já esperam a versão na URL, roteamento por versão no gateway, e a versão fica visível em logs e `curl`. A Decision diz que a versão vai na URL e que mantemos no máximo duas versões ativas. As Consequences listam os pontos positivos e os dois contras que vocês anotaram: URLs que proliferam e o limite de duas versões.
- **Acréscimo meu:** a frase final das Consequences, de que aposentar a versão mais antiga precisa ser planejado a cada lançamento, é uma dedução do limite de duas versões, não algo que você disse. Se não refletir o que o time pensa, é só tirar.
- **Relação com o ADR 2:** ele não foi substituído nem alterado. REST continua valendo e o ADR 3 só define como versionar.
