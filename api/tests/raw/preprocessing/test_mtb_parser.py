from pprint import pprint

from raw.preprocessing.mtb_parser import parse_markers


def test_parse_markers():
    s = "Molekulares Profil & prädiktive Marker\nAngewandte Methode\nAlteration\nBiologische Bewertung\n\n\nNGS-extern\nG13D\npathogenic"
    result = parse_markers(s)
    assert result == [
        {
            "Alteration": "G13D",
            "Angewandte Methode": "NGS-extern",
            "Biologische Bewertung": "pathogenic",
            "Molekulares Profil & prädiktive Marker": "",
        },
    ]

    s = "Molekulares Profil & prädiktive Marker\nAngewandte Methode\nAlteration\nBiologische Bewertung\n\nKRAS\nNGS-extern\nG13D\npathogenic\n\nMET\nNGS-extern\nExon 14, Skipping\n\n\nCTNNB1\nNGS-extern\np.D32Y\n\n\nESR1\nNGS-extern\np.Y537N\n\n\nMS-Status\n\n\nstabil"
    result = parse_markers(s)
    pprint(result)
    assert result == [
        {
            "Alteration": "G13D",
            "Angewandte Methode": "NGS-extern",
            "Biologische Bewertung": "pathogenic",
            "Molekulares Profil & prädiktive Marker": "KRAS",
        },
        {
            "Alteration": "Exon 14, Skipping",
            "Angewandte Methode": "NGS-extern",
            "Biologische Bewertung": "",
            "Molekulares Profil & prädiktive Marker": "MET",
        },
        {
            "Alteration": "p.D32Y",
            "Angewandte Methode": "NGS-extern",
            "Biologische Bewertung": "",
            "Molekulares Profil & prädiktive Marker": "CTNNB1",
        },
        {
            "Alteration": "p.Y537N",
            "Angewandte Methode": "NGS-extern",
            "Biologische Bewertung": "",
            "Molekulares Profil & prädiktive Marker": "ESR1",
        },
        {
            "Alteration": "",
            "Angewandte Methode": "",
            "Biologische Bewertung": "stabil",
            "Molekulares Profil & prädiktive Marker": "MS-Status",
        },
    ]
