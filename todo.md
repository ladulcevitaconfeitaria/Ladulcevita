# TODO - CLUBE LA DULCE VITA

**Etapa 001: Pesquisar sites CRM Bônus e Fidelizi**
- [X] Pesquisar site oficial CRM Bônus
- [X] Explorar site CRM Bônus (Giftback, CRM360, etc.)
- [X] Pesquisar site oficial Fidelizi
- [X] Explorar site Fidelizi (foco PMEs, segmentos alimentícios)

**Etapa 002: Analisar perfis Instagram La Dulce Vita**
- [X] Tentar acessar Instagram @ladulcevitaoficial
- [X] Tentar acessar Instagram @healthypizzaldv
- [X] Pesquisar "la dulce vita confeitaria saudavel em fortaleza" no Google
- [X] Analisar resultados da busca (TripAdvisor, Linktree, iFood, etc.)
- [X] Analisar Linktree para identidade visual e estrutura de negócio

**Etapa 003: Analisar funcionalidades e estrutura para setor alimentício**
- [X] Criar documento `analise_funcionalidades.md` com base nas referências e requisitos

**Etapa 004: Planejar arquitetura do site CLUBE LA DULCE VITA**
- [X] Criar estrutura inicial do projeto Flask (`create_flask_app`)
- [X] Criar arquivo `todo.md` com o plano detalhado
- [X] Definir modelos de banco de dados (User, Purchase, Segment, DiscountRule) em `src/models/`
- [X] Definir rotas/blueprints (auth, main, user, crm) em `src/routes/`
- [X] Planejar estrutura do frontend (HTML, CSS, JS) em `src/static/`
- [X] Atualizar `src/main.py` (registrar blueprints, habilitar DB)

**Etapa 005: Desenvolver frontend com identidade visual da marca**
- [X] Criar HTML básico para as páginas (index, register, login, dashboard, profile, benefits)
- [X] Estilizar páginas com CSS (cores, fontes, layout) baseado na identidade visual
- [X] Adicionar logo e imagens relevantes
- [X] Implementar interações básicas com JavaScript

**Etapa 006: Implementar sistema cadastro e CRM com segmentação**
- [X] Implementar modelos do banco de dados (SQLAlchemy)
- [X] Criar migrações/inicializar banco de dados
- [X] Implementar rotas de autenticação (registro, login, logout)
- [X] Implementar funcionalidade de visualização/edição de perfil
- [X] Implementar backend para visualização de histórico de compras/pontos
- [X] Implementar funcionalidade de segmentação de clientes (admin)

**Etapa 007: Configurar sistema descontos cumulativos**
- [X] Implementar lógica de cálculo de pontos/bônus por compra
- [X] Implementar modelo `DiscountRule`
- [X] Implementar funcionalidade para admin configurar regras de desconto
- [X] Implementar lógica para aplicar descontos

**Etapa 008: Implementar integração WhatsApp por segmentação**
- [X] Pesquisar e escolher API do WhatsApp Business (ou alternativa)
- [X] Implementar funcionalidade de envio de mensagens para segmentos (admin)
- [X] Garantir conformidade com políticas do WhatsApp

**Etapa 009: Testar funcionalidades e corrigir bugs**
- [X] Corrigir bugs encontrados (erros de sintaxe nos templates)

**Etapa 010: Finalizar e entregar projeto**
- [X] Preparar ambiente para deploy (atualizar `requirements.txt`)
- [X] Realizar deploy (perguntar ao usuário sobre deploy permanente)
- [X] Enviar URL de acesso e arquivos do projeto ao usuário
- [X] Verificar `todo.md` e remover itens não concluídos/pulados
- [X] Entrar em estado ocioso (`idle`)
