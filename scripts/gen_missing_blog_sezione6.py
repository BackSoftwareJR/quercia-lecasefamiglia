#!/usr/bin/env python3
"""Generate missing SEZIONE 6 blog articles."""
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://casafamigliaquercia.it"
OG_IMAGE = f"{SITE}/images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/img1.avif"
IMG_DIR = "Pinerolo - Casa Famiglia Quercia 1"

ARTICLES = [
    {
        "slug": "cosa-include-retta-casa-famiglia",
        "title": "Cosa include la retta di una casa famiglia? Tutto quello che devi sapere",
        "meta": "Cosa copre la retta mensile di una casa famiglia? Pasti, assistenza, terapie, pulizie: ecco cosa è incluso (e cosa non lo è). Guida chiara per famiglie.",
        "keywords": "casa famiglia Pinerolo, retta casa famiglia, cosa include retta",
        "category": "Costi",
        "badge": "Costi",
        "hero": "img6.avif",
        "hero_alt": "Cucina domestica con pasti freschi preparati ogni giorno",
        "whatsapp": "Buongiorno%2C%20vorrei%20capire%20cosa%20include%20la%20retta%20di%20una%20casa%20famiglia.",
        "related": [
            ("Costi", "Costi e retta in casa famiglia in Piemonte: guida chiara", "/blog/costi-retta-casa-famiglia-piemonte/"),
            ("Guida", "Casa famiglia vs RSA: differenze vere per la tua famiglia", "/blog/casa-famiglia-vs-rsa-differenze/"),
            ("FAQ", "Le domande che i figli fanno prima della casa famiglia", "/blog/domande-figli-casa-famiglia/"),
        ],
        "toc": [
            ("cosa-comprende", "1) Cosa comprende di solito la retta mensile"),
            ("voci-extra", "2) Le voci extra: cosa chiedere prima di firmare"),
            ("confronto-soluzioni", "3) Confronto con assistenza a domicilio e RSA"),
            ("sostenibilita", "4) Sostenibilità nel tempo per la famiglia"),
            ("conclusione", "Conclusione: trasparenza è cura"),
        ],
        "incipit": (
            '<p class="blog-dropcap">La prima domanda di quasi tutte le famiglie è: "Quanto costa?" Ed è la domanda giusta. '
            'Ma la seconda, quella che fa davvero la differenza, è: "E cosa include?"</p>'
            '<p>Perché una retta apparentemente bassa può nascondere decine di voci extra. E una retta all-inclusive '
            'può essere il miglior investimento che fai per tuo padre o tua madre. In questa guida ti spieghiamo, '
            'con chiarezza e senza giri di parole, cosa trovi dietro al numero mensile di una casa famiglia. '
            'Per iniziare puoi consultare <a href="/rette-e-ammissione/">rette e ammissione</a>, '
            '<a href="/servizi/">servizi</a> e <a href="/contatti/">contatti</a>.</p>'
        ),
        "sections": [
            ("cosa-comprende", "1) Cosa comprende di solito la retta mensile", [
                "In una casa famiglia per anziani autosufficienti, la retta non è solo un affitto con pasti. È un pacchetto di vita quotidiana: alloggio in camera personale o condivisa, vitto completo, gestione della casa, presenza dell'équipe, monitoraggio discreto e attività di relazione. Ogni struttura organizza questi elementi in modo diverso, ma la logica è la stessa: offrire un contesto domestico dove l'ospite non deve più preoccuparsi di tutto da solo.",
                "I pasti sono spesso il cuore dell'inclusione. Non si tratta solo di nutrire, ma di creare momenti di convivialità: colazione, pranzo, merenda, cena. In molte case famiglia i menu sono cucinati in loco, con attenzione alle preferenze e alle esigenze alimentari. Chiedi sempre come vengono gestite le diete speciali e se ci sono supplementi per particolari richieste.",
                "L'assistenza quotidiana comprende supporto nelle attività ordinarie: accompagnamento nei pasti se serve, aiuto nell'igiene personale leggera, promemoria per le terapie, vigilanza notturna discreta. Non è assistenza sanitaria intensiva come in RSA, ma una presenza costante che evita solitudine e piccoli rischi domestici.",
                "Spesso sono inclusi anche pulizia della camera, biancheria, lavanderia, utenze, Wi-Fi e attività ricreative. Alcune strutture includono anche accompagnamento a visite mediche di routine, gestione delle terapie ordinarie e comunicazione periodica con i familiari. Altri servizi, come parrucchiere o podologo, possono essere organizzati internamente o tramite professionisti esterni.",
                "La Casa Famiglia Quercia a Pinerolo adotta un approccio trasparente: durante la visita spieghiamo punto per punto cosa è compreso, così i figli possono confrontare con serenità. Per il dettaglio completo visita <a href='/servizi/'>la pagina servizi</a>.",
            ]),
            ("voci-extra", "2) Le voci extra: cosa chiedere prima di firmare", [
                "Il punto critico di molte rette è ciò che resta fuori. Farmaci, visite specialistiche, pannoloni, servizi di parrucchiere, trasporti per appuntamenti medici, materiali sanitari specifici: possono generare costi aggiuntivi. Non è un problema in sé, ma devono essere comunicati in anticipo, non scoperti a contratto firmato.",
                "Chiedi una lista scritta degli extra possibili e delle modalità di fatturazione. Alcune strutture includono tutto in un prezzo unico; altre applicano tariffe a consumo per servizi specifici. Entrambi i modelli possono funzionare, purché siano chiari fin dall'inizio. La trasparenza protegge il rapporto tra famiglia e casa.",
                "Attenzione anche ai contributi regionali o comunali: in Piemonte esistono possibilità di agevolazione per l'assistenza agli anziani non autosufficienti, ma le regole cambiano. Una casa famiglia seria ti orienta su dove informarti, senza promettere benefici che non può garantire.",
                "Prima di decidere, confronta almeno due o tre strutture con la stessa griglia di domande. Puoi usare la guida <a href='/blog/costi-retta-casa-famiglia-piemonte/'>costi e retta in Piemonte</a> e le <a href='/blog/domande-figli-casa-famiglia/'>domande dei figli</a> come riferimento.",
            ]),
            ("confronto-soluzioni", "3) Confronto con assistenza a domicilio e RSA", [
                "Confrontare la retta di una casa famiglia con altre soluzioni richiede di guardare il quadro completo. L'assistenza a domicilio può sembrare meno costosa sulla carta, ma spesso somma badante, pulizie, pasti a domicilio, telefono di emergenza e il tempo che i figli dedicano all'organizzazione. Quando calcoli tutto, la differenza si assottiglia.",
                "La RSA ha costi generalmente più alti e include assistenza sanitaria strutturata. È la scelta giusta quando le esigenze cliniche sono complesse. La casa famiglia si colloca in uno spazio intermedio: contesto domestico, dimensione ridotta, autonomia preservata. Per capire quale strada è più adatta, leggi <a href='/blog/casa-famiglia-vs-rsa-differenze/'>casa famiglia vs RSA</a>.",
                "Il valore della retta va misurato anche in qualità di vita: compagnia quotidiana, pasti condivisi, giardino, attività, serenità dei figli che non devono correre ogni giorno a sistemare imprevisti. Questi elementi non compaiono in una fattura, ma incidono profondamente sul benessere di tutti.",
                "Molte famiglie del Pinerolese e dell'area torinese ci dicono che, una volta compreso cosa include la retta, la scelta diventa più lucida. Non si tratta di trovare il prezzo più basso, ma il miglior equilibrio tra costo, servizi e serenità.",
            ]),
            ("sostenibilita", "4) Sostenibilità nel tempo per la famiglia", [
                "Una retta sostenibile è quella che la famiglia può mantenere senza tensioni continue. Prima di impegnarsi, valuta le entrate disponibili, eventuali contributi di altri familiari, la possibilità di accesso a agevolazioni e un margine per imprevisti. Parlarne tra fratelli e sorelle prima dell'ingresso evita conflitti futuri.",
                "Il senso di colpa spesso spinge a scegliere la soluzione più economica, anche quando non è la più adatta. Ricorda che investire nella qualità della vita di un genitore non è un lusso: è una scelta di cura. Una retta chiara e sostenibile protegge anche la relazione familiare.",
                "La Casa Famiglia Quercia a Pinerolo accompagna le famiglie in questa valutazione senza pressione commerciale. L'obiettivo è trovare un equilibrio realistico, non convincere a tutti i costi. Quando numeri e aspettative sono allineati, il percorso è più sereno per l'ospite e per i figli.",
                "Per approfondire la scelta consapevole consulta <a href='/blog/scegliere-casa-famiglia-genitori/'>come scegliere una casa famiglia</a> e prenota una visita da <a href='/contatti/'>contatti</a>.",
            ]),
            ("conclusione", "Conclusione: trasparenza è cura", [
                "Capire cosa include la retta non è un dettaglio burocratico: è il fondamento di una scelta consapevole. Quando sai esattamente cosa paghi e cosa ricevi, puoi confrontare le offerte con lucidità e proteggere la serenità della tua famiglia.",
                "Ogni casa famiglia ha la sua organizzazione, ma i principi restano gli stessi: chiarezza, rispetto, comunicazione. Chiedi sempre, scrivi le risposte, confronta. I figli che fanno domande precise prendono decisioni migliori.",
                "Se vuoi un quadro concreto su cosa comprende la retta a Casa Famiglia Quercia, siamo a Pinerolo in Stradale Poirino 152. Una visita gratuita è il modo migliore per capire cosa c'è dietro al numero — e cosa c'è dietro al numero per la vita di tuo padre o tua madre.",
            ]),
        ],
        "faq": [
            ("Cosa include di solito la retta di una casa famiglia?",
             "In genere comprende alloggio, pasti, assistenza quotidiana, pulizia, biancheria, utenze e attività ricreative. I dettagli variano: chiedi sempre un elenco scritto prima di decidere."),
            ("Ci sono costi extra da considerare?",
             "Possono esserci extra per farmaci, visite specialistiche, servizi estetici o trasporti. Una struttura trasparente te li comunica in anticipo, non a sorpresa."),
            ("Come confronto la retta con l'assistenza a domicilio?",
             "Somma tutti i costi della badante, pasti, pulizie e il tempo dei figli. Spesso la differenza reale è minore di quanto sembri, mentre il beneficio relazionale della casa famiglia è maggiore."),
        ],
    },
    {
        "slug": "anziano-solo-soluzioni",
        "title": "Mio genitore vive solo: cosa fare quando inizia a essere un problema",
        "meta": "Tuo genitore è ancora autosufficiente ma la solitudine lo pesa? Ecco le soluzioni concrete, dalla badante alla casa famiglia, e come capire quando è il momento di agire.",
        "keywords": "anziano solo, soluzioni anziani, casa famiglia Pinerolo, solitudine terza età",
        "category": "Cura relazionale",
        "badge": "Cura relazionale",
        "hero": "img7.avif",
        "hero_alt": "Camera confortevole con arredi personali in ambiente domestico",
        "whatsapp": "Buongiorno%2C%20mio%20genitore%20vive%20da%20solo%20e%20vorrei%20capire%20quali%20soluzioni%20esistono.",
        "related": [
            ("Territorio", "Anziani autosufficienti a Pinerolo: quando la casa è la scelta giusta", "/blog/anziani-autosufficienti-coazze/"),
            ("Scelta consapevole", "Come scegliere una casa famiglia per i genitori", "/blog/scegliere-casa-famiglia-genitori/"),
            ("Benessere", "Autonomia e dignità nella terza età: cosa significa davvero", "/blog/autonomia-dignita-terza-eta/"),
        ],
        "toc": [
            ("segnali", "1) I segnali che qualcosa sta cambiando"),
            ("soluzioni-intermedie", "2) Soluzioni intermedie prima della casa famiglia"),
            ("quando-casa-famiglia", "3) Quando la casa famiglia è la risposta giusta"),
            ("parlare-genitore", "4) Come parlarne con tuo padre o tua madre"),
            ("conclusione", "Conclusione: agire prima dell'emergenza"),
        ],
        "incipit": (
            '<p class="blog-dropcap">C\'è un momento, in molte famiglie, in cui ci si rende conto che qualcosa è cambiato. '
            'Non un evento drammatico, solo una sensazione. Tua madre mangia meno. Tuo padre non scende più a fare la spesa da solo. '
            'Le telefonate si fanno più brevi, o più frequenti del solito.</p>'
            '<p>Non è una crisi. È un passaggio. E la buona notizia è che ci sono opzioni, buone opzioni, per affrontarlo senza aspettare '
            'che diventi un\'emergenza. In questa guida esploriamo le soluzioni concrete per un genitore che vive solo ma inizia a faticare. '
            'Per orientarti puoi consultare <a href="/requisiti-autosufficienza/">requisiti di autosufficienza</a>, '
            '<a href="/servizi/">servizi</a> e <a href="/contatti/">contatti</a>.</p>'
        ),
        "sections": [
            ("segnali", "1) I segnali che qualcosa sta cambiando", [
                "La solitudine non si annuncia con un campanello d'allarme. Arriva in piccoli segnali: il frigorifero che resta vuoto troppo a lungo, la casa meno curata, la televisione accesa tutto il giorno, la riluttanza a uscire anche quando il tempo è bello. I figli che vivono lontano spesso se ne accorgono durante le telefonate: risposte più brevi, voce più stanca, meno voglia di raccontare la giornata.",
                "Altri indizi sono più concreti: dimenticanze nelle terapie, difficoltà a gestire la spesa, paura di cadere in casa, chiamate notturne per paure irrazionali. Non significa che serva subito una RSA. Spesso significa che il contesto attuale — casa grande, vicini lontani, figli impegnati — non regge più come prima.",
                "Riconoscere questi segnali presto è un vantaggio enorme. Permette di scegliere con calma, coinvolgere il genitore nella decisione e valutare soluzioni graduali. Aspettare la caduta, il malore o la crisi emotiva significa decidere sotto pressione, con meno opzioni e più stress per tutti.",
                "Se vuoi capire meglio quando intervenire, leggi <a href='/blog/anziani-autosufficienti-coazze/'>anziani autosufficienti a Pinerolo</a> e la pagina <a href='/requisiti-autosufficienza/'>requisiti di autosufficienza</a>.",
            ]),
            ("soluzioni-intermedie", "2) Soluzioni intermedie prima della casa famiglia", [
                "Non tutte le situazioni richiedono subito un cambio di residenza. Esistono passaggi intermedi che possono aiutare: telefono di sicurezza, servizi di consegna pasti a domicilio, badante o assistente familiare a ore, telemedicina, adattamenti della casa (maniglie, luci, eliminazione tappeti). Queste soluzioni funzionano quando il genitore è ancora abbastanza autonomo e la solitudine non è ancora cronica.",
                "Il punto critico è la sostenibilità nel tempo. Una badante a ore può coprire le mattine, ma chi resta la sera e la notte? I figli che lavorano e hanno famiglia propria spesso scoprono che coordinare tutto diventa un secondo lavoro. La stanchezza accumulata porta a sensi di colpa e a decisioni affrettate. Molte famiglie ci raccontano di aver provato più soluzioni prima di capire che serviva un cambiamento più strutturale.",
                "I centri di aggregazione per anziani, le attività nel quartiere e i servizi comunali possono aiutare, soprattutto in città. Ma nel Pinerolese e nelle zone più distanti da Torino, dove i trasporti sono limitati e i vicini meno presenti, la solitudine si accentua. È qui che la casa famiglia inizia a diventare una opzione concreta.",
                "Valuta ogni soluzione con una domanda semplice: «Questo migliora la qualità della vita di mio padre o mia madre, o solo rimanda il problema?» Se la risposta è la seconda, forse è il momento di guardare oltre.",
            ]),
            ("quando-casa-famiglia", "3) Quando la casa famiglia è la risposta giusta", [
                "La casa famiglia è pensata per anziani ancora autosufficienti che non vogliono più vivere da soli. Non è un ospedale, non è una RSA: è una casa con poche persone, pasti condivisi, assistenza discreta e la possibilità di portare i propri arredi e abitudini. Per molti genitori è il giusto equilibrio tra autonomia e sicurezza.",
                "È la scelta giusta quando la solitudine pesa più della voglia di restare nell'appartamento vuoto. Quando i figli vivono lontano e non riescono a garantire presenza quotidiana. Quando la gestione della casa — spesa, pulizie, cucina, manutenzione — diventa fonte di stress per l'anziano. Quando si vuole prevenire, non aspettare l'emergenza.",
                "A Pinerolo, Casa Famiglia Quercia accoglie al massimo 8 ospiti. Questo significa relazioni vere, non folle anonime. Gli ospiti mantengono le proprie routine, le proprie scelte, i propri oggetti. I figli restano parte della vita quotidiana, con visite libere e comunicazione costante con l'équipe.",
                "Per confrontare con altre opzioni leggi <a href='/blog/casa-famiglia-vs-rsa-differenze/'>casa famiglia vs RSA</a> e <a href='/blog/scegliere-casa-famiglia-genitori/'>come scegliere una casa famiglia</a>. Una visita gratuita è il modo migliore per capire se è la strada giusta.",
            ]),
            ("parlare-genitore", "4) Come parlarne con tuo padre o tua madre", [
                "Il tema più delicato non è la soluzione, ma la conversazione. Molti genitori interpretano la proposta come un «ti mando via». Il segreto è il linguaggio: non «devi andare in una casa», ma «vogliamo che tu viva bene, con compagnia e senza preoccupazioni». Mostrare foto, raccontare come funziona una giornata, proporre una visita senza impegno.",
                "Coinvolgere il genitore fin dall'inizio cambia tutto. Chi sceglie partecipando al processo arriva con meno paura e si adatta più in fretta. Chi si sente imposto resiste, soffre, e conferma il proprio timore di essere «abbandonato».",
                "I figli spesso temono la reazione e rimandano il dialogo. Rimandare però peggiora la situazione: la solitudine aumenta, i segnali si intensificano, e quando si parla finalmente si è già in urgenza. Meglio una conversazione difficile oggi che una crisi domani.",
                "Se ti serve supporto nel dialogo familiare, contattaci da <a href='/contatti/'>contatti</a>. Possiamo accogliere voi e vostro padre o madre per una visita conoscitiva, senza pressione e senza obblighi.",
            ]),
            ("conclusione", "Conclusione: agire prima dell'emergenza", [
                "Un genitore che vive solo e inizia a faticare non ha bisogno di drammi: ha bisogno di opzioni. La solitudine è silenziosa, ma non è irreversibile. Con le soluzioni giuste — intermedie o strutturali — si può recuperare qualità di vita e serenità per tutta la famiglia.",
                "Il momento migliore per agire è quando i segnali sono chiari ma non c'è ancora urgenza. È allora che si può scegliere con lucidità, visitare le strutture, coinvolgere il genitore, pianificare con calma.",
                "Se il tuo padre o la tua madre vive nel Pinerolese o nell'area torinese e senti che il tempo da solo pesa troppo, Casa Famiglia Quercia a Pinerolo è a tua disposizione. Una telefonata, una visita, un confronto senza impegno: a volte basta questo per capire che non siete soli in questa scelta.",
            ]),
        ],
        "faq": [
            ("Come capisco se mio genitore ha bisogno di aiuto?",
             "Osserva cambiamenti nelle abitudini: meno appetito, casa meno curata, isolamento, dimenticanze, paura di uscire. Se i segnali persistono per settimane, è il momento di valutare soluzioni."),
            ("La casa famiglia è adatta se è ancora autosufficiente?",
             "Sì, anzi: la casa famiglia è pensata proprio per anziani autonomi che non vogliono più vivere soli. Offre compagnia e sicurezza senza togliere indipendenza."),
            ("Come posso proporre il cambiamento senza creare conflitto?",
             "Usa un linguaggio positivo, proponi una visita senza impegno, coinvolgi il genitore nelle scelte. Mostrare la casa di persona è più efficace di mille discussioni."),
        ],
    },
    {
        "slug": "senso-di-colpa-casa-famiglia",
        "title": "Il senso di colpa di chi cerca una casa famiglia (e perché non dovresti averlo)",
        "meta": "Cercare una soluzione per un genitore anziano non significa abbandonarlo. Un articolo onesto per le famiglie che si trovano a fare questa scelta difficile.",
        "keywords": "senso di colpa casa famiglia, figli anziani, cura genitori Pinerolo",
        "category": "Cura relazionale",
        "badge": "Cura relazionale",
        "hero": "img2.avif",
        "hero_alt": "Spazi comuni accoglienti dove ospiti e familiari si incontrano",
        "whatsapp": "Buongiorno%2C%20sto%20cercando%20una%20casa%20famiglia%20e%20ho%20molto%20senso%20di%20colpa.%20Vorrei%20parlarne.",
        "related": [
            ("FAQ", "Le domande che i figli fanno prima della casa famiglia", "/blog/domande-figli-casa-famiglia/"),
            ("Vita in casa", "Visite familiari in casa famiglia: regole, ritmo e serenità", "/blog/visite-familiari-casa-famiglia/"),
            ("Accoglienza", "Inserimento di un nuovo ospite: i primi 30 giorni", "/blog/inserimento-nuovo-ospite/"),
        ],
        "toc": [
            ("perche-colpa", "1) Perché il senso di colpa è così comune"),
            ("non-abbandono", "2) Cercare aiuto non è abbandonare"),
            ("cambiamento-ruolo", "3) Il cambiamento di ruolo dei figli"),
            ("convivere-colpa", "4) Come convivere con il senso di colpa"),
            ("conclusione", "Conclusione: amore e responsabilità non sono in conflitto"),
        ],
        "incipit": (
            '<p class="blog-dropcap">Se stai leggendo questo articolo, probabilmente stai cercando una soluzione per qualcuno che ami. '
            'E probabilmente, da qualche parte, senti un peso.</p>'
            '<p>È normale. Quasi ogni figlio o figlia che viene da noi lo sente. Il senso di colpa per il solo fatto di cercare. '
            'Come se chiedere aiuto fosse un fallimento. Non lo è. E in questo articolo vogliamo spiegarti perché, con onestà, senza buonismi. '
            'Per approfondire puoi consultare <a href="/servizi/">servizi</a>, '
            '<a href="/contatti/">contatti</a> e la guida <a href="/blog/domande-figli-casa-famiglia/">domande dei figli</a>.</p>'
        ),
        "sections": [
            ("perche-colpa", "1) Perché il senso di colpa è così comune", [
                "Il senso di colpa nasce da un'intuizione profonda: i figli sentono di dover restituire ciò che i genitori hanno dato. Crescere, nutrire, proteggere, educare: quando i ruoli si invertono, sembra che chiedere aiuto equivalga a tradire quel debito affettivo. La cultura italiana rafforza questa idea: «la famiglia si aiuta da sola», «non si manda via mamma».",
                "A questo si aggiunge la paura del giudizio: vicini, parenti, amici che potrebbero pensare «non vogliono occuparsene». Molti figli tra i 45 e i 65 anni vivono questo conflitto in silenzio, cercando informazioni di notte, senza parlarne con fratelli o amici. Il senso di colpa diventa un compagno costante, che appesantisce ogni ricerca.",
                "Ma il senso di colpa non è un indicatore di verità. È un'emozione, spesso legittima nel suo bisogno di proteggere, ma non sempre allineata alla realtà. Riconoscerlo è il primo passo per non lasciare che guidi la decisione al posto tuo. Molti figli ci dicono che il senso di colpa è più forte prima della visita che dopo: vedere la casa, conoscere l'équipe e osservare gli ospiti tranquilli riduce la distanza tra paura e realtà.",
                "Se ti riconosci in questa descrizione, sappi che non sei solo. È la domanda più frequente che ci fanno i figli che visitano Casa Famiglia Quercia a Pinerolo.",
            ]),
            ("non-abbandono", "2) Cercare aiuto non è abbandonare", [
                "Abbandonare significa smettere di essere presenti. Cercare una casa famiglia significa trovare un contesto dove il genitore vive meglio, con compagnia, pasti curati, assistenza discreta e sicurezza. I figli non spariscono: cambiano modo di essere presenti. Da gestori di ogni imprevisto diventano compagni di vita, visitatori sereni, interlocutori affettuosi.",
                "Molte famiglie scoprono che, una volta alleggerito il carico pratico, la relazione con il genitore migliora. Le visite non sono più corse per sistemare la spesa o controllare le medicine: sono tempo di qualità. Conversazioni, passeggiate, pranzi insieme. Il legame si approfondisce perché non è più schiacciato dalla fatica.",
                "Un genitore solo in un appartamento vuoto non è necessariamente più «accolto» di un genitore in una casa famiglia con 7 compagni di vita, un giardino e un'équipe che lo conosce per nome. A volte la scelta più amorevole è proprio quella che sembra più difficile da accettare.",
                "Per capire come funzionano le visite e la continuità relazionale, leggi <a href='/blog/visite-familiari-casa-famiglia/'>visite familiari in casa famiglia</a> e <a href='/blog/inserimento-nuovo-ospite/'>inserimento del primo mese</a>.",
            ]),
            ("cambiamento-ruolo", "3) Il cambiamento di ruolo dei figli", [
                "Per decenni i genitori hanno protetto i figli. Ora i figli sentono il dovere di proteggere i genitori. Ma proteggere non significa fare tutto da soli. Significa garantire le condizioni migliori per il benessere dell'altro, anche quando questo implica chiedere supporto esterno.",
                "Il caregiver che non chiede mai aiuto finisce per esaurirsi. E un figlio esaurito non è un buon sostegno per nessuno. Il senso di colpa che impedisce di cercare una soluzione spesso produce l'effetto opposto: meno energia per la relazione, più irritabilità, più rimpianti.",
                "Accettare di non poter essere ovunque — al lavoro, con i propri figli, a casa del genitore ogni giorno — non è debolezza. È realismo. La casa famiglia esiste proprio per questo: per offrire ciò che la famiglia, da sola, non riesce a garantire 24 ore su 24.",
                "Il cambiamento di ruolo può essere un passaggio di maturità affettiva. Non stai scaricando un peso: stai costruendo una rete di cura più ampia e più sostenibile. I nipoti, quando ci sono, spesso vivono le visite in casa famiglia con più serenità: meno stress, più tempo per stare insieme davvero.",
            ]),
            ("convivere-colpa", "4) Come convivere con il senso di colpa", [
                "Non serve eliminare il senso di colpa per decidere. Serve metterlo al suo posto: ascoltarlo, riconoscerlo, ma non lasciare che sia l'unica voce in sala. Confrontati con i fatti: tuo padre o tua madre è davvero meglio da solo, o solo più abituato alla solitudine?",
                "Parla con fratelli e sorelle. Spesso il senso di colpa si dissolve quando la decisione è condivisa. Un figlio che si sente l'unico responsabile porta un peso doppio. Distribuire la scelta significa distribuire anche la serenità.",
                "Visita le strutture con calma. Vedere con i propri occhi una casa famiglia accogliente — non un reparto freddo — cambia la prospettiva. Molti figli ci dicono, dopo la visita: «Non mi aspettavo che fosse così... normale». Portare con sé il genitore, quando possibile, riduce ancora di più la distanza tra immaginazione e realtà.",
                "Se il peso è troppo forte, parlane con qualcuno di fiducia: un medico di famiglia, un operatore sociale, o semplicemente con noi. A Pinerolo siamo abituati ad accogliere famiglie in questo momento. Nessun giudizio, solo ascolto.",
            ]),
            ("conclusione", "Conclusione: amore e responsabilità non sono in conflitto", [
                "Cercare una casa famiglia per un genitore anziano non è l'opposto dell'amore. È una forma di amore maturo: quello che mette il benessere dell'altro davanti all'immagine che noi abbiamo di noi stessi come figli perfetti.",
                "Il senso di colpa ti dirà che dovresti fare di più. La realtà ti dirà che fare di più, da soli, non è sempre possibile né sempre la scelta migliore per chi ami. Ascolta entrambi, ma decidi con lucidità.",
                "Casa Famiglia Quercia a Pinerolo è qui per questo: per offrire un'alternativa concreta a chi non vuole più vivere da solo, e per accompagnare le famiglie che fanno una scelta difficile con dignità e senza giudizio. Una visita gratuita può essere il primo passo per alleggerire quel peso che porti da solo. Non devi avere tutte le risposte prima di chiamare: basta voler capire, con calma, se questa strada può essere quella giusta per la vostra famiglia.",
            ]),
        ],
        "faq": [
            ("È normale sentirsi in colpa cercando una casa famiglia?",
             "Sì, quasi tutti i figli provano questo sentimento. Non significa che la scelta sia sbagliata: significa che ami profondamente il tuo genitore."),
            ("Cercare una casa famiglia significa abbandonare mio padre o mia madre?",
             "No. Significa trovare un contesto dove vive meglio, con compagnia e assistenza. I figli restano presenti con visite, telefonate e partecipazione attiva."),
            ("Come posso superare il senso di colpa?",
             "Parlane con fratelli, visita le strutture di persona, separa l'emozione dai fatti. Una decisione condivisa e informata alleggerisce il peso emotivo."),
        ],
    },
]


def paragraphs_html(items):
    return "".join(f"<p>{p}</p>" for p in items)


def sections_html(sections):
    out = []
    for sid, title, paras in sections:
        out.append(f'<h2 id="{sid}">{title}</h2>{paragraphs_html(paras)}')
    return "".join(out)


def faq_html(faq, slug):
    items = []
    for i, (q, a) in enumerate(faq, 1):
        uid = f"faq-{slug}-{i}"
        hidden = "" if i == 1 else " hidden"
        expanded = "true" if i == 1 else "false"
        items.append(f"""<div class="accordion__item">
            <button type="button" class="accordion__trigger faq-question" aria-expanded="{expanded}" aria-controls="{uid}" id="faq-trigger-{slug}-{i}">{q}<svg class="accordion__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
            <div id="{uid}" class="accordion__panel faq-answer" role="region" aria-labelledby="faq-trigger-{slug}-{i}"{hidden}><p>{a}</p></div>
          </div>""")
    return "\n          ".join(items)


def faq_schema(faq):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }


def related_html(related):
    items = []
    for cat, title, href in related:
        items.append(f"""<li class="blog-sidebar-related__item">
              <a href="{href}" class="blog-sidebar-related__link">
                <span class="blog-sidebar-related__cat">{cat}</span>
                <span class="blog-sidebar-related__title">{title}</span>
                <span class="blog-sidebar-related__date">22 giugno 2026</span>
              </a>
            </li>""")
    return "".join(items)


def toc_html(toc):
    return "".join(f'<li><a href="#{sid}">{label}</a></li>' for sid, label in toc)


def word_count(html):
    text = re.sub(r"<[^>]+>", " ", html)
    return len(re.findall(r"\w+", text))


def render(article):
    slug = article["slug"]
    url = f"{SITE}/blog/{slug}/"
    body = article["incipit"] + sections_html(article["sections"])
    wc = word_count(body)
    faq_section = f"""<section class="blog-article-faq" aria-labelledby="faq-heading-{slug}">
            <h2 id="faq-heading-{slug}">Domande frequenti</h2>
            <div class="accordion faq-accordion">
          {faq_html(article["faq"], slug)}
            </div>
          </section>"""
    toc_with_faq = article["toc"] + [("faq", "Domande frequenti")]
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{article['title']}</title>
  <meta name="description" content="{article['meta']}">
  <meta name="robots" content="index, follow">
  <meta name="keywords" content="{article['keywords']}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="it" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="it_IT">
  <meta property="og:title" content="{article['title']}">
  <meta property="og:description" content="{article['meta']}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="article:published_time" content="2026-06-22T09:00:00+02:00">
  <meta property="article:modified_time" content="2026-06-22T09:00:00+02:00">
  <meta property="article:author" content="Casa Famiglia Quercia">
  <meta property="article:section" content="{article['category']}">

  <meta name="theme-color" content="#2D5A3D">
  <link rel="icon" href="../../images/favicon.ico" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/design-system.css">
  <link rel="stylesheet" href="../../css/global.css">
  <link rel="stylesheet" href="../../css/animations.css">
  <link rel="stylesheet" href="../../css/components.css">
  <link rel="stylesheet" href="../../css/pages.css">
  <link rel="stylesheet" href="../../blog.css">
  <script type="application/ld+json">
  {json.dumps({
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": article["title"],
    "description": article["meta"],
    "image": OG_IMAGE,
    "datePublished": "2026-06-22T09:00:00+02:00",
    "dateModified": "2026-06-22T09:00:00+02:00",
    "author": {"@type": "Organization", "name": "Casa Famiglia Quercia", "url": SITE + "/"},
    "publisher": {"@type": "Organization", "name": "Casa Famiglia Quercia", "url": SITE + "/"},
    "mainEntityOfPage": {"@type": "WebPage", "@id": url},
    "inLanguage": "it-IT",
    "keywords": article["keywords"],
    "articleSection": article["category"],
    "wordCount": wc,
  }, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">{json.dumps(faq_schema(article["faq"]), ensure_ascii=False)}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}},{{"@type":"ListItem","position":2,"name":"Blog","item":"{SITE}/blog/"}},{{"@type":"ListItem","position":3,"name":{json.dumps(article['title'], ensure_ascii=False)},"item":"{url}"}}]}}</script>
</head>
<body class="blog-page blog-article-page">
  <a href="#main" class="skip-link">Vai al contenuto principale</a>
  <div data-include="header"></div>
  <main id="main">
    <nav class="breadcrumbs container" aria-label="Breadcrumb">
      <ol class="breadcrumbs__list">
        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><a href="/blog/">Blog</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">{article['title']}</span></li>
      </ol>
    </nav>
    <article class="container blog-article">
      <header class="blog-article__header">
        <span class="badge badge--primary">{article['badge']}</span>
        <h1>{article['title']}</h1>
        <p class="blog-article__meta">
          <time datetime="2026-06-22">22 giugno 2026</time>
          · 12 min di lettura
          · <span class="blog-article__author">Casa Famiglia Quercia</span>
        </p>
        <div class="blog-article__tags" aria-label="Tag"></div>
      </header>
      <figure class="blog-article__hero">
        <img src="../../images/{IMG_DIR}/{article['hero']}" alt="{article['hero_alt']}" width="1200" height="630" loading="eager" fetchpriority="high">
        <figcaption>Casa Famiglia Quercia, Stradale Poirino, 152 — Pinerolo, Pinerolese</figcaption>
      </figure>
      <div class="blog-article-layout">
        <div class="blog-article-main">
          <nav class="blog-article__toc" aria-label="Indice dell'articolo">
            <h2>In questo articolo</h2>
            <ol>{toc_html(toc_with_faq)}</ol>
          </nav>
          <div class="content-prose blog-article__body">
{body}
          </div>
          {faq_section}
        </div>
        <aside class="blog-article-sidebar" aria-label="Barra laterale">
          <div class="blog-sidebar-box blog-sidebar-related">
            <h2 class="blog-sidebar-box__title">Articoli correlati</h2>
            <ul class="blog-sidebar-related__list">{related_html(article['related'])}</ul>
          </div><div class="blog-sidebar-box blog-sidebar-cta">
            <h2 class="blog-sidebar-box__title">Scopri Casa Quercia</h2>
            <p class="blog-sidebar-cta__text">Una seconda casa per anziani autosufficienti a Pinerolo, nel Pinerolese.</p>
            <ul class="blog-sidebar-cta__links">
              <li><a href="/galleria/">Galleria fotografica</a></li>
              <li><a href="/servizi/">I nostri servizi</a></li>
              <li><a href="/contatti/">Contatti e visite</a></li>
            </ul>
          </div>
        </aside>
      </div>
      <aside class="blog-article-cta">
        <h2>Hai dubbi? Parliamoci</h2>
        <p>Volete approfondire o prenotare una visita gratuita a Pinerolo? Siamo in Stradale Poirino 152 — rispondiamo con calma, senza pressione.</p>
        <div class="btn-group blog-article-cta__buttons">
          <a href="tel:+393762031211" class="btn btn--accent btn--lg">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" width="20" height="20" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            Chiama — +39 376 203 1211
          </a>
          <a href="https://wa.me/393762031211?text={article['whatsapp']}" class="btn btn--whatsapp btn--lg" target="_blank" rel="noopener noreferrer">
            <img src="../../icons/whatsapp.svg" alt="" width="20" height="20" aria-hidden="true">
            WhatsApp
          </a>
          <a href="/contatti/" class="btn btn--secondary btn--lg">Prenota una visita</a>
        </div>
      </aside>
    </article>
  </main>
  <div data-include="footer"></div>
  <script src="../../js/includes.js" defer></script>
  <script src="../../js/nav.js" defer></script>
  <script src="../../js/main.js" defer></script>
  <script src="../../js/animations.js" defer></script>
  <script src="../../js/cookie-banner.js" defer></script>
</body>
</html>
"""


def main():
    for article in ARTICLES:
        out_dir = os.path.join(BASE, "blog", article["slug"])
        os.makedirs(out_dir, exist_ok=True)
        html = render(article)
        path = os.path.join(out_dir, "index.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        wc = word_count(article["incipit"] + sections_html(article["sections"]))
        print(f"Created {path} ({wc} words)")


if __name__ == "__main__":
    main()
