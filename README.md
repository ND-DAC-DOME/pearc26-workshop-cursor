# Pre-conference installation

Complete these steps **before** the PEARC tutorial session. Conference Wi‑Fi is shared and limited (~1 GB across all tutorials/workshops), so please do **not** wait until you are in the room to install or clone.

---

## Required software

Install and verify each of the following on your laptop before the conference.

### Cursor

1. Download Cursor from [https://cursor.com](https://cursor.com)
2. Install and open the app
3. Sign in with your account (create one if needed)

You will use **Ask**, **Agent**, and **Plan** modes during the session.

### Python

You need **Python 3.10+** on your PATH.

```bash
python3 --version
```

If that fails, install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/) (or your OS package manager), then confirm `python3 --version` again.

On Windows, the installer option **“Add python.exe to PATH”** should be enabled.

### Git

You need Git to clone the workshop repository.

```bash
git --version
```

If that fails:

- **macOS:** install Xcode Command Line Tools (`xcode-select --install`) or Git from [https://git-scm.com/download/mac](https://git-scm.com/download/mac)
- **Windows:** install from [https://git-scm.com/download/win](https://git-scm.com/download/win)
- **Linux:** use your package manager (e.g. `sudo apt install git` / `sudo dnf install git`)

Then confirm `git --version` again.

---

## Clone this repository

```bash
git clone https://github.com/ND-DAC-DOME/pearc26-workshop-cursor.git
cd pearc26-workshop-cursor
```

Open the repo folder in Cursor: **File → Open Folder…**

---

## Set up the Python environment (shared)

Create **one** virtual environment at the **repository root**. It is used for Module 2 and Module 3.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Participant runtime needs `pillow` (PNG wind maps) and `mcp` (Module 3 station metadata tools). Each module bundles its own `data/` folder.

**NOTE**: This repository ships with an MCP server that loads automatically, but it cannot run until the above step is completed. Restarting Cursor after this step is the easiest way to fix this.


---

## Smoke test (optional but recommended)

With the venv activated and your shell at the **repository root**:

```bash
python "Module 2 - Cursor Basics/scripts/plot_wind_map.py"
```

Open `Module 2 - Cursor Basics/output/wind_map.png`. You should see a CONUS basemap (wind overlays are added during the live Module 2 session).

You can also spot-check Module 3’s finished map:

```bash
python "Module 3 - Advanced Cursor Features/scripts/plot_wind_map.py" --timestamp 2025-06-11T12:00:00Z
```

Open `Module 3 - Advanced Cursor Features/output/wind_map.png`. You should see a CONUS map with wind barbs.

You do **not** need to explore the rest of the materials yet — save the hands-on steps for the live session.

---

## Day-of checklist

Bring a laptop with:

- [ ] Cursor installed and signed in  
- [ ] Python 3.10+ available (`python3 --version`)  
- [ ] Git available (`git --version`)  
- [ ] This repo cloned  
- [ ] Root `.venv` created and `pip install -r requirements.txt` succeeded  
- [ ] (Optional) Module 2 and/or Module 3 smoke-test PNG opened successfully  

If anything fails, arrive **10 minutes early** — we will have backup USB copies of the workshop folders and wheels.

---

## Need help before the conference?

Use the contact listed in your registration materials. Please include your OS (`macOS` / `Windows` / `Linux`) and the output of `python3 --version` and `git --version`.
