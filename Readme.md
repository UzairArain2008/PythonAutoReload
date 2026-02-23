# Python Auto Reload Script

Hello there! I am **Muhammad Uzair**, and I’ve created this script. The CLI version is complete and ready to use.  
I’m not making it publicly available right now, but if you want the code, you can contact me through my [Instagram](https://www.instagram.com/uzair_arain_554/).

This script asks whether you want to change the URLs of the websites or not.  
However, I suggest putting your websites directly into `cli.py`. Add the websites exactly as a **Python list**.

Once you do that, you won’t need to enter 5 or even 10 websites manually — the program is fully automatic and will reload all the websites in your list.

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
  git clone https://github.com/UzairArain2008/Python-Auto-Reload.git
  cd Python-Auto-Reload
  ```

  ### 2. Create a Virtual Environment

  ```bash
python -m venv venv
  ```
  activate it

  #### Windows 
  ```bash
venv\Scripts\activate
  ```

  #### MacOS/linux
  ```bash
source venv/bin/activate
  ```

  ### 3. Install the Project in Editable Mode

  ```bash
  pip install -e .
  ```

  > Note: `pip install -e .` installs the project in editable mode, which means any changes you make to the code will be immediately available without reinstalling.
  > This is useful for development.

## Problems / Limitations

1.  Since this program presses buttons instead of targeting specific websites, you should leave your laptop alone while it runs.
2.  Sometimes Upwork shows a CAPTCHA. The moving cursor may help fill it automatically. Otherwise, if the CAPTCHA requires human input, you will need to use a CAPTCHA filler extension.

## Good Things

1. Since this program presses buttons, it’s difficult for platforms to recognize whether it’s a human or a program.
2. Fully automatic: reloads the number of websites you list in main.py.

---

## Contact

If you notice any errors or want to reach out, you can contact me through:
* Instagram: uzair_arain_554
* Discord: uzairarain554
* Portfolio Direct Message: uzairarain2008.github.io
* LinkedIn: Muhammad Uzair
> You can also find all my links through my portfolio.
