import sys
import re

log_path = r'C:\Users\MARLEY\.gemini\antigravity\brain\b5fd5214-1c4a-4613-a99c-29c12c6a8d17\.system_generated\logs\overview.txt'

with open(log_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find the exact start
target_phrase = 'j e t envoi le scrite actuel sur l hebergeur<!DOCTYPE html>'
idx = text.rfind(target_phrase)

if idx == -1:
    print('Failed to find in log')
    sys.exit(1)

html_start = idx + len('j e t envoi le scrite actuel sur l hebergeur')
html_end = text.find('</html>', html_start) + len('</html>')

html_content = text[html_start:html_end]

# We need to replace genererBillet. 
new_func = """  function genererBillet() {
    /* A) Lecture des champs du formulaire */
    resData.nom    = document.getElementById('nom').value.trim();
    resData.tel    = document.getElementById('tel').value.trim();
    resData.places = document.getElementById('places').value.trim();
    resData.billet = document.getElementById('billet').value.trim();
    resData.msg    = document.getElementById('message').value.trim();
    const errEl    = document.getElementById('formError');

    /* B) Validation des champs obligatoires */
    if (!resData.nom || !resData.tel || !resData.places) {
      errEl.textContent = '⚠️ Merci de remplir tous les champs obligatoires (*)';
      errEl.style.display = 'block';
      return;
    }
    if (isNaN(resData.places) || Number(resData.places) < 1) {
      errEl.textContent = '⚠️ Le nombre de places doit être au moins 1.';
      errEl.style.display = 'block';
      return;
    }
    errEl.style.display = 'none';

    // Modifier le bouton pendant le chargement
    const btnSubmit = document.querySelector('.btn-submit');
    const originalBtnText = btnSubmit.innerHTML;
    btnSubmit.innerHTML = '⏳ Création du billet...';
    btnSubmit.disabled = true;

    /* C) Génération du Billet Virtuel */
    // Remplir les données du billet
    document.getElementById('vt-nom').textContent = resData.nom;
    let typeBilletStr = resData.billet ? resData.billet.split('–')[0].trim() : 'Standard';
    document.getElementById('vt-type').textContent = `${typeBilletStr} (${resData.places} place${resData.places > 1 ? 's' : ''})`;
    
    // Générer un code aléatoire style PP26-XXXX-XXX
    const rd1 = Math.floor(1000 + Math.random() * 9000);
    const rd2 = Math.floor(100 + Math.random() * 900);
    resData.codeBillet = `PP26-${rd1}-${rd2}`;
    document.getElementById('vt-code').textContent = resData.codeBillet;

    // ----------------------------------------------------
    // ENVOI À GOOGLE SHEETS
    // Dès que vous avez l'URL de votre application Google, 
    // collez-la ici à la place de "URL_GOOGLE_SCRIPT_ICI"
    // ----------------------------------------------------
    const googleScriptURL = "URL_GOOGLE_SCRIPT_ICI";
    
    // On prépare l'envoi en arrière-plan
    if (googleScriptURL !== "URL_GOOGLE_SCRIPT_ICI") {
      fetch(googleScriptURL, {
        method: 'POST',
        mode: 'no-cors',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          nom: resData.nom,
          tel: resData.tel,
          places: resData.places,
          billet: resData.billet,
          code: resData.codeBillet,
          message: resData.msg
        })
      }).catch(err => console.error("Erreur d'envoi vers Sheets:", err));
    }

    // Restaurer le bouton
    btnSubmit.innerHTML = originalBtnText;
    btnSubmit.disabled = false;

    // Afficher l'animation du billet
    document.getElementById('formArea').style.display = 'none';
    const ticketArea = document.getElementById('ticketArea');
    ticketArea.style.display = 'block';
    
    // Petite animation CSS sur le billet
    const vt = document.querySelector('.virtual-ticket');
    vt.animate([
      { transform: 'translateY(-20px) scale(0.95)', opacity: 0 },
      { transform: 'translateY(0) scale(1)', opacity: 1 }
    ], { duration: 500, easing: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)' });
  }"""

pattern = re.compile(r'function genererBillet\(\)\s*\{.*?\}\s*(?=function envoyerWhatsApp)', re.DOTALL)
new_html = pattern.sub(new_func + '\n\n  ', html_content)

out_file = r'C:\Users\MARLEY\Documents\vscode\piscine_26\Piscine_Party_Pret_a_Coller.html'
with open(out_file, 'w', encoding='utf-8') as fw:
    fw.write(new_html)
print(f'Wrote {len(new_html)} bytes to {out_file}')
