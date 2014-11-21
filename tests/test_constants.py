GM_USER = {
           "customer_name": "test_user",
            "isActive": True,
            "phone_number": "1234567890",
            "user": {
                     "phone_number": "999999999",
                    "user": {
                            "email": "",
                            "first_name": "",
                            "last_name": "",
                            "username": "ppa",
                            "password" :"123"
                            }
                    }
           }

GM_PRODUCTS = {
                "customer_product_number": None,
                "engine": None,
                "insurance_loc": None,
                "insurance_yrs": None,
                "invoice_loc": None,
                "isActive": True,
                "order": 0,
                "product_type": {
                                "brand": {
                                          "brand_id": "Bajaaaaj",
                                          "brand_image_loc": " ",
                                          "brand_name": "Bajaj",
                                          "isActive": True
                                          },
                               "isActive": True,
                               "order": 0,
                               "product_image_loc": None,
                               "product_name": "3700DHPP",
                               "product_type": "3700DHPP",
                               "warranty_email": None,
                               "warranty_phone": None
                               },
               "purchased_from": None,
               "sap_customer_id": None,
               "seller_email": None,
               "seller_phone": None,
               "veh_reg_no": None,
               "vin": 22,
               "warranty_loc": None,
               "warranty_yrs": None
               }

GM_COUPONS = {
           "order": 0,
           "service_type": 2,
           "status": 1,
           "unique_service_coupon": "1",
           "valid_days": 260,
           "valid_kms": 8000,
            "vin": {
                    "created_on": "2014-04-25T15:56:34",
                    "invoice_date": "2013-04-06T00:00:00",
                    "isActive": True,
                    "last_modified": "2014-04-25T15:56:34",
                    "order": 0,
                    "product_type": {
                                     "brand": {
                                               "brand_id": "Bajaj",
                                               "brand_image_loc": " ",
                                               "brand_name": "Bajaj",
                                               "isActive": True
                                               },
                                     "isActive": True,
                                     "order": 0,
                                     "product_image_loc": "",
                                     "product_name": "3700DHFS",
                                     "product_type": "3700DHFS",
                                     "product_type_id": 101959
                                    },
                    "vin": "22"
                    }
            }

USER_PREFERENCE = {
                   "user_profile" : 1,
                   "key" : "name",
                   "value" : "test_user"
                }
APP_PREFERENCE = {
                   "brand" : 1,
                   "key" : "name",
                   "value" : "test_brand"
                }

AFTERBUY_PRODUCTS = {
                     "brand": {
                               "created_date": "2014-11-20T14:49:11",
                               "description": "",
                               "id": 1,
                               "image_url": "a",
                               "industry": {
                                            "created_date": "2014-11-20T14:49:10",
                                            "description": "a",
                                            "id": 1,                                    
                                            "modified_date": "2014-11-20T14:49:10",
                                            "name": "Aruba",                            
                                            "resource_uri": "/afterbuy/v1/industries/1/"
                                            },
                               "is_active": True,
                               "modified_date": "2014-11-20T14:49:11",
                               "name": "Aruba",
                               "resource_uri": "/afterbuy/v1/brands/1/"
                               },
                     "brand_product_id": "11",
                     "color": "red",
                     "consumer": {
                                  "accepted_terms": False,
                                  "address": "",
                                  "consumer_id": "2c099e10-043d-4b59-9243-8ece03b137d0",
                                  "country": "",
                                  "created_date": "2014-11-20T14:48:51",
                                  "date_of_birth": None,
                                  "gender": None,
                                  "image_url": "guest.png",
                                  "modified_date": "2014-11-20T14:48:51",
                                  "phone_number": "9900776655",
                                  "pincode": "",
                                  "resource_uri": "/afterbuy/v1/consumers/2/",
                                  "state": "h",
                                  "tshirt_size": None,
                                  "user": {
                                           "date_joined": "2014-11-20T14:48:24",
                                           "email":"",
                                           "first_name": "",
                                           "id": 2,                                   
                                           "last_login": "2014-11-20T14:48:23",
                                           "last_name": "",
                                           "resource_uri": "",
                                           "username": "test"
                                           }
                                  },
                     "description": "",

                     "image_url": "sss",
                     "is_deleted": False,
                     "nick_name": "aaa",
                     "product_type": {
                                      "created_date": "2014-11-20T14:49:20",
                                      "id": 1,
                                      "image_url": "a",
                                      "is_active": True,
                                      "modified_date": "2014-11-20T14:49:20",
                                      "product_type": "aaa",
                                      "resource_uri": "/afterbuy/v1/product-types/1/"
                                      },
                     "purchase_date": "2014-11-20T14:49:24"
                     }
