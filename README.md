# ComplianceCopilot 🚀

**ComplianceCopilot** is an AI-powered platform that enables organizations to quickly review documents, flag compliance risks, and generate summaries using rentable, on-demand AI review agents. The platform streamlines regulatory and internal audits with real-time insights.

---

## Table of Contents
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [High-Level Flow (MVP)](#high-level-flow-mvp)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Technology Partners](#technology-partners)
- [Business Model](#business-model)
- [Roadmap](#roadmap)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

---

## Problem Statement
Regulated industries face significant compliance challenges:

- Manual document reviews are slow and costly.
- Outsourcing reviews introduces security risks.
- AI tools for compliance are siloed and difficult to access.

**Need:** On-demand, trustworthy compliance document review agents.

---

## Solution
**ComplianceCopilot** provides rentable AI agents that securely review documents, highlight compliance risks, and generate summaries.

Key points:

- **Pay-as-you-go rental:** Hourly or per document.
- **Powered by Coral Protocol & containerized agents.**
- **Integrated with Solana Pay** for instant payments.
- Returns annotated reviews and actionable compliance insights.

---

## Features
- **Rental AI agents** for on-demand compliance reviews.
- **Secure token-based rental system** using JWT.
- **Real-time dashboard** with live logs and remaining rental time.
- **Document upload** with multi-agent analysis.
- **SSE (Server-Sent Events)** for real-time updates.

---

## High-Level Flow (MVP)
1. User connects Solana wallet (Phantom/Backpack).  
2. User selects rental option (hourly/per-document).  
3. Solana Pay payment request is generated.  
4. Backend verifies payment and issues JWT access token.  
5. Rented agent runs in a container and accepts document uploads.  
6. Returns annotated results until rental expires.

---

## Technology Stack
- **Frontend:** HTML, CSS, JavaScript (wallet adapter + Solana Pay SDK)  
- **Backend:** Python (FastAPI)  
- **Agents:** Coral Protocol containers  
- **Blockchain:** Solana (devnet → mainnet)  
- **Smart Contracts:** Anchor (escrow, NFT rental passes)  
- **Storage:** S3/MinIO (documents), optional Arweave/IPFS  
- **Deployment:** Vercel/Netlify + Docker + cloud provider

---

## System Architecture
**Components:**
- Frontend: Wallet connect, document upload, rental timer
- Backend: FastAPI server, JWT issuance, payment verification
- Solana Pay integration: Payment verification
- Agent containers: Document analysis and annotation
- Admin dashboard: Active rentals, logs

---

## Technology Partners
- **AI/ML API:** Reduces cost/time and provides compliance analysis.  
- **Mistral AI:** Fine-tuned LLMs for legal/compliance content.  
- **Nebius AI Studio:** Compute and inference for large documents.  
- **Crossmint:** Token and wallet integration, payment management.

---

## Business Model
**Target Users:**  
- Law firms  
- Financial institutions  
- Compliance-heavy industries  

**Revenue Streams:**  
- Hourly or per-document rental fees  
- Enterprise subscriptions for bulk access  
- Premium features: Escrow, long-term audit storage

---

## Roadmap
**MVP (Hackathon):**  
- Wallet connect + Solana Pay demo  
- JWT rental issuance  
- Single agent document review  

**Next Steps:**  
- Time-limited NFT rental passes  
- Escrow smart contracts  
- Agent orchestration via Coral Protocol  
- Full dashboard + enterprise pilots

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js & npm (optional, for frontend builds)
- Git
- Solana wallet (Phantom/Backpack)

### Installation
1. Clone the repository:  
```bash
git clone https://github.com/<your-username>/ComplianceCopilot.git
cd ComplianceCopilot

###pip install -r requirements.txt

JWT_SECRET=your-secret-key
DEV_MODE=true
SOLANA_RECEIVER=DemoReceiver1

uvicorn main:app --reload --port 8000

###Usage

1.Enter your wallet address.

2.Click Create Payment.

3.Click Verify Payment (dev) to get JWT.

4.Upload documents for AI analysis.

5.Monitor logs and countdown in real-time.

###License

MIT License © 2025 ComplianceCopilot

Contact

Project Lead: Linda Mosemaka

Email:linda.mosemaka@gmail.com.com


