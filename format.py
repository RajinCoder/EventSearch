def format_date(date):
    if not date:
        return "TBA"
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    year, month, day = date.split("-")
    return f"{months[int(month) - 1]} {day}, {year}"

def format_time(time):
    if not time:
        return "TBA"
    hour, minute, seconds = time.split(":")
    AM_PM = "AM" if int(hour) < 12 else "PM"
    hour = "12" if int(hour) % 12 == 0 else str(int(hour) % 12)
    return f"{hour}:{minute} {AM_PM}"

def format_link(uri, label=None):
    if uri is None:
        return label
    if label is None: 
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)

def format_price_range(min_price, max_price, currency):
    if not min_price and not max_price:
        return "TBA"
    if not min_price:
        return f"{max_price:.2f} {currency}"
    if not max_price:
        return f"{min_price:.2f} {currency}"
    return f"{min_price:.2f} - {max_price:.2f} {currency}"

    

def get(d, keys, default_none = None):
    for key in keys:
        try:
            d = d[key]
        except:
            return default_none
    return d