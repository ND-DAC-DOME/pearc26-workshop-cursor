# Pre-conference installation

Complete these steps **before** the PEARC tutorial session. Conference Wi‑Fi is shared and limited (~1 GB across all tutorials/workshops), so please do **not** wait until you are in the room to install or clone.

Workshop materials for this segment live under:

```text
Module 3: Advanced Cursor Features/
```

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

## Set up the Python environment (Module 3)

From the **repository root**:

```bash
cd "Module 3: Advanced Cursor Features"
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Participant runtime depends only on the small `mcp` package (used later for station metadata tools). The wind map itself uses the Python standard library plus data bundled in this folder.

### Offline / USB wheelhouse (if provided)

If facilitators give you a `vendor/wheels` folder (USB or shared drive), prefer:

```bash
cd "Module 3: Advanced Cursor Features"
python3 -m venv .venv
source .venv/bin/activate
pip install --no-index --find-links=vendor/wheels -r requirements.txt
```

---

## Smoke test (optional but recommended)

With the venv activated and your shell still in `Module 3: Advanced Cursor Features`:

```bash
python scripts/plot_wind_map.py --timestamp 2025-06-11T12:00:00Z
```

Open `output/wind_map.svg` in a web browser. You should see a CONUS map with wind barbs.

You do **not** need to explore the rest of the materials yet — save the hands-on steps for the live session.

---

## Day-of checklist

Bring a laptop with:

- [ ] Cursor installed and signed in  
- [ ] Python 3.10+ available (`python3 --version`)  
- [ ] Git available (`git --version`)  
- [ ] This repo cloned  
- [ ] Module 3 venv created and `pip install -r requirements.txt` succeeded  
- [ ] (Optional) Smoke-test SVG map opened successfully  

If anything fails, arrive **10 minutes early** — we will have backup USB copies of the Module 3 folder and wheels.

---

## Need help before the conference?

Use the contact listed in your registration materials. Please include your OS (`macOS` / `Windows` / `Linux`) and the output of `python3 --version` and `git --version`.
