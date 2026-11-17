#!/usr/bin/env python3
"""Pilot-line participant sites (public CORDIS fact sheets, legal seats) -> tools/data/pl_sites_src.json
Roles: C = coordinator, P = participant, T = third party linked to a participant (as marked on CORDIS).
Only organisation names and cities (public project data); no personal data. Re-run after editing the lists below."""
import json, pathlib

READ = '2026-11-17'
SRC = 'CORDIS project fact sheets (participants, legal seats)'

# city|a2 -> [lat, lon]
GAZ = {
 'Paris|FR':[48.857,2.352],'Leuven|BE':[50.879,4.701],'München|DE':[48.137,11.575],'Espoo|FI':[60.205,24.656],
 'Warszawa|PL':[52.230,21.012],'Cork|IE':[51.898,-8.473],'Graz|AT':[47.071,15.439],'Louvain-la-Neuve|BE':[50.669,4.615],
 'Grenoble|FR':[45.188,5.725],'Granada|ES':[37.177,-3.599],'Bucureşti|RO':[44.427,26.103],'Berlin|DE':[52.520,13.405],
 'Frankfurt (Oder)|DE':[52.347,14.551],'Irakleio|GR':[35.339,25.144],'Madrid|ES':[40.417,-3.704],'Braga|PT':[41.551,-8.428],
 'Roma|IT':[41.902,12.496],'Trento|IT':[46.070,11.121],'Bologna|IT':[44.494,11.343],'Catania|IT':[37.507,15.083],
 'Padova|IT':[45.407,11.876],'Pisa|IT':[43.716,10.397],'Torino|IT':[45.070,7.687],'Milano|IT':[45.464,9.190],
 'Modena|IT':[44.647,10.925],'Arcavacata di Rende|IT':[39.357,16.226],'Pavia|IT':[45.185,9.158],'Stockholm|SE':[59.329,18.069],
 'Linköping|SE':[58.411,15.622],'Lund|SE':[55.705,13.191],'Göteborg|SE':[57.709,11.975],'Tampere|FI':[61.498,23.761],
 'Castelldefels|ES':[41.280,1.977],'Eindhoven|NL':[51.441,5.470],'Valencia|ES':[39.470,-0.377],'Den Haag|NL':[52.080,4.311],
 'Enschede|NL':[52.221,6.894],'Gent|BE':[51.054,3.725],'Vigo|ES':[42.240,-8.721],'Aveiro|PT':[40.641,-8.654],
 'Cambridge|UK':[52.205,0.119],'Southampton|UK':[50.910,-1.404],'Leganés|ES':[40.328,-3.764],'Villach|AT':[46.614,13.846],
 'Neubiberg|DE':[48.077,11.661],'Dresden|DE':[51.050,13.738],'Innsbruck|AT':[47.269,11.404],'Mainz|DE':[49.993,8.247],
 'Erlenbach am Main|DE':[49.804,9.165],'Siegen|DE':[50.874,8.024],'Hannover|DE':[52.376,9.732],'Braunschweig|DE':[52.269,10.521],
 'Olomouc|CZ':[49.594,17.251],'Brno|CZ':[49.195,16.608],'Praha|CZ':[50.076,14.438],'Delft|NL':[52.012,4.357],
 'Garching|DE':[48.249,11.651],'Jena|DE':[50.927,11.586],'Napoli|IT':[40.852,14.268],'Barcelona|ES':[41.387,2.170],
 'Cerdanyola del Vallès|ES':[41.491,2.141],'Aachen|DE':[50.776,6.084],'Jülich|DE':[50.922,6.361],'Jyväskylä|FI':[62.242,25.747],
 'Donostia|ES':[43.318,-1.981],'Regensburg|DE':[49.013,12.102],'Lisboa|PT':[38.722,-9.139],'Meudon|FR':[48.812,2.238],
 'Boulogne-Billancourt|FR':[48.835,2.240],'Marolles-en-Hurepoix|FR':[48.562,2.299],'Getafe|ES':[40.306,-3.733],
 'San Cristóbal de La Laguna|ES':[28.487,-16.316],'Murcia|ES':[37.992,-1.131],'Stuttgart|DE':[48.776,9.182],
 'Ummendorf|DE':[48.057,9.835],'Wattens|AT':[47.294,11.591],'Kongens Lyngby|DK':[55.771,12.504],'Wrocław|PL':[51.108,17.038],
 'Hasselt|BE':[50.931,5.338],'Jerusalem|IL':[31.769,35.216],'Rehovot|IL':[31.895,34.808],'Binyamina|IL':[32.518,34.949],
 'Ljubljana|SI':[46.056,14.506],'Wien|AT':[48.208,16.372],'Corbeil-Essonnes|FR':[48.614,2.482],'Toulouse|FR':[43.605,1.444],
 'Trondheim|NO':[63.430,10.395],'Frederiksberg|DK':[55.679,12.531],'Massy|FR':[48.731,2.271],'Palaiseau|FR':[48.715,2.246],
 'Strasbourg|FR':[48.573,7.752],'Lainate|IT':[45.571,9.027],'Rimbo|SE':[59.744,18.364],'Odense|DK':[55.396,10.389],
 'Villeneuve-d’Ascq|FR':[50.623,3.145],'Mons|BE':[50.454,3.952],
}

L = {}
def line(pid, cordis, acronym, parts):
    L[pid] = {'cordis': cordis, 'acronym': acronym, 'parts': [{'n': n, 'city': c, 'a2': a, 'role': r} for n, c, a, r in parts]}

line('apecs', '101183307', 'APECS', [
 ('Fraunhofer-Gesellschaft (HQ)', 'München', 'DE', 'C'), ('Ferdinand-Braun-Institut (FBH)', 'Berlin', 'DE', 'P'),
 ('IHP – Leibniz Institute for High Performance Microelectronics', 'Frankfurt (Oder)', 'DE', 'P'), ('TU Graz', 'Graz', 'AT', 'P'),
 ('VTT', 'Espoo', 'FI', 'P'), ('imec', 'Leuven', 'BE', 'P'), ('CEA (HQ)', 'Paris', 'FR', 'P'), ('FORTH', 'Irakleio', 'GR', 'P'),
 ('CSIC (HQ)', 'Madrid', 'ES', 'P'), ('INL – International Iberian Nanotechnology Laboratory', 'Braga', 'PT', 'P')])

line('fames', '101182279', 'FAMES', [
 ('CEA (HQ)', 'Paris', 'FR', 'C'), ('imec', 'Leuven', 'BE', 'P'), ('Fraunhofer-Gesellschaft (HQ)', 'München', 'DE', 'P'),
 ('VTT', 'Espoo', 'FI', 'P'), ('Warsaw University of Technology (CEZAMAT)', 'Warszawa', 'PL', 'P'), ('University College Cork (Tyndall)', 'Cork', 'IE', 'P'),
 ('Silicon Austria Labs', 'Graz', 'AT', 'P'), ('UCLouvain', 'Louvain-la-Neuve', 'BE', 'P'), ('Grenoble INP', 'Grenoble', 'FR', 'P'),
 ('SiNANO Institute', 'Grenoble', 'FR', 'P'), ('Universidad de Granada', 'Granada', 'ES', 'P')])

line('nanoic', '101183277', 'NanoIC', [
 ('imec', 'Leuven', 'BE', 'C'), ('CEA (HQ)', 'Paris', 'FR', 'P'), ('Fraunhofer-Gesellschaft (HQ)', 'München', 'DE', 'P'),
 ('University College Cork (Tyndall)', 'Cork', 'IE', 'P'), ('POLITEHNICA Bucureşti (CSSNT)', 'Bucureşti', 'RO', 'P'), ('VTT', 'Espoo', 'FI', 'P')])

line('wbg', '101183211', 'WBG', [
 ('CNR (HQ)', 'Roma', 'IT', 'C'), ('Fondazione Bruno Kessler', 'Trento', 'IT', 'P'), ('CINI', 'Bologna', 'IT', 'T'),
 ('Università di Catania', 'Catania', 'IT', 'T'), ('Università di Padova', 'Padova', 'IT', 'T'), ('Università di Pisa', 'Pisa', 'IT', 'T'),
 ('Politecnico di Torino', 'Torino', 'IT', 'T'), ('Politecnico di Milano', 'Milano', 'IT', 'T'), ('Università di Bologna', 'Bologna', 'IT', 'T'),
 ('Università di Modena e Reggio Emilia', 'Modena', 'IT', 'T'), ('Università della Calabria', 'Arcavacata di Rende', 'IT', 'P'),
 ('CIDIS – Centro Italiano Design Circuiti Integrati', 'Pavia', 'IT', 'P'), ('KTH', 'Stockholm', 'SE', 'P'), ('Linköping University', 'Linköping', 'SE', 'P'),
 ('Lund University', 'Lund', 'SE', 'P'), ('Chalmers', 'Göteborg', 'SE', 'P'), ('Łukasiewicz – IMiF', 'Warszawa', 'PL', 'P'),
 ('Institute of High Pressure Physics PAS (Unipress)', 'Warszawa', 'PL', 'P'), ('Tampere University', 'Tampere', 'FI', 'P'),
 ('Silicon Austria Labs', 'Graz', 'AT', 'P'), ('CEA (HQ)', 'Paris', 'FR', 'P'), ('Fraunhofer-Gesellschaft (HQ)', 'München', 'DE', 'P'),
 ('Chip4Power consortium', 'Catania', 'IT', 'P')])

line('pixeurope', '101213727', 'PIXEurope', [
 ('ICFO', 'Castelldefels', 'ES', 'C'), ('University College Cork (Tyndall)', 'Cork', 'IE', 'P'), ('TU Eindhoven', 'Eindhoven', 'NL', 'P'),
 ('Universitat Politècnica de València', 'Valencia', 'ES', 'P'), ('VTT', 'Espoo', 'FI', 'P'), ('imec', 'Leuven', 'BE', 'P'),
 ('CSIC (HQ)', 'Madrid', 'ES', 'P'), ('TNO', 'Den Haag', 'NL', 'P'), ('University of Twente', 'Enschede', 'NL', 'P'), ('Ghent University', 'Gent', 'BE', 'P'),
 ('Universidad de Vigo', 'Vigo', 'ES', 'P'), ('Instituto de Telecomunicações', 'Aveiro', 'PT', 'P'), ('Warsaw University of Technology (CEZAMAT)', 'Warszawa', 'PL', 'P'),
 ('Silicon Austria Labs', 'Graz', 'AT', 'P'), ('Politecnico di Milano', 'Milano', 'IT', 'P'), ('CEA (HQ)', 'Paris', 'FR', 'P'),
 ('Fondazione Bruno Kessler', 'Trento', 'IT', 'P'), ('University of Cambridge', 'Cambridge', 'UK', 'P'), ('University of Southampton', 'Southampton', 'UK', 'P'),
 ('IMDEA Networks', 'Leganés', 'ES', 'P')])

line('champ-ion', '101288915', 'CHAMP-ION SGA1', [
 ('Silicon Austria Labs', 'Graz', 'AT', 'C'), ('Infineon Technologies Austria', 'Villach', 'AT', 'P'), ('Infineon Technologies AG', 'Neubiberg', 'DE', 'P'),
 ('Infineon Technologies Dresden', 'Dresden', 'DE', 'P'), ('Alpine Quantum Technologies', 'Innsbruck', 'AT', 'P'), ('Universität Innsbruck', 'Innsbruck', 'AT', 'P'),
 ('ParityQC', 'Innsbruck', 'AT', 'P'), ('INL – International Iberian Nanotechnology Laboratory', 'Braga', 'PT', 'P'), ('VTT', 'Espoo', 'FI', 'P'),
 ('Johannes Gutenberg-Universität Mainz', 'Mainz', 'DE', 'P'), ('neQxt', 'Erlenbach am Main', 'DE', 'P'), ('Universität Siegen', 'Siegen', 'DE', 'P'),
 ('eleQtron', 'Siegen', 'DE', 'P'), ('Leibniz Universität Hannover', 'Hannover', 'DE', 'P'), ('QUDORA Technologies', 'Braunschweig', 'DE', 'P'),
 ('PTB', 'Braunschweig', 'DE', 'P'), ('INRiM', 'Torino', 'IT', 'P'), ('Università di Padova', 'Padova', 'IT', 'P'),
 ('Palacký University Olomouc', 'Olomouc', 'CZ', 'P'), ('Institute of Scientific Instruments CAS', 'Brno', 'CZ', 'P'), ('AMIRES', 'Praha', 'CZ', 'P')])

line('supreme', '101286304', 'SUPREME 1', [
 ('VTT', 'Espoo', 'FI', 'C'), ('IQM Finland', 'Espoo', 'FI', 'P'), ('Arctic Instruments', 'Espoo', 'FI', 'P'), ('QuantWare', 'Delft', 'NL', 'P'),
 ('Single Quantum', 'Delft', 'NL', 'P'), ('TNO', 'Den Haag', 'NL', 'P'), ('QphoX', 'Delft', 'NL', 'P'), ('TU Delft', 'Delft', 'NL', 'P'),
 ('Bayerische Akademie der Wissenschaften (WMI)', 'München', 'DE', 'P'), ('Fraunhofer-Gesellschaft (HQ)', 'München', 'DE', 'P'),
 ('Infineon Technologies AG', 'Neubiberg', 'DE', 'P'), ('Peak Quantum', 'Garching', 'DE', 'P'), ('Max-Planck-Gesellschaft (HQ)', 'München', 'DE', 'P'),
 ('Leibniz IPHT', 'Jena', 'DE', 'P'), ('CEA (HQ)', 'Paris', 'FR', 'P'), ('Silent Waves', 'Grenoble', 'FR', 'P'), ('Alice & Bob', 'Paris', 'FR', 'P'),
 ('AMIRES', 'Praha', 'CZ', 'P'), ('Università di Napoli Federico II', 'Napoli', 'IT', 'P'), ('Fondazione Bruno Kessler', 'Trento', 'IT', 'P'),
 ('Qilimanjaro Quantum Tech', 'Barcelona', 'ES', 'P'), ('IFAE', 'Cerdanyola del Vallès', 'ES', 'P'), ('Silicon Austria Labs', 'Graz', 'AT', 'P')])

line('spins', '101288553', 'SPINS SGA1', [
 ('imec', 'Leuven', 'BE', 'C'), ('AMIRES', 'Praha', 'CZ', 'P'), ('ARQUE Systems', 'Aachen', 'DE', 'P'), ('CEA (HQ)', 'Paris', 'FR', 'P'),
 ('C12 Quantum Electronics', 'Paris', 'FR', 'P'), ('CSIC (HQ)', 'Madrid', 'ES', 'P'), ('Fraunhofer-Gesellschaft (HQ)', 'München', 'DE', 'P'),
 ('Forschungszentrum Jülich', 'Jülich', 'DE', 'P'), ('Groove Quantum', 'Delft', 'NL', 'P'), ('IHP – Leibniz Institute for High Performance Microelectronics', 'Frankfurt (Oder)', 'DE', 'P'),
 ('Infineon Technologies Dresden', 'Dresden', 'DE', 'P'), ('INL – International Iberian Nanotechnology Laboratory', 'Braga', 'PT', 'P'),
 ('University of Jyväskylä', 'Jyväskylä', 'FI', 'P'), ('Cuantomoción', 'Donostia', 'ES', 'P'), ('Quobly', 'Grenoble', 'FR', 'P'),
 ('SemiQon', 'Espoo', 'FI', 'P'), ('Siltronic', 'München', 'DE', 'P'), ('TNO', 'Den Haag', 'NL', 'P'), ('TU Delft', 'Delft', 'NL', 'P'),
 ('NQSTI', 'Roma', 'IT', 'P'), ('PQI – Portuguese Quantum Institute', 'Lisboa', 'PT', 'P'), ('Universität Regensburg', 'Regensburg', 'DE', 'P'),
 ('VTT', 'Espoo', 'FI', 'P')])

line('direqt', '101291215', 'DIREQT', [
 ('CNR (HQ)', 'Roma', 'IT', 'C'), ('Università di Torino', 'Torino', 'IT', 'P'), ('INRiM', 'Torino', 'IT', 'P'), ('Fondazione Bruno Kessler', 'Trento', 'IT', 'P'),
 ('Thales', 'Meudon', 'FR', 'P'), ('HiQuTe Diamond', 'Boulogne-Billancourt', 'FR', 'P'), ('Diamfab', 'Grenoble', 'FR', 'P'), ('Bestek', 'Marolles-en-Hurepoix', 'FR', 'P'),
 ('CNRS (HQ)', 'Paris', 'FR', 'P'), ('Tecnalia', 'Donostia', 'ES', 'P'), ('Universidad Carlos III de Madrid', 'Getafe', 'ES', 'P'), ('IMDEA Nanociencia', 'Madrid', 'ES', 'P'),
 ('Arquimea Research Center', 'San Cristóbal de La Laguna', 'ES', 'P'), ('Universidad de Murcia', 'Murcia', 'ES', 'P'), ('Quantum Brilliance', 'Stuttgart', 'DE', 'P'),
 ('Fraunhofer-Gesellschaft (HQ)', 'München', 'DE', 'P'), ('Diatope', 'Ummendorf', 'DE', 'P'), ('Silicon Austria Labs', 'Graz', 'AT', 'P'), ('D. Swarovski', 'Wattens', 'AT', 'P'),
 ('PQI – Portuguese Quantum Institute', 'Lisboa', 'PT', 'P'), ('INL – International Iberian Nanotechnology Laboratory', 'Braga', 'PT', 'P'), ('DTU', 'Kongens Lyngby', 'DK', 'P'),
 ('Wrocław University of Science and Technology', 'Wrocław', 'PL', 'P'), ('Hasselt University', 'Hasselt', 'BE', 'P'), ('Czech Technical University in Prague', 'Praha', 'CZ', 'P'),
 ('AMIRES', 'Praha', 'CZ', 'P'), ('Hebrew University of Jerusalem', 'Jerusalem', 'IL', 'P'), ('Weizmann Institute of Science', 'Rehovot', 'IL', 'P'),
 ('Quantum Transistors Technology', 'Binyamina', 'IL', 'P'), ('VTT', 'Espoo', 'FI', 'P'), ('Jožef Stefan Institute', 'Ljubljana', 'SI', 'P')])

line('p4q', '101291189', 'P4Q', [
 ('University of Twente', 'Enschede', 'NL', 'C'), ('AIT Austrian Institute of Technology', 'Wien', 'AT', 'P'), ('Aluvia Photonics', 'Enschede', 'NL', 'P'),
 ('AMIRES', 'Praha', 'CZ', 'P'), ('Alpine Quantum Technologies', 'Innsbruck', 'AT', 'P'), ('CNRS (HQ)', 'Paris', 'FR', 'P'), ('CEA (HQ)', 'Paris', 'FR', 'P'),
 ('Delft Networks', 'Delft', 'NL', 'P'), ('ICFO', 'Castelldefels', 'ES', 'P'), ('imec', 'Leuven', 'BE', 'P'), ('IMS CHIPS', 'Stuttgart', 'DE', 'P'),
 ('Leonardo', 'Roma', 'IT', 'P'), ('Ligentec France', 'Corbeil-Essonnes', 'FR', 'P'), ('LioniX International', 'Enschede', 'NL', 'P'), ('New Origin', 'Enschede', 'NL', 'P'),
 ('planqc', 'Garching', 'DE', 'P'), ('Falqon Systems', 'Delft', 'NL', 'P'), ('QphoX', 'Delft', 'NL', 'P'), ('QuiX Quantum', 'Enschede', 'NL', 'P'),
 ('SINTEF', 'Trondheim', 'NO', 'P'), ('Sparrow Quantum', 'Frederiksberg', 'DK', 'P'), ('Thales Alenia Space France', 'Toulouse', 'FR', 'P'), ('Thales', 'Meudon', 'FR', 'P'),
 ('TNO', 'Den Haag', 'NL', 'P'), ('TU Delft', 'Delft', 'NL', 'P'), ('TU Eindhoven', 'Eindhoven', 'NL', 'P'), ('University College Cork (Tyndall)', 'Cork', 'IE', 'P'),
 ('VTT', 'Espoo', 'FI', 'P'), ('Quandela', 'Massy', 'FR', 'P')])

line('q-planet', '101291743', 'Q-PLANET SGA1', [
 ('Pasqal', 'Palaiseau', 'FR', 'C'), ('Université de Strasbourg', 'Strasbourg', 'FR', 'P'), ('QPerfect', 'Strasbourg', 'FR', 'P'), ('III-V Lab', 'Palaiseau', 'FR', 'P'),
 ('CNRS (HQ)', 'Paris', 'FR', 'P'), ('University of Stuttgart', 'Stuttgart', 'DE', 'P'), ('Fraunhofer-Gesellschaft (HQ)', 'München', 'DE', 'P'), ('DTU', 'Kongens Lyngby', 'DK', 'P'),
 ('INRiM', 'Torino', 'IT', 'P'), ('SAES Getters', 'Lainate', 'IT', 'P'), ('Politecnico di Milano', 'Milano', 'IT', 'P'), ('CSIC (HQ)', 'Madrid', 'ES', 'P'),
 ('ICFO', 'Castelldefels', 'ES', 'P'), ('PQI – Portuguese Quantum Institute', 'Lisboa', 'PT', 'P'), ('Svenska Laserfabriken', 'Rimbo', 'SE', 'P'), ('Welinq', 'Paris', 'FR', 'P'),
 ('University of Warsaw', 'Warszawa', 'PL', 'P'), ('TopGaN', 'Warszawa', 'PL', 'P'), ('Institute of High Pressure Physics PAS (Unipress)', 'Warszawa', 'PL', 'P'),
 ('Qpurpose', 'Odense', 'DK', 'P'), ('Safran Electronics & Defense', 'Paris', 'FR', 'P'), ('Centrale Lille', 'Villeneuve-d’Ascq', 'FR', 'P'), ('ONERA', 'Palaiseau', 'FR', 'P'),
 ('iQrypto', 'Mons', 'BE', 'P'), ('CNR (HQ)', 'Roma', 'IT', 'P'), ('Thales', 'Meudon', 'FR', 'P'), ('VTT', 'Espoo', 'FI', 'P'), ('Silicon Austria Labs', 'Graz', 'AT', 'P')])

# checks
for pid, l in L.items():
    for p in l['parts']:
        k = f"{p['city']}|{p['a2']}"; assert k in GAZ, (pid, k)
        p['lat'], p['lon'] = GAZ[k]
    assert sum(1 for p in l['parts'] if p['role'] == 'C') == 1, pid
out = {'read': READ, 'src': SRC, 'note': 'Legal seats as listed on CORDIS; HQ = organisation headquarters (operating institutes may be elsewhere). T = third party linked to a participant.', 'lines': L}
pathlib.Path('data/pl_sites_src.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print({k: len(v['parts']) for k, v in L.items()}, 'total', sum(len(v['parts']) for v in L.values()))
