export const prerender = false;

import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';
import path from 'path';

const execAsync = promisify(exec);

export async function GET() {
  try {
    // Uprav cestu k Python skriptu podle toho, kam jsi ho reálně uložil
    // Pokud je ve složce scripts, použij: path.resolve('scripts', 'stahovac.py')
    // Pokud je v kořenu, použij: path.resolve('stahovac.py')
    const scriptPath = path.resolve('stahovac.py'); 
    const zipPath = path.resolve('letaky_archiv.zip');

    console.log("🚀 Spouštím Python scraper...");
    
    // ZMĚNA: Získáme výstup (stdout a stderr) z Python skriptu
    const { stdout, stderr } = await execAsync(`python3 "${scriptPath}"`); 
    
    // ZMĚNA: Vypíšeme Python logy do terminálu, abychom viděli, co se děje!
    console.log("=== START PYTHON LOGU ===");
    console.log(stdout);
    if (stderr) console.error("Python chyby:", stderr);
    console.log("=== KONEC PYTHON LOGU ===");

    console.log("✅ Scraping dokončen. Načítám ZIP...");
    const fileBuffer = await fs.readFile(zipPath);

    await fs.unlink(zipPath);

    return new Response(fileBuffer, {
      status: 200,
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': 'attachment; filename="letaky_archiv.zip"'
      }
    });
  } catch (error) {
    console.error("❌ API chyba:", error);
    return new Response(JSON.stringify({ error: "Stažení selhalo." }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}