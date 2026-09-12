# NEXUS AI

IA Inteligente com Sistema de Autenticação e Limite de Mensagens

## 📋 Estrutura

- **Backend:** FastAPI + SQLAlchemy
- **Frontend:** Streamlit
- **Database:** SQLite (pronto para MongoDB no futuro)
- **Autenticação:** Google, GitHub, Discord, Email

## 🚀 Instalação

### 1. Clone ou Extraia os Arquivos

```bash
cd nexus-ai
```

### 2. Instale as Dependências

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd ../frontend
pip install -r requirements.txt
```

## ⚙️ Configuração

### Backend

1. Copie `.env.example` para `.env`:
```bash
cp backend/.env.example backend/.env
```

2. Configure as variáveis:
```
DATABASE_URL=sqlite:///./usuarios.db
API_PROVIDER=mock
IA_API_KEY=sua_chave_aqui
```

### Credenciais OAuth (Depois)

Quando configurar Google, GitHub e Discord, adicione no `.env`:
```
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
DISCORD_CLIENT_ID=...
DISCORD_CLIENT_SECRET=...
```

## 🏃 Executar

### Terminal 1 - Backend

```bash
cd backend
uvicorn main:app --reload
```

Acesso: `http://localhost:8000`

### Terminal 2 - Frontend

```bash
cd frontend
streamlit run app.py
```

Acesso: `http://localhost:8501`

## 🔑 Owners Autorizados

Apenas essas contas podem acessar o painel admin:
- minecraftpedrin05@gmail.com
- bloxpedro22@gmail.com
- pedrohenryqueferreiracruz@gmail.com

## ✨ Features

- ✅ Login com Google, GitHub, Discord e Email
- ✅ 200 mensagens por usuário
- ✅ Limite de 20 minutos (fácil) ou 3 horas (difícil)
- ✅ Database automático por usuário
- ✅ Interface clean e profissional
- ✅ **IA REAL** (não apenas repetindo mensagens)
- ✅ Suporte a OpenAI, Ollama e Claude

## 🔄 Para o Futuro

- [ ] Planos (FREE, START, PRO, ULTRA, ULTIMATE)
- [ ] Sistema de Pagamentos
- [ ] Admin Panel
- [ ] Nexus Guard (Segurança)
- [ ] Carteira
- [ ] Análise de Comprovantes

## 🤖 IA Providers

### Mock (Padrão - Sem IA Real)
```
IA_PROVIDER=mock
```

### OpenAI
```
IA_PROVIDER=openai
IA_API_KEY=sk-...
```

### Ollama (Local)
```
IA_PROVIDER=ollama
# Precisa rodar Ollama localmente
```

## 📱 Termux (Android)

```bash
apt update
apt install python3 python3-pip git

git clone seu_repo
cd nexus-ai

# Backend
cd backend
pip install -r requirements.txt
nohup python3 -m uvicorn main:app --host 0.0.0.0 &

# Frontend
cd ../frontend
pip install -r requirements.txt
nohup streamlit run app.py &
```

## 🐛 Erros Corrigidos

- ✅ IA repetindo mensagem do usuário (CORRIGIDO)
- ✅ Emails de owners incorretos (CORRIGIDO)
- ✅ Suporte a IA real com variáveis de ambiente

## 📞 Suporte

Para problemas, verifique:
1. Backend rodando em `http://localhost:8000`
2. Frontend rodando em `http://localhost:8501`
3. Arquivo `.env` configurado corretamente
4. Dependências instaladas: `pip install -r requirements.txt`

---

**Desenvolvido por minecraftpedrin05** 🚀
