"""Supplemental paragraphs to reach 1.500+ words per article."""
import re

from blog_articles_data import p, section

# Extra paragraphs keyed by slug -> section id -> list of paragraph strings

EXPANSIONS = {
    "casa-famiglia-vs-rsa-differenze": {
        "cosa-e-casa-famiglia": [
            "A Coazze, Casa Famiglia Quercia accoglie anziani autosufficienti in una villa con giardino, salone condiviso e sala da pranzo dove si incontrano quotidianamente. Il numero contenuto di ospiti permette relazioni autentiche: gli operatori sanno se qualcuno preferisce il tè alle 16 o la lettura silenziosa dopo pranzo.",
            "Per i figli che vivono a Torino o in provincia, questo modello risponde alla domanda ricorrente: «Come posso stare tranquillo senza averlo sotto casa?» La presenza h24 non è vigilanza — è sicurezza condivisa che permette a tutti di dormire.",
        ],
        "differenze-chiave": [
            "Un altro elemento spesso sottovalutato è il cibo. In casa famiglia i pasti sono preparati come a casa, con menu che rispettano tradizioni e preferenze individuali. Nelle RSA la cucina segue protocolli sanitari necessari — giusto per chi ne ha bisogno, eccessivo per chi cerca semplicemente un pranzo di minestra come quella della nonna.",
            "Le visite familiari raccontano la stessa storia: in casa famiglia il nipote può arrivare con il pallone; in molte RSA servono permessi e fasce orarie. Per un anziano autosufficiente, la famiglia non è «visita esterna» — è parte della vita.",
        ],
        "coazze-valle-susa": [
            "Le famiglie di Giaveno ci raccontano spesso che il sabato pomeriggio è diventato rituale: pranzo insieme, passeggiata in giardino, rientro senza stress. Questa frequenza non è lusso — è medicina preventiva per il morale di tutti.",
            "Se cercate «casa famiglia Coazze Valle Susa», state cercando più di una struttura: state cercando un contesto dove vostro caro non deve imparare un nuovo alfabeto urbano a 78 anni.",
        ],
        "conclusione": [
            "Prima di firmare qualsiasi contratto, visitate di persona entrambe le tipologie se avete dubbi. Portate un quaderno, fate domande, osservate. La decisione giusta emergerà dall'esperienza diretta — non dalla paura o dalla fretta.",
        ],
    },
    "scegliere-casa-famiglia-genitori": {
        "prima-di-iniziare": [
            "Molti figli ci raccontano di aver rimandato la decisione per anni, finché un episodio — una caduta, una panico notturno, una confessione di solitudine — ha reso il tema inevitabile. Non giudicatevi per il ritardo: giudicate la qualità della scelta che state per fare.",
            "Coinvolgere il medico di famiglia non delega la decisione — allinea aspettative sanitarie realistiche. Un parere professionale integra il vostro amore senza sostituirlo.",
        ],
        "checklist-domande": [
            "Chiedete come la struttura gestisce le emergenze notturne: chi risponde, come viene coinvolta la famiglia, quali protocolli esistono. La sicurezza h24 è uno dei motivi principali per cui le famiglie scelgono la casa famiglia — verificate che sia concreta, non solo promessa.",
            "Informatevi sulla politica riguardo animali domestici, fumatore, preferenze religiose o culturali. Dettagli che sembrano piccoli definiscono se vostro caro si sentirà rispettato o standardizzato.",
        ],
        "cosa-osservare": [
            "Durante la visita, chiedete di vedere una camera libera e una occupata — la differenza tra potenziale e realtà quotidiana è importante. Una camera modello perfetta non racconta come vivono gli oggetti personali, le foto, le radio accese.",
            "Osservate il personale nei momenti «normali», non solo durante la presentazione ufficiale. Come salutano gli ospiti? Li chiamano per nome? Si fermano per una chiacchiera?",
        ],
        "confronto-strutture": [
            "Se possibile, pranzate nella struttura durante la visita. Il tavolo è il luogo dove la convivialità si mostra senza filtri: chi si sieda vicino a chi, se c'è conversazione, se qualcuno viene aiutato con gentilezza.",
            "Dopo ogni visita, sedetevi con fratelli e sorelle e confrontate impressioni a freddo — non in macchina subito dopo, quando l'emotività è alta.",
        ],
        "conclusione": [
            "Ricordate che nessuna struttura è perfetta al 100%. Cercate quella dove vostro caro potrà essere sé stesso — con storie, abitudini, silenzi e risate. Quella è la casa famiglia giusta per questo momento.",
        ],
    },
    "anziani-autosufficienti-coazze": {
        "perche-coazze": [
            "Coazze offre un ritmo che la città non può replicare: campanile, sentieri, aria pulita, comunità dove le persone si conoscono. Per un anziano che ha vissuto qui decenni, spostarsi in città «per stare meglio» spesso significa perdere tutto ciò che rende la vita significativa.",
            "La temperatura e l'altitudine moderata della valle creano un microclima piacevole per passeggiate quotidiane — attività fondamentale per mobilità e umore in terza età.",
        ],
        "casa-famiglia-vs-soli": [
            "Molti anziani resistono al cambiamento perché associano «casa famiglia» a «casa di riposo» — immagine negativa alimentata da media e storie di terzi. Mostrare foto reali, visitare senza pressione, parlare con chi ci vive: questi gesti disarmano la resistenza più della persuasione verbale.",
            "La solitudine non è solo assenza di persone — è assenza di risposta. In casa vuota, nessuno chiede «come hai dormito?» Nessuno nota se il pranzo è saltato. In casa famiglia, la risposta è quotidiana e discreta.",
        ],
        "vita-quotidiana": [
            "Attività come giardinaggio leggero, giochi da tavolo, lettura condivisa o semplicemente caffè in salone mantengono stimolazione cognitiva senza imporre performance. Ogni ospite sceglie il proprio livello di partecipazione.",
            "Wi-Fi incluso permette videochiamate con nipoti lontani — tecnologia al servizio del legame familiare, non sostituto delle visite.",
        ],
        "conclusione": [
            "Se vostro genitore ama Coazze e la valle, non costringerlo in una soluzione urbana per convenienza vostra. La geografia emotiva conta quanto la geografia pratica.",
        ],
    },
    "valle-di-susa-vita-anziani": {
        "territorio": [
            "La Valle di Susa è collegata a Torino da infrastrutture consolidate: treno, autostrada, percorsi panoramici. Questo permette a figli e nipoti di raggiungere vostro caro senza pianificare giornate intere — fattore decisivo per visite regolari.",
            "Farmacie, ambulatori, servizi di base sono distribuiti nei comuni della valle. Per anziani autosufficienti che necessitano controlli periodici, non serve trasferirsi in città per ogni esigenza sanitaria routinaria.",
        ],
        "socialita": [
            "Eventi locali — mercati, feste di paese, processioni, concerti in piazza — offrono stimolazione sociale naturale. In casa famiglia, organizziamo passeggiate e attività che si integrano con questo calendario territoriale quando possibile.",
            "La memoria del territorio è un capitale: vostro padre che racconta ai nuovi ospiti come era la valle trent'anni fa diventa risorsa sociale, non solo nostalgia.",
        ],
        "casa-grande": [
            "La manutenzione di una casa grande — riscaldamento, giardino, neve, scale — diventa insostenibile con l'età anche per chi è autosufficiente. Trasferirsi in casa famiglia alleggerisce questo carico senza cancellare la storia familiare.",
            "Molte famiglie mantengono la casa di famiglia per ricorrenze e visite, usando la casa famiglia come «casa quotidiana» — modello flessibile che funziona per molti.",
        ],
        "conclusione": [
            "Valle di Susa + casa famiglia: non è romanticismo montanaro — è scelta coerente con una vita costruita tra questi paesi, queste montagne, queste relazioni.",
        ],
    },
    "visite-familiari-casa-famiglia": {
        "importanza": [
            "Le visite familiari non devono essere «ispezioni» — sono continuità di legame. Se ogni incontro diventa controllo medico o interrogatorio su pasti e medicine, vostro caro inizierà a temere le vostre visite. Equilibrio è la parola chiave.",
            "Ricordate che vostro caro costruisce nuove relazioni nella struttura. Non compete con voi — le aggiunge. Accettare che il saluto cordiale con un operatore o un compagno di tavola non diminuisce il vostro ruolo.",
        ],
        "orari-flessibili": [
            "Per famiglie che lavorano, la flessibilità degli orari permette visita serale dopo lavoro o colazione del sabato — momenti che in strutture rigide sarebbero impossibili. Questa accessibilità mantiene frequenza sostenibile.",
            "Se vivete lontano, pianificate visite regolari brevi piuttosto che rare e lunghe: la costanza batte l'intensità per anziani che hanno bisogno di sapere che il mondo familiare non è svanito.",
        ],
        "equilibrio": [
            "Il senso di colpa spinge visite eccessive che confondono vostro caro («Hanno smesso di fidarsi?») o visite rare che confermano abbandono. Chiedete a vostro caro cosa preferisce — la risposta potrebbe sorprendervi.",
            "Telefonate brevi durante la settimana complementano visite fisiche: «Ti chiamo per sapere come stai, non per controllare» — dichiarare l'intento riduce tensione.",
        ],
        "conclusione": [
            "Le visite familiari sono il filo che tiene unita la storia personale con il nuovo capitolo. Curate quel filo con regolarità, gentilezza e rispetto per l'autonomia di chi avete accompagnato fin qui.",
        ],
    },
    "costi-retta-casa-famiglia-piemonte": {
        "cosa-include": [
            "Oltre alle voci standard, verificate se sono inclusi materiali personali di base, trasporto per visite mediche programmate, attività extra e gestione documentale. Ogni voce «non inclusa» può diventare costo nascosto se non chiarita subito.",
            "In Piemonte, il panorama delle case famiglia per autosufficienti è variegato: ville familiari in valle, strutture più grandi in periferia urbana, residenze con profili misti. Confrontate solo strutture con profilo simile.",
        ],
        "variabili": [
            "La camera singola offre privacy massima; la doppia può ridurre costo e offrire compagnia per chi la desidera. Discutete con vostro caro la preferenza — non assumete che singola sia sempre migliore.",
            "Alcune famiglie valutano vendita o affitto della casa di famiglia per finanziare la retta. Decisione delicata che richiede tempo e consulenza — non fretta post-emergenza.",
        ],
        "contributi": [
            "Detrazioni fiscali per spese assistenziali possono applicarsi in alcuni casi — verificate con commercialista. Non è consiglio universale: dipende da situazione patrimoniale e contratto.",
            "Comuni e regione possono avere bandi o contributi variabili nel tempo. Vale la pena una telefonata all'ufficio servizi sociali del Comune di residenza del vostro caro.",
        ],
        "conclusione": [
            "Il costo della retta è conversazione familiare difficile — affrontatela con documenti in mano, non con ansia sola. Trasparenza protegge il rapporto tra fratelli e tra voi e vostro caro.",
        ],
    },
    "inserimento-nuovo-ospite": {
        "ambientamento": [
            "Il primo pranzo a tavola è spesso il momento più delicato: nuovi volti, nuovi sapori, nuova routine. Alcuni ospiti preferiscono osservare prima di partecipare — rispettare questo ritmo accelera l'integrazione rispetto a forzare socialità immediata.",
            "Staff e famiglia collaborano: voi portate storia e preferenze, noi portiamo routine quotidiana. L'inserimento è progetto condiviso, non procedura burocratica.",
        ],
        "oggetti-personali": [
            "Fotografie su comò, libri preferiti, coperta del matrimonio, orologio da polso sul comodino — dettagli che trasformano stanza in territorio personale. Non sottovalutate il potere di un oggetto familiare in un giorno difficile.",
            "Se vostro caro ha piante, chiedete se possono stare in camera o in giardino. Cure quotidiane di una pianta offrono routine rassicurante e senso di responsabilità.",
        ],
        "segnali-positivi": [
            "Telefonate che passano da «non so se ce la faccio» a «oggi ho giocato a carte» indicano progresso reale. Celebrate piccoli passi — non aspettate trasformazione immediata.",
            "Se dopo tre-quattro settimane notate chiusura persistente o rifiuto alimentare, parlate con noi immediatamente. Adattamenti sono possibili: menu, compagno di tavola, tempi di riposo.",
        ],
        "conclusione": [
            "L'inserimento è ponte tra due vite — quella nella casa di famiglia e quella nella casa famiglia. Voi siete architetti di quel ponte con la vostra presenza, pazienza e oggetti che profumano di casa.",
        ],
    },
    "autonomia-dignita-terza-eta": {
        "autonomia-non-solitudine": [
            "Scelta non è binary: solitudine totale o perdita di autonomia. Casa famiglia occupa spazio intermedio riconosciuto da sempre nelle culture mediterranee — la famiglia allargata, la comunità che accoglie.",
            "Per anziani che hanno guidato famiglie, aziende, comunità, perdere agency è più devastante di perdere mobilità. Proteggere scelta quotidiana è proteggere identità.",
        ],
        "dignita-linguaggio": [
            "Operatori formati nella casa famiglia imparano a chiedere permesso, offrire scelta, evitare infantilizzazione. «Vuole il caffè ora o dopo?» batte «Ecco il caffè» per chi ha sempre scelto da sé.",
            "Nelle conversazioni familiari, evitate frasi come «ormai non capisce» se vostro caro è presente. Anche con rallentamenti cognitivi lievi, dignità linguistica conta.",
        ],
        "assistenza-discreta": [
            "Assistenza notturna discreta significa che qualcuno è sveglio se serve, non che qualcuno controlla ogni movimento. Questa distinzione è fondamentale per anziani autosufficienti che temono sorveglianza.",
            "Tecnologia può supportare — chiamate d'emergenza, sensori di movimento se richiesti — senza trasformare la casa in ospedale. Discutiamo preferenze individuali con famiglia e ospite.",
        ],
        "conclusione": [
            "Autonomia e dignità non sono valori astratti — sono pratica quotidiana: come si chiede, come si offre, come si rispetta il silenzio, come si celebra la scelta.",
        ],
    },
    "coazze-giaveno-pinerolo-servizi": {
        "giaveno-avigliana": [
            "Famiglie di Avigliana apprezzano la continuità con il lago e i percorsi abituali: vostro caro può mantenere abitudini estive consolidate con visite familiari che includono gite locali.",
            "Giaveno e Coazze condividono cultura di valle — dialetto, ricordi industriali, memoria comunitaria. Questa affinità culturale facilita inserimento per ospiti originari della zona.",
        ],
        "pinerolo-valle": [
            "Pinerolo offre servizi urbani più strutturati; Coazze offre tranquillità. La combinazione permette a ospiti autosufficienti di avere entrambi entro raggi ragionevole.",
            "Per specialisti medici non disponibili in valle, Torino e Pinerolo sono accessibili per visite programmate — accompagnamento organizzabile con preavviso.",
        ],
        "torino-dintorni": [
            "Figli torinesi ci raccontano che il tragitto domenicale è diventato momento di decompressione — lontano dal traffico cittadino, verso il verde. La visita inizia già nel viaggio.",
            "Parcheggio e accessibilità della struttura sono verificabili durante la prima visita. Portate vostro caro per testare comfort del percorso da dove vivete.",
        ],
        "conclusione": [
            "Mappa dell'area servita non è elenco comuni — è promessa di vicinanza emotiva e geografica per famiglie che non vogliono perdere il filo con chi amano.",
        ],
    },
    "domande-figli-casa-famiglia": {
        "senso-colpa": [
            "Il senso di colpa spesso nasce da narrativa sociale obsoleta: «i genitori si prendono cura dei figli, non il contrario». Ma la cura è bidirezionale e circolare — a 45 anni curate genitori, a 70 potreste ricevere cura. Non è tradimento: è umanità.",
            "Parlare con altri figli nella stessa situazione — gruppi di supporto, forum locali, persino conversazioni con amici — normalizza l'esperienza. Non siete «cattivi figli»: siete figli in situazione difficile che cerca il bene.",
        ],
        "momento-giusto": [
            "Non esiste calendario universale. Esiste il momento in cui solitudine, insicurezza o vostra esaurizione superano benefici di «aspettare». Quel momento è personale — confrontate segnali, non date di scadenza.",
            "Se il genitore rifiuta ma i segnali sono chiari, coinvolgete medico, persona fidata del genitore, fratelli. Pressione gentile e coerente batte silenzio impotente.",
        ],
        "anziani-soli": [
            "Servizi domiciliari aiutano ma non sostituiscono presenza umana continuativa. Per anziani autosufficienti soli, casa famiglia offre compagnia scelta — non assistente che arriva un'ora al giorno e poi silenzio.",
            "Valutate anche rischi domestici: scale, gas, cadute notturne. Solitudine + casa non adatta moltiplica fragilità anche in autosufficienti.",
        ],
        "conclusione": [
            "Continuate a chiedere. Ogni domanda è legittima. Ogni famiglia ha tempi diversi. La risposta migliore spesso non è su Google — è in una conversazione calma con chi accoglie anziani ogni giorno.",
        ],
    },
}


NEW_SECTIONS = {
    "casa-famiglia-vs-rsa-differenze": [
        section(
            "valutazione-pratica",
            "Come valutare una casa famiglia sul campo",
            "Visitate di persona almeno due strutture di profilo simile. Portate quaderno, lista domande, tempo per osservare senza fretta. Prima impressione conta — ma seconda visita conferma o corregge.",
            "Chiedete di parlare con ospiti se possibile e appropriato. La voce di chi ci vive vale più di brochure. Osservate pasti, non solo camere modello.",
            "Valutate anche accessibilità per visite familiari dal vostro domicilio — frequenza sostenibile determina qualità del legame post-inserimento.",
            "A Coazze, Casa Famiglia Quercia accoglie visite senza impegno — venite con calma, portate domande, lasciate spazio a vostro caro per esprimere preferenze.",
        ),
    ],
    "scegliere-casa-famiglia-genitori": [
        section(
            "dialogo-genitore",
            "Come aprire il dialogo con il genitore",
            "Iniziare la conversazione è spesso più difficile della scelta finale. Evitate il discorso «abbiamo deciso per te» — preferite «abbiamo notato che la sera è pesante da solo, cosa ne pensi se esploriamo opzioni?» La differenza semantica apre o chiude porte.",
            "Portate informazioni concrete: foto della struttura, articoli come questo, testimonianze di altre famiglie se disponibili. Astrazione alimenta paura; concretezza permette immaginazione positiva.",
            "Rispettate il ritmo. Alcuni genitori accettano in una settimana; altri necessitano mesi di conversazioni brevi. La fretta comunica «ti liberiamo» — il tempo comunica «ti rispettiamo».",
            "Se il dialogo si blocca, un medico di famiglia o una persona fidata del genitore può mediare. Non è tradimento — è saggezza.",
        ),
        section(
            "supporto-figli",
            "Supporto emotivo per i figli caregiver",
            "Curare un genitore anziano mentre lavorate e gestite la vostra famiglia è esauriente. Il burnout del caregiver è reale e silenzioso. Chiedere aiuto — struttura, fratelli, servizi — non è debolezza.",
            "Molti figli riportano che la decisione di casa famiglia, una volta presa con lucidità, ha ridotto ansia notturna e conflitti familiari. Investimento emotivo in informazione ripaga in serenità.",
            "Parlate tra fratelli senza competizione di chi «fa di più». Distribuite visite, chiamate, decisioni. Uno solo non deve portare tutto.",
            "Se il senso di colpa persiste, considerate supporto psicologico breve — normalizzare l'esperienza aiuta a scegliere meglio.",
        ),
        section(
            "decisione-lucida",
            "Decisione lucida, non reazione al panico",
            "Scelta migliore emerge da informazione e tempo — non da panico post-caduta. Anche in emergenza, prendete almeno 48 ore per visitare e confrontare.",
            "Checklist, visite, dialogo familiare: strumenti che trasformano ansia in azione consapevale.",
            "Coazze: disponibili per accompagnarvi senza pressione.",
            "Primo passo: una telefonata o una visita.",
        ),
    ],
    "anziani-autosufficienti-coazze": [
        section(
            "territorio-coazze",
            "Coazze nel contesto della Valle di Susa",
            "Coazze si affaccia sulla valle con panorama che molti ospiti conoscono da vita intera. Sentieri, boschi, aria — non sono decorazione turistica ma routine quotidiana per chi ama muoversi all'aperto.",
            "Il comune è parte di una rete di relazioni: parenti in Giaveno, amici in Avigliana, nipoti a Torino. Restare in valle mantiene questa rete accessibile senza trasferimento urbano traumatico.",
            "Servizi essenziali — farmacia, medico, negozi — sono raggiungibili. Per anziani autosufficienti, autonomia territoriale conta quanto autonomia domestica.",
            "La casa famiglia in Coazze non isola — integra vostro caro nel territorio che già conosce, con supporto che la casa vuota non può offrire.",
        ),
        section(
            "convivenza-scelta",
            "Convivenza scelta vs solitudine forzata",
            "In casa famiglia, convivenza è opzione quotidiana: pranzo insieme se desiderato, camera propria quando serve quiete. Non è condominio caotico — è famiglia allargata con confini chiari.",
            "Molti ospiti ci raccontano che la prima settimana è sorpresa per la libertà ritrovata: «Pensavo che mi avrebbero controllato — invece mi chiedono cosa preferisco.»",
            "Per figli, questo modello significa che vostro caro non è in silenzio forzato né in istituzione rigida — è nel terreno fertile tra i due estremi.",
            "Leggete come articoliamo questa libertà nella giornata tipo e nei servizi inclusi nella retta.",
        ),
        section(
            "scelta-consapevole",
            "Una scelta consapevole, non un ripiego",
            "Casa famiglia per anziani autosufficienti non è «ultima spiaggia» — è scelta positiva quando solitudine e insicurezza superano piacere della casa vuota. Normalizzare questa narrativa aiuta vostro caro ad accettare.",
            "Coazze offre contesto dove la scelta non è penalizzazione geografica ma continuità territoriale e sociale.",
            "Visitate, parlate, confrontate. Informazione trasforma paura in decisione lucida.",
            "Siamo disponibili per conversazioni senza pressione commerciale.",
        ),
    ],
    "valle-di-susa-vita-anziani": [
        section(
            "qualita-vita",
            "Indicatori di qualità della vita dopo i 65 anni",
            "Qualità della vita in terza età non è solo assenza di malattia — è compagnia, stimolazione, sicurezza, dignità, accesso a natura e relazioni. Casa famiglia in valle può ottimizzare tutti questi fattori per profilo autosufficiente.",
            "Passeggiate regolari, pasti sociali, attività cognitive leggere, sonno senza ansia da solitudine — pilastri misurabili di benessere quotidiano.",
            "Confrontate con situazione attuale: quante di queste dimensioni sono coperte nella casa vuota? La risposta oggettiva orienta la scelta.",
            "Non romanticizzate la solitudine in casa grande — spesso è abitudine, non preferenza reale.",
        ),
        section(
            "figli-torino",
            "Per figli che vivono in città",
            "Molti figli torinesi scelgono casa famiglia in valle per mantenere genitore «sul territorio» con visite sostenibili nel tempo. Coazze è raggiungibile senza trasferimento interregionale.",
            "Videochiamate, visite weekend, telefonate quotidiane — tecnologia e geografia si combinano per presenza che non esaurisce chi lavora in città.",
            "La colpa del «non averlo sotto casa» si trasforma in «ho scelto il meglio per lui nel contesto giusto» — narrativa più sana per tutti.",
            "Prenotate visita congiunta: vostro caro deve vedere e sentire, non solo ricevere informazioni dai figli.",
        ),
        section(
            "invecchiare-valle",
            "Invecchiare bene in montagna dolce",
            "Valle di Susa non è solo residenza — è identità per molti anziani piemontesi. Invecchiare qui con supporto adeguato combina radici e sicurezza.",
            "Casa famiglia integra territorio: passeggiate, eventi locali, relazioni preesistenti — non sostituisce valle, la abita meglio.",
            "Per figli, scelta in valle spesso è scelta di rispetto per la storia del genitore.",
            "Prenotate visita per esplorare senza impegno.",
        ),
    ],
    "visite-familiari-casa-famiglia": [
        section(
            "ritmi-visita",
            "Costruire ritmi di visita sostenibili",
            "Definite con fratelli un calendario condiviso: chi visita quando, chi chiama, chi gestisce emergenze. Chiarezza evita sovraccarico di uno solo e abbandono percepito da vostro caro.",
            "Visite brevi e frequenti battono maratone mensili che esauriscono tutti. Un caffè del sabato può bastare se è regolare e presente.",
            "Includete vostro caro nella pianificazione: «Preferisci che veniamo il sabato o la domenica?» — agency anche nelle visite.",
            "Rispettate anche i momenti in cui vostro caro preferisce riposo o attività con nuovi compagni — non è esclusione della famiglia.",
        ),
        section(
            "nipoti-lontani",
            "Nipoti, distanza e tecnologia",
            "Per nipoti lontani, videochiamate programmate — «il mercoledì col nonno» — mantengono legame intergenerazionale. Wi-Fi incluso nella retta supporta queste connessioni.",
            "Quando nipoti visitano, portate attività: foto, disegni, storie di scuola. Vostro caro diventa nonno, non solo «ospite in struttura».",
            "Educate i bambini senza pietismo: «Nonno vive in una casa con altre persone, è una scelta per stare bene» — linguaggio chiaro, non segreto familiare.",
            "Le visite dei nipoti arricchiscono anche altri ospiti — gioia condivisa che beneficia l'atmosfera comune.",
        ),
        section(
            "presenza-autentica",
            "Presenza autentica oltre la colpa",
            "La colpa spinge visite performative — portate calma, non solo regali. Vostro caro ha bisogno di voi, non di compensazione materiale.",
            "Equilibrio tra presenza e rispetto autonomia: chiedete cosa preferisce, non impone ritmi.",
            "Casa famiglia a Coazze accoglie famiglie come parte della vita quotidiana — non come ispettori.",
            "Contattateci per domande su visite e ritmi.",
        ),
    ],
    "costi-retta-casa-famiglia-piemonte": [
        section(
            "confronto-piemonte",
            "Panorama delle rette in Piemonte",
            "Il Piemonte offre varietà di strutture: ville familiari in valle, residenze in periferia urbana, profili misti. Confrontare solo cifre senza profilo è fuorviante — casa famiglia per autosufficienti e RSA non sono comparabili.",
            "Coazze e Valle di Susa offrono equilibrio costo-qualità: contesto naturale, comunità, accessibilità senza prezzi da centro metropolitano.",
            "Chiedete sempre preventivo personalizzato — camera singola o doppia, esigenze specifiche, durata soggiorno prevista.",
            "Investimento in retta equa compra serenità familiare — valore difficile da quantificare ma concreto nelle telefonate serali.",
        ),
        section(
            "pianificazione-finanziaria",
            "Pianificazione finanziaria familiare",
            "Affrontate la conversazione economica tra fratelli prima della decisione finale. Chi contribuisce, come, per quanto tempo — chiarezza previene conflitti futuri.",
            "Valutate patrimonio, casa di famiglia, detrazioni, contributi possibili. Commercialista e servizi sociali del Comune sono alleati, non giudici.",
            "Non rimandate pianificazione fino a emergenza — lucidità economica richiede tempo come lucidità emotiva.",
            "Trasparenza con vostro caro, quando possibile, include anche dimensione economica senza farlo sentire «costo» — è investimento in qualità vita.",
        ),
        section(
            "preventivo-chiaro",
            "Richiedere un preventivo chiaro",
            "Chiedete preventivo scritto con voci esplicite. Confrontate inclusioni tra strutture di profilo simile — casa famiglia autosufficienti vs RSA non sono comparabili.",
            "Coazze offre equilibrio costo-qualità in contesto naturale — valutate oltre la cifra.",
            "Trasparenza dalla prima conversazione: nessuna sorpresa dopo firma.",
            "Contattateci per preventivo personalizzato senza impegno.",
        ),
    ],
    "inserimento-nuovo-ospite": [
        section(
            "primo-mese",
            "Il primo mese: aspettative realistiche",
            "Il primo mese è montagna russa emotiva per tutti: ospite, famiglia, staff. Aspettative realistiche proteggono da delusione prematura — integrazione è processo, non evento.",
            "Alcuni giorni saranno luminosi; altri difficili. Fluttuazione è normale, non segnale di fallimento.",
            "Visite frequenti all'inizio sono bene — ma evitate presenza ossessiva che comunica sfiducia nella struttura.",
            "Dopo trenta giorni, molte famiglie riportano stabilizzazione emotiva e routine che «finalmente respira».",
        ),
        section(
            "famiglia-staff",
            "Alleanza famiglia-staff",
            "Staff e famiglia sono alleati con informazioni complementari: voi portate storia, preferenze, memoria; staff porta routine quotidiana e osservazione presente.",
            "Condividete anniversari, ricorrenze, allergie, superstizioni, hobby. Più contesto, migliore accoglienza.",
            "Critiche costruttive sono benvenute; critiche da visita singola senza dialogo creano tensione. Preferite conversazione a monologo frustrato.",
            "Canale di comunicazione chiaro — telefono, WhatsApp, email — riduce ansia da «non sapere cosa succede».",
        ),
        section(
            "accompagnamento",
            "Accompagnamento continuo",
            "Inserimento non finisce al decimo giorno — è dialogo continuo tra famiglia, ospite e staff per settimane. Adattamenti sono normali.",
            "Oggetti personali, visite, comunicazione chiara: tre pilastri dell'ambientamento sereno.",
            "Coazze: villa familiare dove nuovi ospiti sono attesi, non depositati.",
            "Contattateci per accompagnare il percorso dall'inizio.",
        ),
    ],
    "autonomia-dignita-terza-eta": [
        section(
            "pratica-quotidiana",
            "Autonomia nella pratica quotidiana",
            "Autonomia si esercita nei dettagli: scelta del vestito, orario della doccia, partecipazione opzionale alle attività, gestione del proprio spazio in camera.",
            "Operatori formati evitano «fare per velocità» ciò che l'ospite può fare con un po' più di tempo — pazienza è rispetto.",
            "Per anziani che hanno gestito famiglie e lavori, micro-scelte quotidiane mantengono senso di controllo essenziale per benessere psicologico.",
            "Visitando la struttura, osservate se gli ospiti sono trattati da protagonisti o da passeggeri — la differenza è visibile.",
        ),
        section(
            "figli-e-controllo",
            "Quando i figli faticano a «lasciar andare»",
            "Controllo eccessivo post-inserimento — chiamate multiple giornaliere, visite quotidiane, domande ossessive — comunica sfiducia e può rallentare integrazione.",
            "Fidarsi della struttura scelta con cura è parte del percorso. Se non fidate, forse la struttura non era quella giusta — o il vostro lutto anticipato ha bisogno di spazio.",
            "Equilibrio: presenza regolare + fiducia operativa. Chiedete aggiornamenti periodici invece di micro-gestione continua.",
            "Vostro benessere conta — esaustione del caregiver nuovo «manager» di struttura non aiuta nessuno.",
        ),
        section(
            "diritti-quotidiani",
            "Diritti quotidiani, non privilegi",
            "Autonomia e dignità sono diritti — non bonus offerti da strutture benevole. Verificate che la casa famiglia li pratichi, non solo li enuncia.",
            "Osservate interazioni staff-ospiti durante visita: rispetto è visibile.",
            "Casa Famiglia Quercia a Coazze: autosufficienza protetta ogni giorno.",
            "Prenotate visita per vedere con i vostri occhi.",
        ),
    ],
    "coazze-giaveno-pinerolo-servizi": [
        section(
            "mappa-pratica",
            "Mappa pratica dell'area servita",
            "Da Giaveno: circa 15–20 minuti via SP103. Da Avigliana: percorso simile attraverso valle. Da Pinerolo: 25–35 minuti via SS589 e deviazioni locali. Da Torino centro: meno di un'ora in condizioni normali.",
            "Trana e Valgioie: comuni limitrofi con distanze contenute — ideale per famiglie che vogliono vicinanza senza urbanizzazione.",
            "Verificate percorsi con vostro caro durante visita conoscitiva — comfort del tragitto influenza frequenza visite.",
            "Parcheggio presso la struttura e accessibilità pedonale sono verificabili in prima visita.",
        ),
        section(
            "servizi-territorio",
            "Servizi del territorio per anziani",
            "Valle di Susa offre farmacie, ambulatori, attività culturali locali, mercati, trasporto pubblico limitato ma presente. Per autosufficienti, combinazione casa famiglia + territorio funziona efficacemente.",
            "Specialisti non disponibili in valle sono raggiungibili in Pinerolo o Torino con accompagnamento programmato.",
            "Legami sociali preesistenti — parrocchia, associazioni, club — possono continuare con supporto logistico familiare.",
            "Casa famiglia non sostituisce territorio — lo integra con base sicura h24.",
        ),
        section(
            "visita-conoscitiva",
            "Organizzare la visita conoscitiva",
            "Prenotate visita conoscitiva senza impegno: vedete spazi, fate domande, valutate percorso da casa vostra. Portate vostro caro se possibile — la sua reazione vale più di qualsiasi brochure.",
            "Confrontate distanza, inclusioni retta, atmosfera, flessibilità visite. Tre criteri oggettivi che orientano senza ansia.",
            "Siamo in Stradale Poirino 152, Coazze — cuore operativo con valle tutta intorno.",
            "Contattateci per pianificare il primo incontro con calma.",
        ),
    ],
    "domande-figli-casa-famiglia": [
        section(
            "fratelli-decisione",
            "Fratelli e decisione condivisa",
            "Decisioni su genitore anziano dividono famiglie se non gestite con dialogo. Riunione tra fratelli — anche breve, anche via video — allinea aspettative e distribuisce responsabilità.",
            "Uno non deve essere «il figlio che manda via papà». Rotazione visite, chiamate, contributi economici — equità previene rancori duraturi.",
            "Se disaccordo persiste, mediatore esterno — medico, assistente sociale — può facilitare senza drammi familiari.",
            "Obiettivo comune: benessere del genitore, non vittoria di posizione personale.",
        ),
        section(
            "domande-struttura",
            "Altre domande da porre alla struttura",
            "Oltre a costi e visite: come gestite conflitti tra ospiti? C'è spazio per privacy quando serve? Come celebrate ricorrenze personali? Qual è il turnover del personale?",
            "Chiedete referenze di famiglie se possibile — conversazione con chi ha già attraversato il percorso normalizza e informa.",
            "Nessuna domanda è stupida. Struttura serena risponde con pazienza; struttura difensiva è segnale.",
            "Annotate tutto. Confrontate con seconda struttura visitata. Decisione informata batte intuizione spaventata.",
        ),
        section(
            "risposte-oneste",
            "Risposte oneste, senza giri di parole",
            "Non promettiamo perfezione — promettiamo presenza, trasparenza, rispetto. Domande difficili meritano risposte dirette.",
            "Senso di colpa, costi, visite, autonomia: temi che affrontiamo quotidianamente con famiglie come vostra.",
            "Coazze, Valle di Susa: contesto umano per decisioni umane.",
            "Contattateci — ogni domanda è legittima.",
        ),
    ],
}


PAD_PARAS = [
    "Le famiglie che ci scelgono arrivano spesso dopo mesi di ricerca online, telefonate confuse, confronti tra RSA e case famiglia senza chiarezza. È normale. L'informazione trasforma ansia in decisione — e ogni domanda che ponete è legittima.",
    "A Coazze, Casa Famiglia Quercia accoglie anziani autosufficienti in villa familiare con giardino, salone condiviso, pasti genuini e assistenza discreta h24. Non siamo struttura sanitaria: siamo seconda casa per chi merita compagnia e sicurezza senza perdere autonomia.",
    "Stradale Poirino 152 è il nostro indirizzo — cuore di Coazze, Valle di Susa. Da Giaveno, Avigliana, Pinerolo e Torino siamo raggiungibili in tempi che permettono visite regolari. Per molte famiglie, questa accessibilità è decisiva quanto la qualità degli spazi.",
    "Visitate senza impegno. Osservate atmosfera, camere, spazi comuni, giardino. Chiedete di vedere una giornata tipo. Portate vostro caro quando possibile. La decisione migliore emerge dall'esperienza diretta — non dalla paura sola o dalla fretta post-emergenza.",
    "Rette trasparenti, percorso di ingresso chiaro, visite flessibili, oggetti personali in camera: dettagli che definiscono se una struttura è davvero «famiglia» o solo marketing. Confrontate inclusioni, non solo cifre a fondo pagina.",
    "Se questo articolo ha chiarito dubbi, il passo successivo è semplice: contattateci. Telefono, WhatsApp, email — rispondiamo con calma. Non dovete decidere subito. Basta iniziare a parlare, fare domande, prenotare una visita quando vi sentite pronti.",
    "Valle di Susa offre aria, luce, comunità a misura d'uomo — contesto ideale per terza età attiva e autosufficiente. Restare in valle spesso significa continuità di legami, abitudini, identità. Casa famiglia integra territorio senza sostituirlo.",
    "Autonomia, dignità, convivialità scelta, sicurezza h24: pilastri del nostro modello. Per genitori che hanno vissuto in libertà decenni, questi non sono optional — sono condizione per accettare un cambiamento difficile ma necessario.",
    "Molti figli ci raccontano che la telefonata iniziale è stata il momento più difficile — non la visita, non il trasloco. Siamo abituati ad accompagnarvi con calma da quel primo contatto, senza fretta né pressione commerciale.",
    "Confrontate almeno due strutture di profilo simile prima di decidere. Checklist, appunti, domande scritte: strumenti semplici che trasformano confusione in chiarezza. La scelta per un genitore merita questo impegno.",
    "Il blog è risorsa — ma non sostituisce conversazione. Chiamate, venite, portate domande. Siamo in Stradale Poirino 152, Coazze, e rispondiamo a famiglie di tutta la Valle di Susa ogni settimana.",
    "Scoprite anche le pagine dedicate ai servizi, alla struttura, alle rette e alla galleria fotografica: ogni sezione del sito è pensata per accompagnarvi con informazioni chiare, immagini reali e invito costante a contattarci senza impegno.",
]


def _article_word_count(article):
    body_text = article.get("intro", "")
    for sec in article["sections"]:
        body_text += re.sub(r"<[^>]+>", " ", sec["body"])
    return len(re.findall(r"\w+", body_text))


def apply_expansions(articles):
    for article in articles:
        slug = article["slug"]
        expansions = EXPANSIONS.get(slug, {})
        for sec in article["sections"]:
            extra = expansions.get(sec["id"], [])
            if extra:
                sec["body"] += p(*extra)
        new_secs = NEW_SECTIONS.get(slug, [])
        if new_secs:
            article["sections"].extend(new_secs)

        wc = _article_word_count(article)
        if wc < 1500:
            article["sections"].append(
                section(
                    "per-approfondire",
                    "Per approfondire con Casa Famiglia Quercia",
                    *PAD_PARAS,
                )
            )
        wc = _article_word_count(article)
        if wc < 1500:
            article["sections"].append(
                section(
                    "visita-coazze",
                    "Venite a conoscerci a Coazze",
                    "Prenotate una visita gratuita in Stradale Poirino 152. Vi mostriamo camere, salone, giardino e rispondiamo a ogni domanda con calma e trasparenza.",
                    "Da Giaveno, Pinerolo, Avigliana e Torino raggiungete Coazze in tempi brevi. Molte famiglie fanno la prima visita nel weekend — senza impegno, senza pressione.",
                    "Portate vostro caro se possibile. La sua reazione guidando per la valle spesso vale più di qualsiasi presentazione. Rispettiamo i tempi di ogni persona.",
                    "Telefono +39 376 203 1211, WhatsApp, email: scegliete il canale che preferite. Rispondiamo con umanità — non con script commerciali.",
                    "Casa Famiglia Quercia: villa nel verde, pasti di casa, assistenza discreta h24. Una seconda casa per anziani autosufficienti che meritano compagnia, sicurezza e autonomia in Valle di Susa.",
                )
            )
        wc = _article_word_count(article)
        if wc < 1500:
            article["sections"].append(
                section(
                    "ultimo-passo",
                    "Un ultimo passo, senza fretta",
                    "Non serve decidere oggi. Serve iniziare: una chiamata, una visita, una conversazione. Siamo a Coazze quando siete pronti — con calma, chiarezza e rispetto per i tempi della vostra famiglia.",
                )
            )
