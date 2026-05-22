# Installation Guide

Here are the steps to install Pygame based on the repository's documentation, followed by a clean, professional README.md file you can use for your own project.

## Steps to Install Python on Windows

1. **Download the Installer**: Go to the official [Python Website](https://www.python.org) and download the latest stable Windows installer (usually an .exe file).

2. **Run the Installer**: Double-click the downloaded file to start the setup.

3. **Crucial Step (Add to PATH)**: At the bottom of the installation window, check the box that says "Add python.exe to PATH".

4. **Choose Installation Type**: Click "Install Now".

5. **Verify the Installation**: 
   - Open the Command Prompt (cmd).
   - Type `python --version` and press Enter. It should return your installed version (e.g., Python 3.12.x).

## Steps to Install Pygame

### 1. Verify Pip Installation

Pip usually comes pre-installed with Python. Check it by running:

```bash
pip --version
```

### 2. Install Pygame

If pip is working, run the following command to install the library:

```bash
pip install pygame
```

### 3. Test the Installation

Verify everything works perfectly by launching one of Pygame's built-in example games:

```bash
python3 -m pygame.examples.aliens
```
