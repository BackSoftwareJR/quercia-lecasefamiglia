#!/usr/bin/env python3
"""Append expansion paragraphs to blog articles to reach 800+ words."""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE, "blog")
CONTENT_DIR = os.path.join(BASE, "content", "blog")

EXPANSIONS = {
    "scegliere-casa-famiglia-genitori": """
        <h2>Come parlare con vostro padre o vostra madre</h2>
        <p>Non esiste un discorso perfetto. Evitate di presentare la casa famiglia come unica via d'uscita: proponetela come possibilità da esplorare insieme. "Ho visto un posto a Coazze che mi ha colpito per l'atmosfera — vuoi venire con me a darci un'occhiata?" funziona meglio di "Non puoi più restare solo."</p>
        <p>Preparatevi a resistenze: orgoglio, paura del cambiamento, lealtà verso la casa di una vita. Non forzate. Tornate alla conversazione dopo qualche giorno, con calma. A volte serve che sia un nipote, un fratello, il medico di famiglia a suggerire una visita. Non importa chi apre la porta — importa che si apra con rispetto.</p>
        <p>Portate materiale concreto: foto della struttura, brochure, link al sito. L'astratto spaventa; il visibile rassicura. Mostrate che avete fatto compiti a casa, non che state "scaricando" un problema.</p>
        <h2>Valutare Coazze e la Valle di Susa</h2>
        <p>Se vostro caro ha vissuto in valle o ama la montagna, una casa famiglia a Coazze non è un trasferimento in terra lontana. È continuità territoriale. Valutate distanze da Giaveno, Avigliana, Pinerolo: quanto spesso potete visitare? La risposta influenza la serenità di tutti.</p>
        <p>Considerate anche clima e accessibilità in inverno: domandate come viene gestita la neve, se ci sono passaggi coperti, come si organizzano spostamenti per controlli medici. Domande pratiche che evitano sorprese.</p>
        <p>Infine, fidatevi dell'intuito. Se uscite da una visita con un nodo allo stomaco, non ignoratelo. Se uscite più leggeri — anche con la tristezza di chi sa che qualcosa sta cambiando — siete sulla strada giusta.</p>
""",
    "anziani-autosufficienti-coazze": """
        <h2>Il territorio come alleato del benessere</h2>
        <p>Studi e esperienza quotidiana concordano: ambiente naturale, aria pulita, ritmi non frenetici favoriscono umore e sonno. Coazze offre tutto questo senza isolamento. I servizi essenziali — farmacia, medico, negozi — sono raggiungibili. Torino resta a portata per visite specialistiche.</p>
        <p>Per un ospite autosufficiente, poter sedersi in giardino la mattina, sentire uccelli e conversazione lontana, è terapia silenziosa. Non sostituisce cure quando servono, ma previene la chiusura in casa che alimenta depressione e debolezza.</p>
        <h2>Storie comuni, scelte diverse</h2>
        <p>Conosciamo famiglie da Giaveno che visitano il sabato col pranzo condiviso. Famiglie da Pinerolo che passano il venerdì sera per una partita a carte col padre. Famiglie da Torino che vengono ogni due settimane — e chiamano nel mezzo. Non c'è frequenza giusta universale: c'è quella sostenibile per voi e rassicurante per vostro caro.</p>
        <p>L'autosufficienza non è statica. Può diminuire lentamente nel tempo. Una casa famiglia attenta nota i segnali e parla con voi prima che diventino emergenze. Trasparenza e dialogo sono parte del patto.</p>
        <p>Se state ancora esitando, venite a conoscerci senza impegno. Camminate nel giardino, bevete un caffè, fate domande. Spesso basta vedere con i propri occhi per capire se un posto è "giusto" — o semplicemente possibile.</p>
""",
    "valle-di-susa-vita-anziani": """
        <h2>Stagioni e ritmi in montagna</h2>
        <p>La valle ha un respiro stagionale che molti anziani amano: neve che silenzia, primavera che invita al giardino, estate che profuma di erba tagliata, autunno che colora i boschi. Vivere qui significa restare connessi a cicli naturali — non a sirene e traffico.</p>
        <p>Per chi ha sempre lavorato la terra o frequentato sentieri, restare in valle è identità. Chiedere a vostro padre di trasferirsi in periferia torinese può significare amputare una parte di sé. Una casa famiglia in valle può essere compromesso intelligente.</p>
        <h2>Rete di servizi e famiglia</h2>
        <p>Valle di Susa dispone di ambulatori, RSA per esigenze diverse, associazioni di volontariato, trasporti collegati. Non siete soli nel territorio. Integrare una casa famiglia nella rete locale significa che, se qualcosa cambia, esistono percorsi noti — non labirinti da scoprire in crisi.</p>
        <p>Coinvolgete fratelli e sorelle nelle decisioni. Un figlio non deve portare tutto da solo. Condividere visite, chiamate, responsabilità amministrative alleggerisce e riduce conflitti postumi del tipo "perché hai deciso tu?"</p>
        <p>La terza età in valle può essere capitolo ricco. Con supporto adeguato, vostro caro può ancora essere protagonista — non spettatore — della propria storia.</p>
""",
    "visite-familiari-casa-famiglia": """
        <h2>Gestire distanza e sensi di colpa</h2>
        <p>Molti figli vivono lontano — Torino città, altra regione, altro paese. La distanza amplifica colpa: "Dovrei essere lì di più." Ricordate: presenza di qualità batte presenza ansiosa. Una videochiamata serena il mercoledì e una visita mensile programmata valgono più di trasferte stressate ogni weekend che esauriscono tutti.</p>
        <p>Parlate con vostro caro delle vostre limitazioni reali. Non promettete ciò che non potete mantenere. Meglio dire "Vengo il primo sabato del mese e ti chiamo il martedì" e mantenerlo, che promettere presenza quotidiana e deludere.</p>
        <h2>Conflitti e adattamento</h2>
        <p>Non tutto filerà liscio. Vostro padre potrebbe lamentarsi dei compagni di tavola, vostra madre del programma televisivo. Ascoltate, non sminuite. Portate le preoccupazioni allo staff con rispetto — spesso si risolvono con piccoli aggiustamenti.</p>
        <p>Evitate di trasformare ogni visita in ispezione: armadi aperti, medicine contate, tono investigativo. Vostro caro ha ancora diritto a privacy e dignità. Fiducia e dialogo costruiscono collaborazione migliore del controllo.</p>
        <p>Le visite sono ponti — non catene. Usatele per rinnovare legame, non per vigilare paura. In una casa famiglia a Coazze, siete sempre benvenuti: venite come famiglia, non come ispettori.</p>
""",
    "costi-retta-casa-famiglia-piemonte": """
        <h2>Leggere un contratto con attenzione</h2>
        <p>Prima di firmare, leggete ogni voce. Chiedete cosa succede in caso di assenza temporanea per ricovero breve, come vengono gestite visite mediche extra, se esistono incrementi annuali e con quale preavviso. Annotate tutto per iscritto — email valgono.</p>
        <p>Diffidate di pressioni del tipo "firmi oggi o perde il posto." Una struttura seria vi dà tempo. La decisione merita notti di sonno, non firma affrettata in corridoio.</p>
        <h2>Pianificazione familiare</h2>
        <p>Parlate tra fratelli di come ripartire i costi prima che diventi teso. Un foglio condiviso, un conto dedicato, un appuntamento annuale per rivedere la situazione: piccoli rituali che evitano rancori.</p>
        <p>Considerate anche costi indiretti risparmiati: meno trasferte d'emergenza, meno ore di assistenza informale che esauriscono chi lavora, meno spese per pranzi fuori e pulizie extra nella casa vuota. La retta va letta nel contesto del bilancio familiare completo.</p>
        <p>Non vergognatevi a chiedere preventivi e confronti. Trasparenza economica protegge rapporti affettivi — e garantisce a vostro caro continuità serena nel tempo.</p>
""",
    "inserimento-nuovo-ospite": """
        <h2>Il primo mese: cosa aspettarsi</h2>
        <p>È normale che ci siano alti e bassi. Giorni in cui vostro caro partecipa al gioco a carte, giorni in cui resta in camera. Non interpretate ogni momento difficile come fallimento. L'ambientamento ha tempi propri — settimane, non ore.</p>
        <p>Voi potete aiutare portando oggetti familiari man mano, condividendo ricette preferite con la cucina, raccontando al personale aneddoti utili ("Non gli piace il caffè forte", "Il lunedì chiama sempre mia sorella"). Dettagli che costruiscono cura personalizzata.</p>
        <h2>Quando la famiglia e la struttura collaborano</h2>
        <p>Le migliori esperienze nascono quando famiglia e operatori si considerano alleati. Non avversari che "tengono" vostro padre, non custodi che vi escludono. Chiedete aggiornamenti regolari all'inizio — poi trovate ritmo sostenibile.</p>
        <p>Se qualcosa non vi convince, parlatene subito con calma. Meglio chiarire subito un malinteso che accumulare risentimento. Una casa famiglia seria accoglie feedback.</p>
        <p>L'inserimento è ponte verso una nuova normalità. Non sostituisce il passato — lo onora dando a vostro caro un presente più sicuro e voi figli un po' di respiro meritato.</p>
""",
    "autonomia-dignita-terza-eta": """
        <h2>Piccoli gesti quotidiani che contano</h2>
        <p>Autonomia si esprime nei dettagli: scegliere cosa indossare, decidere se partecipare al gioco a tombola, dire di no a un dolce. In casa famiglia rispettiamo questi no e questi sì. Non uniformiamo per comodità organizzativa.</p>
        <p>Invitate vostro caro a portare decisioni: quale pianta in camera, quale programma TV la sera. Micro-scelte che ricordano: "La mia vita è ancora mia."</p>
        <h2>Quando l'autonomia cambia</h2>
        <p>Con gli anni, capacità possono diminuire lentamente. Il dialogo anticipato evita crisi: se camminare diventa più difficile, se serve più aiuto a tavola, se compagnia diventa necessità più che desiderio. Adattare supporto non è togliere dignità — è riconoscere nuove esigenze con rispetto.</p>
        <p>Per voi figli, accettare che vostro padre non è immutabile richiede maturità. Amare significa anche accogliere cambiamento senza negarlo.</p>
        <p>Dignità e autonomia non sono slogan — sono pratica quotidiana. In una casa famiglia a Coazze le mettiamo al centro di ogni giornata, perché vostro caro resta persona, non numero.</p>
""",
    "coazze-giaveno-pinerolo-servizi": """
        <h2>Distances and practical tips</h2>
        <p>Da Giaveno, percorso tipico in auto verso Coazze richiede pochi minuti — ideale per visite frequenti senza pianificazione complessa. Da Avigliana, percorso simile attraverso strade di valle familiari a chi ha vissuto la zona.</p>
        <p>Da Pinerolo si attraversa un territorio che molti anziani conoscono per mercati, parenti, abitudini. Organizzate visite di prova un giorno feriale e uno festivo per valutare traffico e tempi reali — non solo mappe online.</p>
        <h2>Servizi nel territorio</h2>
        <p>Medici di base, farmacie, laboratori analisi sono presenti nei comuni limitrofi. Per controlli specialistici, Torino e Pinerolo offrono opzioni. Coordinamento con famiglia e medico curante fa parte del lavoro quotidiano in casa famiglia.</p>
        <p>Se vostro caro ha amici o parenti sparsi in valle, restare a Coazze facilita incontri — non li sostituisce, li rende possibili senza lunghe trasferte.</p>
        <p>Non serve abitare in Pinerolo per sentirsi a casa qui. Basta riconoscersi in un territorio amato — e voler per vostro caro serenità, non isolamento.</p>
""",
    "domande-figli-casa-famiglia": """
        <h2>Domande sulla vita quotidiana</h2>
        <p><strong>Mangia bene?</strong> Pasti sono conviviali ma rispettano preferenze. Segnalate allergie, abitudini, piatti amati — la cucina casalinga si adatta dove possibile.</p>
        <p><strong>Si annoia?</strong> Attività variano: lettura, giardinaggio, conversazione, passeggiate. Chi preferisce quiete non viene forzato al bingo. Equilibrio tra stimolo e riposo.</p>
        <p><strong>Posso portarlo fuori per un pranzo?</strong> Concordate con lo staff. Uscite familiari sono benvenute quando compatibili con benessere dell'ospite.</p>
        <h2>Domande emotive</h2>
        <p><strong>Mi perdonerà?</strong> Molti genitori, mesi dopo, ringraziano per aver ascoltato bisogno di compagnia e sicurezza. Non tutti lo diranno apertamente — osservate serenità, sonno, appetito.</p>
        <p><strong>I fratelli non sono d'accordo.</strong> Normalizzate il conflitto. Proponete visita congiunta, confronto su fatti non su colpe. Un medico di famiglia o una terza voce neutrale aiuta.</p>
        <p>Continuate a chiedere. Ogni domanda onesta vi avvicina a decisione condivisa e serena — per vostro caro e per voi.</p>
""",
}

# Fix English header in coazze expansion
EXPANSIONS["coazze-giaveno-pinerolo-servizi"] = EXPANSIONS["coazze-giaveno-pinerolo-servizi"].replace(
    "Distances and practical tips", "Distanze e consigli pratici"
)

EXPANSIONS_PASS2 = {
    "anziani-autosufficienti-coazze": """
        <h2>Segnali che il vostro caro potrebbe stare meglio in casa famiglia</h2>
        <p>Pranzi saltati, frigorifero vuoto a metà settimana, telefonate sempre più brevi, paura di uscire quando piove o quando fa buio presto. Non sono "capricci dell'età" — sono bisogni non soddisfatti. Riconoscerli presto permette scelte condivise invece di decisioni d'urgenza dopo una caduta o un malore.</p>
        <p>Parlate con vicini di casa, amici del paese, parroco se frequenta. Spesso la comunità vede ciò che i figli lontani non vedono. Integrate osservazioni esterne con rispetto — non come spionaggio, ma come rete di cura.</p>
""",
    "autonomia-dignita-terza-eta": """
        <h2>Il linguaggio che usiamo ogni giorno</h2>
        <p>In casa famiglia evitiamo termini che etichettano: niente "il signor Rossi al reparto", niente toni da istituto. Ogni ospite ha nome, storia, preferenze. I figli ci aiutano raccontandoci abitudini: "Mio padre ama Radio Tre", "Mia madre preferisce sedersi vicino alla finestra."</p>
        <p>Questi dettagli non sono superficiali — sono mattoni di dignità. Un anziano che sente di essere ancora riconosciuto come persona intera vive meglio, mangia meglio, dorme meglio.</p>
        <h2>Per voi che vi sentite in colpa</h2>
        <p>Scegliere una casa famiglia non vi rende figli cattivi. Vi rende figli che hanno capito i limiti del corpo e del tempo — e che cercano per il genitore un ambiente dove non debba più aver paura di restare solo la notte.</p>
""",
    "coazze-giaveno-pinerolo-servizi": """
        <h2>Testimonianze di famiglie del territorio</h2>
        <p>Spesso ci scelgono famiglie che dicono: "Volevamo restare in valle." Non sempre Coazze era il comune d'origine — ma la distanza da Giaveno o Avigliana rendeva le visite possibili, non eroiche. Questo fa differenza nel lungo periodo: visite regolari mantengono legame, visite rare alimentano colpa.</p>
        <p>Se venite da Pinerolo o dalla bassa valle, pianificate una prima visita di scoperta un pomeriggio di sole. Portate vostro caro se è possibile — vedere insieme riduce immaginazione peggiorativa.</p>
""",
    "costi-retta-casa-famiglia-piemonte": """
        <h2>Confronto con altre soluzioni</h2>
        <p>Assistenza domiciliare intensiva, badante convivente, modifiche casa con tecnologia: ogni opzione ha costi e limiti. La badante 24 ore su 24 può costare quanto o più di una retta, senza garantire compagnia di pari o spazi comuni. Valutate il pacchetto completo, non solo la cifra isolata.</p>
        <p>Chiedete preventivo scritto e confrontate almeno due strutture. Coazze e valle offrono alternative meno caotiche della città — a parità di qualità, il benessere quotidiano del vostro caro non ha prezzo ma ha valore misurabile in sonno tranquillo per tutti.</p>
""",
    "domande-figli-casa-famiglia": """
        <h2>Domande su sicurezza e salute</h2>
        <p><strong>Cosa succede di notte?</strong> Personale presente h24. Non per controllare ogni respiro — per intervenire se serve.</p>
        <p><strong>Chiama il medico?</strong> Coordinamento con medico di base e famiglia. Per urgenze, protocolli chiari condivisi con voi.</p>
        <p><strong>Posso parlare con chi lo accoglie ogni giorno?</strong> Sì. Comunicazione aperta è parte del servizio. Preferiamo domande in eccesso a silenzio assunto.</p>
""",
    "inserimento-nuovo-ospite": """
        <h2>Cosa portare il giorno dell'ingresso</h2>
        <p>Documenti, farmaci con elenco aggiornato, abiti comodi preferiti, foto, piccoli oggetti affettivi. Evitate di trasferire mobili ingombranti senza concordare — ma una poltrona amata o una lampada possono trasformare una camera in "casa".</p>
        <p>Il primo pranzo insieme è rito importante. Restate se potete, presentate vostro caro agli altri ospiti con naturalezza. Poi, gradualmente, lasciate spazio all'ambientamento — presenza costante all'inizio, distanza rispettosa dopo.</p>
""",
    "valle-di-susa-vita-anziani": """
        <h2>Tradizioni e memoria</h2>
        <p>Sagre, processioni, mercati: la valle vive di ritmi che molti anziani portano nel cuore. Anche se non partecipano come una volta, sapere che quelle tradizioni continuano a pochi chilometri rassicuRA. Visite in occasione di eventi locali possono essere momenti di gioia condivisa.</p>
        <p>Memoria e identità contano quanto assistenza. Una casa famiglia che rispetta radici territoriali non è hotel temporaneo — è continuazione di vita in contesto riconoscibile.</p>
""",
    "visite-familiari-casa-famiglia": """
        <h2>Visite con più figli o generazioni</h2>
        <p>Quando venite in gruppo, concordate prima chi porta notizie delicate e chi si occupa del tono leggero. Nipoti possono animare la visita; evitate però di trasformarla in interrogatorio sul "come stai" ripetuto da ogni adulto.</p>
        <p>Foto di gruppo, passeggiata in giardino se il tempo lo permette, pranzo portato da fuori se concordato: piccoli rituali che segnano continuità familiare senza sovraccaricare vostro caro.</p>
""",
}

# typo fix
EXPANSIONS_PASS2["valle-di-susa-vita-anziani"] = EXPANSIONS_PASS2["valle-di-susa-vita-anziani"].replace("rassicuRA", "rassicura")


def expand_html(path, slug):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if slug not in EXPANSIONS:
        return
    marker = "      </div>\n      <aside class=\"blog-article-cta\">"
    if EXPANSIONS[slug].strip() in html:
        return
    html = html.replace(marker, EXPANSIONS[slug] + "\n" + marker)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def html_to_md(html_path, md_path, title):
    with open(html_path, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r'<div class="content-prose">(.*?)</div>\s*<aside', html, re.S)
    if not m:
        return
    body = m.group(1)
    body = re.sub(r"<h2>(.*?)</h2>", r"\n## \1\n", body)
    body = re.sub(r"<h3>(.*?)</h3>", r"\n### \1\n", body)
    body = re.sub(r"<p>(.*?)</p>", r"\1\n", body, flags=re.S)
    body = re.sub(r"<li>(.*?)</li>", r"- \1\n", body, flags=re.S)
    body = re.sub(r"<[^>]+>", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{body.strip()}\n")


def main():
    all_expansions = {**EXPANSIONS, **EXPANSIONS_PASS2}
    for slug, extra in all_expansions.items():
        html_path = os.path.join(BLOG_DIR, slug, "index.html")
        if not os.path.exists(html_path):
            continue
        with open(html_path, encoding="utf-8") as f:
            html = f.read()
        if extra.strip() not in html:
            marker = "      </div>\n      <aside class=\"blog-article-cta\">"
            html = html.replace(marker, extra + "\n" + marker)
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)
        md_path = os.path.join(CONTENT_DIR, f"{slug}.md")
        with open(html_path, encoding="utf-8") as f:
            t = re.search(r"<h1>(.*?)</h1>", f.read())
        title = t.group(1) if t else slug
        html_to_md(html_path, md_path, title)
        print(f"Expanded {slug}")


if __name__ == "__main__":
    main()
