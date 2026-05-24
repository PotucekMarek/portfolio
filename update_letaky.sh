#!/bin/bash

# 1. Přesun do složky tvého projektu
cd /Users/marek/Dev/marekpotucek/absent-atmosphere || exit

# 2. Spuštění stahování
python3 stahovac.py

# 3. Nahrání hotového ZIPu přímo do Cloudflare R2
echo "Nahrávám do Cloudflare R2..."
npx wrangler r2 object put letaky-sklad/letaky.zip --file=./letaky.zip

echo "Hotovo! Letáky jsou na cloudu."