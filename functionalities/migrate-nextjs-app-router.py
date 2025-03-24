import os
import shutil

SRC_DIR = "."
PAGES_DIR = os.path.join(SRC_DIR, "pages")
APP_DIR = os.path.join(SRC_DIR, "app")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def migrate_pages_to_app():
    if not os.path.exists(PAGES_DIR):
        print("No /pages directory found. Nothing to migrate.")
        return

    ensure_dir(APP_DIR)

    for filename in os.listdir(PAGES_DIR):
        if not filename.endswith(".tsx"):
            continue

        page_name = filename.replace(".tsx", "")
        source_path = os.path.join(PAGES_DIR, filename)

        # Map index.tsx → app/page.tsx
        if page_name == "index":
            target_path = os.path.join(APP_DIR, "page.tsx")
        else:
            target_folder = os.path.join(APP_DIR, page_name)
            ensure_dir(target_folder)
            target_path = os.path.join(target_folder, "page.tsx")

        print(f"Moving {source_path} → {target_path}")
        shutil.move(source_path, target_path)

    confirm = input("\n✅ Migration complete. Delete old /pages directory? (y/N): ").strip().lower()
    if confirm == 'y':
        shutil.rmtree(PAGES_DIR)
        print("✔ /pages directory deleted.")
    else:
        print("ℹ /pages directory kept.")

if __name__ == "__main__":
    migrate_pages_to_app()

