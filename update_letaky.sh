#!/bin/bash

export PATH="/Users/marek/.nvm/versions/node/v24.15.0/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# 1. Přejdeme do složky projektu jako první věc (klíčové pro Cron)
cd /Users/marek/Dev/marekpotucek/absent-atmosphere || exit

# 2. Načteme proměnné ze souboru .env
if [ -f .env ]; then
  source .env
fi

# 3. BEZPEČNÉ PŘIHLÁŠENÍ DO CLOUDFLARE
export CLOUDFLARE_ACCOUNT_ID="4670a5d42eca2fe9b0a2208d0142506d"

# Token se načetl ze .env a tady ho "exportujeme", aby ho mohl použít Wrangler
export CLOUDFLARE_API_TOKEN="$CLOUDFLARE_API_TOKEN"

# 4. Spuštění stahovače
python3 stahovac.py

echo "Nahrávám do Cloudflare R2..."
# Přidali jsme --remote, aby to šlo stoprocentně do cloudu
npx wrangler r2 object put letaky-sklad/letaky.zip --file=./letaky.zip --remote

echo "Hotovo! Letáky jsou na cloudu."