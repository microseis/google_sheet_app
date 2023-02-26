from django.shortcuts import render
from django.conf import settings
from django.db.models import Sum

import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

from .models import Order
from datetime import datetime, date
from bs4 import BeautifulSoup
import urllib.request
import pygal

today = date.today()

cur_date = today.strftime("%d/%m/%Y")


def home(request):
    data = sheet_read()

    currency_xml = urllib.request.urlopen(
        "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(cur_date)
    )
    cur = cur_rate_identify(currency_xml)
    try:
        records = Order.objects.all()
        records.delete()

    except Exception:
        pass

    for item in data:
        update_db(item, cur)

    ord_costs = Order.objects.values_list("ord_cost", flat=True)
    ord_dates = Order.objects.values_list("ord_date", flat=True)
    sum = ord_costs.aggregate(sum=Sum("ord_cost"))["sum"]

    # построение графика
    line_chart = pygal.Line(
        y_title="Стоимость, $",
        x_title="Дата поставки",
        x_label_rotation=-90,
        height=400,
    )
    line_chart.title = "Стоимость заказа на дату поставки"
    line_chart.x_labels = map(str, ord_dates)
    line_chart.add("Заказы", ord_costs)

    line_chart.render()

    chart = line_chart.render_data_uri()
    context = {"chart": chart, "currency_rate": cur, "sum": sum}
    return render(request, "app/index.html", context=context)


def sheet_read() -> list:
    """Метод чтения google spreadsheet таблицы"""
    CREDENTIALS_FILE = settings.CREDSFILE
    spreadsheet_id = settings.SPRSHEET

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build("sheets", "v4", http=httpAuth)

    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range="Лист1!A2:D", majorDimension="ROWS")
        .execute()
    )
    data = result.get("values", [])

    return data


def cur_rate_identify(currency_xml) -> str:
    """Чтение xml и нахождение текущего курса USD/RUB"""
    bs_data = BeautifulSoup(currency_xml, "xml")
    rate = bs_data.find("Valute", {"ID": "R01235"}).find("Value")
    val = rate.text
    return val


def update_db(item, rate) -> None:
    """Обновление БД согласно данным из spreadsheet"""
    p, _ = Order.objects.update_or_create(
        ord_num=item[1],
        defaults={
            "ord_id": item[0],
            "ord_cost": item[2],
            "ord_date": datetime.strptime(item[3], "%d.%m.%Y"),
            "ord_cost_rub": round(float(item[2]) * float(rate.replace(",", ".")), 2),
        },
    )
    p.save()
