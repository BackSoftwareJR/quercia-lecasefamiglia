#!/usr/bin/env python3
"""Generate blog markdown + HTML for Casa Famiglia Quercia."""
import os
import html as html_lib
import textwrap

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE, "content", "blog")
BLOG_DIR = os.path.join(BASE, "blog")

ARTICLES = [
    {
        "slug": "scegliere-casa-famiglia-genitori",
        "title": "Come scegliere una casa famiglia per i genitori",
        "meta_title": "Scegliere casa famiglia genitori | Guida",
        "meta_desc": "Checklist per figli: come scegliere una casa famiglia per genitori autosufficienti a Coazze e in Valle di Susa. Domande, segnali, errori da evitare.",
        "category": "Consigli",
        "badge": "accent",
        "reading": "12 min",
        "keywords": "casa famiglia anziani Coazze, scegliere casa famiglia, genitori anziani",
        "breadcrumb": "Scegliere casa famiglia",
        "sections": [
            ("Intro", """<p>La telefonata che temevate è arrivata: vostro padre ha perso l'equilibrio in cucina, o vostra madre ha ammesso che la sera le pesa troppo il silenzio in casa. Voi, figli tra i 45 e i 65 anni, lavorate, avete famiglia, e vi sentite spezzati tra la gratitudine verso chi vi ha cresciuto e la paura di non reggere il peso di una scelta sbagliata.</p>
<p>Scegliere una <strong>casa famiglia</strong> non è un gesto di abbandono. È spesso il modo più rispettoso per dire: "Meriti di vivere bene, in un posto dove qualcuno è presente e tu resti protagonista della tua giornata." Questa guida vi accompagna passo dopo passo.</p>"""),
            ("Prima di iniziare: cosa chiedervi", """<p>Prima di visitare qualsiasi struttura, fermatevi un momento. Vostro genitore è ancora <strong>autosufficiente</strong>? Cammina, mangia, si veste, gestisce le necessità quotidiane? Se sì, una casa famiglia può essere la soluzione giusta. Se i bisogni sono più complessi, potrebbe servire un percorso diverso — parlatene con il medico di famiglia senza vergogna.</p>
<p>Poi chiedetevi: cosa teme di più vostro caro? La solitudine? La perdita di autonomia? L'idea di "finire in istituto"? Le risposte vi guideranno nella conversazione.</p>"""),
            ("Checklist: domande da fare alla struttura", """<ul>
<li>Quanti ospiti accogliete? Preferite numeri contenuti, dove ogni persona è conosciuta per nome.</li>
<li>Qual è il rapporto tra operatori e ospiti?</li>
<li>Cosa include esattamente la <a href="/rette-e-ammissione/">retta mensile</a>?</li>
<li>Come funzionano le visite? Ci sono orari rigidi?</li>
<li>Esiste un periodo di ambientamento?</li>
<li>Come comunicate con le famiglie in caso di imprevisti?</li>
<li>Che rapporto avete con medici e farmacie del territorio?</li>
</ul>
<p>Annotate le risposte. Confrontatele con calma, non di fretta in macchina.</p>"""),
            ("Cosa osservare durante la visita", """<p>Non guardate solo le camere — guardate l'atmosfera. C'è odore di casa o di disinfettante? Le persone che vivono lì vi sorridono o evitano lo sguardo? Gli operatori parlano con rispetto o perentoriamente?</p>
<p>Chiedete di vedere gli <a href="/la-struttura/">spazi comuni</a>: salone, cucina, giardino. Immaginate vostro padre o vostra madre seduto lì, al mattino, con un caffè. Vi viene naturale? Vi sentite tranquilli?</p>
<p>Fate attenzione ai suoni: un brusio di conversazione è buon segno. Il silenzio assoluto, a volte, nasconde isolamento.</p>"""),
            ("Errori comuni dei figli", """<p><strong>Decidere al posto del genitore.</strong> Coinvolgetelo, anche se fa fatica ad accettare. Una scelta condivisa dura nel tempo.</p>
<p><strong>Confondere casa famiglia e struttura sanitaria.</strong> Se il vostro caro è autosufficiente, non serve un ambiente medicalizzato. Leggete la nostra guida su <a href="/blog/casa-famiglia-vs-rsa-differenze/">casa famiglia vs RSA</a>.</p>
<p><strong>Scegliere solo in base al prezzo.</strong> La retta conta, ma conta di più sentirsi "a casa". Chiedete sempre cosa è incluso.</p>
<p><strong>Rimandare la visita.</strong> Ogni mese di indecisione è un mese di solitudine per chi aspetta una risposta.</p>"""),
            ("Il ruolo della famiglia dopo l'ingresso", """<p>La casa famiglia non sostituisce voi. Resta il vostro compito essere presenti: telefonate, visite, domande su come sta andando. Ma potete farlo con serenità, sapendo che qualcuno veglia anche di notte.</p>
<p>Scoprite come si svolge una <a href="/la-giornata/">giornata tipo</a> e quali <a href="/servizi/">servizi</a> sono inclusi. Più sapete, meno immaginate scenari peggiori.</p>"""),
            ("Conclusione", """<p>Non esiste la scelta perfetta — esiste quella giusta per questo momento. Prendetevi il tempo di visitare, parlare, ascoltare. Vostro genitore ha ancora molto da dire, e voi siete la voce che lo aiuta a farsi sentire.</p>
<p><strong>Hai dubbi? Parliamone.</strong> Siamo a Coazze, in Valle di Susa, e rispondiamo con calma a ogni domanda.</p>"""),
        ],
    },
    {
        "slug": "anziani-autosufficienti-coazze",
        "title": "Anziani autosufficienti a Coazze: perché restare in valle",
        "meta_title": "Anziani autosufficienti Coazze | Casa famiglia",
        "meta_desc": "Perché Coazze è ideale per anziani autosufficienti: natura, comunità, Casa Famiglia Quercia in Valle di Susa. Guida per famiglie di Giaveno e dintorni.",
        "category": "Territorio",
        "badge": "primary",
        "reading": "10 min",
        "keywords": "casa famiglia anziani Coazze, anziani autosufficienti, Valle di Susa",
        "breadcrumb": "Anziani autosufficienti Coazze",
        "sections": [
            ("Intro", """<p>Coazze non è solo un comune sulla carta geografica. Per chi ci è nato o ci ha trascorso le estati, è odore di bosco, campanile, volti che si conoscono al bar. Quando un genitore autosufficiente inizia a pensare che la casa grande è diventata troppo vuota, restare "in valle" può essere la scelta più naturale — e la più bella.</p>"""),
            ("Cosa significa autosufficiente oggi", """<p>Un ospite autosufficiente cammina da solo, mangia, si veste, gestisce l'igiene personale. Non ha bisogno di cure continue, ma può beneficiare di <strong>compagnia, sicurezza e assistenza discreta</strong> — qualcuno che dorme sotto lo stesso tetto, che prepara i pasti, che nota se qualcosa non va.</p>
<p>Non si tratta di "non poter più fare nulla". Si tratta di non voler fare tutto da soli.</p>"""),
            ("Perché Coazze", """<p>Coazze sorge nella <strong>Valle di Susa</strong>, a circa 700 metri di altitudine, circondata da verde e aria buona. Il ritmo è umano: niente caos cittadino, ma neanche isolamento. Da qui si raggiungono facilmente Giaveno, Avigliana, Pinerolo e Torino per visite e commissioni.</p>
<p>Per molti anziani del territorio, restare qui significa mantenere legami con il parrucchiere, il fornaio, la chiesa del paese. Significa che i figli possono passare il sabato pomeriggio senza pianificare un'odissea.</p>"""),
            ("Casa famiglia vs vivere soli", """<p>Vivere soli in una casa di montagna può essere romantico finché va tutto bene. Poi arriva la notte lunga, la paura di scivolare in bagno, la televisione accesa solo per sentire una voce. Una <strong>casa famiglia a Coazze</strong> offre convivialità scelta: pranzo insieme se si vuole, camera propria quando si desidera quiete.</p>
<p>Scoprite i nostri <a href="/servizi/">servizi</a> e come si articola una <a href="/la-giornata/">giornata tipo</a>.</p>"""),
            ("Per i figli che vivono lontano", """<p>Molti figli lavorano a Torino o all'estero. La distanza amplifica l'ansia: "E se cade stanotte?" Sapere che vostro padre o vostra madre è in una casa curata, con persone presenti h24, vi restituisce respiro. Potete chiamare, visitare, videochiamare — senza quella colpa silenziosa che vi mangia.</p>"""),
            ("Quando valutare il cambiamento", """<p>Alcuni segnali: pasti saltati, casa trascurata, chiusura nelle relazioni, paura di uscire, notti insonni. Non serve aspettare una crisi. Meglio parlare quando il vostro caro è ancora lucido e partecipe.</p>
<p>Leggete anche <a href="/rette-e-ammissione/">rette e ammissione</a> per capire il percorso di ingresso.</p>"""),
            ("Conclusione", """<p>Coazze non è una meta lontana: è casa per chi ama la montagna dolce e la comunità vera. Per un anziano autosufficiente, restare qui in una casa famiglia può significare dignità, natura e calore — senza rinunciare alla propria storia.</p>
<p><strong>Hai dubbi? Parliamone.</strong> Venite a conoscerci in Stradale Poirino 152.</p>"""),
        ],
    },
    {
        "slug": "valle-di-susa-vita-anziani",
        "title": "Vita serena in Valle di Susa dopo i 65 anni",
        "meta_title": "Vita anziani Valle di Susa | Guida famiglie",
        "meta_desc": "Com'è la vita dopo i 65 anni in Valle di Susa? Natura, servizi, casa famiglia e consigli per figli che cercano serenità per i genitori a Coazze.",
        "category": "Territorio",
        "badge": "primary",
        "reading": "11 min",
        "keywords": "Valle di Susa anziani, casa famiglia Coazze, terza età",
        "breadcrumb": "Vita anziani Valle di Susa",
        "sections": [
            ("Intro", """<p>La Valle di Susa è una delle porte d'accesso alle Alpi più amate del Piemonte. Per chi ha passato qui decenni di lavoro, famiglia, passeggiate domenicali, invecchiare in valle non è una resa: è continuità. I figli che oggi vivono in città guardano a questi paesi con nostalgia e, a volte, con la domanda: "Mamma starebbe meglio qui o lì?"</p>"""),
            ("Il territorio che abbraccia", """<p>Dalla bassa valle fino ai comuni collinari, la Susa offre un mosaico di paesaggi: boschi, prati, borghi storici come Avigliana, Susa, Bussoleno. I servizi essenziali — farmacie, medici, negozi — sono raggiungibili. La connessione con Torino resta comoda per visite e controlli.</p>
<p>Per un anziano autosufficiente, significa <strong>aria, luce, ritmi lenti</strong> senza tagliarsi fuori dal mondo.</p>"""),
            ("Socialità e comunità", """<p>In valle le relazioni hanno memoria. Conosci chi conosce tua sorella, il parroco saluta per nome, al mercato chiedono del nipote. Questa rete, per chi ha più di 65 anni, è medicina silenziosa contro la solitudine.</p>
<p>In una casa famiglia come la nostra a <a href="/chi-siamo/">Coazze</a>, questa dimensione comunitaria si intreccia con convivialità quotidiana: pasti insieme, chiacchiere in salone, passeggiate in giardino.</p>"""),
            ("Attività e benessere", """<p>La valle invita al movimento dolce: passeggiate, giardinaggio, lettura al sole. Non servono maratone — serve stimolazione. Le nostre <a href="/servizi/">attività</a> rispettano i ritmi di ogni ospite: chi vuole partecipare, chi preferisce la poltrona col giornale.</p>"""),
            ("Quando la casa diventa troppo grande", """<p>Molti genitori restano nella casa di una vita "per non dare fastidio". In realtà, spesso è l'inverso: i figli dormono male pensando a scale, riscaldamento, neve sul vialetto. Una casa famiglia in valle non cancella la storia: la continua in un contesto più leggero.</p>
<p>Visitate la <a href="/la-struttura/">nostra struttura</a> e immaginate vostro caro in uno spazio curato, senza scale infinite da salire da solo.</p>"""),
            ("Per le famiglie che devono scegliere", """<p>Non dovete conoscere ogni comune della valle a memoria. Vi basta chiedervi: mio padre ama il verde? Preferisce silenzio o compagnia? Vuole restare vicino a Giaveno, Pinerolo, Avigliana? Le risposte restringono il campo.</p>"""),
            ("Conclusione", """<p>Invecchiare in Valle di Susa può essere un capitolo pieno, non una parentesi grigia. Con il supporto giusto — una casa famiglia che rispetta l'autonomia — vostro genitore può respirare ancora la montagna che ama.</p>
<p><strong>Hai dubbi? Parliamone.</strong> Siamo a Coazze, cuore della valle.</p>"""),
        ],
    },
    {
        "slug": "visite-familiari-casa-famiglia",
        "title": "Visite familiari in casa famiglia: restare presenti",
        "meta_title": "Visite familiari casa famiglia | Consigli",
        "meta_desc": "Come mantenere legami forti quando un genitore vive in casa famiglia: visite, nipoti, confini sani. Consigli per figli a Coazze e Valle di Susa.",
        "category": "Famiglia",
        "badge": "accent",
        "reading": "9 min",
        "keywords": "visite familiari anziani, casa famiglia Coazze, rapporto famiglia",
        "breadcrumb": "Visite familiari",
        "sections": [
            ("Intro", """<p>Quando un genitore si trasferisce in casa famiglia, molti figli temono una distanza emotiva: "Non sarò più il riferimento." In realtà, la convivenza con altri non cancella il legame — lo ridisegna. Voi restate figli, confidenti, presenza. Solo che non dovete più gestire da soli ogni pasto e ogni notte insonne.</p>"""),
            ("Visite senza orari rigidi", """<p>Nella nostra casa a Coazze le visite sono <strong>sempre benvenute</strong>. Non ci sono fasce orarie da rispettare con ansia. Venite quando potete: un caffè del mattino, un pranzo domenicale, un pomeriggio col nipote che racconta la scuola.</p>
<p>Il buon senso guida: se vostro padre riposa, magari aspettate mezz'ora. Ma non serve un permesso formale.</p>"""),
            ("Cosa portare, cosa lasciare", """<p>Portate ciò che nutre l'anima: fotografie nuove, dolci fatti in casa, notizie del quartiere. Evitate di trasformare ogni visita in un controllo sanitario o in un elenco di lamentele. Chiedete: "Com'è andata la settimana?" prima di "Hai preso le medicine?"</p>"""),
            ("I nipoti e i pronipoti", """<p>I bambini portano luce negli spazi comuni. Non dovete limitare le visite per paura di "disturbare": una casa famiglia vive anche di voci giovani. Concordate con lo staff eventuali momenti più tranquilli se il vostro caro stanca facilmente.</p>"""),
            ("Equilibrio tra presenza e autonomia", """<p>C'è una tentazione opposta: visitare troppo per colpa, o troppo poco per paura di invadere. La via di mezzo è regolarità senza pressione. Una telefonata breve il martedì, una visita il sabato: ritmi sostenibili per voi e rassicuranti per vostro caro.</p>
<p>Scoprite come si articola la <a href="/la-giornata/">giornata</a> per capire i momenti migliori.</p>"""),
            ("Comunicazione con la struttura", """<p>Parlate con chi accoglie vostro padre o vostra madre ogni giorno. Condividete preferenze, anniversari, piccole abitudini. Una casa famiglia funziona quando famiglia e operatori remano dalla stessa parte.</p>
<p>Per qualsiasi dubbio operativo, <a href="/contatti/">contattateci</a> — preferiamo una domanda in più a un malinteso.</p>"""),
            ("Conclusione", """<p>Restare presenti non significa essere sempre fisicamente lì. Significa che vostro caro sa di non essere dimenticato. Le visite, le chiamate, i messaggi WhatsApp con foto del cane: tutto questo tiene acceso il filo familiare.</p>
<p><strong>Hai dubbi? Parliamone.</strong> Vi aiutiamo a trovare il ritmo giusto per tutti.</p>"""),
        ],
    },
    {
        "slug": "costi-retta-casa-famiglia-piemonte",
        "title": "Costi e retta di una casa famiglia in Piemonte",
        "meta_title": "Costi casa famiglia Piemonte | Rette Coazze",
        "meta_desc": "Quanto costa una casa famiglia in Piemonte? Cosa include la retta, come confrontare le offerte e orientarsi a Coazze. Guida trasparente per famiglie.",
        "category": "Pratico",
        "badge": "accent",
        "reading": "13 min",
        "keywords": "costi casa famiglia Piemonte, retta anziani Coazze, casa famiglia prezzi",
        "breadcrumb": "Costi e retta Piemonte",
        "sections": [
            ("Intro", """<p>Parlare di soldi quando si tratta di un genitore fa male. Vorreste il meglio senza peso sulle spalle, e spesso i prezzi online sono confusi, incompleti, difficili da confrontare. Cerchiamo chiarezza: cosa significa "retta" in una casa famiglia piemontese, cosa dovreste aspettarvi, come leggere un preventivo senza cadere in trappole.</p>"""),
            ("Cosa include normalmente la retta", """<p>In strutture come la nostra, la retta mensile comprende in genere:</p>
<ul>
<li>Alloggio in camera singola o doppia</li>
<li>Pensione completa (colazione, pranzo, cena)</li>
<li>Assistenza h24</li>
<li>Pulizia degli spazi personali e comuni</li>
<li>Lavanderia</li>
<li>Attività ricreative</li>
<li>Utenze e Wi-Fi</li>
</ul>
<p>Dettagli completi nella pagina <a href="/rette-e-ammissione/">rette e ammissione</a>.</p>"""),
            ("Variabili che influenzano il prezzo", """<p>La tipologia di camera incide: singola o doppia. Il luogo conta: una casa famiglia a Coazze in valle può avere costi diversi rispetto al centro di Torino. I servizi extra — accompagnamenti speciali, esigenze particolari — vanno chiesti esplicitamente.</p>
<p>Diffidate di cifre troppo basse che non specificano cosa è incluso. Diffidate anche di cifre altissime vendute come "lusso" quando cercate semplicemente calore e cura.</p>"""),
            ("Confrontare senza stress", """<p>Preparate un foglio con tre colonne: struttura, cosa include, costo mensile. Visitate almeno due posti. Chiedete se esistono soggiorni di prova. Parlate con altre famiglie se possibile.</p>
<p>Non siete obbligati a decidere al primo incontro. Una buona struttura vi darà tempo.</p>"""),
            ("Contributi e agevolazioni", """<p>A seconda della situazione, possono esistere contributi regionali, comunali o forme di detrazione. Informatevi presso il Comune di residenza del vostro caro e con un commercialista di fiducia. Noi vi aiutiamo con la documentazione necessaria quando possibile.</p>"""),
            ("Valore oltre il prezzo", """<p>Il vero "costo" da evitare è la solitudine non interrotta, la casa vuota, le notti in cui nessuno risponde al telefono. Una retta equa compra serenità — per vostro caro e per voi.</p>
<p>Scoprite i <a href="/servizi/">servizi inclusi</a> e contattateci per un preventivo personalizzato.</p>"""),
            ("Conclusione", """<p>Trasparenza è il minimo che meritate. Chiedete, confrontate, dormiteci sopra. Scegliere con lucidità economica protegge il rapporto familiare da rancori futuri.</p>
<p><strong>Hai dubbi? Parliamone.</strong> Vi spieghiamo ogni voce con pazienza.</p>"""),
        ],
    },
    {
        "slug": "inserimento-nuovo-ospite",
        "title": "L'inserimento sereno di un nuovo ospite",
        "meta_title": "Inserimento nuovo ospite | Casa famiglia",
        "meta_desc": "Come avviene l'inserimento in casa famiglia: ambientamento, oggetti personali, ruolo della famiglia. Guida per figli che accompagnano un genitore a Coazze.",
        "category": "Percorso",
        "badge": "primary",
        "reading": "10 min",
        "keywords": "inserimento casa famiglia, nuovo ospite anziani, Coazze",
        "breadcrumb": "Inserimento nuovo ospite",
        "sections": [
            ("Intro", """<p>Il giorno del trasloco arriva sempre troppo presto o troppo tardi. Vostro padre impacchetta la foto del matrimonio. Vostra madre chiede se può portare la coperta di lana. Voi stringete le mani e pensate: "Starà bene?" L'inserimento in casa famiglia, se gestito con cura, può essere dolce — non traumatico.</p>"""),
            ("Prima dell'ingresso", """<p>Tutto inizia con una telefonata e una visita. Poi la valutazione condivisa: siamo compatibili? Cosa serve a vostro caro? Documenti, certificato medico base, contratto chiaro. Nella pagina <a href="/rette-e-ammissione/">rette e ammissione</a> trovate il percorso passo per passo.</p>"""),
            ("Il periodo di ambientamento", """<p>I primi giorni sono ascolto. Ogni ospite ha tempi diversi: qualcuno si integra subito a tavola, qualcuno preferisce mangiare in camera un paio di volte. Non forziamo. Presentiamo gli spazi, le persone, i ritmi. Voi potete visitare più spesso all'inizio — la vostra presenza è un ponte sicuro.</p>"""),
            ("Oggetti personali", """<p>Portate ciò che profuma di casa: quadri, libri, la poltrona se entra in camera, radio vecchia, piante. Lo spazio deve diventare "suo", non un hotel. Nella <a href="/la-struttura/">nostra struttura</a> ogni camera accoglie storie diverse.</p>"""),
            ("Comunicazione famiglia-struttura", """<p>Condividete abitudini alimentari, preferenze, paure notturne, nomi degli affetti. Nessun dettaglio è ridicolo. Più sappiamo, meglio accogliamo.</p>
<p>Restiamo in contatto con voi nelle prime settimane: un messaggio, una chiamata, un "come l'avete visto oggi?"</p>"""),
            ("Segnali di un buon inserimento", """<p>Sorrisi spontanei, appetito regolare, curiosità verso gli altri, telefonate che raccontano piccole cose ("oggi ho visto un uccellino dal salone"). Non serve euforia — serve stabilità crescente.</p>"""),
            ("Conclusione", """<p>Accogliere un nuovo ospite è per noi un impegno morale, non solo organizzativo. Vostro caro merita di sentirsi atteso, non depositato. Voi meritate di vedere che la scelta si è fatta con il cuore — e con la testa.</p>
<p><strong>Hai dubbi? Parliamone.</strong> Vi accompagniamo dall'inizio.</p>"""),
        ],
    },
    {
        "slug": "autonomia-dignita-terza-eta",
        "title": "Autonomia e dignità in terza età: perché contano",
        "meta_title": "Autonomia e dignità terza età | Guida",
        "meta_desc": "Perché autonomia e dignità sono centrali per anziani autosufficienti. Come una casa famiglia a Coazze le rispetta ogni giorno. Per figli e caregiver.",
        "category": "Valori",
        "badge": "primary",
        "reading": "11 min",
        "keywords": "autonomia anziani, dignità terza età, casa famiglia Coazze",
        "breadcrumb": "Autonomia e dignità",
        "sections": [
            ("Intro", """<p>Quando parliamo di genitori anziani, è facile cadere nel linguaggio che toglie agency: "non può più", "bisogna decidergli noi", "ormai è fragile." Ma vostro padre che ha costruito una casa, vostra madre che ha cresciuto tre figli — non sono improvvisamente bambini. Sono persone con una biografia. <strong>Autonomia</strong> e <strong>dignità</strong> non sono lussi: sono diritti.</p>"""),
            ("Autonomia non significa solitudine", """<p>Confondiamo spesso "autonomo" con "deve restare solo a casa." Un anziano autosufficiente può aver bisogno di compagnia, sicurezza, pasti preparati — e restare padrone delle proprie scelte quotidiane: quando alzarsi, cosa leggere, se uscire in giardino.</p>
<p>Una casa famiglia protegge questa libertà meglio di una solitudine forzata.</p>"""),
            ("Dignità nel linguaggio", """<p>Evitate di parlare di vostro caro come assente quando è presente. Evitate decisioni totali senza ascoltarlo. In famiglia, piccoli gesti costruiscono dignità: chiedere "cosa ne pensi?" invece di annunciare.</p>
<p>Nella nostra casa a Coazze trattiamo ogni ospite per nome, non per numero di camera. Leggete <a href="/chi-siamo/">chi siamo</a> per capire la nostra filosofia.</p>"""),
            ("Assistenza discreta", """<p>Essere presenti h24 non significa controllare ogni respiro. Significa essere lì se serve aiutare ad alzarsi, se c'è un imprevisto, se serve una mano con la confezione difficile da aprire. Per il resto, spazio e silenzio rispettati.</p>
<p>I nostri <a href="/servizi/">servizi</a> sono pensati così: sostegno, non sostituzione.</p>"""),
            ("Per i figli: lasciar andare un po' di controllo", """<p>È duro. Sempre lo è stato, anche quando eravate adolescenti. Lasciar respirare vostro caro in un ambiente protetto vi sembra un tradimento — ma può essere il regalo più grande. Fidarsi non è abbandono.</p>"""),
            ("Conclusione", """<p>Invecchiare con dignità significa continuare a sentirsi persona, non carico. Una casa famiglia che rispetta l'autonomia non vi chiede di smettere di amare — vi chiede di amare in modo più saggio.</p>
<p><strong>Hai dubbi? Parliamone.</strong> Siamo qui per ascoltarvi.</p>"""),
        ],
    },
    {
        "slug": "coazze-giaveno-pinerolo-servizi",
        "title": "Coazze, Giaveno, Pinerolo: la nostra area servita",
        "meta_title": "Area servita Coazze Giaveno Pinerolo | Casa Famiglia Quercia",
        "meta_desc": "Casa Famiglia Quercia serve Coazze, Giaveno, Avigliana, Pinerolo, Trana, Valgioie e Valle di Susa. Mappa, distanze e info per famiglie del territorio.",
        "category": "Territorio",
        "badge": "primary",
        "reading": "9 min",
        "keywords": "casa famiglia Coazze, Giaveno anziani, Pinerolo Valle Susa",
        "breadcrumb": "Area servita",
        "sections": [
            ("Intro", """<p>Siamo in Stradale Poirino 152, Coazze — ma le famiglie che ci scelgono arrivano da tutta la Valle di Susa e dai comuni limitrofi. Giaveno, Avigliana, Pinerolo, Trana, Valgioie: nomi che suonano vicini a chi vive il Piemonte occidentale. Questo articolo vi aiuta a capire se siamo comodi per voi.</p>"""),
            ("Coazze: cuore della casa", """<p>Coazze è un comune collinare, verde, tranquillo. Qui vive la nostra casa famiglia: villa familiare, giardino, ritmi umani. Se vostro caro ha radici in valle, restare qui è continuità — non esilio.</p>"""),
            ("Giaveno e Avigliana", """<p>Da Giaveno e Avigliana si raggiunge Coazze in pochi minuti di auto. Molte famiglie fanno visite settimanali senza stress: pranzo insieme il sabato, rientro a casa la sera. La vicinanza mantiene vivi i legami.</p>"""),
            ("Pinerolo e valle oltre", """<p>Da Pinerolo la strada attraversa paesaggi che molti anziani conoscono bene — mercati, parenti, ricordi. Anche da più lontano, restare "in zona" è spesso preferibile a un trasferimento in città caotica.</p>"""),
            ("Trana, Valgioie e dintorni", """<p>I comuni più piccoli hanno spesso meno servizi per anziani che vivono soli. Una casa famiglia centralizzata ma immersa nel territorio offre soluzione senza allontanare troppo.</p>"""),
            ("Come organizzare visite e contatti", """<p>Parlate con noi per pianificare il primo incontro. Siamo raggiungibili da Torino in meno di un'ora. Per info su <a href="/servizi/">servizi</a> e <a href="/contatti/">contatti</a>, siamo a disposizione telefonicamente o via WhatsApp.</p>"""),
            ("Conclusione", """<p>Non dovete abitare Coazze per sentirvi a casa qui. Basta amare la montagna dolce, la comunità vera, la possibilità di passare quando volete.</p>
<p><strong>Hai dubbi? Parliamone.</strong> Vi indichiamo il percorso migliore da dove siete.</p>"""),
        ],
    },
    {
        "slug": "domande-figli-casa-famiglia",
        "title": "Le domande che ogni figlio si pone sulla casa famiglia",
        "meta_title": "FAQ figli casa famiglia | Domande comuni",
        "meta_desc": "Risposte alle domande più frequenti dei figli: costi, visite, autonomia, differenza con RSA. Casa Famiglia Quercia a Pinerolo, Pinerolese.",
        "category": "FAQ",
        "badge": "accent",
        "reading": "14 min",
        "keywords": "domande figli casa famiglia, FAQ anziani Coazze, casa famiglia dubbi",
        "breadcrumb": "FAQ per i figli",
        "sections": [
            ("Intro", """<p>Di notte, quando il telefono resta muto, le domande arrivano a ondate: "Ho aspettato troppo?" "Sono un cattivo figlio?" "E se non si ambienta?" Non siete soli. Queste sono le domande che sentiamo più spesso — con risposte oneste, senza giri di parole.</p>"""),
            ("Sto tradendo mio padre se lo porto in casa famiglia?", """<p>No. Tradimento sarebbe lasciarlo solo e spaventato. Accoglierlo in un luogo curato, con persone presenti e autonomia rispettata, è cura. Molti ospiti ci dicono mesi dopo: "Avrei dovuto farlo prima."</p>"""),
            ("Come capisco se è il momento giusto?", """<p>Segnali comuni: solitudine cronica, casa trascurata, pasti saltati, paura di uscire, notti inquiete, vostra ansia costante. Non serve una crisi grave. Meglio anticipare che rincorrere un'emergenza.</p>"""),
            ("Qual è la differenza con una RSA?", """<p>La casa famiglia accoglie <strong>autosufficienti</strong> in ambiente familiare. Le RSA sono strutture sanitarie per bisogni più complessi. Leggete l'articolo completo: <a href="/blog/casa-famiglia-vs-rsa-differenze/">casa famiglia vs RSA</a>.</p>"""),
            ("Quanto costa?", """<p>La retta varia in base a camera e servizi. Noi includiamo pensione completa, assistenza h24, pulizia, lavanderia, attività. Dettagli in <a href="/rette-e-ammissione/">rette e ammissione</a> e nell'articolo sui <a href="/blog/costi-retta-casa-famiglia-piemonte/">costi in Piemonte</a>.</p>"""),
            ("Posso visitarlo quando voglio?", """<p>Sì. Le visite sono benvenute senza orari rigidi. Leggete <a href="/blog/visite-familiari-casa-famiglia/">visite familiari in casa famiglia</a>.</p>"""),
            ("Cosa succede se le condizioni di salute cambiano?", """<p>Parliamo con voi e valutiamo insieme. Se servono cure non compatibili, vi orientiamo con trasparenza. La comunicazione anticipata è parte del rispetto.</p>"""),
            ("Come funziona l'inserimento?", """<p>Periodo di ambientamento, oggetti personali in camera, visite frequenti all'inizio. Tutto il percorso in <a href="/blog/inserimento-nuovo-ospite/">inserimento sereno</a>.</p>"""),
            ("Conclusione", """<p>Non esiste figlio perfetto — esiste figlio che cerca il bene con informazioni e amore. Continuate a fare domande. È così che si protegge chi vi ha protetto.</p>
<p><strong>Hai dubbi? Parliamone.</strong> <a href="/contatti/">Contattateci</a> — rispondiamo con calma.</p>"""),
        ],
    },
]


def sections_to_html(sections):
    return "\n".join(f"        <h2>{html_lib.escape(title)}</h2>\n        {body}" for title, body in sections)


def sections_to_md(sections, title):
    lines = [f"# {title}", ""]
    for stitle, body in sections:
        lines.append(f"## {stitle}")
        lines.append("")
        # strip html tags roughly for md
        import re
        text = re.sub(r"<[^>]+>", "", body)
        text = text.replace("&nbsp;", " ")
        for para in re.split(r"\n\s*\n", text.strip()):
            p = para.strip()
            if p:
                lines.append(p)
                lines.append("")
    return "\n".join(lines)


def build_html(a):
    slug = a["slug"]
    badge_class = "badge--primary" if a["badge"] == "primary" else "badge--accent"
    body = sections_to_html(a["sections"])
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_lib.escape(a["meta_title"])}</title>
  <meta name="description" content="{html_lib.escape(a["meta_desc"])}">
  <meta name="robots" content="index, follow">
  <meta name="keywords" content="{html_lib.escape(a["keywords"])}">
  <link rel="canonical" href="https://casafamigliaquercia.it/blog/{slug}/">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html_lib.escape(a["title"])}">
  <meta property="og:description" content="{html_lib.escape(a["meta_desc"][:120])}">
  <meta property="og:url" content="https://casafamigliaquercia.it/blog/{slug}/">
  <meta property="article:published_time" content="2026-06-22">
  <meta name="theme-color" content="#3a6b4a">
  <link rel="icon" href="../../images/favicon.ico" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=DM+Sans:opsz,wght@9..40,400;9..40,600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../design-system.css">
  <link rel="stylesheet" href="../../components.css">
  <link rel="stylesheet" href="../../pages.css">
  <link rel="stylesheet" href="../../blog.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": {json_str(a["title"])},
    "description": {json_str(a["meta_desc"])},
    "datePublished": "2026-06-22",
    "dateModified": "2026-06-22",
    "author": {{"@type": "Organization", "name": "Casa Famiglia Quercia"}},
    "publisher": {{"@type": "Organization", "name": "Casa Famiglia Quercia", "url": "https://casafamigliaquercia.it/"}},
    "mainEntityOfPage": "https://casafamigliaquercia.it/blog/{slug}/",
    "inLanguage": "it-IT",
    "keywords": {json_str(a["keywords"])}
  }}
  </script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://casafamigliaquercia.it/"}},{{"@type":"ListItem","position":2,"name":"Blog","item":"https://casafamigliaquercia.it/blog/"}},{{"@type":"ListItem","position":3,"name":{json_str(a["breadcrumb"])},"item":"https://casafamigliaquercia.it/blog/{slug}/"}}]}}</script>
</head>
<body class="blog-page blog-article-page">
  <a href="#main" class="skip-link">Vai al contenuto principale</a>
  <div data-include="header"></div>
  <main id="main">
    <nav class="breadcrumbs container" aria-label="Breadcrumb">
      <ol class="breadcrumbs__list">
        <li class="breadcrumbs__item"><a href="/">Home</a></li>
        <li class="breadcrumbs__item"><a href="/blog/">Blog</a></li>
        <li class="breadcrumbs__item"><span aria-current="page">{html_lib.escape(a["breadcrumb"])}</span></li>
      </ol>
    </nav>
    <article class="container blog-article">
      <header>
        <span class="badge {badge_class}">{html_lib.escape(a["category"])}</span>
        <h1>{html_lib.escape(a["title"])}</h1>
        <p class="blog-article__meta">22 giugno 2026 · {html_lib.escape(a["reading"])} di lettura · Casa Famiglia Quercia</p>
      </header>
      <div class="content-prose">
{body}
      </div>
      <aside class="blog-article-cta">
        <h2>Ti aiutiamo noi</h2>
        <p>Hai dubbi? Parliamone senza impegno — siamo a Coazze, in Valle di Susa.</p>
        <div class="btn-group" style="justify-content: center;">
          <a href="/contatti/" class="btn btn--accent">Contattaci</a>
          <a href="/servizi/" class="btn btn--secondary">I nostri servizi</a>
        </div>
      </aside>
    </article>
  </main>
  <div data-include="footer"></div>
  <script src="../../tokens.js"></script>
  <script src="../../js/includes.js"></script>
  <script src="../../js/nav.js"></script>
  <script src="../../js/main.js"></script>
</body>
</html>
"""


def json_str(s):
    import json
    return json.dumps(s, ensure_ascii=False)


def main():
    for a in ARTICLES:
        slug = a["slug"]
        md_path = os.path.join(CONTENT_DIR, f"{slug}.md")
        html_dir = os.path.join(BLOG_DIR, slug)
        html_path = os.path.join(html_dir, "index.html")
        os.makedirs(html_dir, exist_ok=True)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(sections_to_md(a["sections"], a["title"]))
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(build_html(a))
        print(f"Created {slug}")


if __name__ == "__main__":
    main()
