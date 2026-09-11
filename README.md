# 🩺 Medical RAG Chatbot

An end-to-end **Retrieval-Augmented Generation (RAG) Medical Chatbot** that retrieves relevant information from medical documents and generates context-aware answers using a Large Language Model.

The project also implements a complete CI/CD workflow using **Docker, Jenkins, Trivy, AWS ECR, AWS Systems Manager, and Amazon EC2**.

> **Disclaimer:** This project is intended for educational and demonstration purposes and should not be used as a substitute for professional medical advice.

---

## 🚀 Project Overview

Traditional LLMs may generate answers based only on their training knowledge and can hallucinate information.

This project uses **Retrieval-Augmented Generation (RAG)** to first retrieve relevant information from a medical knowledge base and then provide that context to the LLM before generating an answer.

The application supports:

- Medical PDF document ingestion
- Text chunking
- Semantic embeddings
- FAISS vector search
- Context-based response generation
- Flask web interface
- Docker containerization
- Jenkins CI/CD
- Trivy image vulnerability scanning
- AWS ECR image storage
- Automatic deployment to EC2 through AWS Systems Manager

---

## 🧠 RAG Architecture

```text
Medical PDF Documents
        ↓
PyPDFLoader
        ↓
RecursiveCharacterTextSplitter
        ↓
Text Chunks
        ↓
all-MiniLM-L6-v2 Embeddings
        ↓
FAISS Vector Database
        ↓
User Question
        ↓
Semantic Similarity Search
        ↓
Top-K Relevant Chunks
        ↓
Prompt + Retrieved Context
        ↓
Qwen LLM
        ↓
Context-Aware Answer
```

---

## ⚙️ CI/CD Architecture

```text
Developer
    ↓
GitHub Repository
    ↓
Jenkins Pipeline
    ↓
Docker Image Build
    ↓
Trivy Security Scan
    ↓
AWS ECR
    ↓
AWS Systems Manager (SSM)
    ↓
Amazon EC2
    ↓
Pull Latest Docker Image
    ↓
Run Medical RAG Chatbot
```

---

## 🛠️ Technology Stack

| Area | Technology |
|---|---|
| Programming | Python |
| Web Framework | Flask |
| RAG Framework | LangChain |
| Embedding Model | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| LLM | Qwen/Qwen3-4B-Instruct-2507 |
| Model Provider | Hugging Face |
| Containerization | Docker |
| CI/CD | Jenkins |
| Security Scanning | Trivy |
| Container Registry | AWS ECR |
| Deployment | Amazon EC2 |
| Remote Deployment | AWS Systems Manager (SSM) |
| Cloud | AWS |

---

## 📂 Project Structure

```text
RAG-MEDICAL-CHATBOT/
│
├── app/
│   ├── application.py
│   ├── components/
│   ├── common/
│   ├── config/
│   └── templates/
│
├── custom_jenkins/
│
├── data/
│
├── vectorstore/
│   └── db_faiss/
│
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── setup.py
├── .gitignore
├── .dockerignore
└── README.md
```

---

## 🔍 How RAG Works

### 1. Document Loading

Medical PDF documents are loaded using `PyPDFLoader`.

### 2. Text Chunking

Documents are divided into smaller chunks using:

```text
RecursiveCharacterTextSplitter
Chunk Size: 500
Chunk Overlap: 50
```

Chunking makes the documents suitable for embedding and semantic retrieval.

### 3. Embeddings

Each chunk is converted into a numerical vector using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### 4. Vector Storage

The generated embeddings are stored in **FAISS**, which enables efficient similarity search.

### 5. Retrieval

When the user asks a question, the question is embedded and FAISS retrieves the most relevant chunks.

The retriever uses:

```text
k = 3
```

### 6. Response Generation

The retrieved context and user question are passed to:

```text
Qwen/Qwen3-4B-Instruct-2507
```

The model generates an answer using the retrieved medical context.

---

## 💻 Running Locally

### Clone the repository

```bash
git clone https://github.com/tallojarshith/RAG-MEDICAL-CHATBOT.git
cd RAG-MEDICAL-CHATBOT
```

### Create a virtual environment

```bash
conda create -n medi python=3.10 -y
conda activate medi
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file:

```text
HF_TOKEN=your_huggingface_token
FLASK_SECRET_KEY=your_secret_key
```

Never commit the `.env` file to GitHub.

### Run the application

```bash
python -m app.application
```

The application runs on port `5000`.

---

## 🐳 Docker

The application is containerized using Docker.

Build the image:

```bash
docker build -t medical-rag-chatbot .
```

Run:

```bash
docker run -p 5000:5000 --env-file .env medical-rag-chatbot
```

The Docker image uses **CPU-only PyTorch** to reduce unnecessary GPU dependencies and image size.

---

## 🔄 Jenkins CI/CD Pipeline

The Jenkins pipeline automates the deployment process.

The pipeline performs:

```text
1. Checkout source code from GitHub
2. Build Docker image
3. Scan Docker image using Trivy
4. Authenticate with AWS
5. Push Docker image to Amazon ECR
6. Send deployment command using AWS SSM
7. EC2 pulls the latest image
8. Existing container is replaced
9. Updated chatbot starts automatically
```

This removes the need to manually SSH into EC2 for every deployment.

---

## 🔐 Security

Several security practices are implemented:

- Hugging Face tokens are stored as environment variables.
- `.env` is excluded from Git.
- Secrets are not embedded inside Docker images.
- EC2 uses an IAM role instead of static AWS credentials.
- EC2 has read-only access to Amazon ECR.
- AWS Systems Manager is used for remote deployment.
- Jenkins uses restricted SSM permissions.
- Docker images are scanned with Trivy.
- Port `5000` is not publicly exposed on EC2.
- SSH access is restricted to the administrator's IP.
- Public users access the application only through HTTP port `80`.

---

## 🧩 Major Challenges Solved

### LangChain Package Changes

Newer LangChain versions moved several components into separate packages.

Examples:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

and retrieval-chain utilities are provided through `langchain_classic`.

### Hugging Face Provider Compatibility

Several instruction models were tested before selecting a model compatible with the available inference provider.

Final model:

```text
Qwen/Qwen3-4B-Instruct-2507
```

### Docker Image Optimization

The initial Docker build pulled large GPU-related PyTorch dependencies.

The application was changed to use the CPU-only PyTorch wheel, significantly reducing unnecessary dependencies.

A `.dockerignore` was also introduced to prevent the virtual environment and development files from being included in the Docker build context.

### Python Module Import in Docker

Running:

```text
python app/application.py
```

caused module-resolution issues inside the container.

It was changed to:

```text
python -m app.application
```

### Automated AWS Deployment

Instead of storing AWS credentials on EC2, an IAM role provides ECR and SSM permissions.

Jenkins sends deployment commands through AWS Systems Manager, allowing EC2 to automatically pull and start the latest image.

---

## 📈 Future Improvements

- Use Gunicorn instead of the Flask development server.
- Add HTTPS with a domain name.
- Add an Application Load Balancer.
- Introduce automated tests before Docker builds.
- Add monitoring with Prometheus and Grafana.
- Add conversation-aware retrieval.
- Add source citations to chatbot responses.
- Implement reranking for retrieved documents.
- Add evaluation metrics for RAG quality.
- Configure vulnerability thresholds in Trivy to block unsafe deployments.

---

## 🎯 Key Learning Outcomes

This project demonstrates practical experience with:

- Retrieval-Augmented Generation
- Embeddings and vector databases
- LangChain
- Large Language Models
- Prompt engineering
- Flask application development
- Docker
- CI/CD pipelines
- Container vulnerability scanning
- AWS IAM
- Amazon ECR
- Amazon EC2
- AWS Systems Manager
- Cloud deployment and debugging

---

## 👨‍💻 Author

**Talloj Harshith**

M.Tech Data Science  
SVNIT Surat