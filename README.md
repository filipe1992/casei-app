### Descrição para Repositório do App de Organização de Casamentos  

---

**Nome do Projeto**: **WeddingPlanner**  
**Descrição**: Uma plataforma web completa para organização de casamentos, conectando noivos, convidados e equipe de recepção com ferramentas intuitivas para gestão do evento.  

---

### ✨ Recursos Principais  

#### 👰 **Área dos Noivos (Login Protegido)**  
- **Cadastro de Convidados**: Nome (obrigatório) + telefone (opcional)  
- **Editor de Convites**: Textos personalizados com placeholders `[nome]` + links de vídeo (YouTube/Vimeo)  
- **Linha do Tempo Interativa**:  
  - Eventos com datas, textos, fotos e vídeos  
  - Layout com linha central e elementos alternados (+ responsivo)  
- **Lista de Presentes Virtuais**:  
  - Presentes fictícios (imagem, título, valor)  
  - Integração com PIX (QR Code ou chave copiável)  
- **Dashboard de Confirmações**:  
  - Gráficos de % de confirmados vs. pendentes  
  - Lista filtrada por status  
- **Álbum de Fotos Compartilhado**:  
  - Vinculação com Google Drive/Microsoft OneDrive  
  - Opção de upload direto (via API)  

#### 📱 **Interface do Convidado (Sem Login)**  
- **Convite Personalizado**:  
  - Mensagem dinâmica com nome do convidado + botão de confirmação  
- **Menu Principal**:  
  - 📜 Linha do Tempo dos Noivos (história multimídia)  
  - 🕒 Cronograma do Evento (ordem de atividades + dress code)  
  - 🎁 Lista de Presentes (seleção + simulação de pagamento via PIX)  
  - 📸 Desafios Fotográficos (checklist + upload para álbum)  
- **Contagem Regressiva**:  
  - "Faltam [XX] dias!" destacado no cabeçalho  

#### 🎫 **Painel do Recepcionista (Acesso via Link Especial)**  
- Busca instantânea de convidados  
- Geração de QR Code individual para check-in  
- Marcação automática de presença  

---

### 🛠 Stack Tecnológica  
| Área          | Tecnologias                                                                 |
|---------------|-----------------------------------------------------------------------------|
| **Frontend**  | React.js + TypeScript, Tailwind CSS, Framer Motion (animações)             |
| **Backend**   | Node.js (Express), PostgreSQL (Prisma ORM), Firebase Authentication        |
| **Cloud**     | AWS S3 (armazenamento), Google Drive API (álbum de fotos)                  |
| **Bibliotecas**| `react-qrcode`, `react-vertical-timeline`, `react-hook-form`, `Chart.js`   |
| **DevOps**    | Docker, GitHub Actions (CI/CD), Vercel (deploy)                            |

---

### ⚙️ Como Executar Localmente  
```bash
# 1. Clonar repositório
git clone https://github.com/seu-usuario/weddingplanner.git

# 2. Configurar variáveis de ambiente (backend)
cp .env.example .env
# Preencher credenciais do banco e APIs

# 3. Iniciar containers
docker-compose up -d

# 4. Instalar dependências (frontend)
cd frontend && npm install

# 5. Executar
npm run dev  # Frontend (localhost:3000)
npm run start # Backend (localhost:5000)
```

---

### 📂 Estrutura de Diretórios  
```markdown
weddingplanner/
├── backend/
│   ├── src/
│   │   ├── controllers/  # Lógica de endpoints
│   │   ├── models/       # Schemas do banco
│   │   ├── routes/       # Definição de rotas
│   │   └── utils/        # Helpers (geração QR Code, etc.)
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/   # UI reutilizável
│       ├── pages/        # Telas principais
│       │   ├── Admin/    # Painel dos noivos
│       │   ├── Guest/    # Interface convidado
│       │   └── Reception # Painel recepcionista
│       ├── contexts/     # Gestão de estado (Auth, Convidados)
│       └── services/     # Chamadas API
│
└── docker-compose.yml    # Configuração Docker
```

---

### 🌟 Diferenciais  
- **Privacidade Garantida**: Links únicos por convidado (sem exposição pública)  
- **Otimizado para Mobile**: PWA com suporte offline para áreas do evento  
- **Zero Configuração**: Recepcionista acessa via link direto (sem login)  
- **Integração Pix Instantânea**: Geração automática de QR Codes para presentes  

---

### 📄 Licença  
MIT License - Livre para uso e modificação. Atribuição opcional.  

**Nota**: Projeto voltado para fins educacionais e portfólio. Para uso comercial, recomenda-se validação jurídica de fluxos financeiros.  

--- 

> ✨ "Transformando momentos especiais em experiências digitais inesquecíveis"