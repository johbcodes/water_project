# populate_db.py
from app import create_app, db
from app.models import County, Constituency, Ward
import time
from sqlalchemy.exc import OperationalError, IntegrityError

# Create the Flask app
app = create_app()

# Use the app context to interact with the database
with app.app_context():
    print("Starting database population process...")

    # Clear existing data (optional, to avoid duplicates)
    try:
        db.session.query(Ward).delete()
        db.session.query(Constituency).delete()
        db.session.query(County).delete()
        db.session.commit()
        print("Cleared existing data from Counties, Constituencies, and Wards.")
    except Exception as e:
        db.session.rollback()
        print(f"Error clearing existing data: {str(e)}")
        raise

    # Define all 47 counties in Kenya
    county_names = [
        'Mombasa', 'Kwale', 'Kilifi', 'Tana River', 'Lamu', 'Taita-Taveta', 'Garissa', 'Wajir', 'Mandera', 'Marsabit',
        'Isiolo', 'Meru', 'Tharaka-Nithi', 'Embu', 'Kitui', 'Machakos', 'Makueni', 'Nyandarua', 'Nyeri', 'Kirinyaga',
        'Murang\'a', 'Kiambu', 'Turkana', 'West Pokot', 'Samburu', 'Trans Nzoia', 'Uasin Gishu', 'Elgeyo-Marakwet',
        'Nandi', 'Baringo', 'Laikipia', 'Nakuru', 'Narok', 'Kajiado', 'Kericho', 'Bomet', 'Kakamega', 'Vihiga',
        'Bungoma', 'Busia', 'Siaya', 'Kisumu', 'Homa Bay', 'Migori', 'Kisii', 'Nyamira', 'Nairobi'
    ]

    max_retries = 5
    retry_delay = 2  # seconds

    # Add Counties
    counties_added = False
    for attempt in range(max_retries):
        try:
            counties = [County(CountyName=name) for name in county_names]
            db.session.add_all(counties)
            db.session.commit()
            print(f"Added {len(counties)} counties successfully!")
            counties_added = True
            break
        except OperationalError as e:
            db.session.rollback()
            if "database is locked" in str(e):
                print(f"Database locked, retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                print(f"OperationalError while adding counties: {str(e)}")
                raise
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError while adding counties (possible duplicate): {str(e)}")
            raise
        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error while adding counties: {str(e)}")
            raise
    if not counties_added:
        raise Exception("Failed to commit counties after maximum retries.")

    # Define all 290 constituencies with wards (complete for some counties, placeholders for others)
    constituencies_data = {
        'Mombasa': [
            ('Changamwe', ['Port Reitz', 'Kipevu', 'Airport', 'Miritini', 'Chaani']),
            ('Jomvu', ['Jomvu Kuu', 'Mikindani', 'Mjambere']),
            ('Kisauni', ['Mjawuni', 'Junda', 'Bamburi', 'Mwakirunge', 'Mtopanga', 'Magongoni', 'Shanzu']),
            ('Nyali', ['Frere Town', 'Ziwa La Ng\'ombe', 'Mkomani', 'Kongowea', 'Kadzandani']),
            ('Likoni', ['Mtongwe', 'Shika Adabu', 'Bofu', 'Likoni', 'Timbwani']),
            ('Mvita', ['Mji Wa Kale/Makadara', 'Tudor', 'Tononoka', 'Shimanzi/Ganjoni', 'Majengo'])
        ],
        'Kwale': [
            ('Msambweni', ['Gombato Bongwe', 'Ukunda', 'Kinondo', 'Ramisi']),
            ('Lungalunga', ['Pongwe/Kikoneni', 'Dzombo', 'Mwereni', 'Vanga']),
            ('Matuga', ['Tsimba Golini', 'Kubo South', 'Mkongani', 'Tsunza', 'Waa']),
            ('Kinango', ['Ndavaya', 'Puma', 'Kinango', 'Mackinnon Road', 'Chengoni/Samburu', 'Mwavumbo', 'Kasemeni'])
        ],
        'Kilifi': [
            ('Kilifi North', ['Tezo', 'Sokoni', 'Kibarani', 'Dabaso', 'Matsangoni', 'Watamu', 'Mnarani']),
            ('Kilifi South', ['Junju', 'Mwarakaya', 'Shimo la Tewa', 'Chasimba', 'Mtepeni']),
            ('Kaloleni', ['Mariakani', 'Kayafungo', 'Kaloleni', 'Mwana Mwinga']),
            ('Rabai', ['Mwawesa', 'Ruruma', 'Kambe/Ribe', 'Rabai/Kisurutuni']),
            ('Ganze', ['Ganze', 'Bamba', 'Jaribuni', 'Sokoke']),
            ('Malindi', ['Jilore', 'Kakuyuni', 'Ganda', 'Malindi Town', 'Shella']),
            ('Magarini', ['Marafa', 'Magarini', 'Gongoni', 'Adu', 'Garashi', 'Sabaki'])
        ],
        'Tana River': [
            ('Garsen', ['Garsen South', 'Garsen Central', 'Garsen West', 'Kipini East']),
            ('Galole', ['Wayu', 'Chewani', 'Hirimani', 'Kinakomba']),
            ('Bura', ['Chewele', 'Hirimani', 'Bangale', 'Sala'])
        ],
        'Lamu': [
            ('Lamu East', ['Faza', 'Kiunga', 'Basuba']),
            ('Lamu West', ['Shella', 'Mkomani', 'Hindi', 'Mkunumbi', 'Hongwe', 'Witu'])
        ],
        'Taita-Taveta': [
            ('Taveta', ['Chala', 'Mahoo', 'Bomani', 'Mboghoni', 'Mata']),
            ('Wundanyi', ['Wundanyi/Mbale', 'Werugha', 'Wumingu/Kishushe', 'Mwanda/Mgange']),
            ('Mwatate', ['Rong\'e', 'Mwatate', 'Bura', 'Chawia', 'Wusi/Kishamba']),
            ('Voi', ['Mbololo', 'Sagala', 'Kaloleni', 'Marungu', 'Kasigau', 'Ngolia'])
        ],
        'Garissa': [
            ('Garissa Township', ['Waberi', 'Galbet', 'Township', 'Iftin']),
            ('Balambala', ['Balambala', 'Danyere', 'Jarajara', 'Saka']),
            ('Lagdera', ['Modogashe', 'Beno', 'Goreale', 'Maalimin']),
            ('Dadaab', ['Dertu', 'Dadaab', 'Labasigale', 'Damajale', 'Liboi', 'Abakaile']),
            ('Fafi', ['Bura', 'Dekaharia', 'Jarajila', 'Fafi', 'Nanighi']),
            ('Ijara', ['Ijara', 'Masalani', 'Sangailu', 'Hulugho'])
        ],
        'Wajir': [
            ('Wajir North', ['Gurar', 'Bute', 'Korondile', 'Malkagufu']),
            ('Wajir East', ['Wagberi', 'Township', 'Barwago', 'Khorof/Harar']),
            ('Tarbaj', ['Elben', 'Sarman', 'Tarbaj', 'Wargadud']),
            ('Wajir West', ['Adan Awale', 'Arbajahan', 'Hadado/Athibohol', 'Ganyure/Wajir-Bor']),
            ('Eldas', ['Eldas', 'Della', 'Lakoley South/Basir', 'Kone Goba']),
            ('Wajir South', ['Benane', 'Burder', 'Dadaja Bulla', 'Habaswein', 'Lagboghol South'])
        ],
        'Mandera': [
            ('Mandera West', ['Takaba South', 'Takaba', 'Lagsure', 'Dandu']),
            ('Banissa', ['Banissa', 'Derkhale', 'Guba', 'Malkamari']),
            ('Mandera North', ['Ashabito', 'Guticha', 'Morothile', 'Rhamu', 'Rhamu Dimtu']),
            ('Mandera South', ['Wargadud East', 'Kutulo', 'Elwak South', 'Elwak North', 'Shimbir Fatuma']),
            ('Mandera East', ['Arabia', 'Bulla Mpya', 'Neboi', 'Khalalio', 'Libehia']),
            ('Lafey', ['Lafey', 'Warankara', 'Alango Gof', 'Libahia'])
        ],
        'Marsabit': [
            ('Moyale', ['Butiye', 'Sololo', 'Heilu/Manyatta', 'Golbo']),
            ('North Horr', ['Dukana', 'Maikona', 'Turbi', 'North Horr', 'Illeret']),
            ('Laisamis', ['Loiyangalani', 'Kargi/South Horr', 'Korr/Ngurunit', 'Logologo']),
            ('Saku', ['Sagante/Jaldesa', 'Karare', 'Marsabit Central'])
        ],
        'Isiolo': [
            ('Isiolo North', ['Wabera', 'Bulla Pesa', 'Chari', 'Cherab', 'Ngare Mara']),
            ('Isiolo South', ['Garbatulla', 'Kinna', 'Sericho'])
        ],
        'Meru': [
            ('Igembe South', ['Maua', 'Kiegoi/Antuambui', 'Athiru Gaiti']),
            ('Igembe Central', ['Igembe East', 'Njia', 'Kangeta', 'Auki']),
            ('Igembe North', ['Antuambui', 'Naathu', 'Amwathi', 'Akachiu']),
            ('Tigania West', ['Athwana', 'Akithi', 'Kianjai', 'Nkomo']),
            ('Tigania East', ['Thangatha', 'Mikinduri', 'Kiguchwa', 'Muthara']),
            ('North Imenti', ['Municipality', 'Ntima East', 'Ntima West']),
            ('Buuri', ['Timau', 'Kisima', 'Kiirua/Naari', 'Ruiri/Rwarera']),
            ('Central Imenti', ['Mwangathia', 'Abothuguchi Central', 'Abothuguchi West']),
            ('South Imenti', ['Mitunguu', 'Igoji East', 'Igoji West', 'Abogeta East'])
        ],
        'Tharaka-Nithi': [
            ('Maara', ['Mitheru', 'Muthambi', 'Mwimbi', 'Ganga']),
            ('Chuka/Igambang’ombe', ['Karingani', 'Magumoni', 'Mugwe', 'Igambang’ombe']),
            ('Tharaka', ['Gatunga', 'Mukothima', 'Nkondi', 'Chiakariga'])
        ],
        'Embu': [
            ('Manyatta', ['Ruguru/Ngandori', 'Kithimu', 'Nginda', 'Mbeti North']),
            ('Runyenjes', ['Gaturi North', 'Gaturi South', 'Kagaari South', 'Kagaari North']),
            ('Mbeere South', ['Mbeti South', 'Mavuria', 'Kiambere', 'Makima']),
            ('Mbeere North', ['Nthawa', 'Muminji', 'Evurore'])
        ],
        'Kitui': [
            ('Mwingi North', ['Ngomeni', 'Kyuso', 'Mumoni', 'Tseikuru']),
            ('Mwingi West', ['Kiomo/Kyethani', 'Migwani', 'Nguutani', 'Mwingi Central']),
            ('Mwingi Central', ['Central', 'Kivou', 'Nguni', 'Nuu']),
            ('Kitui West', ['Mutonguni', 'Kauwi', 'Matinyani', 'Kwa Mutonga/Kithumula']),
            ('Kitui Rural', ['Kisasi', 'Mbitini', 'Kwavonza/Yatta', 'Kanyangi']),
            ('Kitui Central', ['Miambani', 'Township', 'Kyangwithya West', 'Mulango']),
            ('Kitui East', ['Zombe/Mwitika', 'Nzambani', 'Chuluni', 'Voo/Kyamatu']),
            ('Kitui South', ['Ikanga/Kyatune', 'Mutomo', 'Mathima', 'Kanziko'])
        ],
        'Machakos': [
            ('Masinga', ['Kivaa', 'Masinga Central', 'Ekalakala', 'Muthesya']),
            ('Yatta', ['Ndalani', 'Matuu', 'Kithimani', 'Ikombe']),
            ('Kangundo', ['Kangundo North', 'Kangundo Central', 'Kangundo East', 'Kangundo West']),
            ('Matungulu', ['Tala', 'Matungulu East', 'Matungulu West', 'Kyeleni']),
            ('Kathiani', ['Mitaboni', 'Kathiani Central', 'Upper Kaewa/Kaani', 'Lower Kaewa/Kaani']),
            ('Mavoko', ['Athi River', 'Kinanie', 'Muthwani', 'Syokimau/Mulolongo']),
            ('Machakos Town', ['Kalama', 'Mua', 'Mutituni', 'Machakos Central']),
            ('Mwala', ['Mbiuni', 'Makutano/Mwala', 'Masii', 'Muthetheni'])
        ],
        'Makueni': [
            ('Mbooni', ['Tulimani', 'Mbooni', 'Kithungo/Kitundu', 'Kiteta/Kisau']),
            ('Kilome', ['Kasikeu', 'Mukaa', 'Kiima Kiu/Kalanzoni']),
            ('Kaiti', ['Ukia', 'Kee', 'Kilungu', 'Ilima']),
            ('Makueni', ['Wote', 'Muvau/Kikumini', 'Mavindini', 'Kitise/Kithuki']),
            ('Kibwezi West', ['Makindu', 'Nguumo', 'Kikumbulyu North', 'Kikumbulyu South']),
            ('Kibwezi East', ['Masongaleni', 'Mtito Andei', 'Thange', 'Ivingoni/Nzambani'])
        ],
        'Nyandarua': [
            ('Kinangop', ['Engineer', 'Gathara', 'North Kinangop', 'Murungaru']),
            ('Kipipiri', ['Wanjohi', 'Kipipiri', 'Geta', 'Githioro']),
            ('Ol Kalou', ['Karau', 'Kanjuiri Ridge', 'Rurii', 'Mirangine']),
            ('Ol Joro Orok', ['Gathanji', 'Gatimu', 'Weru', 'Charagita']),
            ('Ndaragwa', ['Lesha', 'Kaimbaga', 'Shamata', 'Ndaragwa'])
        ],
        'Nyeri': [
            ('Tetu', ['Wamagana', 'Aguthi-Gaaki', 'Dedan Kimathi']),
            ('Kieni', ['Mweiga', 'Naromoru Kiamathaga', 'Mwiyogo/Endarasha', 'Mugunda']),
            ('Mathira', ['Ruguru', 'Magutu', 'Iriaini', 'Karatina Town']),
            ('Othaya', ['Mahiga', 'Iria-Ini', 'Chinga', 'Karima']),
            ('Mukurweini', ['Gikondi', 'Rugi', 'Mukurwe-Ini West', 'Mukurwe-Ini Central']),
            ('Nyeri Town', ['Karia', 'Gatitu/Muruguru', 'Rware', 'Kamkunji'])
        ],
        'Kirinyaga': [
            ('Gichugu', ['Kabare', 'Njukiini', 'Ngariama', 'Karumandi']),
            ('Ndia', ['Mukure', 'Kiine', 'Kariti']),
            ('Kirinyaga Central', ['Mutira', 'Kanyekiine', 'Kerugoya', 'Inoi']),
            ('Mwea', ['Mutithi', 'Kangai', 'Wamumu', 'Nyamindi'])
        ],
        'Murang\'a': [
            ('Kangema', ['Kanyenyaini', 'Rwathia', 'Muguru']),
            ('Mathioya', ['Gitugi', 'Kiru', 'Kamacharia']),
            ('Kiharu', ['Wangu', 'Mugoiri', 'Mbiri', 'Township']),
            ('Kigumo', ['Kahumbu', 'Muthithi', 'Kigumo', 'Kangari']),
            ('Maragwa', ['Kimorori/Wempa', 'Makuyu', 'Kambiti', 'Kamahuha']),
            ('Kandara', ['Ng’araria', 'Muruka', 'Kagundu-Ini', 'Gaichanjiru']),
            ('Gatanga', ['Ithanga', 'Kakuzi/Mitubiri', 'Mugumo-Ini', 'Kihumbu-Ini'])
        ],
        'Kiambu': [
            ('Gatundu South', ['Kiamwangi', 'Kiganjo', 'Ndarugo', 'Ngenda']),
            ('Gatundu North', ['Gituamba', 'Githobokoni', 'Chania', 'Mang’u']),
            ('Juja', ['Murera', 'Theta', 'Juja', 'Witeithie', 'Kalimoni']),
            ('Thika Town', ['Township', 'Kamenu', 'Hospital', 'Gatuanyaga', 'Ngoliba']),
            ('Ruiru', ['Gitothua', 'Biashara', 'Gatongora', 'Kahawa Sukari', 'Kahawa Wendani']),
            ('Githunguri', ['Githunguri', 'Githiga', 'Ikinu', 'Ngewa', 'Komothai']),
            ('Kiambaa', ['Cianda', 'Karuri', 'Ndenderu', 'Muchatha']),
            ('Kabete', ['Gitaru', 'Muguga', 'Nyadhuna', 'Kabete', 'Uthiru']),
            ('Kikuyu', ['Karai', 'Nachu', 'Sigona', 'Kikuyu', 'Kinoo']),
            ('Limuru', ['Bibirioni', 'Limuru Central', 'Ndeiya', 'Limuru East', 'Ngecha Tigoni']),
            ('Lari', ['Kinale', 'Kijabe', 'Nyanduma', 'Kamburu', 'Lari/Kirenga']),
            ('Kiambu', ['Tinganga', 'Ndumberi', 'Riabai', 'Township'])
        ],
        'Turkana': [
            ('Turkana North', ['Kaeris', 'Lakezone', 'Lapur', 'Kaaleng/Kaikor']),
            ('Turkana West', ['Kakuma', 'Lopur', 'Letea', 'Songot']),
            ('Turkana Central', ['Kerio Delta', 'Kangatotha', 'Kalokol', 'Lodwar Township']),
            ('Loima', ['Loima', 'Turkwel', 'Lokiriama/Lorenji', 'Namalukuny']),
            ('Turkana South', ['Katilu', 'Lobokat', 'Kaputir', 'Kalapata']),
            ('Turkana East', ['Kapedo/Napeitom', 'Katilia', 'Lokori/Kochodin'])
        ],
        'West Pokot': [
            ('Kapenguria', ['Kapenguria', 'Mnagei', 'Sook', 'Endugh']),
            ('Kacheliba', ['Suam', 'Kodich', 'Kasei', 'Kapchok']),
            ('Sigor', ['Sekerr', 'Masool', 'Lomut', 'Weiwei']),
            ('Pokot South', ['Chepareria', 'Batei', 'Lelan', 'Tapach'])
        ],
        'Samburu': [
            ('Samburu West', ['Lodokejek', 'Suguta Marmar', 'Maralal', 'Loosuk']),
            ('Samburu North', ['El Barta', 'Nachola', 'Ndoto', 'Nyiro']),
            ('Samburu East', ['Wamba West', 'Wamba East', 'Wamba North', 'Waso'])
        ],
        'Trans Nzoia': [
            ('Kwanza', ['Kwanza', 'Keiyo', 'Bidii', 'Kapomboi']),
            ('Endebess', ['Endebess', 'Chepchoina', 'Matumbei']),
            ('Saboti', ['Kinyoro', 'Matisi', 'Tuwani', 'Saboti']),
            ('Kiminini', ['Kiminini', 'Waitaluk', 'Sirende', 'Sikhendu']),
            ('Cherangany', ['Sinyerere', 'Makutano', 'Kaplamai', 'Motosi'])
        ],
        'Uasin Gishu': [
            ('Soy', ['Ziwa', 'Segero/Barsombe', 'Kipsomba', 'Soy']),
            ('Turbo', ['Tapsagoi', 'Kamagut', 'Kiplombe', 'Ngenyilel']),
            ('Moiben', ['Tembelio', 'Sergoit', 'Karuna/Meibeki', 'Moiben']),
            ('Ainabkoi', ['Kapsoya', 'Kaptagat', 'Ainabkoi/Olare']),
            ('Kapseret', ['Simat/Kapseret', 'Kipkenyo', 'Ngeria', 'Megun']),
            ('Kesses', ['Racecourse', 'Cheptiret/Kipchamo', 'Tulwet/Chuiyat', 'Tarakwa'])
        ],
        'Elgeyo-Marakwet': [
            ('Marakwet East', ['Kapyego', 'Sambirir', 'Endo']),
            ('Marakwet West', ['Lelan', 'Sengwer', 'Cherangany/Chebororwa', 'Moiben/Kuserwo']),
            ('Keiyo North', ['Emsoo', 'Kamariny', 'Kapchemutwa', 'Tambach']),
            ('Keiyo South', ['Kaptarakwa', 'Chepkorio', 'Soy North', 'Soy South'])
        ],
        'Nandi': [
            ('Tinderet', ['Songhor/Soba', 'Tindiret', 'Chemelil/Chemase', 'Kapsimotwo']),
            ('Aldai', ['Kabwareng', 'Terik', 'Kaptumo/Kaboi', 'Koyo/Ndurio']),
            ('Nandi Hills', ['Nandi Hills', 'Chepkunyuk', 'Ol’lessos', 'Kapchorua']),
            ('Chesumei', ['Chemundu/Kapng’etuny', 'Kosirai', 'Lelmokwo/Ngechek', 'Kiptaiyat']),
            ('Emgwen', ['Chepkumia', 'Kapkangani', 'Kapsabet', 'Kilibwoni']),
            ('Mosop', ['Chepterwai', 'Kipkaren', 'Kurgung/Surungai', 'Kabiyet'])
        ],
        'Baringo': [
            ('Tiaty', ['Tirioko', 'Kolowa', 'Ribkwo', 'Silale']),
            ('Baringo North', ['Barwessa', 'Kabartonjo', 'Saimo/Kipsaraman', 'Saimo/Soi']),
            ('Baringo Central', ['Kapropita', 'Eldama Ravine', 'Lembus', 'Kabimoi']),
            ('Baringo South', ['Marigat', 'Ilchamus', 'Mochongoi', 'Mukutani']),
            ('Mogotio', ['Mogotio', 'Emsos', 'Kisanana']),
            ('Eldama Ravine', ['Lembus West', 'Lembus East', 'Ravine', 'Mumberes/Maji Mazuri'])
        ],
        'Laikipia': [
            ('Laikipia West', ['Ol-Moran', 'Rumuruti Township', 'Kinamba', 'Marmanet']),
            ('Laikipia East', ['Ngobit', 'Tigithi', 'Thingithu', 'Nanyuki']),
            ('Laikipia North', ['Mukogodo East', 'Mukogodo West', 'Segera', 'Sosian'])
        ],
        'Nakuru': [
            ('Molo', ['Mariashoni', 'Elburgon', 'Turi', 'Molo']),
            ('Njoro', ['Mau Narok', 'Mauche', 'Kihingo', 'Nessuit']),
            ('Naivasha', ['Biashara', 'Hells Gate', 'Lake View', 'Maiella']),
            ('Gilgil', ['Gilgil', 'Elementaita', 'Mbaruk/Eburu', 'Malewa West']),
            ('Kuresoi South', ['Keringet', 'Kiptagich', 'Amalo', 'Kiptororo']),
            ('Kuresoi North', ['Sirikwa', 'Kamara', 'Kiptororo', 'Nyota']),
            ('Subukia', ['Subukia', 'Waseges', 'Kabazi']),
            ('Rongai', ['Menengai West', 'Soin', 'Visoi', 'Mosop']),
            ('Bahati', ['Dundori', 'Kabatini', 'Kiamaina', 'Lanet/Umoja']),
            ('Nakuru Town West', ['Barut', 'London', 'Kaptembwo', 'Kapkures']),
            ('Nakuru Town East', ['Biashara', 'Kivumbini', 'Flamingo', 'Menengai'])
        ],
        'Narok': [
            ('Kilgoris', ['Kilgoris Central', 'Keyian', 'Angata Barikoi', 'Shankoe']),
            ('Emurua Dikirr', ['Ilkerin', 'Ololmasani', 'Mogondo', 'Kapsasian']),
            ('Narok North', ['Olpusimoru', 'Olokurto', 'Narok Town', 'Nkareta']),
            ('Narok East', ['Mosiro', 'Ildamat', 'Keekonyokie', 'Suswa']),
            ('Narok South', ['Majimoto/Naroosura', 'Ololulunga', 'Melelo', 'Loita']),
            ('Narok West', ['Ilmotiok', 'Mara', 'Siana', 'Naikarra'])
        ],
        'Kajiado': [
            ('Kajiado North', ['Olkeri', 'Ongata Rongai', 'Nkaimurunya', 'Oloolua']),
            ('Kajiado Central', ['Purko', 'Ildamat', 'Dalalekutuk', 'Matapato North']),
            ('Kajiado East', ['Kaputiei North', 'Kitengela', 'Oloosirkon/Sholinke', 'Kenyawa-Poka']),
            ('Kajiado West', ['Keekonyokie', 'Magadi', 'Ewuaso Oonkidong’i', 'Mosiro']),
            ('Kajiado South', ['Entonet/Lenkisim', 'Mbirikani/Eselenkei', 'Kuku', 'Rombo'])
        ],
        'Kericho': [
            ('Kipkelion East', ['Londiani', 'Kedowa/Kimugul', 'Chepseon', 'Tendeno/Sorget']),
            ('Kipkelion West', ['Kunyak', 'Kamasian', 'Kipkelion', 'Chilchila']),
            ('Ainamoi', ['Ainamoi', 'Kapsoit', 'Kapsaos', 'Kipchebor']),
            ('Bureti', ['Kisiara', 'Tebesonik', 'Cheboin', 'Chemosot']),
            ('Belgut', ['Waldai', 'Kabianga', 'Cheptororiet/Seretut', 'Chaik']),
            ('Sigowet/Soin', ['Sigowet', 'Kaplelartet', 'Soin', 'Soliat'])
        ],
        'Bomet': [
            ('Sotik', ['Ndanai/Abosi', 'Chemagel', 'Kipsonoi', 'Kapletundo']),
            ('Chepalungu', ['Chebunyo', 'Siongiroi', 'Kong’asis', 'Nyongores']),
            ('Bomet East', ['Merigi', 'Kembu', 'Longisa', 'Kipreres']),
            ('Bomet Central', ['Silibwet Township', 'Ndaraweta', 'Singorwet', 'Chesoen']),
            ('Konoin', ['Kimulot', 'Mogogosiek', 'Boito', 'Embomos'])
        ],
        'Kakamega': [
            ('Lugari', ['Mautuma', 'Lugari', 'Lumakanda', 'Chekalini']),
            ('Likuyani', ['Likuyani', 'Sango', 'Kongoni', 'Nzoia']),
            ('Malava', ['West Kabras', 'Chemuche', 'East Kabras', 'Butali/Chegulo']),
            ('Lurambi', ['Butsotso East', 'Butsotso South', 'Butsotso Central', 'Sheywe']),
            ('Navakholo', ['Ingostse-Mathia', 'Shinoyi-Shikomari-Esumeyia', 'Bunjoro', 'Nambachi']),
            ('Mumias West', ['Mumias Central', 'Mumias North', 'Etenje', 'Musanda']),
            ('Mumias East', ['Lusheya/Lubinu', 'Malaha/Isongo/Makunga', 'East Wanga']),
            ('Matungu', ['Koyonzo', 'Khalaba', 'Mayoni', 'Namamali']),
            ('Butere', ['Marama Inaya', 'Marama West', 'Marama Central', 'Marama North']),
            ('Khwisero', ['Kisa North', 'Kisa East', 'Kisa West', 'Kisa Central']),
            ('Shinyalu', ['Isukha North', 'Murhanda', 'Isukha Central', 'Isukha South']),
            ('Ikolomani', ['Idakho South', 'Idakho North', 'Idakho East', 'Idakho Central'])
        ],
        'Vihiga': [
            ('Vihiga', ['Lugaga-Wamuluma', 'South Maragoli', 'Central Maragoli', 'Mungoma']),
            ('Sabatia', ['Lyaduywa/Izava', 'West Sabatia', 'Chavakali', 'North Maragoli']),
            ('Hamisi', ['Shiru', 'Muhandis', 'Shamakhokho', 'Gisambai']),
            ('Luanda', ['Luanda Township', 'Wemilabi', 'Mwibona', 'Luanda South']),
            ('Emuhaya', ['North East Bunyore', 'Central Bunyore', 'West Bunyore'])
        ],
        'Bungoma': [
            ('Mt. Elgon', ['Cheptais', 'Chesikaki', 'Chepyuk', 'Kapkateny']),
            ('Sirisia', ['Namwela', 'Malakisi/South Kulisiru', 'Lwandanyi']),
            ('Kabuchai', ['Kabuchai/Chwele', 'West Nalondo', 'Bwake/Luuya', 'Mukuyuni']),
            ('Bumula', ['South Bukusu', 'Bumula', 'Khasoko', 'Kabula']),
            ('Kanduyi', ['Bukembe West', 'Bukembe East', 'Township', 'Khalaba']),
            ('Webuye East', ['Mihuu', 'Ndivisi', 'Maraka']),
            ('Webuye West', ['Sitikho', 'Matulo', 'Bokoli', 'Misikhu']),
            ('Kimilili', ['Kibingei', 'Kimilili', 'Maeni', 'Kamukuywa']),
            ('Tongaren', ['Mbakalo', 'Naitiri/Kabuyefwe', 'Milima', 'Ndalu/Tabani'])
        ],
        'Busia': [
            ('Teso North', ['Malaba Central', 'Malaba North', 'Ang’urai South', 'Ang’urai North']),
            ('Teso South', ['Ang’orom', 'Chakol South', 'Chakol North', 'Amukura West']),
            ('Nambale', ['Nambale Township', 'Bukhayo North/West', 'Bukhayo East', 'Bukhayo Central']),
            ('Matayos', ['Bukhayo West', 'Mayenje', 'Busibwabo', 'Burumba']),
            ('Butula', ['Marachi West', 'Marachi East', 'Marachi Central', 'Marachi North']),
            ('Funyula', ['Nangina', 'Ageng’a Nanguba', 'Bwiri', 'Namboboto Nambuku']),
            ('Budalangi', ['Bunjimba', 'Magombe West', 'Magombe East', 'Mundere'])
        ],
        'Siaya': [
            ('Ugenya', ['West Ugenya', 'East Ugenya', 'Ukwala', 'North Ugenya']),
            ('Ugunja', ['Sidindi', 'Sigomere', 'Ugunja']),
            ('Alego Usonga', ['Usonga', 'West Alego', 'Central Alego', 'Siaya Township']),
            ('Gem', ['North Gem', 'West Gem', 'East Gem', 'South Gem']),
            ('Bondo', ['West Yimbo', 'Central Sakwa', 'South Sakwa', 'Yimbo East']),
            ('Rarieda', ['West Asembo', 'East Asembo', 'West Uyoma', 'North Uyoma'])
        ],
        'Kisumu': [
            ('Kisumu East', ['Kajulu', 'Kolwa East', 'Manyatta B', 'Nyalenda A']),
            ('Kisumu West', ['South West Kisumu', 'Central Kisumu', 'Kisumu North', 'West Kisumu']),
            ('Kisumu Central', ['Railways', 'Migosi', 'Shaurimoyo Kaloleni', 'Market Milimani']),
            ('Seme', ['West Seme', 'East Seme', 'Central Seme', 'North Seme']),
            ('Nyando', ['East Kano/Wawidhi', 'Awasi/Onjiko', 'Ahero', 'Kabonyo/Kanyagwal']),
            ('Muhoroni', ['Miwani', 'Ombeyi', 'Masogo/Nyang’oma', 'Chemelil']),
            ('Nyakach', ['South West Nyakach', 'North Nyakach', 'Central Nyakach', 'West Nyakach'])
        ],
        'Homa Bay': [
            ('Kasipul', ['West Kasipul', 'East Kamagak', 'West Kamagak', 'South Kasipul']),
            ('Kabondo Kasipul', ['Kabondo East', 'Kabondo West', 'Kojwach']),
            ('Karachuonyo', ['West Karachuonyo', 'North Karachuonyo', 'Central', 'Kanyaluo']),
            ('Rangwe', ['West Gem', 'East Gem', 'Kagan', 'Kochia']),
            ('Homa Bay Town', ['Homa Bay Central', 'Homa Bay Arujo', 'Homa Bay West', 'Homa Bay East']),
            ('Ndhiwa', ['Kwabwai', 'Kanyadoto', 'Kanyamwa Kologi', 'Kanyamwa Kosewe']),
            ('Mbita', ['Mfangano Island', 'Rusinga Island', 'Lambwe', 'Gembe']),
            ('Suba', ['Kaksingri East', 'Gwassi South', 'Gwassi North', 'Ruma Kaksingri'])
        ],
        'Migori': [
            ('Rongo', ['North Kamagambo', 'Central Kamagambo', 'East Kamagambo', 'South Kamagambo']),
            ('Awendo', ['North East Sakwa', 'South Sakwa', 'West Sakwa', 'Central Sakwa']),
            ('Suna East', ['God Jope', 'Suna Central', 'Kakrao', 'Kwa']),
            ('Suna West', ['Wiga', 'Wasweta II', 'Ragana-Oruba', 'Wasimbete']),
            ('Uriri', ['West Kanyamkago', 'East Kanyamkago', 'North Kanyamkago', 'Central Kanyamkago']),
            ('Nyatike', ['Kachieng’', 'Kanyasa', 'North Kadem', 'Macalder/Kanyarwanda']),
            ('Kuria West', ['Bukira East', 'Bukira Central/Ikerege', 'Isibania', 'Makerero']),
            ('Kuria East', ['Gokeharaka/Getambwega', 'Ntimaru West', 'Ntimaru East', 'Nyabasi East'])
        ],
        'Kisii': [
            ('Bonchari', ['Bomariba', 'Bokeira', 'Riana', 'Bomorenda']),
            ('South Mugirango', ['Bogetenga', 'Borabu/Chitago', 'Moticho', 'Getenga']),
            ('Bomachoge Borabu', ['Boochi Borabu', 'Bokimonge', 'Magenche']),
            ('Bobasi', ['Masige West', 'Masige East', 'Bassi Central', 'Nyacheki']),
            ('Bomachoge Chache', ['Majoge Bassi', 'Boochi/Tendere', 'Bosoti/Sengera']),
            ('Nyaribari Masaba', ['Ichuni', 'Nyamasibi', 'Masimba', 'Gesusu']),
            ('Nyaribari Chache', ['Bobaracho', 'Kisii Central', 'Keumbu', 'Kiogoro']),
            ('Kitutu Chache North', ['Marani', 'Sensii', 'Kegogi', 'Monyerero']),
            ('Kitutu Chache South', ['Bogusero', 'Bogeka', 'Nyakoe', 'Kitutu Central'])
        ],
        'Nyamira': [
            ('Kitutu Masaba', ['Rigoma', 'Gachuba', 'Kemera', 'Magombo']),
            ('West Mugirango', ['Bonyamatuta', 'Bogichora', 'Nyamaiya', 'Township']),
            ('North Mugirango', ['Itibo', 'Bomwagamo', 'Bokeira', 'Manga']),
            ('Borabu', ['Mekenene', 'Kiabonyoru', 'Nyansiongo', 'Esise'])
        ],
        'Nairobi': [
            ('Westlands', ['Kitisuru', 'Parklands/Highridge', 'Kangemi', 'Mountain View', 'Karura']),
            ('Dagoretti North', ['Kilimani', 'Kawangware', 'Gatina', 'Kileleshwa', 'Kabiro']),
            ('Dagoretti South', ['Mutu-ini', 'Ngando', 'Riruta', 'Uthiru/Ruthimitu', 'Waithaka']),
            ('Langata', ['Karen', 'Nairobi West', 'Nyayo Highrise', 'Mugumo-ini', 'South C']),
            ('Kibra', ['Laini Saba', 'Lindi', 'Makina', 'Woodley/Kenyatta Golf Course', 'Sarangombe']),
            ('Roysambu', ['Githurai', 'Kahawa West', 'Zimmerman', 'Roysambu', 'Kahawa']),
            ('Kasarani', ['Clay City', 'Mwiki', 'Kasarani', 'Njiru', 'Ruai']),
            ('Ruaraka', ['Babadogo', 'Utalii', 'Mathare North', 'Lucky Summer', 'Korogocho']),
            ('Embakasi South', ['Imara Daima', 'Kwa Njenga', 'Kwa Reuben', 'Pipeline', 'Kware']),
            ('Embakasi North', ['Kariobangi North', 'Dandora Area I', 'Dandora Area II', 'Dandora Area III', 'Dandora Area IV']),
            ('Embakasi Central', ['Kayole North', 'Kayole Central', 'Kayole South', 'Komarock', 'Matopeni/Spring Valley']),
            ('Embakasi East', ['Upper Savanna', 'Lower Savanna', 'Embakasi', 'Utawala', 'Mihango']),
            ('Embakasi West', ['Umoja I', 'Umoja II', 'Mowlem', 'Kariobangi South']),
            ('Makadara', ['Maringo/Hamza', 'Viwandani', 'Harambee', 'Makongeni', 'Mbotela']),
            ('Kamukunji', ['Pumwani', 'Eastleigh North', 'Eastleigh South', 'Airbase', 'California']),
            ('Starehe', ['Nairobi Central', 'Ngara', 'Pangani', 'Ziwani/Kariokor', 'Landimawe', 'Nairobi South']),
            ('Mathare', ['Hospital', 'Mabatini', 'Huruma', 'Ngei', 'Mlango Kubwa', 'Kiamaiko'])
        ]
    }

    # Add Constituencies and Wards
    constituencies_added = False
    total_constituencies = 0
    total_wards = 0

    for county_name, const_data in constituencies_data.items():
        county = County.query.filter_by(CountyName=county_name).first()
        if not county:
            print(f"Error: {county_name} county not found in the database.")
            continue

        constituencies = []
        wards = []

        for constituency_name, ward_names in const_data:
            constituency = Constituency(ConstituencyName=constituency_name, CountyID=county.CountyID)
            constituencies.append(constituency)
            db.session.add(constituency)
            try:
                db.session.flush()  # Generate ConstituencyID
            except Exception as e:
                db.session.rollback()
                print(f"Error flushing constituency {constituency_name} for {county_name}: {str(e)}")
                raise

            for ward_name in ward_names:
                ward = Ward(WardName=ward_name, ConstituencyID=constituency.ConstituencyID)
                wards.append(ward)

        # Commit constituencies and wards for this county
        for attempt in range(max_retries):
            try:
                db.session.add_all(wards)
                db.session.commit()
                print(f"Added {len(const_data)} constituencies and {len(wards)} wards for {county_name} successfully!")
                total_constituencies += len(const_data)
                total_wards += len(wards)
                constituencies_added = True
                break
            except OperationalError as e:
                db.session.rollback()
                if "database is locked" in str(e):
                    print(f"Database locked for {county_name}, retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    print(f"OperationalError while adding data for {county_name}: {str(e)}")
                    raise
            except IntegrityError as e:
                db.session.rollback()
                print(f"IntegrityError while adding data for {county_name} (possible duplicate): {str(e)}")
                raise
            except Exception as e:
                db.session.rollback()
                print(f"Unexpected error while adding data for {county_name}: {str(e)}")
                raise
        if not constituencies_added:
            raise Exception(f"Failed to commit constituencies and wards for {county_name} after maximum retries.")

    # Verify counts and print success message only if everything succeeds
    county_count = County.query.count()
    constituency_count = Constituency.query.count()
    ward_count = Ward.query.count()
    print(f"Verification - Total Counties: {county_count}, Constituencies: {constituency_count}, Wards: {ward_count}")

    if county_count == len(county_names) and constituency_count == total_constituencies and ward_count == total_wards:
        print("Database populated successfully!")
    else:
        print("Database population incomplete. Check counts and logs for issues.")