from database.DB_connect import DBConnect
from model.go_retailers import Retailer
from model.go_daily_sales import Vendita

class DAO:

    @staticmethod
    def mostraAnni():
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()

        query = """SELECT DISTINCT YEAR(Date) AS anno 
                    FROM go_daily_sales 
                    ORDER BY anno"""
        cursor.execute(query)

        tutto = cursor.fetchall()

        res= []
        for row in tutto:
            res.append(row[0]) #senno restituisce tupla


        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def mostraBrand():
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()

        query = """SELECT DISTINCT p.Product_brand as brand
                            FROM go_products as p
                            ORDER BY brand"""
        cursor.execute(query)

        tutto = cursor.fetchall()

        res = []
        for row in tutto:
            res.append(row[0]) #senno restituisce tupla

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def mostraRetailer():
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor(dictionary=True)

        query = """SELECT * 
                    FROM go_retailers 
                    ORDER BY Retailer_name"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Retailer(
                Retailer_code= row["Retailer_code"],
                Retailer_name= row["Retailer_name"],
                Type= row["Type"],
                Country= row["Country"]))


        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def topVendite(anno, brand, retailer_code):

        cnx = DBConnect.get_connection()
        if cnx is not None:
            cursor = cnx.cursor(dictionary=True)
            # spiegazione query:
            # seleziona tutta la vendita (gds.*), e il ricavo
            # da tutte le tabelle
            # fai il join tra le tabelle
            # e poi filtri in base a data, brand e retailer selezionati
            # SPIEGAZIONE COALESCE:
            # es: AND (YEAR(gds.Date)=COALESCE(%s,YEAR(gds.Date)))
            #A seconda di cosa passi tramite il parametro %s dal tuo codice Python, si verificano due scenari:

            # Se l'utente ha selezionato un anno specifico (es. 2016):
            # La funzione diventa COALESCE(2016, YEAR(gds.Date)).
            # Poiché il primo valore (2016) non è nullo, COALESCE restituisce 2016.
            # La condizione nel WHERE diventa: YEAR(gds.Date) = 2016. Di conseguenza, il database filtra i risultati solo per quell'anno.

            # Se l'utente non ha selezionato alcun anno (passi None o NULL da Python):
            # La funzione diventa COALESCE(NULL, YEAR(gds.Date)).
            # Poiché il primo valore è nullo (NULL), COALESCE passa al secondo argomento e restituisce YEAR(gds.Date).
            # La condizione nel WHERE diventa: YEAR(gds.Date) = YEAR(gds.Date). Questa è un'equazione sempre vera (una tautologia) per ogni riga della tabella. Di fatto, il filtro viene ignorato e vengono inclusi tutti gli anni.

            query = """SELECT gds.*, gds.Unit_sale_price*gds.Quantity AS Ricavo
                       FROM go_daily_sales gds, go_retailers gr, go_products gp 
                       WHERE gds.Retailer_code  = gr.Retailer_code  
                       AND gds.Product_number = gp.Product_number 
                       AND (YEAR(gds.Date)=COALESCE(%s,YEAR(gds.Date)))
                       AND (gp.Product_brand =COALESCE(%s,gp.Product_brand))
                       AND (gr.Retailer_code =COALESCE(%s,gr.Retailer_code))"""
            cursor.execute(query, (anno, brand, retailer_code,))
            result = []
            for row in cursor:
                result.append(Vendita(
                    Retailer_code=row["Retailer_code"],
                    Product_number=row["Product_number"],
                    Order_method_code=row["Order_method_code"],
                    Date=row["Date"],
                    Quantity=row["Quantity"],
                    Unit_price=row["Unit_price"],
                    Unit_sale_price=row["Unit_sale_price"]))

            cursor.close()
            cnx.close()
            return result
        else:
            print("Errore nella connessione")
            return None




# per analizza vendite, posso creare una query appositva e contare direttamente qui anzichè nel model:
#        SELECT SUM(gds.Unit_sale_price * gds.Quantity) AS giro_affari,
#        COUNT(*) AS num_vendite,
#        COUNT(DISTINCT gds.Retailer_code) AS num_retailers,
#        COUNT(DISTINCT gds.Product_number) AS num_prodotti
#
#       FROM go_daily_sales gds, go_products gp
#
#       WHERE gds.Product_number = gp.Product_number
#       AND YEAR(gds.Date) = COALESCE(%s, YEAR(gds.Date))
#       AND gp.Product_brand = COALESCE(%s, gp.Product_brand)
#       AND gds.Retailer_code = COALESCE(%s, gds.Retailer_code)