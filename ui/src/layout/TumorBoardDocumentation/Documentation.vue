<template>
<<<<<<< Updated upstream
    <div
        class="w-full h-full p-2 p-splitter border-1 border-200 flex flex-column"
    >
        <DocumentationFieldGroup>
            <DocumentationField label="Name" />
            <DocumentationField label="Diagnose" />
            <DocumentationField label="Diagnose nach der Nachbehandlung" />
        </DocumentationFieldGroup>
=======
    <div class="w-full h-full p-2 border-1 border-200 border-round bg-white">
        <DocumentationField label="TUMORKONFERENZPROTOKOLL" />
        <DocumentationField label="MTB 17.08.2023 14:05" />
        <DocumentationField label="Postdiagnostisch" />
        <div style="margin-top: 20px">
            <DocumentationField label="Patient:" />
            <div style="margin-left: 30px">
                <DocumentationField label="Pat-ID:" />
                <DocumentationField label="Name, Vorn., GebDatum:" />
                <DocumentationField label="PLZ, Ort:" />
                <DocumentationField label="Aufenthaltsklinik/ -station:" />
                <DocumentationField label="Klinik, Abt., Arzt, Rufnr.:" />
            </div>
        </div>
        <DocumentationField label="Teilnehmer und Dokumentation:" />
        <div style="margin-left: 30px">
            <DocumentationField
                label="Teilnehmer: Dr. Friedrich Stock, FA, UME, HUMGE"
            />
            <DocumentationField label="Dokumentationskraft:" />
        </div>
        <DocumentationField label="Verlauf:" />
        <DocumentationField label="Metastasen:" />
        <div style="margin-left: 30px">
            <DocumentationField label="Datum Erstdiagnose:" />
            <DocumentationField label="Primärfall:" />
            <DocumentationField label="Tumorstadium:" />
        </div>
        <DocumentationField label="Progress unter LL-Therapie:" />
        <DocumentationField label="Alle LL-Therapien durchlaufen:" />
        <div style="margin-left: 30px">
            <DocumentationField
                label="Anzahl durchlaufener TL (n) und aktuelle L:"
            />
        </div>
        <DocumentationField
            label="Westdeutsches Tumorzentrum Seite 1 von 4 gedruckt am 25.01.2024 13:18 Uhr"
        />
        <DocumentationField label="Morphologie:" />
        <DocumentationField label="Histologie:" />
        <DocumentationField label="Bisheriger Therapieverlauf:" />
        <DocumentationField label="Komorbiditäten:" />
        <DocumentationField label="Fam. Tumorerkrankungen:" />
        <DocumentationField label="Karnofsky-Index/ECOG:" />
        <DocumentationField label="Fragestellung:" />
        <DocumentationField label="Evidenzlage:" />
        <DocumentationField label="Beschluss:" />
        <DocumentationField
            label="Westdeutsches Tumorzentrum Seite 2 von 4 gedruckt am 25.01.2024 13:18 Uhr"
        />
        <DocumentationField label="Administration:" />
        <div style="margin-left: 30px">
            <DocumentationField label="Molekularpathologische Analyse" />
            <div style="margin-left: 30px">
                <DocumentationField label="Befunddatum:" />
                <DocumentationField label="Histo.EinsendeNr.:" />
                <DocumentationField label="Pathologie Inst.:" />
                <DocumentationField label="Analyse basiert auf:" />
                <DocumentationField label="Lokalisation PE:" />
                <DocumentationField label="Tumorprobe:" />
                <DocumentationField label="Art der Tumorprobe:" />
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Molekulares Profil & prädiktive Marker</th>
                        <th>Angewandte Methode</th>
                        <th>Alteration</th>
                        <th>Biologische Bewertung</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(row, index) in rows" :key="index">
                        <td>{{ row }}</td>
                        <td>
                            <DocumentationField
                                v-model="rowValues[index].method"
                                :editable="editable"
                            />
                        </td>
                        <td>
                            <DocumentationField
                                v-model="rowValues[index].alteration"
                                :editable="editable"
                            />
                        </td>
                        <td>
                            <DocumentationField
                                v-model="rowValues[index].rating"
                                :editable="editable"
                            />
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <DocumentationField label="Evidenzgraduierung der ZPM für die MTB" />
        <div style="margin-left: 30px">
            <DocumentationField label="Gleiche Tumorentität" />
            <DocumentationField label="m1A" />
            <DocumentationField label="m1B" />
            <DocumentationField label="m1C" />
        </div>
        <div style="margin-left: 30px">
            <DocumentationField label="Andere Tumorentität" />
            <DocumentationField label="m2A" />
            <DocumentationField label="m2B" />
            <DocumentationField label="m2C" />
        </div>
        <div style="margin-left: 30px">
            <DocumentationField label="In vitro oder Tiermodell" />
            <DocumentationField label="m3" />
        </div>
        <DocumentationField label="Biologische Rationale" />
        <DocumentationField label="m4" />
        <DocumentationField label="Zusatzverweise:" />
        <DocumentationField
            label="Westdeutsches Tumorzentrum Seite 4 von 4 gedruckt am 25.01.2024 13:18 Uhr"
        />
>>>>>>> Stashed changes
    </div>
</template>

<script setup>
import DocumentationField from "@/layout/TumorBoardDocumentation/DocumentationField.vue";
</script>
<script>
export default {
    props: {
        editable: {
            type: Boolean,
            default: true,
        },
    },
    data() {
        return {
            rows: [
                "TP53",
                "FGFR1",
                "ALK",
                "MS-Status",
                "PD-L1",
                "NTRK1-3",
                "HER2/neu",
            ],
            rowValues: [
                { method: "", alteration: "", rating: "" },
                { method: "", alteration: "", rating: "" },
                { method: "", alteration: "", rating: "" },
                { method: "", alteration: "", rating: "" },
                { method: "", alteration: "", rating: "" },
                { method: "", alteration: "", rating: "" },
                { method: "", alteration: "", rating: "" },
            ],
        };
    },
};
</script>
