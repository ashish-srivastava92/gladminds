from django import template
from src.gladminds.models.common import STATUS_CHOICES

register = template.Library()

@register.filter(name="get_coupon_status")
def get_coupon_status(value):
    """Get coupons on basis of status that will be int returned value string"""
    coupon_status = dict((str(k), v) for k, v in dict(STATUS_CHOICES).items())
    return coupon_status.get(str(value), value)
    