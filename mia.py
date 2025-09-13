#!/usr/bin/env python3
import argparse
import os
import shutil
from pathlib import Path

def cmd_pwd(args):
    print(Path.cwd())

def cmd_ls(args):
    p = Path(args.path).expanduser().resolve()
    if not p.exists():
        print("Hata: Yol bulunamadı:", p)
        return
    items = list(p.iterdir())
    if not args.all:
        items = [i for i in items if not i.name.startswith('.')]
    for i in sorted(items, key=lambda x: (x.is_file(), x.name.lower())):
        suffix = "/" if i.is_dir() else ""
        print(i.name + suffix)

def cmd_tree(args):
    root = Path(args.path).expanduser().resolve()
    max_depth = args.depth
    if not root.exists():
        print("Hata: Yol bulunamadı:", root)
        return

    def walk(dir_path, prefix="", depth=0):
        if max_depth is not None and depth > max_depth:
            return
        entries = sorted(dir_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        for i, entry in enumerate(entries):
            connector = "└── " if i == len(entries)-1 else "├── "
            print(prefix + connector + entry.name + ("/" if entry.is_dir() else ""))
            if entry.is_dir():
                extension = "    " if i == len(entries)-1 else "│   "
                if max_depth is None or depth < max_depth:
                    walk(entry, prefix + extension, depth+1)

    print(root.name + "/")
    walk(root, "", 1)

def cmd_mkcd(args):
    p = Path(args.path).expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)
    # "cd" komutunu Python içinden kalıcı değiştiremeyiz; kullanıcıya yolu yazdırıyoruz.
    print(f"Oluşturuldu: {p}")
    print(f"İçine girmek için: cd \"{p}\"")

def cmd_rename(args):
    src = Path(args.src).expanduser().resolve()
    dst = Path(args.dst).expanduser().resolve()
    if not src.exists():
        print("Hata: Kaynak bulunamadı:", src)
        return
    dst_parent = dst.parent
    dst_parent.mkdir(parents=True, exist_ok=True)
    src.replace(dst)
    print(f"Yeniden adlandırıldı/taşındı: {src} -> {dst}")

def cmd_organize(args):
    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print("Hata: Yol bulunamadı:", root)
        return

    # Kategoriler
    categories = {
        "Resimler": [".jpg", ".jpeg", ".png", ".gif"],
        "Belgeler": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".csv"],
        "Muzikler": [".mp3", ".wav", ".flac"],
        "Videolar": [".mp4", ".mkv", ".mov"],
        "Arsivler": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Kodlar": [".py", ".js", ".ts", ".html", ".css", ".ipynb"]
    }

    moved = 0
    for item in root.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            target_dir = None
            for cat, exts in categories.items():
                if ext in exts:
                    target_dir = root / cat
                    break
            if target_dir is None:
                if args.other:
                    target_dir = root / args.other
                else:
                    continue
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(target_dir / item.name))
            moved += 1
            if args.verbose:
                print(f"{item.name} -> {target_dir.name}/")
    print(f"Taşınan dosya sayısı: {moved}")

def cmd_find(args):
    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print("Hata: Yol bulunamadı:", root)
        return
    pattern = args.pattern.lower()
    count = 0
    for p in root.rglob("*"):
        if pattern in p.name.lower():
            print(p)
            count += 1
    print(f"Bulunan: {count}")

def build_parser():
    parser = argparse.ArgumentParser(
        prog="mia",
        description="Mizgin’in Terminal Asistanı (CLI). Dosya/klasör işlemlerini hızlandırır."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pwd = sub.add_parser("pwd", help="Çalışma dizinini yazdır")
    p_pwd.set_defaults(func=cmd_pwd)

    p_ls = sub.add_parser("ls", help="Dosya/klasörleri listele")
    p_ls.add_argument("path", nargs="?", default=".", help="Listeleme yolu (varsayılan: .)")
    p_ls.add_argument("-a", "--all", action="store_true", help="Gizli dosyaları da göster")
    p_ls.set_defaults(func=cmd_ls)

    p_tree = sub.add_parser("tree", help="Ağaç görünümünde listele")
    p_tree.add_argument("path", nargs="?", default=".", help="Başlangıç yolu")
    p_tree.add_argument("-d", "--depth", type=int, help="Maksimum derinlik (örn: 2)")
    p_tree.set_defaults(func=cmd_tree)

    p_mkcd = sub.add_parser("mkcd", help="Klasör oluşturup içine girme komutunu yazdır")
    p_mkcd.add_argument("path", help="Oluşturulacak klasör")
    p_mkcd.set_defaults(func=cmd_mkcd)

    p_rename = sub.add_parser("rename", help="Dosya/klasör yeniden adlandır/taşı")
    p_rename.add_argument("src", help="Kaynak")
    p_rename.add_argument("dst", help="Hedef (yeni ad veya yeni yol)")
    p_rename.set_defaults(func=cmd_rename)

    p_org = sub.add_parser("organize", help="Dosyaları kategori klasörlerine ayır")
    p_org.add_argument("path", nargs="?", default=".", help="Hedef klasör")
    p_org.add_argument("--other", help="Kategoriye uymayanlar için klasör adı")
    p_org.add_argument("-v", "--verbose", action="store_true", help="Hareketleri yazdır")
    p_org.set_defaults(func=cmd_organize)

    p_find = sub.add_parser("find", help="İsme göre dosya/klasör ara")
    p_find.add_argument("pattern", help="Aranacak desen (isimde geçecek)")
    p_find.add_argument("path", nargs="?", default=".", help="Arama yolu")
    p_find.set_defaults(func=cmd_find)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
