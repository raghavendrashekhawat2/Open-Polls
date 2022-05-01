from datetime import date


def convert_date(d):
    # yyyy/mm/dd

    res = d[8] + d[9]
    months_string = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                     'November', 'December']
    ordinal_string = ['st', 'nd', 'th']

    if int(d[9] + d[9]) == 1:
        res += 'st '
    elif int(d[9] + d[9]) == 2:
        res += 'nd '
    else:
        res += "th "

    res += months_string[int(d[5] + d[6])]
    res += (d[0] + d[1] + d[2] + d[3])
    return res


def compare_date(val):
    d = int(val[8] + val[9])
    m = int(val[5] + val[6])
    y = int(val[0] + val[1] + val[2] + val[3])

    curr_date = date.today()
    val1 = str(curr_date.strftime("%Y/%m/%d"))

    cd = int(val1[8] + val1[9])
    cm = int(val1[5] + val1[6])
    cy = int(val1[0] + val1[1] + val1[2] + val1[3])

    # 24-12-2021 26-12-2022
    if cy > y:
        return 1
    elif cy < y:
        return 0

    if cm > m:
        return 1
    elif cm < m:
        return 0

    if cd > d:
        return 1
    elif cd < d:
        return 0
    return 0


if __name__ == '__main__':
    r = compare_date("2022/06/15")
    print(r)