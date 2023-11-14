import calendar
from django.db.models import Sum

from .models import Sales, Expences


def get_filtered_sales(request, current_month):
    role = request.headers.get('role')
    if role == 'admin':
        sales = Sales.objects.filter(Date__month=current_month).order_by('Date')

        if(request.GET.get('staff')):
            if(request.GET.get('staff') != 'All'):
                sales = sales.filter(Staff__id = request.GET.get('staff'))
    else:
        staff = request.headers.get('staff')
        sales = Sales.objects.filter(Staff__id=staff, Date__month=current_month).order_by('Date')

    return filterSales(sales)


def get_current_month_full(current_month):
    return calendar.month_name[int(current_month)]


def filterSales(data):
    if(len(data) == 0):
        return ''
    output = []
    values = {'totalNumberProducts': 0, 'totalSale_rs': 0, 'profit': 0}
    for index, sales in enumerate(data):
        if index == 0:
            values['date'] = sales.Date.isoformat()
            values[sales.Product.id] = sales.NumberOfSales
            values['totalNumberProducts'] = values[sales.Product.id]
            values['totalSale_rs'] = sales.Total + values['totalSale_rs']
            values['profit'] = sales.Profit + values['profit']
        else:
            if sales.Date.isoformat() != values['date']:
                try:
                    expence = Expences.objects.filter(Date=values['date']).aggregate(Sum('Amount'))
                    values['expence'] = expence['Amount__sum']
                    values['profit'] = values['profit']
                    values['total_profit'] = values['profit'] - expence['Amount__sum']
                except:
                    values['profit'] = values['profit']
                    values['total_profit'] = values['profit']
                output.append(values)
                values = {'totalNumberProducts': 0, 'totalSale_rs': 0, 'profit': 0}
                values['date'] = sales.Date.isoformat()
                if sales.Product.id in values:
                    values[sales.Product.id] = values[sales.Product.name] + sales.NumberOfSales
                    values['totalNumberProducts'] = sales.NumberOfSales + values['totalNumberProducts']
                else:
                    values[sales.Product.id] = sales.NumberOfSales
                    values['totalNumberProducts'] = sales.NumberOfSales + values['totalNumberProducts']
                values['totalSale_rs'] = sales.Total + values['totalSale_rs']
                values['profit'] = sales.Profit + values['profit']

            else:
                if sales.Product.id in values:
                    values[sales.Product.id] = values[sales.Product.id] + sales.NumberOfSales
                    values['totalNumberProducts'] = sales.NumberOfSales + values['totalNumberProducts']
                else:
                    values[sales.Product.id] = sales.NumberOfSales
                    values['totalNumberProducts'] = sales.NumberOfSales + values['totalNumberProducts']
                values['profit'] = sales.Profit + values['profit']
                values['totalSale_rs'] = sales.Total + values['totalSale_rs']


    try:
        expence = Expences.objects.filter(Date=values['date']).aggregate(Sum('Amount'))
        values['expence'] = expence['Amount__sum']
        values['total_profit'] = values['profit'] - expence['Amount__sum']
    except:
        values['total_profit'] = values['profit']
    output.append(values)

    return output


def getSummary(data, month):
    summary = {'total_psc': 0, 'total_expence': 0, 'total_profit': 0, 'total_income': 0}
    expences = Expences.objects.filter(Date__month = month)
    total = expences.aggregate(Sum('Amount'))
    if (total['Amount__sum']) is None:
        summary['total_expence'] = 0
    else:
        summary['total_expence'] = total['Amount__sum']

    for i in data:
        summary['total_income'] = summary['total_income'] + i['totalSale_rs']
        summary['total_profit'] = summary['total_profit'] + i['profit']
        summary['total_psc'] = summary['total_psc'] + i['totalNumberProducts']

    summary['total_profit'] = summary['total_profit'] - summary['total_expence']

    return summary