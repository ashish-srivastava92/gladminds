from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from gladminds.core.services.loyalty import feed_models as loyalty_feed

tns = settings.CORE_WSDL_TNS

all_app = Application([loyalty_feed.PartMasterService,
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
part_master_service = csrf_exempt(DjangoApplication(part_master_app))
part_upc_service = csrf_exempt(DjangoApplication(part_upc_app))
part_point_service = csrf_exempt(DjangoApplication(part_point_app))
distributor_service = csrf_exempt(DjangoApplication(distributor_app))
mechanic_service = csrf_exempt(DjangoApplication(mechanic_app))
