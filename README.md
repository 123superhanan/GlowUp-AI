Here is everything completely merged into one single, clean, production-ready `README.md` file. It includes the fixed GitHub table alignments, the correct spacing, your project structure, your tech stack, and your contact information.

Copy and paste the entire block below directly into your file:

```markdown
# StockWise - AI-Powered Inventory Management

**Smart receipt scanning + demand forecasting for small businesses**

## Overview

StockWise helps small business owners automate inventory tracking by scanning receipts. The AI extracts products, quantities, and prices, then updates stock levels automatically. A demand forecaster predicts future sales and sends reorder alerts.

## Problem Solved

Small business owners waste hours manually entering receipts into spreadsheets. Stockouts cost sales. Overstock ties up cash. StockWise solves both.

## Features

| Feature | Description |
| :--- | :--- |
| Receipt Scanner | Take photo → AI extracts items, prices, date, total |
| Inventory Tracking | Auto-updates stock levels from receipts |
| Demand Forecast | Predicts next week's sales using LSTM/Prophet |
| Low Stock Alerts | Push notification when stock falls below threshold |
| Sales Analytics | Dashboard with trends and insights |

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| Frontend | React Native (Expo) |
| Backend | Node.js + Express |
| AI Service | FastAPI (Python) |
| Database | Supabase (PostgreSQL) |
| ML Models | YOLOv8, LayoutLM, LSTM |
| OCR | PaddleOCR |
| Deployment | Render + Hugging Face |

## Architecture


```

Receipt Photo → YOLOv8 (detect) → PaddleOCR (read text) → LayoutLM (extract) → Database → LSTM (forecast) → Alert

```

## Project Structure


```

stockwise/
├── frontend/           # React Native mobile app
├── backend/            # Node.js API server
│   ├── controllers/    # Route handlers
│   ├── models/         # Database models
│   ├── routes/         # API endpoints
│   └── middleware/     # Auth, upload
├── ai-service/         # Python FastAPI + ML models
│   ├── models/         # Trained YOLO/LayoutLM
│   └── services/       # OCR, prediction
└── docs/               # Documentation

```

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | /api/receipts/upload | Upload receipt image |
| GET | /api/receipts | List all receipts |
| GET | /api/products | Get inventory |
| POST | /api/products | Add product |
| GET | /api/predictions/:id | Get demand forecast |

## Database Schema

- **businesses** - Company details, subscription tier
- **products** - Name, stock level, threshold, price
- **receipts** - Image URL, merchant, total, date
- **receipt_items** - Product name, quantity, price
- **sales** - Quantity sold, date, revenue
- **predictions** - Forecasted quantity, confidence interval

## ML Models Trained

| Model | Task | Dataset | Accuracy |
| :--- | :--- | :--- | :--- |
| YOLOv8 | Receipt detection | 500 annotated images | 94% |
| LayoutLM | Info extraction | SROIE (1000 receipts) | 89% F1 |
| LSTM | Demand forecast | Proprietary sales data | MAE: 5.2 units |

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Supabase account (free)

### Installation

```bash
# Clone repository
git clone [https://github.com/yourusername/stockwise.git](https://github.com/yourusername/stockwise.git)
cd stockwise

# Backend setup
cd backend
npm install
npm run dev

# AI service setup (new terminal)
cd ai-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Frontend setup (new terminal)
cd frontend
npm install
npx expo start

```

### Environment Variables

Create `.env` files:

**backend/.env**

```
PORT=5000
SUPABASE_URL=your_url
SUPABASE_ANON_KEY=your_key
JWT_SECRET=your_secret

```

**ai-service/.env**

```
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
MODEL_PATH=./models

```

## Training Your Own Models

### YOLOv8 Receipt Detector

```bash
cd ai-service
python train_yolo.py --data dataset.yaml --epochs 100 --img 640

```

### LayoutLM Extractor

```bash
python train_layoutlm.py --dataset sroie --epochs 20 --batch_size 8

```

### LSTM Forecaster

```bash
python train_lstm.py --window 30 --epochs 50

```

## Deployment

| Service | Platform | Cost |
| --- | --- | --- |
| Backend | Render | Free |
| AI Service | Hugging Face Spaces | Free |
| Database | Supabase | Free (500MB) |
| Storage | Supabase | Free (1GB) |

## Future Improvements

* [ ] Multi-language receipt support
* [ ] WhatsApp integration for alerts
* [ ] Accounting software export (QuickBooks)
* [ ] Barcode scanning
* [ ] Team accounts

## Contributors

* Abdul Hanan

## License

MIT

## Contact

Email: abdulhananabbasi50@gmail.com

---

**Built with:** React Native, Node.js, FastAPI, PyTorch, Supabase

```

```
