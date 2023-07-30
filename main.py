import json
import pandas as pd
from statistics import mean


def find_highway_cost_rate(data):
    # Задание №1
    table_data = {
        "Warehouse": [],
        "Highway_rate": []
    }
    for warehouse in data:
        name = warehouse["warehouse_name"]
        if name in table_data["Warehouse"]:
            continue

        table_data["Warehouse"].append(name)
        hig_cost = warehouse["highway_cost"] * (-1)
        quantity_sum = 0

        for prod in warehouse["products"]:
            quantity_sum += prod["quantity"]
        table_data["Highway_rate"].append(int(hig_cost / quantity_sum))

    df = pd.DataFrame(table_data)
    table_str = df.to_string(index=False, header=True)

    with open("task_1.csv", 'w', encoding='utf-8') as file:
        file.write(table_str)

    print("First task is done!\n")
    return table_data


def each_product(data, from_1):
    # Задание №2
    table_data = {
        "product": [],
        "quantity": [],
        "income": [],
        "expenses": [],
        "profit": []
    }
    for warehouse in data:
        for prod in warehouse["products"]:
            prod_name = prod["product"]
            if prod_name not in table_data["product"]:
                table_data["product"].append(prod_name)
    prod_count = len(table_data["product"])
    table_data["quantity"] = [0] * prod_count
    table_data["income"] = [0] * prod_count
    table_data["expenses"] = [0] * prod_count
    table_data["profit"] = [0] * prod_count

    for warehouse in data:
        wh_name = warehouse["warehouse_name"]
        for prod in warehouse["products"]:
            prod_name = prod["product"]
            prod_index = table_data["product"].index(prod_name)

            table_data["quantity"][prod_index] += prod["quantity"]
            table_data["income"][prod_index] += prod["quantity"] * prod["price"]

            rate = from_1["Highway_rate"][from_1["Warehouse"].index(wh_name)]
            table_data["expenses"][prod_index] += prod["quantity"] * rate

        for prod in warehouse["products"]:
            prod_name = prod["product"]
            prod_index = table_data["product"].index(prod_name)
            table_data["profit"][prod_index] = table_data["income"][prod_index] - table_data["expenses"][prod_index]

    df = pd.DataFrame(table_data)
    table_str = df.to_string(index=False, header=True)

    with open("task_2.csv", 'w', encoding='utf-8') as file:
        file.write(table_str)

    print("Second task is done!\n")


def each_order(data, from_1):
    # Задание №3
    table_data = {
        "order_id": [],
        "order_profit": [],
    }
    for order in data:
        table_data["order_id"].append(order["order_id"])
        wh_name = order["warehouse_name"]
        rate = from_1["Highway_rate"][from_1["Warehouse"].index(wh_name)]
        profit = 0
        for prod in order["products"]:
            profit += prod["quantity"] * prod["price"] - prod["quantity"] * int(rate)
        table_data["order_profit"].append(profit)

    df = pd.DataFrame(table_data)
    table_str = df.to_string(index=False, header=True)

    with open("task_3.csv", 'w', encoding='utf-8') as file:
        file.write(table_str)

    print("Third task is done!")
    print("Средняя прибыль заказов -", mean(table_data["order_profit"]), "\n")


def percent_for_each_wh(data, from_1):
    # Задание №4
    table_data = {
        "warehouse_name": [],
        "product": [],
        "quantity": [],
        "profit": [],
        "percent_profit_product_of_warehouse": []
    }

    wh_list = []
    for order in data:
        if order["warehouse_name"] not in wh_list:
            wh_list.append(order["warehouse_name"])

    prof_list = [0, 0, 0, 0, 0]
    for order in data:
        wh_name = order["warehouse_name"]
        rate = from_1["Highway_rate"][from_1["Warehouse"].index(wh_name)]
        wh_index = wh_list.index(wh_name)
        for prod in order["products"]:
            prof_list[wh_index] += prod["quantity"] * prod["price"] - prod["quantity"] * rate

    comb_list = []
    for order in data:
        for prod in order["products"]:
            pare = [order["warehouse_name"], prod["product"]]
            if pare not in comb_list:
                comb_list.append(pare)

    res_list = []
    for pare in comb_list:
        res_list.append({pare[0]: [pare[1], 0, 0]})

    for elem in res_list:
        wh_name = list(elem.keys())[0]
        rate = from_1["Highway_rate"][from_1["Warehouse"].index(wh_name)]
        val = list(elem.values())[0]
        for order in data:
            if order["warehouse_name"] == wh_name:
                for prod in order["products"]:
                    if prod["product"] == val[0]:
                        val[1] += prod["quantity"]
                        val[2] += prod["quantity"] * prod["price"] - prod["quantity"] * rate
        res_list[res_list.index(elem)] = {wh_name: val}

    for elem in res_list:
        wh_name = list(elem.keys())[0]
        table_data["warehouse_name"].append(wh_name)
        table_data["product"].append(elem[wh_name][0])
        table_data["quantity"].append(elem[wh_name][1])
        table_data["profit"].append(prof_list[wh_list.index(wh_name)])
        table_data["percent_profit_product_of_warehouse"].append(
            abs(elem[wh_name][2] * 100 / prof_list[wh_list.index(wh_name)]))

    df = pd.DataFrame(table_data)
    table_str = df.to_string(index=False, header=True)

    with open("task_4.csv", 'w', encoding='utf-8') as file:
        file.write(table_str)

    print("Fourth task is done!\n")
    return table_data


def sorted_fourth_table(from_4):
    # Задание №5
    table_data = from_4
    data_tuples = list(zip(table_data["warehouse_name"],
                           table_data["product"],
                           table_data["quantity"],
                           table_data["profit"],
                           table_data["percent_profit_product_of_warehouse"]))

    sorted_data_tuples = sorted(data_tuples, key=lambda x: x[4], reverse=False)

    sorted_table_data = {
        "warehouse_name": [item[0] for item in sorted_data_tuples],
        "product": [item[1] for item in sorted_data_tuples],
        "quantity": [item[2] for item in sorted_data_tuples],
        "profit": [item[3] for item in sorted_data_tuples],
        "percent_profit_product_of_warehouse": [item[4] for item in sorted_data_tuples],
        "accumulated_percent_profit_product_of_warehouse": []
    }
    sum = 0
    percents = sorted_table_data["percent_profit_product_of_warehouse"]
    for i in range(len(percents)):
        sum += percents[i]
        sorted_table_data["accumulated_percent_profit_product_of_warehouse"].append(sum)

    df = pd.DataFrame(sorted_table_data)
    table_str = df.to_string(index=False, header=True)
    with open("task_5.csv", 'w', encoding='utf-8') as file:
        file.write(table_str)

    print("Fifth task is done!\n")
    return sorted_table_data


def create_category(from_5):
    # Задание №6
    table_data = from_5
    table_data["category"] = []
    for perc in table_data["accumulated_percent_profit_product_of_warehouse"]:
        if perc <= 70:
            table_data["category"].append('A')
        elif 70 <= perc <= 90:
            table_data["category"].append('B')
        elif perc > 90:
            table_data["category"].append('C')

    df = pd.DataFrame(table_data)
    table_str = df.to_string(index=False, header=True)
    with open("task_6.csv", 'w', encoding='utf-8') as file:
        file.write(table_str)

    print("Sixth task is done!")


with open('trail_task.json', 'r', encoding='utf-8') as f:
    file_data = json.load(f)
rate_data = find_highway_cost_rate(file_data)
each_product(file_data, rate_data)
each_order(file_data, rate_data)
fourth_tabel_data = percent_for_each_wh(file_data, rate_data)
fifth_table_data = sorted_fourth_table(fourth_tabel_data)
create_category(fifth_table_data)
