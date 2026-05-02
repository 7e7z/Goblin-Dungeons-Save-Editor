# /// script
# requires-python = ">=3.10"
# dependencies = ["pycryptodome"]
# ///

import os, json, shutil
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad



# CONFIGURATION
# Exact AES keys from LocalFilesDataWriter class in Assembly-CSharp.dll using DNSpy

KEY = bytes([18, 52, 86, 120, 154, 188, 222, 240, 17, 34, 51, 68, 85, 102, 119, 136, 153, 170, 187, 204, 221, 238, 255, 0, 171, 205, 239, 18, 52, 86, 120, 144])
IV = bytes([1, 35, 69, 103, 137, 171, 205, 239, 254, 220, 186, 152, 118, 84, 50, 16])
SAVE_PATH = os.path.expanduser(r"~\AppData\LocalLow\Loolust\GoblinDungeons\ProgressData.save")

def decrypt(data: bytes) -> str:
    """Decrypt AES-CBC encrypted save data."""
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return unpad(cipher.decrypt(data), AES.block_size).decode('utf-8')


def encrypt(plain: str) -> bytes:
    """Encrypt plaintext to AES-CBC format."""
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return cipher.encrypt(pad(plain.encode('utf-8'), AES.block_size))


# DISPLAY LAYOUT
# Format: (section_title, [(internal_key, display_name), ...])

LAYOUT = [
    ("Resource", [
        ("dick", "Dick"),
        ("ore", "Ore"),
        ("fabric", "Fabric"),
        ("bone", "Leather (Bone)"),
        ("essenceEvil", "Essence of Evil"),
        ("heart", "Heart of Passion"),
    ]),
    ("Equipment Level", [
        ("hatLvl", "Hat"),
        ("robeLvl", "Robe"),
        ("beltLvl", "Belt"),
        ("amuletLvl", "Amulet"),
        ("tomeLvl", "Lexicon (Tome)"),
    ]),
    ("Spell", [
        ("spellLvl", "Spell Level"),
        ("selectSpell", "Select Spell"),
        ("blockSpells", "Blocked Spells"),
    ]),
    ("Maps Progress", [
        ("runeSynergy", "Rotting Grottos"),
        ("runeResonance", "Mine Tunnels"),
        ("runeForesight", "Grave Quarry"),
        ("runeRestoration", "Frost Burrow"),
    ]),
    ("Other", [
        ("person", "Person"),
    ]),
]



def load_save() -> dict:
    """Read, decrypt, and parse the save file."""
    with open(SAVE_PATH, 'rb') as f:
        return json.loads(decrypt(f.read()))


def save_data(data: dict) -> None:
    """Backup, encrypt, and write the save file."""
    shutil.copy2(SAVE_PATH, SAVE_PATH + ".bak")
    with open(SAVE_PATH, 'wb') as f:
        f.write(encrypt(json.dumps(data, indent=2)))


def render_menu(data: dict) -> list[tuple[int, str, str]]:
    """Print the editable fields with global indices. Returns indexed list."""
    print("Goblin Dungeons Save Editor")
    print("=" * 40)

    indexed: list[tuple[int, str, str]] = []
    known_keys: set[str] = set()
    idx = 1

    for section, fields in LAYOUT:
        print(f"\n{section}")
        for key, name in fields:
            if key in data:
                print(f"  [{idx:2d}] {name:20} = {data[key]}")
                indexed.append((idx, key, name))
                known_keys.add(key)
                idx += 1

    # Show any keys not in our predefined layout
    for key in sorted(data.keys() - known_keys):
        print(f"  [{idx:2d}] {key:20} = {data[key]}")
        indexed.append((idx, key, key))
        idx += 1

    print("\n" + "=" * 40)
    return indexed


def handle_edit(data: dict, indexed: list[tuple[int, str, str]]) -> None:
    """Prompt user to edit a value by index."""
    try:
        choice = input("Enter number to edit: ").strip()
        if not choice or choice == "0":
            print("Exiting without changes.")
            return

        n = int(choice)
        match = next((item for item in indexed if item[0] == n), None)
        if not match:
            print("Invalid number.")
            return

        _, key, name = match
        print(f"\nEditing: {name} (Key: {key})")
        print(f"Current: {data[key]}")

        new_val = input("New value: ").strip()
        if new_val:
            data[key] = new_val
            save_data(data)
            print("Saved! (Backup created at .bak)")
        else:
            print("Cancelled.")

    except ValueError:
        print("Please enter a valid number.")
    except Exception as e:
        print(f"Error: {e}")




def main() -> None:
    data = load_save()
    indexed = render_menu(data)
    handle_edit(data, indexed)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
