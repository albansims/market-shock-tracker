import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

events = [
    (
        "2026-02-03",
        "IRGC attempts to seize US tanker Stena Imperative",
        "Six IRGC Navy gunboats attempted to stop a US tanker in the Strait of Hormuz; "
        "the Stena Imperative continued under USS McFaul escort. First kinetic incident "
        "of the pre-war period.",
        "military",
        "https://en.wikipedia.org/wiki/Prelude_to_the_2026_Iran_war",
        2,
    ),
    (
        "2026-02-17",
        "Iran briefly closes Strait of Hormuz during military drill",
        "During the second round of nuclear talks in Geneva, Khamenei threatened US "
        "warships and Iran closed the Strait for several hours during a live-fire drill. "
        "War-risk insurance premiums for the Strait began rising from 0.125% toward "
        "0.2–0.4% of insured value per transit.",
        "supply_disruption",
        "https://en.wikipedia.org/wiki/2026_Strait_of_Hormuz_crisis",
        3,
    ),
    (
        "2026-02-19",
        "US deploys warships, tankers, submarines; Trump warns of imminent strikes",
        "Reports that the US could launch military strikes within days. Trump positioned "
        "naval and air assets at a level not seen since the 2003 invasion of Iraq.",
        "military",
        "https://en.wikipedia.org/wiki/Prelude_to_the_2026_Iran_war",
        3,
    ),
    (
        "2026-02-25",
        "US Treasury sanctions 30+ entities in Iran's oil shipping network",
        "Department of the Treasury imposed sanctions on more than 30 individuals, "
        "entities, and vessels linked to Iran's oil shipping network.",
        "diplomatic",
        "https://en.wikipedia.org/wiki/2026_Iran_war_ceasefire",
        2,
    ),
    (
        "2026-02-28",
        "Operation Epic Fury — US-Israel launch coordinated strikes on Iran",
        "US and Israeli forces launched nearly 900 strikes in 12 hours targeting Iranian "
        "missiles, air defences, military infrastructure, and leadership. Supreme Leader "
        "Ali Khamenei killed. Brent crude rose 10–13% to $80–82 by 2 March.",
        "military",
        "https://en.wikipedia.org/wiki/2026_Iran_war",
        5,
    ),
    (
        "2026-03-02",
        "IRGC officially confirms Strait of Hormuz closed",
        "Senior IRGC official confirmed the Strait was closed and threatened any ship "
        "attempting passage. Crude tanker transits dropped from ~24/day pre-war to 4 "
        "vessels on 1 March. The IEA later called it the largest oil supply disruption "
        "in history.",
        "supply_disruption",
        "https://en.wikipedia.org/wiki/2026_Strait_of_Hormuz_crisis",
        5,
    ),
    (
        "2026-03-04",
        "Maersk, CMA CGM, Hapag-Lloyd suspend Strait and Red Sea transits",
        "Major container shipping companies suspended transits through the Strait of "
        "Hormuz and Red Sea, forcing rerouting around the Cape of Good Hope and adding "
        "weeks to transit times.",
        "supply_disruption",
        "https://en.wikipedia.org/wiki/2026_Strait_of_Hormuz_crisis",
        4,
    ),
    (
        "2026-03-15",
        "Houthi Red Sea shipping attacks intensify; Cape rerouting becomes default",
        "Yemen's Houthis escalated attacks on commercial shipping in the Red Sea, "
        "compounding the Hormuz disruption. Suez Canal traffic rerouted around Africa.",
        "supply_disruption",
        "https://en.wikipedia.org/wiki/2026_Iran_war",
        3,
    ),
    (
        "2026-03-31",
        "Brent crude posts +51% monthly gain — one of largest in history",
        "March 2026 marked one of the largest monthly oil price surges on record, with "
        "Brent gaining 51% as Gulf output collapsed and exports stalled. Global oil "
        "supply fell 10.1 mb/d to 97 mb/d.",
        "market",
        "https://www.iea.org/reports/oil-market-report-april-2026",
        4,
    ),
    (
        "2026-04-08",
        "US-Iran agree two-week ceasefire mediated by Pakistan",
        "After Iran rejected a 45-day two-phased framework, the US and Iran agreed to a "
        "two-week ceasefire mediated by Pakistan. Initial relief rally in oil and risk "
        "assets.",
        "diplomatic",
        "https://en.wikipedia.org/wiki/2026_Iran_war_ceasefire",
        4,
    ),
    (
        "2026-04-13",
        "US imposes naval blockade on Iranian ports after Islamabad talks fail",
        "JD Vance announced US-Iran talks had failed. Trump declared a naval blockade "
        "of Iranian ports, with the US Navy intercepting vessels paying tolls to Iran. "
        "Ceasefire effectively broke.",
        "military",
        "https://en.wikipedia.org/wiki/2026_Iran_war_ceasefire",
        4,
    ),
    (
        "2026-04-17",
        "Iran declares Strait of Hormuz fully open; Brent drops 10%+",
        "Iran's Foreign Minister Seyed Abbas Araghchi declared the Strait fully open to "
        "commercial traffic, sending crude prices down more than 10% on the day — one "
        "of Brent's largest single-day declines in decades.",
        "supply_resolution",
        "https://www.cnbc.com/2026/04/21/oil-price-iran-war-middle-east.html",
        5,
    ),
    (
        "2026-04-19",
        "US Navy seizes Iranian container ship in Gulf of Oman",
        "US Navy fired on and seized an Iranian container ship; Iran re-imposed tighter "
        "control over the Strait within hours of reopening, with reports of gunfire on "
        "tankers. Reopening unwound — oil jumped on 20 April.",
        "military",
        "https://www.cnbc.com/2026/04/21/oil-price-iran-war-middle-east.html",
        4,
    ),
    (
        "2026-05-04",
        "Brent +6% to $114 as Strait functionally closed again; UAE attacked",
        "Brent crude rose nearly 6% to $114.44/bbl after US destroyed six Iranian small "
        "boats in response to attacks on commercial vessels, and the UAE reported "
        "Iranian missile and drone strikes. ~20,000 seafarers stranded on ~2,000 vessels.",
        "supply_disruption",
        "https://www.aljazeera.com/economy/2026/5/5/oil-prices-surge-as-violence-flares-in-strait-of-hormuz",
        4,
    ),
    (
        "2026-05-07",
        "US destroyers attacked in Hormuz; CENTCOM strikes Iranian launch sites",
        "Iran attacked three US Navy destroyers (USS Truxtun, USS Rafael Peralta, USS "
        "Mason) transiting the Strait with drones, fast-attack boats, and missiles. "
        "CENTCOM responded with self-defence strikes on Iranian missile and drone "
        "launch sites and command nodes.",
        "military",
        "https://www.cnn.com/2026/05/07/world/live-news/trump-iran-war-news",
        3,
    ),
]


def main():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    cur = conn.cursor()

    inserted = 0
    skipped = 0

    for event_date, event_name, description, event_type, source_url, severity in events:
        cur.execute(
            "SELECT 1 FROM events WHERE event_date = %s AND event_name = %s;",
            (event_date, event_name),
        )
        if cur.fetchone() is not None:
            print(f"⏭  Skipped: {event_date} — {event_name}")
            skipped += 1
            continue

        cur.execute(
            """
            INSERT INTO events
                (event_date, event_name, description, event_type, source_url, severity)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (event_date, event_name, description, event_type, source_url, severity),
        )
        print(f"✅ Inserted: {event_date} — {event_name}")
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()

    print(f"\nDone. Inserted: {inserted}, Skipped: {skipped}, Total: {len(events)}")


if __name__ == "__main__":
    main()