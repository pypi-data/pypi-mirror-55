class Order:
    def __init__(self, dest_name,
                 dest_address, dest_pcode, dest_pcodelocal,
                 dest_mobile_telef, Dest_email, ship_label_of,
                 ship_cod='0,00', ship_weight='0,00',
                 dest_code=None, dest_telef=None, dest_contact=None, account='09990001',
                 ship_clientref=None,ship_descr=None, dest_country='PT'):
        self.account = account
        self.dest_name = dest_name
        self.dest_address = dest_address
        self.dest_pcode = dest_pcode
        self.dest_pcodelocal = dest_pcodelocal
        self.dest_country = dest_country
        self.dest_mobile_telef = dest_mobile_telef
        self.Dest_email = Dest_email
        self.ship_weight = ship_weight
        self.ship_label_of = ship_label_of
        self.ship_cod = ship_cod
        self.dest_code = dest_code
        self.dest_telef = dest_telef
        self.dest_contact = dest_contact
        self.ship_clientref = ship_clientref
        self.ship_descr = ship_descr