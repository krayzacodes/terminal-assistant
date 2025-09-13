# 🐍 Mia CLI — Mizgin's Terminal Assistant

Mia CLI is a **command-line assistant** built with Python to make file and folder operations faster and easier.  
It helps you list, organize, rename, and search files directly from your terminal.  

---

## 🚀 Features

- `pwd` → Print the current working directory  
- `ls` → List files and folders (optionally show hidden files)  
- `tree` → Display folder structure in a tree view  
- `mkcd` → Create a new folder and print the command to enter it  
- `rename` → Rename or move a file/folder  
- `organize` → Sort files into category folders by extension  
- `find` → Search for files/folders by name substring  

---

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/krayzacodes/terminal-assistant.git
   cd terminal-assistant

---

## 📌 Usage Examples

```bash
# Print working directory
python3 mia.py pwd

# List files (including hidden ones)
python3 mia.py ls -a

# Tree view (max depth 2)
python3 mia.py tree -d 2

# Create folder
python3 mia.py mkcd demo

# Rename or move file
python3 mia.py rename old.txt new.txt

# Organize files into category folders
python3 mia.py organize --other Others

# Search files/folders by name
python3 mia.py find "notes" .

---

## ✨ Contribution
Contributions and pull requests are welcome!  
You can improve this tool by adding features like:  
- Colored output (`rich`)  
- Auto-completion (`argcomplete`)  
- Logging support  
- Regex-based batch rename  
- Zip/Unzip commands  

---

## 👩‍💻 Author
**Mizgin Yakın**  
Learning Python, AI & Cybersecurity 🚀  

🔗 GitHub Profile → [krayzacodes](https://github.com/krayzacodes)
