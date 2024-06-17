import requests
import json
import pandas as pd
import datetime

sitios = {"Álava": ['9073X', '1060X', '1044X', '9178X', '9091O', '9122I', '9060X', '9145X', '9087', '9091R'],
          "Albacete": ["8178D", "8175",'8198Y', "8177A", "7096B", '4096Y','7067Y','4007Y','7103Y','4091Y','7072Y','7066Y'],
          "Alicante": ['8025', '8059C', '8019', '8036Y', '7247X', '8018X', '8050X', '8013X', '7244X', '8057C', '7261X', '8008Y'],
          "Almería": ['6302A', '6277B', '6381', '6364X', '6297', '6325O', '6329X', '6332X', '6332Y', '6291B', '6340X', '6367B', '6307C', '6307X', '6335O', '6293X', '6312E', '5060X'],
          "Asturias": ['1226X', '1186P', '1212E', '1283U', '1210X', '1179B', '1331A', '1203D', '1302F', '1208', '1207U', '1208H', '1208A', '1309C', '1223P', '1183X', '1234P', '1249I', '1249X', '1221D', '1199X', '1276F', '1542', '1279X', '1178R', '1341B', '1272B', '1327A'],
          "Ávila": ['2456B', '2828Y', '3422D', '3337U', '2453E', '2430Y', '2811A', '3319D', '2512Y', '3391', '2444', '2444C'],
          "Badajoz": ['4464X', '4489X', '4436Y', '5473X', '4478X', '4452', '4492F', '4325Y', '4358X', '4520X', '4501X', '4244X', '4511C', '4386B', '4499X', '4410X', '4340', '4486X', '4260', '4468X', '4362X', '4395X', '4497X', '4427X'],
          "Baleares": ['B103B', 'B526X', 'B603X', 'B087X', 'B662X', 'B398A', 'B158X', 'B362X', 'B373X', 'B569X', 'B860X', 'B870C', 'B957', 'B825B', 'B013X', 'B684A', 'B986', 'B954', 'B800X', 'B334X', 'B301', 'B614E', 'B893', 'B605X', 'B278', 'B228', 'B236C', 'B640X', 'B760X', 'B346X', 'B780X', 'B434X', 'B691Y', 'B925', 'B908X', 'B656A', 'B410B', 'B248', 'B644B', 'B496X', 'B051A'],
          "Barcelona": ['0252D', '0106X', '0201D', '0076', '0200E', '0201X', '0092X', '0222X', '0194D', '0260X', '0171X', '0149X', '0149D', '0120X', '0158X', '0158O', '0061X', '0114X', '0229I', '0349', '0255B', '0073X', '0341X', '0341', '0066X', '0244X'],
          "Vizcaya": ['1069Y', '1074C', '1078C', '1082', '1056K', '1078I', '1055B', '1057B', '1064L', '1059X', '1083B'],
          "Burgos": ['2117D', '9111', '9031C', '2331', '2106B', '9051', '9069C', '2302N', '2298', '2290Y', '9012E', '9027X', '2285B', '2311Y'],
          "Cáceres": ['4411C', '3562X', '3565X', '4339X', '3475X', '3526X', '3469A', '3469', '3436D', '4245X', '3503', '3504X', '3536X', '3455X', '3423I', '3512X', '3434X', '3386A', '3494U', '3516X', '3519X', '4236Y', '3448X', '3514B', '3531X', '3463X', '3463Y', '3576X', '3547X', '3540X', '4347X'],
          "Cádiz": ['5996B', '5906X', '5973', '5941X', '5911A', '5960', '6042I', '5983X', '5919X', '5910', '5972X', '5950X', '6056X', '6001', '5995B'],
          "Cantabria": ['9001S', '1096X', '1167B', '1083L', '1174I', '1167J', '1135C', '1167G', '1089U', '9001D', '1152C', '1103X', '1159', '1111', '1111X', '1109', '1109X', '1110', '1740', '1154H', '1176A', '9016X', '9019B', '1124E'],
          "Castellón": ['8492X', '9563X', '8500A', '8501', '8520X', '8472A', '9562X', '8439X', '8503Y', '8489X', '8523X'],
          "Ceuta" : ['5000C', '5000A'],
          "Ciudad Real": ['4210Y', '4064Y', '4195E', '4300Y', '4116I', '4121', '4121C', '4193Y', '5341C', '4220X', '5304Y', '4103X', '4147X', '4138Y', '4148'],
          "Córdoba": ['5624X', '5598X', '5346X', '5402', '5394X', '5429X', '5427X', '5459X', '5470', '4267X', '5625X', '5361X', '5412X', '4263X', '5390Y'],
          "A Coruña": ['1387', '1387E', '1387D', '1363X', '1442U', '1393', '1390X', '1351', '1354C', '1400', '1406X', '1437O', '1435C', '1473A', '1476R', '1475X', '1428', '1410X', '1399'],
          "Cuenca": ['4070Y', '4089A', '4051Y', '4095Y', '3040Y', '3044X', '8096', '8245Y', '8155Y', '4093Y', '8084Y', '8210Y', '4090Y', '3094B', '4075Y'],
          "Girona": ['0281Y', '0433D', '0321', '0284X', '0411X', '0421X', '0421E', '0429X', '0370E', '0367', '0370B', '0385X', '0294B', '9585', '0394X', '0360X', '0413A', '0320I', '0372C', '0324A', '0363X', '0312X'],
          "Granada": ['5047E', '5103E', '5103F', '6272X', '6248D', '5107D', '5530E', '5514', '5514Z', '5515X', '5051X', '6299I', '6258X', '5582A', '6268X', '6268Y', '5511', '6267X', '5516D', '6281X', '5515D'],
          "Guadalajara": ['3209Y', '9377Y', '3168D', '3168C', '3168A', '3140Y', '3013', '3103', '3085Y', '3130C', '3021Y'],
          "Guipuzcoa": ['1048X', '1038X', '1025X', '1014A', '1024E', '1049N', '1050J', '1021X', '1014', '1012P', '1037X', '1052A', '1026X', '1025A', '1041A', '1037Y'],
          "Huelva": ['4560Y', '5858X', '4589X', '4527X', '4549Y', '5769X', '4554X', '4608X', '4584X', '4541X', '4605', '4642E', '5860E', '4575X', '4622X'],
          "Huesca": ['9491X', '9208E', '9195C', '9808X', '9211F', '9911X', '9866C', '9756X', '9838B', '9784P', '9453X', '9198X', '9855E', '9839V', '9445L', '9924X', '9901X', '9898', '9201K', '9201X', '9908X', '9451F', '9812M', '9460X', '9894Y', '9843A', '9751', '9918Y', '9814A', '9814X', '9814I', '9207'],
          "Jaén": ['5406X', '5298X', '5181D', '5164B', '5281X', '5038X', '5038Y', '5270B', '5270', '5279X', '5246', '5165X', '5210X', '5192'],
          "León": ['2734D', '2701D', '2742R', '2626Y', '2737E', '2661B', '2661', '1549', '1178Y', '2630X', '2728B', '2624C', '2664B', '1561I', '1541B'],
          "Lleida": ['9650X', '9994X', '9590D', '9988B', '9638D', '9775X', '9776D', '9657X', '9772X', '9619', '9771C', '9771', '9707', '9590', '9729X', '9990X', '9724X', '9677', '9660', '9698U', '9718X', '9689X', '9647X', '9632X', '9720X', '9744B'],
          "Lugo": ['1521X', '1347T', '1297E', '1658', '1518A', '1505', '1344X', '1679A', '1446X', '1521I', '1342X'],
          "Madrid": ['3170Y', '3268C', '3100B', '3182Y', '3110C', '3191E', '3200', '3129', '3194U', '3196', '3126Y', '3195', '3194Y', '3266A', '2462', '3104Y', '3338', '3330Y', '3125Y', '3111D', '3229Y', '3175', '3343Y'],
          "Málaga": ['6201X', '6045X', '6106X', '6100B', '6069X', '6040X', '6143X', '6058I', '6084X', '6375X', '6050X', '6057X', '6083X', '6076X', '6172X', '6155A', '6156X', '6172O', '6213X', '6175X', '6032B', '6032X', '6088X', '6205X', '6199X', '6127X'],
          "Murcia": ['7250C', '7228', '7227X', '7158X', '7127X', '7121A', '7119B', '7195X', '7012C', '7012D', '7019X', '7145D', '7023X', '7138B', '7209', '7203A', '7007Y', '7237E', '7080X', '7172X', '7178I', '7020C', '7211B', '7031', '7031X', '7026X', '7218Y', '7275C', '7002Y'],
          "Melilla": ['6000A'],
          "Navarra": ['9263X', '1033X', '1021Y', '9294E', '1002Y', '1010X', '9283X', '9245X', '9257X', '9274X', '9218A', '9280B', '9171K', '9262P', '9301X', '9238X', '9252X', '9228J', '9262', '9263D', '9228T', '9302Y', '9995Y', '', '9263X', '1033X', '1021Y', '9294E', '1002Y', '1010X', '9283X', '9245X', '9257X', '9274X', '9218A', '9280B', '9171K', '9262P', '9301X', '9238X', '9252X', '9228J', '9262', '9263D', '9228T', '9302Y', '9995Y'],
          "Ourense": ['2969U', '1631E', '1706A', '1696O', '1639X', '1738U', '1583X', '1700X', '1690A', '1690B', '1701X', '2978X', '1735X'],
          "Palencia": ['2243A', '2400E', '2374X', '2235U', '2401X', '2401', '2568D', '2362C', '2276B'],
          "Las Palmas": ['C619X', 'C668V', 'C648C', 'C248E', 'C669B', 'C249I', 'C649I', 'C038N', 'C619I', 'C619Y', 'C628B', 'C839X', 'C258K', 'C029O', 'C658L', 'C659M', 'C659H', 'C658X', 'C689E', 'C639M', 'C629X', 'C629Q', 'C229J', 'C623I', 'C639U', 'C635B', 'C625O', 'C839I', 'C614H', 'C612F', 'C648N', 'C649R', 'C656V', 'C048W', 'C239N', 'C018J', 'C665T', 'C611E', 'C019V'],
          "Pontevedra": ['1719', '1468X', '1489A', '1486E', '1465U', '1730E', '1723X', '1484C', '1484', '1455I', '1466A', '1496X', '1495', '1477U', '1477V'],
          "La Rioja": ['9293X', '9136X', '9145Y', '9188', '9121X', '9170', '9141V', '9115X'],
          "Salamanca": ['2873X', '2926B', '2914C', '2945A', '2918Y', '2491C', '2930Y', '2863C', '2847X', '2946X', '2870', '2867', '2891A', '2916A'],
          "Santa Cruz de Tenerife": ['C419X', 'C317B', 'C449F', 'C428T', 'C316I', 'C438N', 'C428U', 'C418I', 'C426R', 'C456E', 'C426E', 'C436I', 'C468O', 'C415A', 'C457E', 'C456R', 'C456P', 'C458U', 'C467I', 'C417J', 'C418L', 'C426I', 'C437E', 'C455M', 'C453I', 'C412N', 'C423R', 'C466O', 'C448C', 'C422A', 'C436L', 'C449Q', 'C468I', 'C126A', 'C916Q', 'C917E', 'C939T', 'C129V', 'C439J', 'C328W', 'C929I', 'C430E', 'C329B', 'C406G', 'C139E', 'C457I', 'C419L', 'C459Z', 'C117A', 'C101A', 'C148F', 'C925F', 'C446G', 'C468X', 'C329Z', 'C449C', 'C919K', 'C458A', 'C129Z', 'C447A', 'C429I', 'C117Z', 'C314Z', 'C319W', 'C928I'],
          "Segovia": ['2140A', '2192C', '2135A', '2150H', '2482B', '2182C', '2471Y', '2465', '2465A'],
          "Sevilla": ['5733X', '5702X', '5835X', '5704B', '5656', '5726X', '5654X', '5612B', '5891X', '5612X', '5796', '5998X', '5783', '5790Y', '5788X', '5641X', '', '5733X', '5702X', '5835X', '5704B', '5656', '5726X', '5654X', '5612B', '5891X', '5612X', '5796', '5998X', '5783', '5790Y', '5788X', '5641X'],
          "Soria": ['9352A', '9344C', '2092', '2017Y', '2059B', '2096B', '2044B', '2048A', '9287A', '2030', '2084Y', '2005Y', '2296A'],
          "Tarragona": ['0009X', '9961X', '9981A', '9946X', '9947X', '9726E', '9975X', '0016B', '0016A', '9987P', '0042Y', '0034X', '0002I'],
          "Teruel": ['8354X', '9573X', '9550C', '9998X', '9381I', '9381', '9569A', '9561X', '8458X', '9436X', '9546B', '8376', '9531Y', '8486X', '9513X', '9374X', '8368U', '9935X'],
          "Toledo": ['3362Y', '4067', '3254Y', '3305Y', '3099Y', '3427Y', '4061X', '3298X', '3365A', '3245Y', '3260B', '3259'],
          "Valencia": ['8381X', '8072Y', '8270X', '8300X', '8395X', '8005X', '8193E', '8409X', '8058Y', '8058X', '8283X', '8325X', '8446Y', '8337X', '8309X', '8414A', '8416X', '8416', '8416Y', '8293X', '8203O'],
          "Valladolid": ['2517A', '2604B', '2503X', '2503B', '2166Y', '2507Y', '2172Y', '2422', '2539', '2593D'],
          "Zamora": ['2966D', '2755X', '2565', '2885K', '2555B', '2536D', '2882D', '2789H', '2766E', '2777K', '2804F', '2611D', '2775X', '2614'],
          "Zaragoza": ['9354X', '9576C', '9394X', '9574B', '9336D', '9390', '9321X', '9427X', '9495Y', '9510X', '9244X', '9299X', '9501X', '9434', '9434P']}


def clima(lugar, fecha_inicial, fecha_final, api_key):
          '''
          lugar = Provincia de España, con la primera letra en mayúscula. Para obtener un listado: list(climaemet.sitios.keys())
          fecha_inicial = Fecha de inicio del histórico con el siguiente formato: "2024-06-01T12:10:00UTC"
          fecha_final = Fecha de fin del histórico, con el mismo formato
          api_key = Api key de AEMET (https://opendata.aemet.es/centrodedescargas/altaUsuario?)
          '''
    estaciones = sitios.get(lugar)
    if not estaciones:
        print(f"No se encontraron estaciones para el lugar especificado: {lugar}")
        return

    for estacion in estaciones:
        url = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fecha_inicial}/fechafin/{fecha_final}/estacion/{estacion}/?api_key={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            datos_url = data.get("datos")

            if datos_url:
                datos_response = requests.get(datos_url)

                if datos_response.status_code == 200:
                    data = datos_response.json()
                    df = pd.DataFrame(data)
                    nombre_estacion = df.iloc[0]["nombre"]
                    csv_file = f'{nombre_estacion}.csv'
                    df.to_csv(csv_file, index=False)
                else:
                    print(f'Error al obtener los datos climáticos para la estación {estacion}: {datos_response.status_code}')
            else:
                print(f'No se encontraron datos para la estación {estacion}')
        else:
            print(f'Error al obtener los datos climáticos para la estación {estacion}: {response.status_code}')
