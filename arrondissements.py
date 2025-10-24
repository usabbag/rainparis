"""
Paris arrondissements data with center coordinates for weather queries.
Data source: OpenDataSoft Paris open data
"""

ARRONDISSEMENTS = {
    0: {
        "name": "Paris",
        "lat": 48.8566,
        "lon": 2.3522
    },
    1: {
        "name": "1er - Louvre",
        "lat": 48.8625627018,
        "lon": 2.33644336205
    },
    2: {
        "name": "2ème - Bourse",
        "lat": 48.8682792225,
        "lon": 2.34280254689
    },
    3: {
        "name": "3ème - Temple",
        "lat": 48.86287238,
        "lon": 2.3600009859
    },
    4: {
        "name": "4ème - Hôtel-de-Ville",
        "lat": 48.8543414263,
        "lon": 2.35762962032
    },
    5: {
        "name": "5ème - Panthéon",
        "lat": 48.8444431505,
        "lon": 2.35071460958
    },
    6: {
        "name": "6ème - Luxembourg",
        "lat": 48.8491303586,
        "lon": 2.33289799905
    },
    7: {
        "name": "7ème - Palais-Bourbon",
        "lat": 48.8561744288,
        "lon": 2.31218769148
    },
    8: {
        "name": "8ème - Élysée",
        "lat": 48.8727208374,
        "lon": 2.3125540224
    },
    9: {
        "name": "9ème - Opéra",
        "lat": 48.8771635173,
        "lon": 2.33745754348
    },
    10: {
        "name": "10ème - Entrepôt",
        "lat": 48.8761300365,
        "lon": 2.36072848785
    },
    11: {
        "name": "11ème - Popincourt",
        "lat": 48.8590592213,
        "lon": 2.3800583082
    },
    12: {
        "name": "12ème - Reuilly",
        "lat": 48.8349743815,
        "lon": 2.42132490078
    },
    13: {
        "name": "13ème - Gobelins",
        "lat": 48.8283880317,
        "lon": 2.36227244042
    },
    14: {
        "name": "14ème - Observatoire",
        "lat": 48.8292445005,
        "lon": 2.3265420442
    },
    15: {
        "name": "15ème - Vaugirard",
        "lat": 48.8400853759,
        "lon": 2.29282582242
    },
    16: {
        "name": "16ème - Passy",
        "lat": 48.8603921054,
        "lon": 2.26197078836
    },
    17: {
        "name": "17ème - Batignolles-Monceau",
        "lat": 48.887326522,
        "lon": 2.30677699057
    },
    18: {
        "name": "18ème - Buttes-Montmartre",
        "lat": 48.892569268,
        "lon": 2.34816051956
    },
    19: {
        "name": "19ème - Buttes-Chaumont",
        "lat": 48.8870759966,
        "lon": 2.38482096015
    },
    20: {
        "name": "20ème - Ménilmontant",
        "lat": 48.8634605789,
        "lon": 2.40118812928
    }
}


def get_arrondissement(number):
    """Get arrondissement data by number (0 for Paris overall, 1-20 for specific arrondissements)"""
    return ARRONDISSEMENTS.get(number)


def get_all_arrondissements():
    """Get all arrondissements as a list"""
    return [
        {"number": num, **data}
        for num, data in sorted(ARRONDISSEMENTS.items())
    ]


def get_coordinates(number):
    """Get (lat, lon) tuple for an arrondissement (0 for Paris overall, 1-20 for specific)"""
    arr = get_arrondissement(number)
    if arr:
        return (arr["lat"], arr["lon"])
    return None


if __name__ == "__main__":
    # Test the data
    print("Paris Arrondissements Center Coordinates")
    print("=" * 60)
    for num in range(0, 21):
        arr = get_arrondissement(num)
        if num == 0:
            print(f" 0. {arr['name']:30s} ({arr['lat']:.6f}, {arr['lon']:.6f}) [Overall]")
        else:
            print(f"{num:2d}. {arr['name']:30s} ({arr['lat']:.6f}, {arr['lon']:.6f})")
