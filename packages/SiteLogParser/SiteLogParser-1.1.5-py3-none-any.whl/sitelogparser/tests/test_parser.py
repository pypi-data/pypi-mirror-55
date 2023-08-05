#!/usr/bin/env python3

import unittest
import os
import pprint

from sitelogparser.common.sitelog import SiteLogParser

TEST_DATA = {
    "AMST": {
        "file": "AMST_20190705.txt",
        "antennas": 6,
        "receivers": 20
    },
    "TLMF": {
        "file": "tlmf_20190313.log",
        "antennas": 3,
        "receivers": 21
    },
    "SODA": {
        "file": "soda_20190131.log",
        "antennas": 2,
        "receivers": 25
    },
    "SCOR": {
        "file": "scor_20190926.log",
        "antennas": 1,
        "receivers": 7
    },
    "TOUL": {
        "file": "toul_20100113.log",
        "antennas": 1,
        "receivers": 1
    }
}


class TestSitelogParser(unittest.TestCase):

    def setUp(self):
        self.sitelog_data = {}
        for station in TEST_DATA:
            sitelog_file = os.path.join(os.path.dirname(__file__), TEST_DATA[station]["file"])
            parser = None
            with open(sitelog_file, 'r') as f:
                parser = SiteLogParser(sitelog_read=f.read())
            self.sitelog_data[station] = parser.get_data()
            # pprint.pprint(self.sitelog_data[station])

    def test_antennas(self):
        for station in TEST_DATA:
            self.assertEqual(len(self.sitelog_data[station]["sitelog"]["gnss_antennas"]["list"]), TEST_DATA[station]["antennas"])

    def test_receivers(self):
        for station in TEST_DATA:
            self.assertEqual(len(self.sitelog_data[station]["sitelog"]["gnss_receivers"]["list"]), TEST_DATA[station]["receivers"])

    # def test_apos_sis(self):
    #     d = self.sitelog_data["sitelog"]
    #     site = {
    #         "name": d["site_identification"]["site_name"],
    #         "four_letter_code": d["site_identification"]["four_character_id"],
    #         "ip_address": "0.0.0.0",
    #         "monument": {
    #             "antennas": [],
    #             "domes_number": d["site_identification"]["iers_domes_number"],
    #             "station": {
    #                 "four_letter_code": d["site_identification"]["four_character_id"],
    #                 "receivers": [],                        
    #             }
    #         }
    #     }
    #     for obj in d["gnss_antennas"]["list"]:
    #         site["monument"]["antennas"].append({
    #             "valid_from": obj["gnss_antenna"]["date_installed"],
    #             "valid_until": obj["gnss_antenna"]["date_removed"],
    #             "antenna_typ": str(obj["gnss_antenna"]["antenna_type"][:-4]).strip(),
    #             "antenna_snr": obj["gnss_antenna"]["serial_number"],
    #             "radome_typ": obj["gnss_antenna"]["antenna_radome_type"],
    #             "radome_snr": obj["gnss_antenna"]["radome_serial_number"],
    #         })
    #     for obj in d["gnss_receivers"]["list"]:
    #         site["monument"]["station"]["receivers"].append({
    #             "valid_from": obj["gnss_receiver"]["date_installed"],
    #             "valid_until": obj["gnss_receiver"]["date_removed"],
    #             "firmware": obj["gnss_receiver"]["firmware_version"],
    #             "receiver_typ": obj["gnss_receiver"]["receiver_type"],
    #             "receiver_snr": obj["gnss_receiver"]["serial_number"],
    #         })


if __name__ == '__main__':
    unittest.main()



