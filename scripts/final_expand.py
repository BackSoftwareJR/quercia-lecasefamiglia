#!/usr/bin/env python3
"""Final expansion pass to ensure all blog HTML articles >= 800 words."""
import os
import re
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE, "blog")

FINAL = {
    "casa-famiglia-vs-rsa-differenze": """
        <h2>Il ruolo dei figli nella scelta</h2>
        <p>Voi non siete "chi manda via" il genitore. Siete chi ascolta un bisogno spesso taciuto per orgoglio. Molti anziani ammettono in privato di sentirsi soli mesi prima che la famiglia agisca. Agire con delicatezza non è fretta — è rispetto del tempo giusto per ogni persona.</p>
        <p>Coinvolgete fratelli e sorelle. Condividete visita, confronto, decisione. Un figlio solo soffre il peso della scelta; una famiglia allineata offre a vostro caro messaggio coerente: "Ti vogliamo bene, vogliamo che tu stia bene."</p>
        <h2>Costi e aspettative realistiche</h2>
        <p>Case famiglia e RSA hanno rette diverse e inclusioni diverse. Confrontate sempre cosa è incluso: pasti, assistenza notturna, attività, lavanderia. Leggete <a href="/rette-e-ammissione/">rette e ammissione</a> e parlate con noi per chiarezza senza impegno.</p>
        <p>Non promettete a vostro padre "sarà come a casa" — sarà una nuova casa, con calore vero ma cambiamento vero. Onestà emotiva costruisce fiducia più delle frasi rassicuranti vuote.</p>
""",
    "anziani-autosufficienti-coazze": """
        <h2>Coazze nel contesto della famiglia</h2>
        <p>Quando proponete Coazze, mostrate mappa, tempi di percorrenza, foto del paese. Demistificate l'idea di "paesino perso": è comunità viva, servizi essenziali, connessioni reali. Vostro caro potrebbe scoprire che conosce qualcuno che ha vissuto qui o che ha parenti in valle.</p>
        <p>La <a href="/chi-siamo/">nostra filosofia</a> mette al centro l'ospite autosufficiente: persone attive che vogliono compagnia e sicurezza, non cure intensive. Se questo profilo corrisponde a vostro genitore, siete nel posto giusto per approfondire.</p>
""",
    "autonomia-dignita-terza-eta": """
        <h2>Esempi concreti di rispetto quotidiano</h2>
        <p>Autonomia significa poter rifiutare un'attività di gruppo senza sentirsi "antipatici". Significa mantenere la propria routine del mattino — caffè lento, giornale, telefonata alla sorella — senza essere scaglionati come in una fabbrica.</p>
        <p>Dignità significa essere chiamati per nome, non per numero. Significa che le famiglie sono ascoltate quando segnalano preferenze. Significa che un ospite può dire "oggi no" e che il no viene accettato.</p>
        <h2>Costruire fiducia nel tempo</h2>
        <p>La fiducia tra famiglia e struttura cresce con comunicazione onesta. Preferiamo una domanda difficile all'inizio a un risentimento silenzioso dopo mesi. <a href="/contatti/">Contattateci</a> per qualsiasi dubbio — è parte del percorso.</p>
""",
    "coazze-giaveno-pinerolo-servizi": """
        <h2>Organizzare il primo incontro</h2>
        <p>Indipendentemente da dove venite — Giaveno, Pinerolo, Torino — il primo passo è una conversazione. Telefonata, WhatsApp, email: scegliete voi. Spieghiamo servizi, retta, disponibilità camere, tempi di ingresso. Poi visita, senza pressione.</p>
        <p>Portate domande scritte se aiuta. "Come funzionano le visite?" "Cosa succede se un giorno non sta bene?" "Posso parlare con chi lo accoglie ogni giorno?" Domande semplici, risposte chiare.</p>
        <h2>Restare in valle come scelta consapevole</h2>
        <p>Molte famiglie ci dicono: "Volevamo che restasse qui, non in città." La valle non è seconda scelta — è scelta d'amore per un territorio e per una qualità di vita. <a href="/la-struttura/">Venite a vedere</a> se lo sentite anche voi.</p>
""",
    "costi-retta-casa-famiglia-piemonte": """
        <h2>Domande da fare sul preventivo</h2>
        <p>Chiedete: ci sono costi una tantum? Cosa non è incluso? Come si gestisce assenza per ricovero temporaneo? Esistono adeguamenti annuali? Tutto per iscritto. Trasparenza protegge tutti.</p>
        <p>Confrontate almeno due strutture in Piemonte, non solo per prezzo ma per atmosfera. Una retta leggermente superiore in ambiente giusto può costare meno in ansia familiare e interventi d'emergenza.</p>
""",
    "domande-figli-casa-famiglia": """
        <h2>Domande sul futuro</h2>
        <p><strong>E se un giorno non sarà più autosufficiente?</strong> Parliamo con voi per tempo. Orientamento trasparente fa parte del rispetto — non vi lasciamo soli di fronte a cambiamenti.</p>
        <p><strong>Posso cambiare idea?</strong> La decisione si costruisce nel tempo. Visita, riflessione, secondo incontro: nessuna buona struttura vi mette con le spalle al muro.</p>
        <p>Per approfondire, leggete <a href="/blog/scegliere-casa-famiglia-genitori/">come scegliere una casa famiglia</a> e <a href="/servizi/">i nostri servizi</a>.</p>
""",
    "inserimento-nuovo-ospite": """
        <h2>Dopo le prime settimane</h2>
        <p>Il telefono inizia a squillare con notizie piccole: "Oggi ho fatto una passeggiata", "Ho conosciuto la signora Maria." Celebrateli. Non minimizzate. Sono segnali che il ponte tra vecchia e nuova normalità regge.</p>
        <p>Se qualcosa non va — umore basso persistente, rifiuto alimentare, chiusura totale — parlatene con noi subito. Adattamento non è linea retta. Insieme troviamo soluzioni: cambio tavolo, visita extra, oggetto familiare in più.</p>
""",
    "valle-di-susa-vita-anziani": """
        <h2>Connessione con Torino senza caos urbano</h2>
        <p>Molti anziani della valle hanno figli in città. Coazze permette equilibrio: natura e quiete per chi vive qui, reachability per chi visita da Torino senza percorso stressante quotidiano per il genitore.</p>
        <p>Valutate insieme frequenza visite realistica. Meglio promessa mantenuta che presenza irregolare carica di colpa. La valle resta ponte, non barriera.</p>
""",
    "visite-familiari-casa-famiglia": """
        <h2>Quando vivete lontano</h2>
        <p>Videochiamate con tablet semplice, foto WhatsApp dei nipoti, messaggi vocali brevi: tecnologia al servizio del legame, non sostituto delle visite ma complemento tra una e l'altra.</p>
        <p>Programmate visite con anticipo così vostro caro ha qualcosa da attendere. "Il 15 arrivi tu" dà struttura al tempo — riduce sensazione di abbandono.</p>
""",
}


def word_count(html):
    m = re.search(r'content-prose">(.*?)</div>\s*<aside', html, re.S)
    if not m:
        return 0
    text = re.sub(r"<[^>]+>", " ", m.group(1))
    return len(re.findall(r"\w+", text))


def inject(slug, extra):
    path = os.path.join(BLOG_DIR, slug, "index.html")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if extra.strip() in html:
        return
    marker = "      </div>\n      <aside class=\"blog-article-cta\">"
    html = html.replace(marker, extra + "\n" + marker)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    for slug, extra in FINAL.items():
        inject(slug, extra)
    for path in sorted(glob.glob(os.path.join(BLOG_DIR, "*/index.html"))):
        slug = os.path.basename(os.path.dirname(path))
        wc = word_count(open(path, encoding="utf-8").read())
        status = "OK" if wc >= 800 else "SHORT"
        print(f"{status} {wc:4d} {slug}")


if __name__ == "__main__":
    main()
