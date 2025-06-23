# Auto Clicker

An intuitive and customizable **Python autoclicker** for productivity, software-testing, or gaming. A lightweight GUI, global hot-keys, and flexible options make repetitive clicking effortless on **Windows, macOS, and Linux**.

---

## ✨ Features

- **Custom click intervals** – specify clicks per second (CPS) or milliseconds between clicks.  
- **Mouse-button choice** – left, right, or middle button.  
- **Simple GUI** – clean Tkinter interface for all settings.  
- **Global key bindings** – start / stop with convenient shortcuts.  
- **Visual indicator** – live status label shows when clicking is active.  
- **Cross-platform** – one codebase runs on Windows, macOS, and Linux.

---

## 🛠  Technologies Used

| Purpose                | Library |
|------------------------|---------|
| Core language          | **Python 3.8+** |
| Mouse automation       | `pyautogui` |
| Global hot-keys        | `pynput` (preferred) or `keyboard`* |
| Graphical interface    | `tkinter` (built-in) |

\* `keyboard` requires admin/root on some OSes; `pynput` avoids that.

---

## 🚀 How to Use

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/autoclicker-app.git
cd autoclicker-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python autoclicker.py

