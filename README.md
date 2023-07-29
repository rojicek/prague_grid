1 - strava_preprocessing 
asi hodina, klidne vsechno znova ze strava archivu
zpracuje i fit, tcx, atd a vytvori nove gpx, ktere jsou konzistentni a daji se jednotne zpracovat
zpracovane soubory ulozi do podadresare, typicky activities_processed_gpx


2 - process_rides
trva par hodin, ale muze navazovat (diva se na uz zpracovane soubory)
vstupem jsou predchozi gpx
vystupem 2 adresare (typicky v rides)
processed_activities_df : data frames s jednotlivymi body, ktere jsou zhustene na ~10m (nebo jak je parametr)
processed_ctivities_js : javascript pro vlozeni do zobrazeni na mapy.cz
ignoruji virtualni jizdy, takze pocet df nemusi sedet

