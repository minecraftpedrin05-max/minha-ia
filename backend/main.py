from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./usuarios.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

OWNERS = [
    "minecraftpedrin05@gmail.com",
    "bloxpedro22@gmail.com",
    "pedrohenryqueferreiracruz@gmail.com"
]

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    nome = Column(String)
    mensagens_usadas = Column(Integer, default=0)
    ultimo_reset = Column(DateTime, default=datetime.now)
    metodo_login = Column(String)
    codigo_verificacao = Column(String, nullable=True)
    verificado = Column(Integer, default=0)
    is_owner = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

class LoginRequest(BaseModel):
    email: str
    nome: str
    metodo: str

class ChatRequest(BaseModel):
    email: str
    mensagem: str
    tipo: str

def chamar_ia_real(mensagem: str) -> str:
    """
    Chama uma IA real em vez de apenas repetir a mensagem.
    Suporta: OpenAI, Claude, Ollama ou outro modelo.
    """
    api_key = os.getenv("IA_API_KEY", None)
    ia_provider = os.getenv("IA_PROVIDER", "mock")
    
    if ia_provider == "openai" and api_key:
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": mensagem}]
            }
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json=data,
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Erro ao chamar IA: {str(e)}"
    
    elif ia_provider == "ollama":
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "mistral", "prompt": mensagem},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()["response"]
        except Exception as e:
            return f"Erro ao chamar Ollama: {str(e)}"
    
    # Mock/padrão
    return f"Nexus IA: {mensagem[:100]}... [Resposta real será gerada com API configurada]"

@app.post("/login")
def login(request: LoginRequest):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    
    if not usuario:
        is_owner = 1 if request.email in OWNERS else 0
        usuario = Usuario(
            email=request.email,
            nome=request.nome,
            metodo_login=request.metodo,
            verificado=1,
            is_owner=is_owner
        )
        db.add(usuario)
        db.commit()
    
    return {"status": "logado", "usuario": usuario.nome, "is_owner": usuario.is_owner}

@app.post("/chat")
def chat(request: ChatRequest):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Não autenticado")
    
    if usuario.mensagens_usadas >= 200:
        tempo_espera = 20 if request.tipo == "facil" else 180
        proximo_reset = usuario.ultimo_reset + timedelta(minutes=tempo_espera)
        
        if datetime.now() < proximo_reset:
            tempo_falta = (proximo_reset - datetime.now()).total_seconds() / 60
            return {
                "status": "limite_atingido",
                "tempo_espera_minutos": int(tempo_falta)
            }
        else:
            usuario.mensagens_usadas = 0
            usuario.ultimo_reset = datetime.now()
    
    usuario.mensagens_usadas += 1
    db.commit()
    
    # CORRIGIDO: Chama IA real em vez de apenas repetir
    resposta = chamar_ia_real(request.mensagem)
    
    return {
        "status": "sucesso",
        "resposta": resposta,
        "mensagens_restantes": 200 - usuario.mensagens_usadas
    }

@app.get("/info")
def info(email: str):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {
        "nome": usuario.nome,
        "mensagens_usadas": usuario.mensagens_usadas,
        "mensagens_restantes": 200 - usuario.mensagens_usadas,
        "metodo_login": usuario.metodo_login,
        "is_owner": bool(usuario.is_owner)
    }
