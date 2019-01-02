rm -r "dist/"
python -m PyInstaller --name taskord -F src/main.py
cp -v "src/taskord.kv" "dist/"
cp -v -r "src/resources/" "dist/resources/"
