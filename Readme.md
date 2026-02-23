# Python Auto Reload Script

Hello there! I am **Muhammad Uzair**, and I've created this script. The CLI version is complete and ready to use.  
I'm not making it publicly available right now, but if you want the code, you can contact me through my [Instagram](https://www.instagram.com/uzair_arain_554/).

This script automatically reloads websites at specified intervals to keep them active. Perfect for maintaining activity on platforms like Upwork.

---

## Features

- ✅ Fully automatic website reloading
- ✅ Keyboard simulation (CTRL+TAB, CTRL+R)
- ✅ Hard to detect as a bot (uses realistic button presses)
- ✅ Configurable interval and website list
- ✅ No manual interaction required

---

## Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Windows, macOS, or Linux**
- A keyboard automation library (pyautogui or similar)

---

## How It Works

The script opens the websites first, and then, after the chosen interval, starts pressing:

* **CTRL + TAB** (switch tabs)
* **CTRL + R** (reload tab)

> ⚠️ Note: If you have other websites open, this program may not work properly.  
> It works best if you leave your laptop or PC alone while it runs.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/UzairArain2008/PythonAutoReload.git
cd PythonAutoReload
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install the Project in Editable Mode

```bash
pip install -e .
```

> Note: `pip install -e .` installs the project in editable mode, which means any changes you make to the code will be immediately available without reinstalling.
> This is useful for development.

---

## Usage

### 1. Configure Your Websites

Open `cli.py` and add your websites as a Python list:

```python
websites = [
    "https://www.upwork.com/your-profile",
    "https://www.example.com",
    "https://www.another-site.com"
]
```

### 2. Run the Script

```bash
python cli.py
```

Or if installed as a module:

```bash
python -m PythonAutoReload.cli
```

### 3. Follow the Prompts

The script will ask you to:
- Confirm the websites to reload
- Set the interval (in seconds) between reloads

Then sit back and let it work!

---

## Problems & Limitations

1. **Manual attention required**: Since this program presses buttons instead of targeting specific websites, you should leave your laptop alone while it runs.
2. **CAPTCHA handling**: Sometimes Upwork shows a CAPTCHA. The moving cursor may help fill it automatically. Otherwise, if the CAPTCHA requires human input, you will need to use a CAPTCHA filler extension.
3. **Tab interference**: If you have other websites open, this program may not work properly.

---

## Good Things

1. **Bot detection avoidance**: Since this program presses buttons, it's difficult for platforms to recognize whether it's a human or a program.
2. **Fully automatic**: Reloads all the websites you list without manual intervention.

---

## Contact

If you notice any errors or want to reach out, you can contact me through:

* **Instagram**: [uzair_arain_554](https://www.instagram.com/uzair_arain_554/)
* **Discord**: uzairarain554
* **Portfolio**: [uzairarain2008.github.io](https://uzairarain2008.github.io)
* **LinkedIn**: Muhammad Uzair

> You can also find all my links through my portfolio.