from datetime import timedelta, datetime
from io import BytesIO
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from app.models import Order

def render_to_pdf(template_name, context_dict={}):
    """
    Renders an HTML template to a PDF file.

    Args:
        template_name (str): The path to the HTML template.
        context_dict (dict, optional): The context dictionary to be passed to the template. Defaults to {}.

    Returns:
        HttpResponse or None: Returns an HttpResponse object with the PDF content if rendering is successful, else returns None.
    """

    template = get_template(template_name)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def get_week_start(today):
    """
    Gets the start of the week for a given date.

    Args:
        today (datetime): The reference date for which the start of the week is to be found.

    Returns:
        datetime: Returns the start of the week for the provided date.
    """
    monday = today - timedelta(days=today.weekday())
    start_of_week = timezone.make_aware(datetime.combine(monday, datetime.min.time()))
    return start_of_week


def get_week_end(monday):
    """
    Gets the end of the week based on the provided start of the week.

    Args:
        monday (datetime): The start of the week.

    Returns:
        datetime: Returns the end of the week based on the provided start of the week.
    """
    friday = monday + timedelta(days=4)
    end_of_week = timezone.make_aware(datetime.combine(friday, datetime.max.time()))
    return end_of_week
    

def get_relatory_orders(week_start, week_end):
    """
    Gets approved or delivered orders within a certain time interval.

    Args:
        week_start (datetime): The start of the time interval.
        week_end (datetime): The end of the time interval.

    Returns:
        QuerySet: Returns the filtered orders within the specified time interval.
    """
    orders = Order.objects.filter(
        timestamp__gte=week_start,
        timestamp__lt=week_end,
        status='approved' or 'delived',
    )
    return orders


def calculate_total_products(orders):
    """
    Calculates the total products ordered in a list of orders.

    Args:
        orders (QuerySet): A list of orders.

    Returns:
        dict: A dictionary containing the product name as key and the total ordered quantity as value.
    """
    total_products = {}
    for order in orders:
        if (order.status == 'approved') or (order.status == 'delived'):   
            for ordered_product in order.call_products.all():
                product_name = ordered_product.call_product.product.name
                product_unit = ordered_product.call_product.product.unit  
                if ordered_product.status == 'available':   
                    ordered_quantity = ordered_product.ordered_quantity
                elif ordered_product.status == 'parcial':   
                    ordered_quantity = ordered_product.available_quantity
                else:
                    continue  

                if product_name in total_products:
                    total_products[product_name]['quantity'] += ordered_quantity
                else:
                    total_products[product_name] = {'quantity': ordered_quantity, 'unit': product_unit}

    return total_products
