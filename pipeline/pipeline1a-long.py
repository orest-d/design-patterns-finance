def fetch_data1():
    return "data1"

def fetch_data2():
    return "data2"

def process_data1():
    return fetch_data1().upper()

def process_data2():
    return fetch_data2().upper()

def process_data3():
    return process_data1() + "-" + process_data2()

def show_report1():
    print(process_data3())

def show_report2():
    print(process_data1(), "<->", process_data2())

show_report1()
show_report2()