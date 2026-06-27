from typing import Any, Tuple, List

LIST_OF_CHAR = "abcdefghijklmnopqrstuvwxyz0123456789"

SAMPLES = {
    "data1": {
        "HEAP_STACK": "aaaaddaaabbbbbc",
        "SEARCH_QUERIES": [
            "a-c",
            "c,a,b",
            "a,c",
            "c,b",
            "d,a",
            "d,b-c,a",
            "a-d",
            "a-c,b-d",
            "d,d",
            "a",
            "c",
        ],
    },
    "data2": {
        "HEAP_STACK": "sepermutationofpc234n112nandzqisthenumberofcyclesofthepermutationqexamplea49indeedp34121324istheonlyinvolutionof1234withgenus0thisfollowseasilyfromthefactthatapermutationpof12nhasgenus0ifandonlyifthecycledecompositionofpgivesanoncrossingpartitionof12nandeachcycleofpisincreasingseelemma21ofthedulucqsimionreferencealsoredundantlyforp34121324wehavecp2341341241231432andsogp1241211emericdeutschmay292010letwijndenotewalksinn2whichsatisfythemultivariaterecurrencewijnwij1n1wi1jn1wi1j1n1withboundaryconditionsw0001andwijn0ifiorjornis0thenansumi0nj0nwijnisthenumberofsuchwalksoflengthnpeterluschnymay212011anan1tendsto30asninfinity12cos2pinrelatingtolongestoddnregularpolygondiagonalsbywayofexamplen7usingthetridiagonalgeneratorcfcommentofjan072009forpolygonn7weextractann123x3matrix010111011withanevalof224697thelongestheptagondiagonalwithedge1asntendstoinfinitythediagonallengthstendto30theconvergentofthesequencegarywadamsonjun082011numberofn1lengthpermutationsavoidingthepattern132andthedottedpattern23dot1jeanlucbarilmar072012numberofnlengthwordswoveralphabetabcsuchthatforeveryprefixzofwwehavezazbzcwherezxcountsthelettersxinwordzthea49wordsareaaaaaaabaabaabaaaabbababaabcabacabcaaloispheinzmay262012numberoflengthnrestrictedgrowthstringsrgsr1r2rnsuchthatr11rkkandrkrk1forexamplethe9rgsforn4are101010121201121012121230123112321234joergarndtapr162013numberoflengthnrestrictedgrowthstringsrgsr1r2rnsuchthatr10rkkandrkrk11forexamplethe9rgsforn4are000000020003000400220024003302220224joergarndtapr172013numberof42315276143avoidinginvolutionsinsnalexanderbursteinmar052014anisthenumberofincreasingunarybinarytreeswithnnodeswhohaveanassociatedpermutationavoids132formoreinformationaboutunarybinarytreeswithassociatedpermutationsseea245888mandariehlaug072014anisthenumberofinvolutionsonnavoidingthesinglepatternpwherepisanyoneofthe8classicalpatterns12341243143221342143321434124321alsonumberof3412241334123142341224133142avoidinginvolutionsonnbecauseeachofthese3setsactuallycoincideswiththe3412avoidinginvolutionsonnthisisacompletelistofthe8singles2pairsand1tripleof4letterclassicalpatternswhoseinvolutionavoidersarecountedbythemotzkinnumbersseebarnabeietal2011referencedavidcallanaug272014fromtonyfosteriiijul282016startaseriescreatedusing2anan1hashankeltransformoff2noffset3fbeingthefibonaccibisectiona001906empiricalobservationaseriescreatedusing2an3an1an2givesthehankeltransformofsumk0nkfibonacci2koffset3a197649empiricalobservationendconjecture2nsumk1n2k1ak2isanintegerforeachpositiveintegernzhiweisunnov162017therubeyandstumpreferenceprovesarefinementofaconjectureofrenmarczinzikwhichtheystateasthenumberof2gorensteinalgebraswhicharenakayamaalgebraswithnsimplemodulesandhaveanorientedlineasassociatedquiverequalsthenumberofmotzkinpathsoflengthnericmschmidtdec162017numberofukequivalenceclassesofukasiewiczpathsukasiewiczpathsarepequivalentiffthepositionsofpatternpareidenticalinthesepathssergeykirgizovapr082018iftau1andtau2aretwodistinctpermutationpatternschosenfromtheset132231312thenanisthenumberofvalidhookconfigurationsofpermutationsofn1thatavoidthepatternstau1andtau2colindefantapr282019numberofpermutationsoflengthnthataresortedtotheidentitybyaconsecutive321avoidingstackfollowedbyaclassical21avoidingstackcolindefantaug292020fromhelmutprodingerdec132020startanisthenumberofpathsinthefirstquadrantstartingat00andconsistingofnstepsfromtheinfiniteset11111213forexampledenotingu11d11dj1jforj2a4countsuuuuuuuduuud2uuud3uuduuudduud2uuduuududthisstepsetisinspiredby11111315suggestedbyemericdeutscharound2000seeprodingerlinkthatcontainsabijectiontomotzkinpathsendnamedbydonaghey1977aftertheisraeliamericanmathematiciantheodoremotzkin19081970insloanesahandbookofintegersequences1973theywerecalledgeneralizedballotnumbersamirameldarapr152021numberofmotzkinnpathsanissplitintoa107587nnumberofevenmotzkinnpathsanda343386nnumberofoddmotzkinnpathsthevaluea107587na343386ncanbecalledtheshadowofanseea343773gennadyereminmay172021conjectureifpisaprimeoftheform6m1a002476thenap2isdivisiblebypcurrentlynocounterexampleexistsforp107personalcommunicationfromrobertgerbiczmodsuchpthisisequivalenttoa066796withcommenteverya066796nfroma066796p12toa066796p1isdivisiblebyprimepofform6m1sergebatalovfeb082022frompeterbalafeb102022startconjectures1forprimep1mod6andnr1anpr2a005717n1modpwherewetakea00571700tomatchbatalovsconjectureabove2forprimep5mod6andn1anp2a005773nmodp3forprimep3andk1anpkanmodpfor0npk34forprimep5andk2anpkanmodp2for0npk13endthehankeltransformofthissequencewitha0omittedgivestheperiod6sequence101101whichisa010892withitsfirsttermomittedwhilethehankeltransformofthecurrentsequenceistheallonessequencea000012andalsoitistheuniquesequencewiththispropertywhichissimilartotheuniquehankeltransformpropertyofthecatalannumbersmichaelsomosapr172022referencesebarcuccirpinzaniandrsprugnolithemotzkinfamilypumaseravol21991no34pp249279fbergeronlfavreauanddkrobconjecturesontheenumerationoftableauxofboundedheightdiscretemathvol139no131995463468frbernhartcatalanmotzkinandriordannumbersdiscrmath204199973112rbojicicandmdpetkovicorthogonalpolynomialsapproachtothehankeltransformofsequencesbasedonmotzkinnumbersbulletinofthemalaysianmathematicalsciences2015doi101007s4084001502493miklosbonaeditorhandbookofenumerativecombinatoricscrcpress2015pp24298618912alinbostancalculformelpourlacombinatoiredesmarcheshabilitationdirigerdesrechercheslaboratoiredinformatiquedeparisnorduniversitparis13december2017httpsspecfuninriafrbostanhdrpdfajbuautomatedcountingofrestrictedmotzkinpathsenumerativecombinatoricsandapplicationseca122021articles2r12naiomicameronjemcleodreturnsandhillsongeneralizeddyckpathsjournalofintegersequencesvol1920161661lcarlitzsolutionofcertainrecurrencessiamjapplmath171969251259michaeldairykosamanthatynerlarapudwellandcaseywynnnoncontiguouspatternavoidanceinbinarytreeselectronjcombin192012no3paper2221ppmr2967227dedavenportlwshapiroandlcwoodsonthedoubleriordangrouptheelectronicjournalofcombinatorics1822012p33edeutschandlshapiroasurveyofthefinenumbersdiscretemath2412001241265tdoslicdsvrtananddveljanenumerativeaspectsofsecondarystructuresdiscrmath28520046782tomislavdoslicanddarkoveljanlogarithmicbehaviorofsomecombinatorialsequencesdiscretemath3082008no1121822212mr24045442009j05019sdulucqandrsimioncombinatorialstatisticsonalternatingpermutationsjalgebraiccombinatorics81998169191mdziemianczukenumerationsofplanetreeswithmultipleedgesandraneylatticepathsdiscretemathematics3372014924wenjiefangapartialorderonmotzkinpathsdiscretemath3432020111802ipgouldenanddmjacksoncombinatorialenumerationwileyny19835210nssgunyliandtmansour2binarytreesbijectionsandrelatedissuesdiscrmath308200812091221krishatchpresentationofthemotzkinmonoidseniorthesisunivcalsantabarbara2012httpccsmathucsbeduseniorthesiskrishatchpdfvjelinektoufikmansourandmshattuckonmultiplepatternavoidingsetpartitionsadvancesinappliedmathematicsvolume50issue2february2013pp292326hanakimandrpstanleyarefinedenumerationofhextreesandrelatedpolynomialshttpwwwmathmitedurstanpapershextreespdfpreprint2015skitaevpatternsinpermutationsandwordsspringerverlag2011seep399tablea7akuznetsovetaltreesassociatedwiththemotzkinnumbersjcombintheorya761996145147tlengyelondivisibilitypropertiesofsomedifferencesofmotzkinnumbersannalesmathematicaeetinformaticae412013pp121136walorenzypontyandpcloteasymptoticsofrnashapesjournalofcomputationalbiology20081513163doi101089cmb20060153pieramanaraandclaudioperellicippothefinestructureof4321avoidinginvolutionsand321avoidinginvolutionspumavol222011227238httpwwwmatunisiitnewsitopumapublichtml222manaraperellicippopdftoufikmansourrestricted132permutationsandgeneralizedpatternsannalsofcombin620026576toufikmansourmatthiasschorkandmarkshattuckcatalannumbersandpatternrestrictedsetpartitionsdiscretemath3122012no2029792991mr2956089tsmotzkinrelationsbetweenhypersurfacecrossratiosandacombinatorialformulaforpartitionsofapolygonforpermanentpreponderanceandfornonassociativeproductsbullamermathsoc541948352360jocelynquaintanceandharriskwongacombinatorialinterpretationofthecatalanandbellnumberdifferencetablesintegers132013a29jriordanenumerationofplanetreesbybranchesandendpointsjcombintheorya231975214222asapounakisetalorderedtreesandtheinordertransversaldiscmath306200617321741asapounakisitasoulasandptsikourascountingstringsindyckpathsdiscretemath307200729092924eschroederviercombinatorischeproblemezfmathphys151870361376lwshapiroetaltheriordangroupdiscreteappliedmath341991229239markshattuckonthezerosofsomepolynomialswithcombinatorialcoefficientsannalesmathematicaeetinformaticae422013pp93101httpamiektfhunjasloaneahandbookofintegersequencesacademicpress1973includesthissequencenjasloaneandsimonplouffetheencyclopediaofintegersequencesacademicpress1995includesthissequencemichaelzspiveyandlauralsteilthekbinomialtransformsandthehankeltransformjournalofintegersequencesvol92006article0611rpstanleyenumerativecombinatoricscambridgevol21999seeproblem637alsoproblem716by3nprsteinandmswatermanonsomenewsequencesgeneralizingthecatalanandmotzkinnumbersdiscretemath261979261272zwsunconjecturesinvolvingarithmeticalsequencesnumbertheoryarithmeticinshangrilaedsskanemitsuhzliandjyliuprocthe6thchinajapansemnumbertheoryshanghaiaugust15172011worldscisingapore2013pp244258httpmathnjueducnzwsun142ppdfchenyingwangpiotrmiskaandistvnmeztherderangementnumbersdiscretemathematics3407201716811692yingwangandguocexinaclassificationofmotzkinnumbersmodulo8electronjcombin2512018p154wenjinwoanacombinatorialproofofarecursiverelationofthemotzkinsequencebylatticepathsfibonacciquart402002no138wenjinwoanarecursiverelationforweightedmotzkin12",
        "SEARCH_QUERIES": [
            "a-z",
            "0-9",
            "0-4,5-9",
            "0-9,a-z",
            "m-z,k-n,1,9",
            "a,e,i,o,u,y",
            "a-j,6-9",
            "c-o,w-z,3,8",
            "n-w,c-j,1,4,5,9",
            "r-s,y-z,j-k,3",
            "d,v,z,7,b,f,k,n,q,8,y",
            "g-k,a-f,x-z,b-d",
        ],
    },
}


def get_start_parameters(start_data: str | None = None):
    def parse(data):
        # Placeholder for parsing logic
        return data

    if start_data and start_data in SAMPLES:
        HEAP_STACK = SAMPLES[start_data]["HEAP_STACK"]
        SEARCH_QUERIES = SAMPLES[start_data]["SEARCH_QUERIES"]
    else:
        w, h = [int(i) for i in input().split()]
        HEAP_STACK = [input().strip() for _ in range(h)]
        HEAP_STACK = "".join(HEAP_STACK)
        n = int(input())
        SEARCH_QUERIES = [input().strip() for _ in range(n)]

    return HEAP_STACK, SEARCH_QUERIES


def generate_single_set(str):
    # Takes a simple string like "a-c" or "0-9" and returns a set of characters
    if len(str) == 1:
        return {str}
    if len(str) != 3 or str[1] != "-":
        raise ValueError("Invalid range format")
    start, end = str[0], str[2]
    start_idx = LIST_OF_CHAR.index(start)
    end_idx = LIST_OF_CHAR.index(end)
    res = set()
    for i in range(start_idx, end_idx + 1):
        res.add(LIST_OF_CHAR[i])
    return res


def generate_full_set(query: str) -> set:
    # Takes a query like "a-c,1-3,x,z" and returns a set of characters
    parts = query.split(",")
    full_set = set()
    for part in parts:
        single_set = generate_single_set(part)
        full_set.update(single_set)
    return full_set


def is_contained(sub_set: str, start_idx: int, end_idx_int) -> bool:
    # checks if the set of characters sub_set is fully contained in HEAP_STACK[start_idx:end_idx]
    sub_heap = set(HEAP_STACK[start_idx : end_idx_int + 1])
    res = sub_set - sub_heap
    return len(res) == 0


def find_longest_needle(needle_query, start_idx):
    end_idx = start_idx
    needle_set = generate_full_set(needle_query)
    while True:
        if end_idx >= len(HEAP_STACK):
            return -1
        if is_contained(needle_set, start_idx, end_idx):
            return end_idx
        end_idx += 1


def shorten_needle(needle_query, start_idx, end_idx):
    needle_set = generate_full_set(needle_query)
    while True:
        start_idx += 1
        if not is_contained(needle_set, start_idx, end_idx):
            return start_idx - 1


def find_shortest_needle(needle_query):
    start_idx = 0
    res = []
    while start_idx < len(HEAP_STACK):
        end_idx = find_longest_needle(needle_query, start_idx)
        start_idx = shorten_needle(needle_query, start_idx, end_idx)
        if start_idx == -1 or end_idx == -1:
            break
        res.append((start_idx, end_idx))
        start_idx += 1

    sorted_res = sorted(res, key=lambda tup: (tup[1] - tup[0], tup[0]))
    return sorted_res[0]


# ********************************************************

HEAP_STACK, SEARCH_QUERIES = get_start_parameters("data1")

for needle_query in SEARCH_QUERIES:
    res = find_shortest_needle(needle_query)
    print(res[0], res[1])
