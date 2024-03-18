"""
Parse ASCII renderings of .docx MTB-protocols. Documents are parsed line-by-line. Section boundaries are identified through a whitelist of section headers. The parser does not yield proper results when section headers are not separated by newlines.
"""

from collections import defaultdict

SECTIONS = {
    "Patient:": [
        "Pat-ID:",
        "Name, Vorn., GebDatum:",
        "Name, Vorn., GebDat.:",
        "Name, Vorn., GebDat.",
        "PLZ, Ort:",
        "Aufenthaltsklinik/ -station:",
        "Klinik, Abt., Arzt, Rufnr.:",
        "Zuweisender Arzt:",
    ],
    "Teilnehmer und Dokumentation:": [
        "Teilnehmer:",
        "Dokumentationskraft:",
    ],
    "Verlauf:": [
        "Diagnose:",
        "Metastasen:",
        "Datum Erstdiagnose:",
        "Primärfall:",
        "Zweitmeinung:",
        "Tumorstadium:",
        "Progress unter LL-Therapie:",
        "Alle LL-Therapien durchlaufen:",
        "Anzahl durchlaufener TL (n) und aktuelle L:",
        "Morphologie:",
        "Histologie:",
        "Bisheriger Therapieverlauf:",
        "Komorbiditäten:",
        "Fam. Tumorerkrankungen:",
        "Karnofsky-Index/ECOG:",
    ],
    "Fragestellung:": [],
    "Evidenzlage:": [],
    "Beschluss:": [],
    "Beschluss letzte MTB-Vorstellung:": [],
    "Administration:": [],
    "Anmerkungen Pathologie:": [],
    "Molekularpathologische Analyse": [
        "Befunddatum:",
        "Histo.EinsendeNr.:",
        "Pathologie Inst.:",
        "Pathologisches Institut:",
        "Befundtext:",
        "Analyse basiert auf:",
        "Lokalisation PE:",
        "Tumorprobe:",
        "Art der Tumorprobe :",
        "Art der Tumorprobe:",
        "Molekulares Profil & prädiktive Marker",
    ],
    "Evidenzgraduierung der ZPM für die MTB": [],
    "Zusatzverweise:": [],
}

RENAME = {
    "Art der Tumorprobe :": "Art der Tumorprobe:",
    "Pathologisches Institut:": "Pathologie Inst.:",
    "Name, Vorn., GebDat.:": "Name, Vorn., GebDatum:",
    "Name, Vorn., GebDat.": "Name, Vorn., GebDatum:",
}


def parse(txt, debug=False):
    sections = []

    allowed_sections = SECTIONS.keys()
    allowed_fields = []
    section = defaultdict(str)
    section["_name"] = "header"
    current_field = "_text"

    for line in txt.split("\n"):
        line = line.strip()

        if current_field == "_text" and len(line) == 0:
            # skip blank lines in between section header and start of first field
            continue
        elif line in allowed_sections:
            if debug:
                print("=" * 20, line, "=" * 20)

            # Persist completed section
            # Cast defaultdict to dict
            sections.append(dict(section))

            # Start new section
            section = defaultdict(str)
            section["_name"] = line
            current_field = "_text"
            allowed_fields = SECTIONS[line]
        elif line in allowed_fields:
            if debug:
                print("-" * 10, line)
            current_field = RENAME.get(line, line)
        else:
            if debug:
                print(line)
            section[current_field] += line + "\n"

        if (
            len(sections) == 0
            and section["_name"] == "header"
            and len(section["_text"]) > 200
        ):
            # for a small fraction of documents the docx --> ASCII conversion is broken (there are too few newlines)
            # when we find that the header grows larger than a typical header, we skip parsing altogether
            return []

    sections.append(dict(section))

    for section in sections:
        if (
            section["_name"] == "Molekularpathologische Analyse"
            and "Molekulares Profil & prädiktive Marker" in section
        ):
            markers = section.pop("Molekulares Profil & prädiktive Marker")
            try:

                markers = parse_markers(
                    "Molekulares Profil & prädiktive Marker\n" + markers
                )
                section["marker"] = markers
            except ValueError:
                section["marker"] = []

    return sections


def parse_markers(s):
    """
    Tables such as molecular genetic analysis. Values are separated by newlines. Rows are separated by two consecutive newlines. Column headers come first, separated from first row by three newlines. An empty line within one row indicates a missing value and is parsed as such.

    Caveat: when there are newlines within values/cells this results will be misaligned.

    Example
    -------
        c1
        c2
        c3
        c4

        v1
        [missing]
        v3
        v4

        v5
        ...
    """
    s = s.strip()

    # Table format seems to be inconsistent (2-3 newlines in between header and first row).
    header_sep = "\n\n\n" if "\n\n\n" in s else "\n\n"
    columns = s[: s.index(header_sep)].strip().split("\n")
    data = s[s.index(header_sep) + len(header_sep) :].split("\n")
    rows = []
    row = {}
    i = 0
    for line in data:
        if i < len(columns):
            row[columns[i]] = line
            i += 1
        else:
            i = 0
            rows.append(row)
            row = {}
    if len(row) > 0:
        for c in columns:
            if c not in row:
                row[c] = ""
        rows.append(row)
    return rows
