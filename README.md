# Goblin Dungeons Save Editor

A simple Python CLI tool to view and edit save files for **Goblin Dungeons** (by Loolust). Decrypts, modifies, and re-encrypts `ProgressData.save` using the game's internal AES-CBC keys.

> **Use at your own risk.** Always back up your save files before editing.

---

## Features

- Decrypts `ProgressData.save` using extracted game keys
- Edit resources, equipment levels, spells, and map progress via numbered menu
- Auto-backups original save to `.bak` before writing changes
- Re-encrypts and saves in original format
- Unknown keys in save file are still displayed for advanced editing

---

## Requirements

- Python **3.10+**
- `pycryptodome` library

Install dependencies:

```bash
pip install pycryptodome
```

> The script uses [PEP 723 inline script metadata](https://peps.python.org/pep-0723/). If your environment supports it (e.g., `uv`, `pipx run`), dependencies can be installed automatically.

---

## Usage

1. **Place the script** in any folder (no installation required).

2. **Ensure your save file exists** at the default path:
   ```
   %USERPROFILE%\AppData\LocalLow\Loolust\GoblinDungeons\ProgressData.save
   ```
   > To change the path, edit the `SAVE_PATH` variable in the script.

3. **Run the script**:
   ```bash
   python save_editor.py
   ```

4. **Follow the menu**:
   - View current values with numbered indices
   - Enter a number to edit that field
   - Type a new value and press Enter
   - Changes are saved automatically (backup created)

---

## Configuration

The AES key and IV are pre-configured from the game's `LocalFilesDataWriter` class (extracted via dnSpy). Only modify these if you're certain the game has updated its encryption:

```python
KEY = bytes([...])  # 32-byte AES-256 key
IV  = bytes([...])  # 16-byte CBC IV
```

To edit which fields appear in the menu, modify the `LAYOUT` list:

```python
LAYOUT = [
    ("Resource", [
        ("ore", "Ore"),
        # ... add or remove fields
    ]),
    # ... more sections
]
```

---

## File Structure

```
save_editor.py          # Main script
ProgressData.save       # Game save file (auto-located)
ProgressData.save.bak   # Auto-generated backup
```

---

## Disclaimer

- This tool is for **personal, educational use only**.
- The author is not affiliated with Loolust or Goblin Dungeons.
- Editing saves may cause instability, achievements to break.
- **Always keep backups** — corruption is possible.

---

## 📄 License

MIT License — Feel free to use, modify, and share. See [LICENSE](LICENSE) for details.
