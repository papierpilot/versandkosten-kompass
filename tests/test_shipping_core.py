"""
Core tests for the TES-modularized Versandkosten-Kompass.

BUILD_MARKER = "VERSANDKOMPASS_2026_07_01_BUILD_001"
PURPOSE = "Verify pure shipping and pricing logic without Streamlit UI"
"""

import unittest

from data.demo_data import ANBIETER_MODELLE
from modules.location_demo import berechne_demo_entfernung_km, normalisiere_plz
from modules.pickup_costs import summarize_unbooked_pickups
from modules.pricing_simulation import simuliere_anbieterpreise, simuliere_anbieterpreise_fuer_pakete
from modules.shipment_model import PackageItem, ShipmentInput
from modules.shipping_workflow import evaluate_shipment
from ui.provider_panel import render_provider_grid
from ui.result_panel import build_decision_note
from modules.shipping_rules import berechne_gurtmass, berechne_volumen_gewicht, pruefe_plausibilitaet


class ShippingCoreTest(unittest.TestCase):
    def test_normalisiere_plz_keeps_first_five_digits(self):
        self.assertEqual(normalisiere_plz("51379 Leverkusen"), "51379")

    def test_package_measurements_are_calculated(self):
        self.assertEqual(berechne_gurtmass(30, 20, 10), 90)
        self.assertAlmostEqual(berechne_volumen_gewicht(30, 20, 10), 1.2)

    def test_demo_distance_for_known_plz(self):
        distance, reason = berechne_demo_entfernung_km("44135", "Deutschland")
        self.assertIsInstance(distance, int)
        self.assertGreater(distance, 1)
        self.assertIn("PLZ", reason)

    def test_pricing_returns_best_possible_provider_first(self):
        results = simuliere_anbieterpreise(1, 1.4, 30, 22, 12, 80)
        self.assertTrue(results)
        self.assertTrue(results[0]["moeglich"])
        self.assertEqual(results[0]["anbieter"], "DHL")

    def test_plausibility_warns_for_large_quantity(self):
        warnings = pruefe_plausibilitaet(24, 12, 60, 40, 35)
        self.assertTrue(any("Hohe Paketmenge" in warning for warning in warnings))


    def test_workflow_returns_complete_evaluation(self):
        evaluation = evaluate_shipment(
            ShipmentInput(
                paket_menge=1,
                gewicht_kg=1.4,
                laenge_cm=30,
                breite_cm=22,
                hoehe_cm=12,
                empfaenger="Musterkunde GmbH",
                land="Deutschland",
                plz="44135",
                ort="Dortmund",
            )
        )
        self.assertEqual(evaluation.plz_norm, "44135")
        self.assertTrue(evaluation.ergebnisse)
        self.assertEqual(evaluation.bestes_ergebnis["anbieter"], "DHL")
        self.assertGreaterEqual(evaluation.vertrauensscore, 78)

    def test_workflow_makes_missing_address_visible(self):
        evaluation = evaluate_shipment(
            ShipmentInput(
                paket_menge=1,
                gewicht_kg=1.4,
                laenge_cm=30,
                breite_cm=22,
                hoehe_cm=12,
                empfaenger="",
                land="Deutschland",
                plz="",
                ort="",
            )
        )
        self.assertTrue(any("Zieladresse noch unvollständig" in warning for warning in evaluation.warnungen))


    def test_provider_grid_renders_prepared_results(self):
        results = simuliere_anbieterpreise(1, 1.4, 30, 22, 12, 80)
        html = render_provider_grid(results, results[0], produktivmodus=False)
        self.assertIn("provider-grid", html)
        self.assertIn("DHL", html)
        self.assertIn("Empfehlung", html)


    def test_decision_note_uses_workflow_contract(self):
        evaluation = evaluate_shipment(
            ShipmentInput(
                paket_menge=1,
                gewicht_kg=1.4,
                laenge_cm=30,
                breite_cm=22,
                hoehe_cm=12,
                empfaenger="Musterkunde GmbH",
                land="Deutschland",
                plz="44135",
                ort="Dortmund",
            )
        )
        note = build_decision_note(evaluation)
        self.assertIn("Alle Anbieter geprüft", note)
        self.assertIn("Empfehlung: DHL", note)
        self.assertIn("Dortmund", note)


    def test_jumingo_provider_is_available(self):
        provider_names = {provider["name"] for provider in ANBIETER_MODELLE}
        self.assertIn("Jumingo", provider_names)
        results = simuliere_anbieterpreise(3, 4.0, 40, 30, 20, 120)
        self.assertTrue(any(result["anbieter"] == "Jumingo" for result in results))

    def test_unbooked_pickup_costs_are_summed(self):
        summary = summarize_unbooked_pickups(
            [
                {"status": "ungebucht", "kosten": 10.50},
                {"status": "gebucht", "kosten": 99.00},
                {"status": "ungebucht", "kosten": 4.25},
            ]
        )
        self.assertEqual(summary.count, 2)
        self.assertEqual(summary.total_cost, 14.75)


    def test_multipackage_pricing_uses_different_package_items(self):
        packages = (
            PackageItem(position=1, gewicht_kg=1.4, laenge_cm=30, breite_cm=22, hoehe_cm=12),
            PackageItem(position=2, gewicht_kg=18.0, laenge_cm=145, breite_cm=38, hoehe_cm=28),
        )
        results = simuliere_anbieterpreise_fuer_pakete(packages, 80)
        self.assertEqual(results[0]["paket_menge"], 2)
        self.assertEqual(len(results[0]["paket_details"]), 2)
        self.assertGreater(results[0]["gesamt_abrechnungsgewicht"], results[0]["abrechnungsgewicht"])

    def test_workflow_accepts_explicit_package_items(self):
        evaluation = evaluate_shipment(
            ShipmentInput(
                paket_menge=2,
                gewicht_kg=1.4,
                laenge_cm=30,
                breite_cm=22,
                hoehe_cm=12,
                empfaenger="Musterkunde GmbH",
                land="Deutschland",
                plz="44135",
                ort="Dortmund",
                packages=(
                    PackageItem(position=1, gewicht_kg=1.4, laenge_cm=30, breite_cm=22, hoehe_cm=12),
                    PackageItem(position=2, gewicht_kg=18.0, laenge_cm=145, breite_cm=38, hoehe_cm=28),
                ),
            )
        )
        self.assertEqual(evaluation.input_data.effective_paket_menge, 2)
        self.assertEqual(evaluation.referenz["paket_menge"], 2)
        self.assertTrue(evaluation.ergebnisse)


if __name__ == "__main__":
    unittest.main()
