#!/usr/bin/env python3
import argparse
import csv
import os
from datetime import datetime
from collections import defaultdict

CSV_PATH_DEFAULT = "sessions.csv"
DATE_FMT = "%Y-%m-%d"

def ensure_csv(csv_path):
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["date","plateforme","heures","km","euros","pourboires"])

def parse_date(s):
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except ValueError:
        raise ValueError(f"Date invalide '{s}'. Format attendu: YYYY-MM-DD.")

def read_rows(csv_path, dfrom=None, dto=None):
    rows = []
    if not os.path.exists(csv_path):
        return rows
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                d = parse_date(r["date"])
            except Exception:
                continue
            if dfrom and d < dfrom:
                continue
            if dto and d > dto:
                continue
            try:
                heures = float(r["heures"])
                km = float(r["km"])
                euros = float(r["euros"])
                pourboires = float(r.get("pourboires", 0.0))
            except Exception:
                continue
            rows.append({
                "date": d,
                "plateforme": r["plateforme"].strip(),
                "heures": heures,
                "km": km,
                "euros": euros,
                "pourboires": pourboires,
            })
    return rows

def cmd_init(args):
    ensure_csv(args.csv)
    print(f"Initialisé: {args.csv}")

def cmd_add(args):
    ensure_csv(args.csv)
    d = parse_date(args.date)
    with open(args.csv, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([d.strftime(DATE_FMT), args.plateforme, args.heures, args.km, args.euros, args.pourboires])
    print("Ajout OK.")

def summarize(rows):
    total_euros = sum(r["euros"] for r in rows)
    total_pourboires = sum(r["pourboires"] for r in rows)
    total_gross = total_euros + total_pourboires
    total_heures = sum(r["heures"] for r in rows)
    total_km = sum(r["km"] for r in rows)

    euros_h = (total_gross / total_heures) if total_heures > 0 else 0.0
    euros_km = (total_gross / total_km) if total_km > 0 else 0.0

    by_date = defaultdict(lambda: 0.0)
    for r in rows:
        by_date[r["date"]] += (r["euros"] + r["pourboires"])
    best_day = None
    if by_date:
        best_day = max(by_date.items(), key=lambda kv: kv[1])

    return {
        "n_rows": len(rows),
        "total_euros": total_euros,
        "total_pourboires": total_pourboires,
        "total_gross": total_gross,
        "total_heures": total_heures,
        "total_km": total_km,
        "euros_h": euros_h,
        "euros_km": euros_km,
        "best_day": best_day,
    }

def cmd_summary(args):
    dfrom = parse_date(args.from_date) if args.from_date else None
    dto = parse_date(args.to_date) if args.to_date else None
    rows = read_rows(args.csv, dfrom, dto)
    s = summarize(rows)

    print("=== RÉSUMÉ ===")
    rng = []
    if dfrom: rng.append(f"du {dfrom}")
    if dto: rng.append(f"au {dto}")
    if rng:
        print("Période:", " ".join(rng))
    print(f"Lignes: {s['n_rows']}")
    print(f"Revenus (hors tips): {s['total_euros']:.2f} €")
    print(f"Pourboires: {s['total_pourboires']:.2f} €")
    print(f"Total brut: {s['total_gross']:.2f} €")
    print(f"Heures: {s['total_heures']:.2f} h")
    print(f"Kilomètres: {s['total_km']:.2f} km")
    print(f"€/h: {s['euros_h']:.2f}")
    print(f"€/km: {s['euros_km']:.2f}")
    if s["best_day"]:
        d, m = s["best_day"]
        print(f"Meilleur jour: {d} ({m:.2f} €)")

def cmd_plot(args):
    import matplotlib.pyplot as plt
    from collections import defaultdict

    dfrom = parse_date(args.from_date) if args.from_date else None
    dto = parse_date(args.to_date) if args.to_date else None
    rows = read_rows(args.csv, dfrom, dto)

    by_date = defaultdict(lambda: 0.0)
    for r in rows:
        by_date[r["date"]] += (r["euros"] + r["pourboires"])

    dates = sorted(by_date.keys())
    values = [by_date[d] for d in dates]

    if not dates:
        print("Aucune donnée à tracer sur cette période.")
        return

    plt.figure()
    plt.bar([d.strftime("%Y-%m-%d") for d in dates], values)
    plt.xticks(rotation=45, ha="right")
    plt.title("Revenus par jour")
    plt.xlabel("Date")
    plt.ylabel("€ (brut)")
    plt.tight_layout()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    plt.savefig(args.output, dpi=150)
    print(f"Graphique enregistré: {args.output}")

def build_parser():
    p = argparse.ArgumentParser(description="Tracker revenus livreur (CLI)")
    p.add_argument("--csv", default=CSV_PATH_DEFAULT, help="Chemin du CSV (défaut: sessions.csv)")
    sp = p.add_subparsers(dest="cmd", required=True)

    p_init = sp.add_parser("init", help="Créer le CSV si absent")
    p_init.set_defaults(func=cmd_init)

    p_add = sp.add_parser("add", help="Ajouter une session")
    p_add.add_argument("--date", required=True, help="YYYY-MM-DD")
    p_add.add_argument("--plateforme", required=True, choices=["uber","deliveroo","autre"], help="Plateforme")
    p_add.add_argument("--heures", type=float, required=True)
    p_add.add_argument("--km", type=float, required=True)
    p_add.add_argument("--euros", type=float, required=True, help="Revenus hors pourboires")
    p_add.add_argument("--pourboires", type=float, default=0.0)
    p_add.set_defaults(func=cmd_add)

    p_sum = sp.add_parser("summary", help="Résumé chiffré")
    p_sum.add_argument("--from", dest="from_date", help="YYYY-MM-DD")
    p_sum.add_argument("--to", dest="to_date", help="YYYY-MM-DD")
    p_sum.set_defaults(func=cmd_summary)

    p_plot = sp.add_parser("plot", help="Graphique revenus/jour (PNG)")
    p_plot.add_argument("--from", dest="from_date", help="YYYY-MM-DD")
    p_plot.add_argument("--to", dest="to_date", help="YYYY-MM-DD")
    p_plot.add_argument("--output", required=True, help="Chemin PNG de sortie")
    p_plot.set_defaults(func=cmd_plot)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
