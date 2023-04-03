from teams.exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError

def data_processing(data):
    all_cups = (1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022)

    if data["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")
    
    if int(data["first_cup"].split("-")[0]) < 1930:
        raise InvalidYearCupError("there was no world cup this year")

    if int(data["first_cup"].split("-")[0]) not in all_cups:
        raise InvalidYearCupError("there was no world cup this year")
    
    if len(all_cups) - all_cups.index(int(data["first_cup"].split("-")[0])) < data["titles"]:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")