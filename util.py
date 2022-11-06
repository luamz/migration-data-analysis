import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


def generate_age_pyramid(df):
    male_infants = df[df.gender == "M"].months.dropna().astype(int).value_counts(bins=[0, 3, 6, 9, 12]).sort_index(
        ascending=False)
    female_infants = df[df.gender == "F"].months.dropna().astype(int).value_counts(bins=[0, 3, 6, 9, 12]).sort_index(
        ascending=False)
    male_general = df[df.gender == "M"].years.dropna().astype(int) \
        .value_counts(bins=[0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 80]).sort_index(ascending=False)
    female_general = df[df.gender == "F"].years.dropna().astype(int) \
        .value_counts(bins=[0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 80]).sort_index(ascending=False)

    pyramid = pd.DataFrame()
    pyramid["male"] = pd.concat([male_general, male_infants])
    pyramid["male"] = pyramid["male"] * -1
    pyramid["female"] = pd.concat([female_general, female_infants])
    pyramid["age"] = ['60+', '55-59', '50-54', '45-49', '40-44', '35-39', '30-34', '25-29',
                      '20-24', '15-19', '10-14', '5-9', '1-4', '10-12m', '7-9m', '4-6m', '0m-3m']
    pyramid = pyramid.reset_index(drop=True)
    return pyramid


def generate_distritos_map(df, how=True):
    distritos_data = df.naturality_state_id.dropna().reset_index(drop=True).value_counts().to_frame("count")
    distritos_data.reset_index(inplace=True)
    distritos_data = distritos_data.rename(columns={'index': 'DI'})
    distritos_data["DI"] = distritos_data["DI"].astype(str)
    distritos_geodata = gpd.read_file("data/distritos.geojson")
    if how:
        return distritos_geodata.merge(distritos_data, how='left', on='DI')
    else:
        return distritos_geodata.merge(distritos_data, on='DI')


def generate_concelhos_map(df, how=True):
    concelhos_data = df.naturality_city_id.dropna().reset_index(drop=True).value_counts().to_frame("count")
    concelhos_data.reset_index(inplace=True)
    concelhos_data = concelhos_data.rename(columns={'index': 'DICO'})
    concelhos_data["DICO"] = concelhos_data["DICO"].astype(str)
    concelhos_geodata = gpd.read_file("data/concelhos.geojson")
    if how:
        return concelhos_geodata.merge(concelhos_data, how='left', on='DICO')
    else:
        return concelhos_geodata.merge(concelhos_data, on='DICO')


def generate_freguesias_map(df, how=True):
    freguesias_data = df.naturality_place_id.dropna().reset_index(drop=True).value_counts().to_frame("count")
    freguesias_data.reset_index(inplace=True)
    freguesias_data = freguesias_data.rename(columns={'index': 'Dicofre'})
    freguesias_data["Dicofre"] = freguesias_data["Dicofre"].astype(str)
    freguesias_geodata = gpd.read_file("data/freguesias.geojson")
    if how:
        return freguesias_geodata.merge(freguesias_data, how='left', on='Dicofre')
    else:
        return freguesias_geodata.merge(freguesias_data, on='Dicofre')


def generate_texts_distritos(distritos_map):
    distritos_map['center'] = distritos_map['geometry'].centroid
    distritos_map["long"] = distritos_map.center.map(lambda p: p.x)
    distritos_map["lat"] = distritos_map.center.map(lambda p: p.y)
    distritos_map['Distrito'] = distritos_map['Distrito'].str.replace(' ', '\n', 1)

    for i in range(len(distritos_map)):
        tam = len(distritos_map.Distrito[i])

        if distritos_map['count'][i] > 0:
            if tam < 9:
                plt.text(distritos_map.long[i] - (tam * 3000), distritos_map.lat[i] - 5000,
                         f"{distritos_map.Distrito[i]}\n{' ' * 4}{int(distritos_map['count'][i])}",
                         size=6.8)
            else:
                plt.text(distritos_map.long[i] - (tam * 1000), distritos_map.lat[i] - 5000,
                         f"{distritos_map.Distrito[i]}\n{' ' * 4}{int(distritos_map['count'][i])}",
                         size=6.8)


def generate_texts_distrito_concelho(distritos_concelhos_map, concelhos_map):
    distritos_concelhos_map['center'] = distritos_concelhos_map['geometry'].centroid
    distritos_concelhos_map["long"] = distritos_concelhos_map.center.map(lambda p: p.x)
    distritos_concelhos_map["lat"] = distritos_concelhos_map.center.map(lambda p: p.y)
    distritos_concelhos_map['Distrito'] = distritos_concelhos_map['Distrito'].str.replace(' ', '\n', 1)

    for i in range(len(distritos_concelhos_map)):
        if distritos_concelhos_map['count'][i] > 0:
            plt.text(distritos_concelhos_map.long[i] + 3000, distritos_concelhos_map.lat[i] + 7500,
                     f"{distritos_concelhos_map.Distrito[i]}",
                     size=7.5)

    concelhos_map['center'] = concelhos_map['geometry'].centroid
    concelhos_map["long"] = concelhos_map.center.map(lambda p: p.x)
    concelhos_map["lat"] = concelhos_map.center.map(lambda p: p.y)
    concelhos_map['Concelho'] = concelhos_map['Concelho'].str.replace(' ', '\n', 1)

    for j in range(len(concelhos_map)):
        if concelhos_map['count'][j] > 0:
            plt.text(concelhos_map.long[j] - 4000, concelhos_map.lat[j],
                     f"{concelhos_map.Concelho[j]}",
                     size=4.8)


def generate_texts_alijo(alijo_freguesias_map):
    alijo_freguesias_map['center'] = alijo_freguesias_map['geometry'].centroid
    alijo_freguesias_map["long"] = alijo_freguesias_map.center.map(lambda p: p.x)
    alijo_freguesias_map["lat"] = alijo_freguesias_map.center.map(lambda p: p.y)

    alijo_freguesias_map['Freguesia'] = alijo_freguesias_map['Freguesia'].str.replace('União das freguesias de ', '')
    alijo_freguesias_map['Freguesia'] = alijo_freguesias_map['Freguesia'].str.replace(' ', '\n', 1)

    for i in range(len(alijo_freguesias_map)):
        tam = len(alijo_freguesias_map.Freguesia[i])
        if tam <= 5:
            plt.text(alijo_freguesias_map.long[i] - (tam * 75),
                     alijo_freguesias_map.lat[i] - 500,
                     f"{alijo_freguesias_map.Freguesia[i]}\n{' ' * 2}{alijo_freguesias_map['count'][i]}",
                     size=10)
        elif 5 < tam <= 10:
            plt.text(alijo_freguesias_map.long[i] - (tam * 150),
                     alijo_freguesias_map.lat[i] - 500,
                     f"{alijo_freguesias_map.Freguesia[i]}\n{' ' * (tam - 3)}{alijo_freguesias_map['count'][i]}",
                     size=10)
        elif tam > 10:
            plt.text(alijo_freguesias_map.long[i] - (tam * 75),
                     alijo_freguesias_map.lat[i] - 500,
                     f"{alijo_freguesias_map.Freguesia[i]}\n{' ' * (tam // 2)}{alijo_freguesias_map['count'][i]}",
                     size=10)


def generate_passport_map(df):
    passport_data = df.passport_emission_id.dropna(). \
        reset_index(drop=True).value_counts().to_frame("count")
    passport_data.reset_index(inplace=True)
    passport_data = passport_data.rename(columns={'index': 'DI'})
    passport_data["DI"] = passport_data["DI"].astype(str)
    passport_geodata = gpd.read_file("data/distritos.geojson")
    passport_map = passport_geodata.merge(passport_data, on='DI')
    return passport_map


def generate_passport_bar(df):
    vila_real = df.query("passport_emission == 'Vila Real'")[['passport_emission', 'passport_date']] \
        .value_counts().to_frame("Vila Real").reset_index().drop(columns=['passport_emission'])
    braga = df.query("passport_emission == 'Braga'")[['passport_emission', 'passport_date']] \
        .value_counts().to_frame("Braga").reset_index().drop(columns=['passport_emission'])
    aveiro = df.query("passport_emission == 'Aveiro'")[['passport_emission', 'passport_date']] \
        .value_counts().to_frame("Aveiro").reset_index().drop(columns=['passport_emission'])
    porto = df.query("passport_emission == 'Porto'")[['passport_emission', 'passport_date']] \
        .value_counts().to_frame("Porto").reset_index().drop(columns=['passport_emission'])

    passports = vila_real.merge(braga, on='passport_date', how='outer') \
        .merge(aveiro, on='passport_date', how='outer') \
        .merge(porto, on='passport_date', how='outer')
    passports["passport_date"] = pd.to_datetime(passports['passport_date'], format='%d/%m/%Y')
    passports = passports.sort_values(by='passport_date')
    return passports