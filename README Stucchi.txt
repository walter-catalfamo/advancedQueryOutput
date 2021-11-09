Per runnare il codice bisogna fare run sul file query_by_output mettendo dei dataset nel metodo
main come file csv sia per la sorgente che per il target. Ci sono varie righe commentate per i vari 
casi che mi ero creato. Inoltre servono i file csv che indicano le tuple che si stanno cercando nei due dataset.
fin rappresenta le query ottenute dalla sorgente mentre pro le liste di query ottenute dal target.

Una volta ottenute le query della sorgente e del target inizio a confrontarle usando una funzione
che gestisce i diversi casi possibili a seconda di come sono i predicati nelle where-clauses.
Confronto solo i valori degli attributi, non il nome dell'attributo.

Una volta trovate le query del target più simili a quelle della sorgente incremento la matrice.
Prima incrementando i valori degli attributi che si corrispondono nella clausola select e poi 
incrementando i valori degli attributi presenti nelle where-clauses.

La matrice è inizializzata esternamente con tutti i valori a zero dal file "Matrice" che crea 
una matrice guardando ai due dataset (sorgente e target) che si vogliono considerare.

Il codice rischia di andare in loop se non trova possibili split. Ho fatto in modo che il codice deve
sempre tornare delle query e quindi se non ne trova va il loop e non da nessun errore, bisogna stare
attenti sul tipo di dataset e esempio si passano all'algoritmo.

