#!/usr/bin/env python3
"""P03 - külső ellenpróba nyílt adattal: a hirdetésben szereplő "143 m-re megálló"
állítás és a Zöld kapu-terület távolsága az épülettől.

Élő szolgáltatásokat hív (Nominatim, Overpass), ezért az eredmény időfüggő;
a futás időbélyege a kimenetben szerepel. Egyszeri, kis terhelésű lekérdezés.
Adatforrás: (c) OpenStreetMap contributors, ODbL 1.0 - terjesztésnél
a forrásmegjelölés kötelező. A távolságok légvonalbeliek (haversine), a
gyaloglási útvonal ennél hosszabb lehet.

Használat:  python3 osm_proximity_check.py
"""
import json
import math
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

UA = "property-datasheet-verification/1.0 (one-off check)"
NOMINATIM = "https://nominatim.openstreetmap.org/search"
OVERPASS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
BUILDING_QUERY = "Hungária utca 28, Pécs, Hungary"
AREA_QUERY = "Steinmetz kapitány tér, Pécs, Hungary"
RADIUS_M = 450


def haversine(lat1, lon1, lat2, lon2):
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return 2 * r * math.asin(math.sqrt(a))


def http_json(url, data=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=40) as resp:
        return json.load(resp)


def geocode(query):
    params = urllib.parse.urlencode({"q": query, "format": "json", "limit": 1})
    hits = http_json(f"{NOMINATIM}?{params}")
    time.sleep(1.5)
    if not hits:
        raise SystemExit(f"Nincs geokódolási találat: {query}")
    return float(hits[0]["lat"]), float(hits[0]["lon"]), hits[0]["display_name"]


def stops_near(lat, lon):
    ql = (f"[out:json][timeout:25];(node(around:{RADIUS_M},{lat},{lon})[highway=bus_stop];"
          f"node(around:{RADIUS_M},{lat},{lon})[public_transport=platform];);out;")
    body = urllib.parse.urlencode({"data": ql}).encode()
    last_error = None
    for endpoint in OVERPASS:
        try:
            return http_json(endpoint, data=body)
        except Exception as exc:
            last_error = exc
    raise SystemExit(f"Az Overpass nem érhető el: {last_error}")


def main():
    blat, blon, bname = geocode(BUILDING_QUERY)
    alat, alon, aname = geocode(AREA_QUERY)
    data = stops_near(blat, blon)

    print(f"Futás időpontja (UTC): {datetime.now(timezone.utc):%Y-%m-%d %H:%M}")
    print(f"OSM-adat időbélyege: {data.get('osm3s', {}).get('timestamp_osm_base', 'n/a')}")
    print(f"Épület (geokódolt): {blat:.6f}, {blon:.6f} - {bname.split(',')[0]}")
    print(f"Zöld kapu-terület (geokódolt pont): {alat:.6f}, {alon:.6f} - {aname.split(',')[0]}")
    print(f"Távolság az épülettől a terület geokódolt pontjáig: {haversine(blat, blon, alat, alon):.0f} m\n")

    stops = sorted(
        (haversine(blat, blon, e["lat"], e["lon"]), e.get("tags", {}).get("name", "(névtelen)"))
        for e in data.get("elements", [])
    )
    print(f"Megállók {RADIUS_M} m-en belül: {len(stops)}")
    print("| Távolság (m, légvonal) | Megálló |")
    print("|---|---|")
    for dist, name in stops[:8]:
        print(f"| {dist:.0f} | {name} |")
    if stops:
        print(f"\nLegközelebbi feltérképezett megálló: {stops[0][0]:.0f} m (hirdetésben: 143 m)")


if __name__ == "__main__":
    main()
