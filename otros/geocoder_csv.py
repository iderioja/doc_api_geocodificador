import csv
import requests


def geocoding(name, locality, localadmin, region, macroregion, country):
    url = "https://geocoder-5-ign.larioja.org/v1/search"
    params = dict(
        text=",".join([name, locality, localadmin,
                      region, macroregion, country]),
        size=1
    )

    resp = requests.get(url=url, params=params)
    data = resp.json()
    if data['features']:
        result = data['features'][0]['geometry']['coordinates']
        print("encontrado: ", params)
    else:
        print("fallo: ", params)
        result = [0, 0]
    return result


with open('direcciones-input.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Nombres de columnas del fichero CSV: {", ".join(row)}')
            with open('direcciones-output.csv', mode='w') as csv_file:
                csv_writer = csv.writer(
                    csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(
                    ['_count', 'name', 'locality', 'localadmin', 'region', 'macroregion', 'country', 'lat', 'lon'])
            line_count += 1
        else:
            print(
                f'\t Procesando dirección... {row[1]}.')
            result = geocoding(row[1], row[2], row[3], row[4], row[5], row[6])
            with open('direcciones-output.csv', mode='a') as csv_file:
                csv_writer = csv.writer(
                    csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(
                    [row[0], row[1], row[2], row[3], row[4], row[5], row[6], result[0], result[1]])

            line_count += 1
    print(f'Processed {line_count} lines.')
