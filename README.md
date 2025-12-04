# LinkedIn Bot - Automated Login & Challenge Handler

Aplikasi untuk automation LinkedIn login dengan PyQt6 dan Playwright, menangani checkpoint/challenge verification secara otomatis.

## 🎯 Features

- ✅ **Automated Login** - Automatic email/password login ke LinkedIn
- ✅ **URL Monitoring** - Real-time page navigation tracking dengan Qt signals
- ✅ **Challenge Detection** - Automatic detection checkpoint/reCAPTCHA
- ✅ **reCAPTCHA Auto-Click** - Attempt to auto-click reCAPTCHA checkbox
- ✅ **Session Management** - Save & load cookies untuk persistent sessions
- ✅ **Browser Stealth** - Anti-detection features untuk avoid bot detection
- ✅ **Qt Signal/Slot Architecture** - Thread-safe cross-thread communication

## 📦 Tech Stack

- **PyQt6** - GUI framework & threading
- **Playwright** - Browser automation (sync API)
- **Python 3.13.7** - Core language

## 🚀 Project Structure

```
LinkedIn/
├── main.py                          # Entry point
├── config.py                        # Configuration
├── state.py                         # Global state management
├── utils.py                         # Utility functions
├── concurrent_map.py                # Thread-safe dictionary
├── src/
│   ├── browser.py                   # Browser manager (launch, page, signals)
│   ├── session.py                   # Session/cookies handling
│   ├── script/
│   │   └── stealth.js              # Browser stealth script
│   └── worker/
│       ├── AutoLogin.py            # Login automation worker
│       └── AutoChallenge.py         # Challenge verification worker
└── output/
    └── html/                        # Saved page HTML for debugging
```

## 🔧 Setup

### Prerequisites
- Python 3.13.7+
- Chrome/Chromium browser

### Installation

```bash
# Clone repository
git clone https://github.com/erixjunior/linkedin-bot.git
cd linkedin-bot

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Edit `config.py`:
```python
LINKEDIN_EMAIL = "your-email@example.com"
LINKEDIN_PASSWORD = "your-password"
BROWSER_PORT = 9222
SESSION_DIR = "sessions"
```

## 🎮 Usage

```bash
python main.py
```

### Flow

1. **Initialize** → Create Browser, AutoLoginWorker, AutoChallengeWorker
2. **Launch Browser** → Open Chrome dengan CDP & stealth injection
3. **Navigate to Login** → Go to https://www.linkedin.com/login
4. **Monitor URL** → Listen untuk page navigation events
5. **Detect Login Page** → Auto-trigger login form fill
6. **Submit Form** → Fill email/password & click submit
7. **Handle Checkpoint** → Detect reCAPTCHA & attempt auto-click
8. **Save Session** → Save cookies untuk future logins

## 📊 Architecture

### Signal Flow

```
Browser.page_loaded(page)
    ↓
AutoLoginWorker._on_page_loaded(page)
    ↓ (if login page)
AutoLoginWorker.on_start()
    ↓
Fill form & submit

Browser.url_changed(url)
    ↓
AutoChallengeWorker._on_url_changed(url)
    ↓ (if checkpoint)
AutoChallengeWorker.on_start()
    ↓
Auto-click reCAPTCHA & wait for user
```

### Thread Safety

- **Main Thread** - Qt event loop, browser operations
- **Qt Signals/Slots** - QueuedConnection untuk cross-thread invocation
- **Global State** - ConcurrentMap dengan RLock untuk thread-safe access

## 🤖 Browser Stealth Features

`src/script/stealth.js` includes:
- Navigator spoofing (userAgent, platform, plugins)
- Chrome runtime properties
- WebGL fingerprinting protection
- Canvas fingerprinting protection
- Window/screen properties spoofing

## 🔐 Security

- ⚠️ **Use responsibly** - Hanya untuk testing & automation personal account
- 🔒 **Credentials** - Stored locally, tidak di-share ke remote
- 🛡️ **Anti-Detection** - Stealth techniques untuk reduce bot detection risk

## 🐛 Troubleshooting

### reCAPTCHA Not Detected

Check `output/html/challenge_page.html` untuk verify page structure

### Browser Not Launching

- Pastikan Chrome/Chromium installed
- Check `BROWSER_PORT` tidak sudah digunakan

### Login Form Not Found

- LinkedIn page structure mungkin berubah
- Check selector `input[name='session_key']` di page HTML

## 📝 Notes

- reCAPTCHA v2 Enterprise tidak bisa di-automate sepenuhnya
- Manual verification mungkin diperlukan untuk checkpoint
- Session cookies save otomatis untuk future logins

## 🔗 References

- [Playwright Docs](https://playwright.dev/python/)
- [PyQt6 Docs](https://doc.qt.io/qt-6/)
- [Bitget API](https://www.bitget.com/api-doc) (original project context)

## 📄 License

Private use only. Do not distribute.

---

**Author**: erixjunior  
**Last Updated**: December 4, 2025

