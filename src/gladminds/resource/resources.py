from tastypie.resources import Resource


class GladmindsResources(Resource):
    
    class META:
        resource_name = 'messages'
        
    def __init__(self):
        Resource.__init__();
    
    def base_urls(self):
        return [
            url(r"^messages$", self.wrap_view('dispatch_handler'), kwargs={'handler': self.get_patients})
            ]   
    
    def dispatch_handler(self):
        pass
    
    def register_customer(self):
        pass
    
    def register_product(self):
        pass
    
    def customer_service_detail(self):
        pass

    
    
    