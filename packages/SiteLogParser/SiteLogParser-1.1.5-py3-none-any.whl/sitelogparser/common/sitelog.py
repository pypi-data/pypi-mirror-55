# ------------------------------------------------------------------------------
# Name:        sitelog.py
# Purpose:
#
# Author:      fredriksson
#
# Created:     22.06.2016
# Copyright:   (c) fredriksson 2016
# ------------------------------------------------------------------------------

import re
import pprint


class SiteLogRegex(object):
    """

    """
    RD = {
        'h1': r'\d+\.\ *[\w\ \(\)]*',  # section
        'h2': r'\d+\.(\d*|x)(\.(\d*|x))? \ *[\w\ ()]*',  # subsection
        'al': r'[\ \s]{,5}.*:.*',  # default line, key : value
        'cl': r'[\ \s]+:.*',  # continued line, no key
        'll': r'[\ \s]{,5}.*',  # long line, no value
        'an': r'.*',  # antenna
    }
    RD['info'] = r'((%(al)s)|(%(ll)s))+' % RD
    RD['sec'] = r'\s*%(h1)s(\s*(%(h2)s)?\s*)(\s*%(info)s\s*)' % RD

    def get_full_sitelog_str(self):
        return r'(%(sec)s)+(%(an)s)?' % self.RD

    def get_full_sitelog_rc(self):
        return re.compile(self.get_full_sitelog_str())


class SiteLogParser(object):
    '''
    classdocs
    '''

    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        self.slr = SiteLogRegex()
        sitelog_file = kwargs.get("sitelog_file", None)
        sitelog_file_read = kwargs.get("sitelog_read", None)
        assert sitelog_file is not None or sitelog_file_read is not None        
        self.slt = None
        self.form_information_str = ""
        self.site_identification_str = ""
        self.site_location_str = ""
        self.gnss_receiver_str = ""
        self.gnss_receivers = []
        self.gnss_antenna_str = ""
        self.gnss_antennas = []
        self.secs = None
        self.on_site_agency_str = ""
        self.responsible_agency_str = ""
        
        if sitelog_file:
        	self.initialize_file(sitelog_file)
        elif sitelog_file_read:
        	self.initialize_file_read(sitelog_file_read)
        else:
        	raise NotImplementedError
        
    def initialize_file_read(self, file_read):
        if file_read:
            self.initialize_text(file_read)

    def initialize_file(self, sitelog_file):
        if sitelog_file:
        	with open(sitelog_file, 'r') as f:
        		self.initialize_file_read(f.read())

    def initialize_text(self, sitelog_text):
        self.slt = sitelog_text
        self.secs = re.findall("^(\d+\.\ +).*", self.slt, flags=re.MULTILINE)

    def get_data_as_cls(self):
        """
        """
        return None

    def get_data_as_json(self):
        """
        """
        # return json.dumps(self.get_data())
        return self.get_data()

    @staticmethod
    def prepare_multiline_string(multiline_string):
        """prepares Multiline String and condenses information"""
        ref = re.findall(r'\s+(.*:.*)', multiline_string)
        new_ref = []
        for line in ref:
            line_split = line.split(':', 1)
            key = line_split[0].strip()
            value = line_split[-1].strip()
            if key != "":
                new_ref.append(line)
            else:
                parts = new_ref[-1].split(":", 1)
                new_part = value
                new_ref[-1] = "{}: {} {}".format(parts[0].strip(), parts[-1].strip(), new_part)
        return new_ref

    def get_data(self):
        """
        :returns: Sitelog dict
        """
        self.generate_section_form_information()
        self.generate_section_site_identification()
        self.generate_section_site_location()

        obj = {"sitelog": {}}
        obj["sitelog"].update(self.get_section_form_information())
        obj["sitelog"].update(self.get_section_site_identification())
        obj["sitelog"].update(self.get_section_site_location())

        self.generate_section_gnss_receiver()
        self.generate_section_gnss_antenna()

        obj["sitelog"].update(self.generate_subsections_gnss_receiver())
        obj["sitelog"].update(self.generate_subsections_gnss_antenna())

        self.generate_section_on_site_agency()
        obj["sitelog"].update(self.get_section_on_site_agency())
        self.generate_section_responsible_agency()
        obj["sitelog"].update(self.get_section_responsible_agency())
        return obj

    @staticmethod
    def extract_value(line):
        try:
            return line.split(':', 1)[-1].strip()
        except:
            return ""

    @staticmethod
    def extract_notes(l, start=8):
        """
        extract multiline notes assuming there is no further
        information in subsection
        """
        n = ""
        for i in range(start, len(l)):
            n += l[i].split(":", 1)[-1].strip().replace("   ",
                                                        " ").replace("  ",
                                                                     " ") + " "
        return n.strip()

    def generate_section_form_information(self):
        self.form_information_str = self.slt[
            self.slt.index(self.secs[0]):self.slt.index(self.secs[1])
        ].strip()

    def get_section_form_information(self):
        ref = self.prepare_multiline_string(self.form_information_str)
        assert ref is not None
        assert len(ref) >= 3
        fid = {
            "form_information": {
                "section": "00",
                "prepared_by": self.extract_value(ref[0]),
                "date_prepared": self.extract_value(ref[1]),
                "report_type": self.extract_value(ref[2]),
                "previous_site_log": self.extract_value(ref[4]) if len(ref) > 3 else "",
                "modified_added_sections": self.extract_value(ref[5]) if len(ref) > 4 else "",
            }
        }
        return fid

    def generate_section_site_identification(self):
        self.site_identification_str = self.slt[
            self.slt.index(self.secs[1]):self.slt.index(self.secs[2])
        ].strip()

    def get_section_site_identification(self):
        # ref = re.findall(r'\s+(.*:.*)', self.site_identification_str)
        ref = self.prepare_multiline_string(self.site_identification_str)
        assert ref is not None
        assert len(ref) >= 18
        obj = {
            "site_identification": {
                "section": "01",
                'site_name': self.extract_value(ref[0]),
                'four_character_id': self.extract_value(ref[1]),
                'monument_inscription': self.extract_value(ref[2]),
                'iers_domes_number': self.extract_value(ref[3]),
                'cdp_number': self.extract_value(ref[4]),
                'monument_description': self.extract_value(ref[5]),
                'height_of_the_monument': self.extract_value(ref[6]),
                'monument_foundation': self.extract_value(ref[7]),
                'foundation_depth': self.extract_value(ref[8]),
                'marker_description': self.extract_value(ref[9]),
                'date_installed': self.extract_value(ref[10]),
                'geologic_characteristic': self.extract_value(ref[11]),
                'bedrock_type': self.extract_value(ref[12]),
                'bedrock_condition': self.extract_value(ref[13]),
                'fracture_spacing': self.extract_value(ref[14]),
                'fault_zones_nearby': self.extract_value(ref[15]),
                'fault_zones_distance_activity': self.extract_value(ref[16]),
                'notes': self.extract_notes(ref, 17),
            }
        }
        return obj

    def generate_section_site_location(self):
        self.site_location_str = self.slt[
            self.slt.index(self.secs[2]):self.slt.index(self.secs[3])
        ].strip()

    def get_section_site_location(self):
        # ref = re.findall(r'\s+(.*:.*)', self.site_location_str)
        ref = self.prepare_multiline_string(self.site_location_str)
        assert ref is not None
        assert len(ref) >= 5
        obj = {
            "site_location": {
                "section": "02",
                "city": self.extract_value(ref[0]),
                "state": self.extract_value(ref[1]),
                "country": self.extract_value(ref[2]),
                "tectonic_plate": self.extract_value(ref[3]),
                "x": self.extract_value(ref[4]),
                "y": self.extract_value(ref[5]),
                "z": self.extract_value(ref[6]),
                "latitude": self.extract_value(ref[7]),
                "longitude": self.extract_value(ref[8]),
                "elevation": self.extract_value(ref[9]),
                "notes": self.extract_value(ref[10]),
            }
        }
        return obj

    def generate_section_gnss_receiver(self):
        self.gnss_receiver_str = self.slt[
            self.slt.index(self.secs[3]):self.slt.index(self.secs[4])
        ].strip()

    def generate_subsections_gnss_receiver(self):
        """

        """

        obj = {
            "gnss_receivers": {
                "section": "03",
                "list": []
            }
        }
        assert self.gnss_receiver_str != ""

        grf = re.findall(
            r'3\..*\ *Receiver\ Type\ +:',
            self.gnss_receiver_str
        )
        for i in range(len(grf) - 1):
            # Delete Leading Section number
            von = self.gnss_receiver_str.index(grf[i])
            bis = self.gnss_receiver_str.index(grf[i + 1])
            gr = self.gnss_receiver_str[von:bis]
            gr_n = gr[:5].strip().split('.')[-1]
            gr = "     " + gr[5:]
            grs = gr.split('\n')
            grd = {
                'gnss_receiver': {
                    'number': int(gr_n),
                    'receiver_type': self.extract_value(grs[0]),
                    'satellite_sytem': self.extract_value(grs[1]),
                    'serial_number': self.extract_value(grs[2]),
                    'firmware_version': self.extract_value(grs[3]),
                    'elevation_cutoff_setting': self.extract_value(grs[4]),
                    'date_installed': self.extract_value(grs[5]),
                    'date_removed': self.extract_value(grs[6]),
                    'temperature_stabilization': self.extract_value(grs[7]),
                    'notes': self.extract_notes(grs, 8),
                }
            }
            # grd['gnss_receiver']["receiver_type"] = " ".join(grd['gnss_receiver']["receiver_type"])
            obj["gnss_receivers"]["list"].append(grd)
        return obj

    def generate_section_gnss_antenna(self):
        self.gnss_antenna_str = self.slt[
            self.slt.index(self.secs[4]):self.slt.index(self.secs[5])
        ].strip()

    def generate_section_on_site_agency(self):
        self.on_site_agency_str = self.slt[
            self.slt.index(self.secs[11]):self.slt.index(self.secs[12])
        ].strip()

    def generate_section_responsible_agency(self):
        self.responsible_agency_str = self.slt[
            self.slt.index(self.secs[12]):self.slt.index(self.secs[13])
        ]

    def extract_agency(self, agency_name, agency_str, section):
        ref = self.prepare_multiline_string(agency_str)
        obj = {
            "section": section,
            "name": "",
            "abbrevation": "",
            "mail_address": "",
            "primary_contact" : {
                "name": "",
                "phone1": "",
                "phone2": "",
                "fax": "",
                "email": ""
            },
            "secondary_contact" : {
                "name": "",
                "phone1": "",
                "phone2": "",
                "fax": "",
                "email": ""
            }   
        }
        contact_counter = -1
        for part in ref:
            if part.startswith("Agency"):
                obj["name"] = self.extract_value(part)
            elif part.startswith("Preferred Abbreviation"):
                obj["abbrevation"] = self.extract_value(part)
            elif part.startswith("Mailing Address"):
                obj["mail_address"] = self.extract_value(part)
            else:
                # Now it get's tricky
                contact_number = ["primary_contact", "secondary_contact"]
                if part.startswith("Contact Name"):
                    contact_counter += 1
                    obj[contact_number[contact_counter]]["name"] = self.extract_value(part)
                elif part.startswith("Telephone (primary)"):
                    obj[contact_number[contact_counter]]["phone1"] = self.extract_value(part)
                elif part.startswith("Telephone (secondary)"):
                    obj[contact_number[contact_counter]]["phone2"] = self.extract_value(part)
                elif part.startswith("Fax"):
                    obj[contact_number[contact_counter]]["fax"] = self.extract_value(part)
                elif part.startswith("E-mail"):
                    obj[contact_number[contact_counter]]["email"] = self.extract_value(part)
        return obj


    def get_section_on_site_agency(self):
        """Extract Section 11 - On-Site Agency"""
        return {
            "on_site_agency": self.extract_agency("on_site_agency", self.on_site_agency_str, 11)
        }

    def get_section_responsible_agency(self):
        """Extract Section 12 - Responsible Agency"""
        return {
            "responsible_agency": self.extract_agency("responsible_agency", self.responsible_agency_str, 12)
        }

    def generate_subsections_gnss_antenna(self):
        """

        """
        obj = {
            "gnss_antennas": {
                "section": "04",
                "list": []
            }
        }
        assert self.gnss_antenna_str != ""

        grf = re.findall(
            r'4\..*\ *Antenna\ Type\ +:',
            self.gnss_antenna_str
        )
        for i in range(len(grf) - 1):
            # Delete Leading Section number
            von = self.gnss_antenna_str.index(grf[i])
            bis = self.gnss_antenna_str.index(grf[i + 1])
            gr = self.gnss_antenna_str[von:bis]
            gr_n = gr[:5].strip().split('.')[-1]
            gr = "     " + gr[5:]
            grs = gr.split('\n')
            grd = {
                'gnss_antenna': {
                    'number': int(gr_n),
                    'antenna_type': self.extract_value(grs[0]),
                    'serial_number': self.extract_value(grs[1]),
                    'antenna_reference_point': self.extract_value(grs[2]),
                    'marker_arp_up_ecc': self.extract_value(grs[3]),
                    'marker_arp_north_ecc': self.extract_value(grs[4]),
                    'marker_arp_east_ecc': self.extract_value(grs[5]),
                    'alignment_of_true_n': self.extract_value(grs[6]),
                    'antenna_radome_type': self.extract_value(grs[7]),
                    'radome_serial_number': self.extract_value(grs[8]),
                    'antenna_cable_type': self.extract_value(grs[9]),
                    'antenna_cable_length': self.extract_value(grs[10]),
                    'date_installed': self.extract_value(grs[11]),
                    'date_removed': self.extract_value(grs[12]),
                    'notes': self.extract_notes(grs, 13),
                }
            }
            obj["gnss_antennas"]["list"].append(grd)
        return obj
