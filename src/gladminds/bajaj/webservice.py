from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from gladminds.bajaj.services.coupons import feed_models as fsc_feed

tns = settings.WSDL_TNS

all_app = Application([fsc_feed.BrandService,
                       fsc_feed.DealerService,
                       fsc_feed.ProductDispatchService,
                       fsc_feed.ProductPurchaseService,
                       fsc_feed.ASCService,
                       fsc_feed.OldFscService,
                       fsc_feed.CreditNoteService,
                       fsc_feed.BillOfMaterialService,
                       fsc_feed.ECOReleaseService,
                       fsc_feed.ContainerTrackerService,
                       fsc_feed.ECOImplementationService,
                       ],
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

bom_app = Application([fsc_feed.BillOfMaterialService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

bom_app = Application([fsc_feed.BillOfMaterialService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

eco_release_app = Application([fsc_feed.ECOReleaseService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )
 
container_tracker_app = Application([fsc_feed.ContainerTrackerService],
                           tns=tns,
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11()
                           )

eco_implementation_app = Application([fsc_feed.ECOImplementationService],
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
bom_service = csrf_exempt(DjangoApplication(bom_app))
eco_release_app = csrf_exempt(DjangoApplication(eco_release_app))
container_tracker_app = csrf_exempt(DjangoApplication(container_tracker_app))
eco_implementation_app = csrf_exempt(DjangoApplication(eco_implementation_app))
