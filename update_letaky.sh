#!/bin/bash

# Načtení běžných systémových cest
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# 1. Přesun do složky projektu
cd /Users/marek/Dev/marekpotucek/absent-atmosphere || exit

# 2. Spuštění stahování
python3 stahovac.py

# 3. Nahrání hotového ZIPu do Cloudflare R2 pomocí absolutní cesty k npx
echo "Nahrávám do Cloudflare R2..."
/Users/marek/.nvm/versions/node/v24.15.0/bin/npx wrangler r2 object put letaky-sklad/letaky.zip --file=./letaky.zip

echo "Hotovo! Letáky jsou na cloudu."