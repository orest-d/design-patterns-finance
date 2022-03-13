def fetch_data():
    return "data"

def process_data(data):
    return data.upper()

def show_report(data):
    print(data)

def run():
    data = fetch_data()
    data = process_data(data)
    show_report(data)

run()