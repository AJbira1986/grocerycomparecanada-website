# 🛒 GroceryCompare - Ontario Grocery Price Comparison

**Find the best grocery prices across Ontario's major chains!**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/AJbira1986/grocerycomparecanada-website)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![React](https://img.shields.io/badge/React-18.2.0-61dafb.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-000000.svg)](https://flask.palletsprojects.com/)

## 🎯 Overview

GroceryCompare helps Ontario families save money on groceries by comparing prices across major grocery chains including **Walmart**, **Loblaws**, **Metro**, **No Frills**, **Costco**, and **Food Basics**.

Simply enter your postal code, search for products, and instantly see where you can find the best deals near you!

## ✨ Features

- 🏪 **Store Locator**: Find nearby grocery stores based on your postal code
- 🔍 **Smart Product Search**: Intelligent search with fuzzy matching
- 💰 **Price Comparison**: Compare prices across multiple stores
- 📱 **Mobile Responsive**: Optimized for all devices
- ⚡ **Fast Performance**: Sub-second search results

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ with npm
- Python 3.11+ with pip
- Git for version control

### Frontend (React)

```bash
cd grocery-price-frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend (Flask)

```bash
cd grocery-price-api
pip install -r requirements.txt
python src/main.py
```

The backend API will be available at `http://localhost:5002`

## 📁 Project Structure

```
grocerycomparecanada-website/
├── 📁 grocery-price-frontend/    # React frontend application
│   ├── src/                      # Source code
│   ├── public/                   # Static assets
│   ├── package.json              # Dependencies
│   └── .env.development          # Development environment
│
├── 📁 grocery-price-api/         # Flask backend API
│   ├── src/                      # Source code
│   │   ├── models/               # Database models
│   │   └── routes/               # API endpoints
│   ├── requirements.txt          # Python dependencies
│   └── .env.example              # Environment template
│
├── 📁 docs/                      # Documentation
└── README.md                     # This file
```

## 🌐 Live Website

- **Frontend**: https://grocerycompare.ca
- **API**: https://api.grocerycompare.ca

## 🛠️ Technology Stack

### Frontend
- **React 18.2.0** - Modern JavaScript framework
- **Tailwind CSS 3.3.0** - Utility-first CSS framework
- **Vite 4.4.5** - Fast build tool and dev server
- **Radix UI** - High-quality component library

### Backend
- **Python 3.11** - Programming language
- **Flask 2.3.3** - Lightweight web framework
- **SQLAlchemy 2.0** - Database ORM
- **PostgreSQL** - Database storage

## 📚 Documentation

See the `docs/` folder for comprehensive documentation:

- **Technical Documentation** - Developer guide and API reference
- **User Guide** - How to use GroceryCompare
- **Deployment Guide** - Step-by-step deployment instructions

## 🚀 Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Select the `grocery-price-frontend` folder
3. Deploy with automatic builds on push

### Backend (Railway)

1. Connect your GitHub repository to Railway
2. Select the `grocery-price-api` folder
3. Add environment variables
4. Deploy with automatic PostgreSQL database

## 🔧 Environment Variables

### Frontend (.env.development)
```bash
VITE_API_BASE_URL=http://localhost:5002/api
VITE_ENVIRONMENT=development
```

### Backend (.env.example)
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
CORS_ORIGINS=https://grocerycompare.ca
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all the grocery chains for providing public pricing information
- Built with amazing open-source tools and libraries
- Special thanks to the Ontario families who will save money using this tool

## 📞 Support

- **Issues**: Report bugs or request features on GitHub Issues
- **Email**: Contact us at support@grocerycompare.ca
- **Documentation**: Check the `docs/` folder for detailed guides

---

**Start saving money on groceries today with GroceryCompare!** 🛒💰

