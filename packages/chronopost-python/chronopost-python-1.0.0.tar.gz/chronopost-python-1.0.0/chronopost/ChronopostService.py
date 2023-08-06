from chronopost.Order import Order

class ChronopostService:
    def get_header(self):
        return 'account;dest_code;dest_name;dest_address;dest_pcode;dest_pcodelocal;dest_country;dest_telef;dest_mobile_telef;Dest_email;dest_contact;ship_weight;ship_label_of;ship_cod;ship_clientref;ship_descr;'

    def get_row(self, order: Order):
        if not order.dest_code:
           order.dest_code = ''
        if not order.dest_telef:
            order.dest_telef = ''
        if not order.dest_contact:
            order.dest_contact = ''
        if not order.ship_clientref:
            order.ship_clientref = ''
        if not order.ship_descr:
            order.ship_descr = ''

        return f"{order.account};{order.dest_code};{order.dest_name};{order.dest_address};{order.dest_pcode};{order.dest_pcodelocal};{order.dest_country};{order.dest_telef};{order.dest_mobile_telef};{order.Dest_email};{order.dest_contact};{order.ship_weight};{order.ship_label_of};{order.ship_cod};{order.ship_clientref};{order.ship_descr}\n"

    def get_chronopost_file(self, orders):
        output_text = ""

        for order in orders:

            output_text += self.get_row(order)

        return output_text