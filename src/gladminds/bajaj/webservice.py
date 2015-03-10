from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from gladminds.bajaj.services.coupons import feed_models as fsc_feed
from gladminds.bajaj.services.loyalty import feed_models as loyalty_feed
from gladminds.bajajcv.services.loyalty import feed_models as loyalty_feed

tns = settings.WSDL_TNS

all_app = Application([fsc_feed.BrandService,
                       fsc_feed.DealerService,
                       fsc_feed.ProductDispatchService,
                       fsc_feed.ProductPurchaseService,
                       fsc_feed.ASCService,
                       fsc_feed.OldFscService,
                       fsc_feed.CreditNoteService,
                       loyalty_feed.PartMasterService,
                       loyalty_feed.PartUPCService,
                       loyalty_feed.PartPointService,
                       loyalty_feed.DistributorService,
                       loyalty_feed.MechanicService,
                       loyalty_feed.NSMService,
                       loyalty_feed.ASMService],
                      tns=tns,
                      in_protocol=Soap11(validator='lxml'),
                      out_protocol=Soap11()
                      )

brand_app = Application([fsc_feed.BrandService],
                        tns=tns,
                        in_protocol=Soap11(validator='lxml'),
                        out_protocol=Soap11()
                        )

dealer_app = Application([fsc_feed.DealerService],
                         tns=tns,
                         in_protocol=Soap11(validator='lxml'),
                         out_protocol=Soap11()
                         )

asc_app = Application([fsc_feed.ASCService],
                         tns=tns,
                         in_protocol=Soap11(validator='lxml'),
                         out_protocol=Soap11()
                         )

dispatch_app = Application([fsc_feed.ProductDispatchService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

purchase_app = Application([fsc_feed.ProductPurchaseService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

old_fsc_app = Application([fsc_feed.OldFscService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

credit_note_app = Application([fsc_feed.CreditNoteService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

part_master_app = Application([loyalty_feed.PartMasterService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

part_upc_app = Application([loyalty_feed.PartUPCService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

part_point_app = Application([loyalty_feed.PartPointService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

distributor_app = Application([loyalty_feed.DistributorService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

mechanic_app = Application([loyalty_feed.MechanicService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

all_service = csrf_exempt(DjangoApplication(all_app))
brand_service = csrf_exempt(DjangoApplication(brand_app))
dealer_service = csrf_exempt(DjangoApplication(dealer_app))
asc_service = csrf_exempt(DjangoApplication(asc_app))
dispatch_service = csrf_exempt(DjangoApplication(dispatch_app))
purchase_service = csrf_exempt(DjangoApplication(purchase_app))
old_fsc_service = csrf_exempt(DjangoApplication(old_fsc_app))
credit_note_service = csrf_exempt(DjangoApplication(credit_note_app))
part_master_service = csrf_exempt(DjangoApplication(part_master_app))
part_upc_service = csrf_exempt(DjangoApplication(part_upc_app))
part_point_service = csrf_exempt(DjangoApplication(part_point_app))
distributor_service = csrf_exempt(DjangoApplication(distributor_app))
mechanic_service = csrf_exempt(DjangoApplication(mechanic_app))
