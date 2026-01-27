## Making Rayvn Executable (Development Setup)

Rayvn can be run as a command-line tool during development.
This setup is intended for contributors and local experimentation.

---

### Requirements

- Python 3.9+
- macOS or Linux (Windows users should use WSL)

Verify Python:

```bash
python3 --version
```

---

### Project Structure

Rayvn expects the following layout:

```
rayvn/
├─ rayvn               # executable CLI entry
├─ compiler/
│  ├─ main.py
│  ├─ lexer.py
│  ├─ parser.py
│  └─ ...
├─ language-support/
├─ .vscode/
└─ README.md
```

---

### Make the CLI Executable

From the project root, run:

```bash
chmod +x rayvn
```

Ensure the first line of the `rayvn` file is:

```python
#!/usr/bin/env python3
```

---

### Running Rayvn Locally

Rayvn relies on local imports and should be run from the project directory:

```bash
cd rayvn
./rayvn example.rv
```

Or using Python directly:

```bash
python3 rayvn example.rv
```

---

### Optional: Run Rayvn From Anywhere

To make `rayvn` available globally, create a symlink:

```bash
sudo ln -sf "$(pwd)/rayvn" /usr/local/bin/rayvn
```

Verify the link:

```bash
which rayvn
```

Expected output:

```
/usr/local/bin/rayvn
```

Now you can run:

```bash
rayvn example.rv
```

---

### Removing or Rebuilding the Executable

If the project is moved or you want to reset the executable:

```bash
sudo rm /usr/local/bin/rayvn
```

Then recreate it from the new location:

```bash
cd rayvn
sudo ln -sf "$(pwd)/rayvn" /usr/local/bin/rayvn
```

---

### Notes for Contributors

- If you move the project directory, you must recreate the symlink.
- If imports break, ensure you are running Rayvn from the project root.
- This setup is for development only and may change as the language matures.