# 🌧️ Rain Paris

**Minute-by-minute rain forecasts for Paris arrondissements**

A clean, minimalist weather app inspired by DarkSky, built specifically for Paris. Get hyperlocal rain predictions for any of the 20 Paris arrondissements with minute-by-minute accuracy.

![Rain Paris Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=Rain+Paris)

## ✨ Features

- 🎯 **Hyperlocal forecasts** - Separate predictions for each of the 20 Paris arrondissements
- ⏱️ **Minute-by-minute** - Know exactly when rain will start or stop
- 🎨 **Beautiful UI** - Clean, Apple/Notion-inspired design
- ⚡ **Fast & Lightweight** - No heavy frameworks, pure performance
- 💻 **CLI tool** - Quick terminal access: `rainparis 11`
- 🌐 **Web interface** - Elegant web app with interactive charts

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Tomorrow.io API key (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/rainparis.git
   cd rainparis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**

   Create a `.env` file in the project root:
   ```bash
   echo "TOMORROW_API_KEY=your_api_key_here" > .env
   ```

   Get your free API key at [tomorrow.io](https://www.tomorrow.io/)

4. **You're ready!** Choose your interface:

## 🖥️ Web Interface

Start the web server:

```bash
python server.py
```

Then open http://localhost:5000 in your browser.

### Features

- Select any Paris arrondissement from dropdown
- Large, readable temperature display
- DarkSky-style rain summaries ("Rain starting in 8 minutes")
- Interactive precipitation chart
- Responsive design - works on mobile

## 💻 CLI Tool

### Basic Usage

```bash
./rainparis 2
```

Output:
```
📍 2ème - Bourse, Paris
🌡️  13°C
☀️  Dry (0.0 mm/hr)
☀️  No rain expected in the next hour

Updated: 17:19
```

### Commands

**Check a specific arrondissement:**
```bash
./rainparis 11
```

**Verbose mode (minute-by-minute breakdown):**
```bash
./rainparis 11 -v
```

**List all arrondissements:**
```bash
./rainparis --list
```

**Get help:**
```bash
./rainparis --help
```

### Installing globally

To use `rainparis` from anywhere:

```bash
pip install -e .
```

Now you can run `rainparis` from any directory!

## 📍 Paris Arrondissements

The app covers all 20 Paris arrondissements:

1. **Louvre** - Historic center
2. **Bourse** - Financial district
3. **Temple** - Arts et Métiers
4. **Hôtel-de-Ville** - City Hall area
5. **Panthéon** - Latin Quarter
6. **Luxembourg** - Saint-Germain-des-Prés
7. **Palais-Bourbon** - Eiffel Tower area
8. **Élysée** - Champs-Élysées
9. **Opéra** - Department stores
10. **Entrepôt** - Canal Saint-Martin
11. **Popincourt** - Bastille
12. **Reuilly** - Bercy
13. **Gobelins** - Bibliothèque Nationale
14. **Observatoire** - Montparnasse
15. **Vaugirard** - Largest arrondissement
16. **Passy** - Trocadéro
17. **Batignolles-Monceau** - Parc Monceau
18. **Buttes-Montmartre** - Sacré-Cœur
19. **Buttes-Chaumont** - Parc des Buttes-Chaumont
20. **Ménilmontant** - Père Lachaise

## 🛠️ How It Works

Rain Paris uses the [Tomorrow.io Weather API](https://www.tomorrow.io/) with the **Météo-France AROME** model for hyperlocal French forecasts.

### Technical Stack

**Backend:**
- Flask - Lightweight web framework
- Python 3.9+
- Tomorrow.io API integration

**Frontend:**
- Vanilla HTML/CSS/JavaScript
- Chart.js for visualizations
- No heavy frameworks - pure performance

**Data:**
- Real-time weather conditions
- Minute-by-minute forecasts (next hour)
- Coordinates for all 20 Paris arrondissements from OpenDataSoft

## 📊 API Rate Limits

Tomorrow.io free tier:
- **25 requests/hour** (most restrictive)
- 500 requests/day
- 3 requests/second

The app caches data for 30 minutes to stay within limits.

## 🚀 Deployment

Want to deploy Rain Paris to production? See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed guides:

- **Railway** (recommended) - Easy Python deployment
- **Cloudflare** - Connect your domain
- **Alternatives** - Render, Fly.io

**TL;DR:** Deploy to Railway, point your Cloudflare domain → Done!

## 🔧 Development

### Project Structure

```
rainparis/
├── server.py              # Flask backend
├── rainparis              # CLI tool
├── arrondissements.py     # Coordinates data
├── templates/
│   └── index.html         # Web UI template
├── static/
│   ├── css/
│   │   └── style.css      # Minimalist styles
│   └── js/
│       └── app.js         # Frontend logic
├── .env                   # API key (not in git)
├── requirements.txt       # Python dependencies
└── README.md
```

### Running Tests

```bash
python test_api.py                    # Test API connection
python test_arrondissement.py         # Test multiple locations
```

### Development Mode

The Flask server runs in debug mode by default:

```bash
python server.py
```

Changes to Python files will auto-reload.

## 🎨 Design Philosophy

Rain Paris is inspired by:

- **DarkSky** - Simple, accurate rain predictions
- **Apple Design** - Clean typography, generous whitespace
- **Notion** - Minimalist UI, subtle gradients

Design principles:
- ✨ Minimalism over features
- 📱 Mobile-first responsive design
- ⚡ Speed and performance
- 🎯 Hyperlocal accuracy

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - feel free to use for personal or commercial projects.

## 🙏 Acknowledgments

- **Tomorrow.io** - Weather API and data
- **OpenDataSoft** - Paris arrondissement coordinates
- **DarkSky** - Inspiration (RIP, acquired by Apple)
- **Météo-France** - AROME weather model

## 📮 Contact

Questions or suggestions? Open an issue or reach out!

---

**Made with ☔ in Paris**
