from datetime import datetime
# import locale

def formatar_data_pt(data):
    if isinstance(data, str):
        data = datetime.fromisoformat(data)

    # return data.strftime("%d/%m/%Y %H:%M")
    return data.strftime("%d/%m/%Y")



