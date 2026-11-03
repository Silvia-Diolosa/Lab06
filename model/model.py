from database.DAO import DAO

class Model:
    def __init__(self):
        pass

    def mostraAnni(self):
        return DAO.mostraAnni()

    def mostraBrand(self):
        return DAO.mostraBrand()

    def mostraRetailer(self):
        return DAO.mostraRetailer()

    def topVendite(self, anno, brand, retailer):
        vendite = DAO.topVendite(anno, brand, retailer)

        vendite.sort(reverse=True)
        return vendite[:5]

    def analizzaVendite(self, anno, brand, retailer):
        vendite = DAO.topVendite(anno, brand, retailer)

        ricavo_totale = sum([sale.ricavo for sale in vendite])
        retailers_involved = set([sale.Retailer_code for sale in vendite])
        product_involved = set([sale.Product_number for sale in vendite])
        return ricavo_totale, len(vendite), len(retailers_involved), len(product_involved)



