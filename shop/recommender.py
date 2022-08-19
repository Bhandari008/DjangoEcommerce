from itertools import product
import redis
from django.conf import settings
from .models import Product

# connect to redis

r = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

class Recommender(object):
    def get_product_key(self,id):
        return f'product:{id}:purchased_with'
    
    def products_bought(self,products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchases together
                    r.zincrby(self.get_product_key(product_id),1,with_id)
    
    def suggest_products_for(self,products,max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # if only 1 product
            suggestions = r.zrange(self.get_product_key(product_ids[0]),0,-1,desc=True)[:max_results]
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # Multiple products the combining scores of all products
            # and storing the resulting sored set in a temporaray key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key,keys)
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key,*product_ids)
            # get the product uds by thier score, descendenat sort
            suggestions = r.zrange(tmp_key,0,-1,desc=True)[:max_results]
            # destroying the temp key
            r.delete(tmp_key)
        suggested_prodcuts_ids = [int(id) for id in suggestions]

        suggested_prodcuts = list(Product.objects.filter(id__in=suggested_prodcuts_ids))
        suggested_prodcuts.sort(key=lambda x: suggested_prodcuts_ids.index(x.id))
        return suggested_prodcuts

    def clear_purchases(self):
        for id in Product.objects.values_list('id',flat=True):
            r.delete(self.get_product_key(id))