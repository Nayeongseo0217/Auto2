import openai
import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time
from streamlit_option_menu import option_menu
import datetime
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="Auto Connect Chat Bot",  page_icon="https://ifh.cc/g/P8K9BV.png", layout="centered", initial_sidebar_state="expanded")

with st.sidebar:
    choice = option_menu("MENU", ["원클릭으로 나에게 맞는 모빌리티 추천 서비스", "온라인 상담사와 함께하는 모빌리티 컨설팅", "상담사 바로 연결하기"],
                         icons=['bi bi-hand-index-fill', 'bi bi-person-circle', 'bi bi-telephone-outbound-fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#0D6FBA"},
    }
    )

if choice == "원클릭으로 나에게 맞는 모빌리티 추천 서비스":

    custom_header = """
        <style>
        /* Streamlit 기본 헤더와 푸터 숨기기 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .center-img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%; /* <- 여기가 이미지 사이즈 조절하는 곳입니다~ */
        }
        </style>
    """
    st.markdown(custom_header, unsafe_allow_html=True)

    # https://ifh.cc/g/P8K9BV.png <- 오토커넥트 로고 이미지 url입니다.

    image_url = "https://ifh.cc/g/P8K9BV.png"
    st.markdown(f"""
        <div style="text-align: center;">
            <img src="{image_url}" class="center-img" alt="Auto Connect Logo">
        </div>
    """, unsafe_allow_html=True)


    page_bg = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
    }
    </style>
    '''
    st.markdown(page_bg, unsafe_allow_html=True)

    st.title("AUTO CONNECT CHAT BOT")

    st.markdown("""
    안녕하세요. 환영합니다!<br><br>
    자동차 종합 모빌리티 플랫폼 오토커넥트입니다!<br><br>
    나만의 모빌리티를 찾기 위한 여정, 너무 어려우시죠?<br>
    오토커넥트 나만의 AI파트너, "AUTO CONNECT CHAT BOT"이 도와드리겠습니다^^<br><br>
    *언제든지 더 자세한 상담을 원하신다면 지금 바로 전화해주세요! 상담가능 시간(00:00~23:59)<br>
    -> 전화 상담 : 010 - 4433 - 1708
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    def main():
        pages = {
            "main": main_page,
            "manufacturer": manufacturer_page,
            "model": model_page,
            "submodel": submodel_page
        }

        if "page" not in st.session_state:
            st.session_state.page = "main"
        
        pages[st.session_state.page]()

    def main_page():
        st.write("자동차 제조사를 선택하세요")
        
        manufacturers = {
            "현대": "https://file.cartner.kr/assets/images/brand/20221214095246420.png",
            "제네시스": "https://file.cartner.kr/assets/images/brand/20220921152125483.png",
            "기아": "https://file.cartner.kr/assets/images/brand/20210120174425118.png",
            "쉐보레": "https://file.cartner.kr/assets/images/brand/20201208181121596.png",
            "KG모빌리티": "https://file.cartner.kr/assets/images/brand/20230406133530420.png",
            "르노": "https://file.cartner.kr/assets/images/brand/20240403102049490.png",
            "다피코": "https://file.cartner.kr/assets/images/brand/20230424091829566.png",
            "스마트 EV": "https://file.cartner.kr/assets/images/brand/20240131102725606.png",
            "마이브": "https://file.cartner.kr/assets/images/brand/20220510100133723.gif",
            "벤츠": "https://file.cartner.kr/assets/images/brand/20201029103011923.png",
            "BMW": "https://file.cartner.kr/assets/images/brand/20201029102620474.png",
            "아우디": "https://file.cartner.kr/assets/images/brand/20201208181455790.png",
            "폭스바겐": "https://file.cartner.kr/assets/images/brand/20220510100809233.png",
            "미니": "https://file.cartner.kr/assets/images/brand/20201028113446186.png",
            "볼보": "https://file.cartner.kr/assets/images/brand/20220225115936490.png",
            "폴스타": "https://file.cartner.kr/assets/images/brand/20220119092723270.png",
            "랜드로버": "https://file.cartner.kr/assets/images/brand/20201028111236546.png",
            "포르쉐": "https://file.cartner.kr/assets/images/brand/20201028112134627.png",
            "람보르기니": "https://file.cartner.kr/assets/images/brand/20240422173352961.png",
            "벤틀리": "https://file.cartner.kr/assets/images/brand/20201028111930656.png",
            "맥라렌": "https://file.cartner.kr/assets/images/brand/20201028111353471.png",
            "페라리": "https://file.cartner.kr/assets/images/brand/20201028112527222.png",
            "에스턴마틴": "https://file.cartner.kr/assets/images/brand/20201028111711775.png",
            "로터스": "https://file.cartner.kr/assets/images/brand/20220510101934912.png",
            "마세라티": "https://file.cartner.kr/assets/images/brand/20220921152013149.png",
            "롤스로이스": "https://file.cartner.kr/assets/images/brand/20201028111545347.png",
            "푸조": "https://file.cartner.kr/assets/images/brand/20210308160525480.png",
            "이네오스": "https://file.cartner.kr/assets/images/brand/20240418174440746.png",
            "포드": "https://file.cartner.kr/assets/images/brand/20201028112054275.png",
            "링컨": "https://file.cartner.kr/assets/images/brand/20201028111557815.png",
            "지프": "https://file.cartner.kr/assets/images/brand/20201028112447456.png",
            "GMC": "https://file.cartner.kr/assets/images/brand/20230103094619477.png",
            "캐딜락": "https://file.cartner.kr/assets/images/brand/20221121090638501.png",
            "테슬라": "https://file.cartner.kr/assets/images/brand/20201028112520954.png",
            "토요타": "https://file.cartner.kr/assets/images/brand/20201028111212557.png",
            "렉서스": "https://file.cartner.kr/assets/images/brand/20201028112607227.png",
            "혼다": "https://file.cartner.kr/assets/images/brand/20201029103043373.png"
        }
        
        cols = st.columns(5)
        for i, (name, img_url) in enumerate(manufacturers.items()):
            with cols[i % 5]:
                image = resize_image(img_url, (150, 150))
                st.image(image, caption=name, use_column_width=True)
                st.write(f"<div style='text-align: center;'>", unsafe_allow_html=True)
                if st.button(name, key=name):
                    st.session_state.manufacturer = name
                    st.session_state.page = "manufacturer"
                    st.experimental_rerun()
                st.write("</div>", unsafe_allow_html=True)
            
            if (i + 1) % 5 == 0:
                st.write("")

    def resize_image(url, size):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize(size)
        return img

    def manufacturer_page():
        st.write(f"{st.session_state.manufacturer}의 차종을 선택하세요")

        models = {
            "현대": [
                        "캐스퍼",
                        "캐스퍼 일렉트릭",
                        "더 뉴 아반떼(CN7 F/L)",
                        "더 뉴 아반떼N(CN7 F/L)",
                        "더 뉴 아반떼 HEV(CN7 F/L)",
                        "쏘나타 디 엣지(DN8 F/L)",
                        "쏘나타 디 엣지 HEV(DN8 F/L)",
                        "아이오닉6",
                        "디 올-뉴 그랜저(GN7)",
                        "디 올-뉴 그랜저 HEV(GN7)",
                        "베뉴",
                        "디 올 뉴 코나(SX2)",
                        "디 올 뉴 코나 HEV(SX2)",
                        "디 올 뉴 코나 EV(SX2)",
                        "넥쏘",
                        "더 뉴 투싼 (NX4 F/L)",
                        "더 뉴 투싼 HEV(NX4 F/L)",
                        "디 올-뉴 싼타페(MX5)",
                        "디 올-뉴 싼타페 HEV(MX 5)",
                        "더 뉴 아이오닉5",
                        "아이오닉5",
                        "아이오닉5N",
                        "더 뉴 팰리세이드",
                        "스타리아",
                        "스타리아 HEV",
                        "스타리아 아클란",
                        "스타리아 아클란S",
                        "ST1",
                        "더 뉴 포터 II",
                        "더 뉴 포터 II 특장차",
                        "포터II EV",
                        "포터II EV 특장차",
                        "올 뉴마이티",
                        "쏠라티"],
            "제네시스": [
                        "더 뉴 G70",
                        "더 뉴 G70 슈팅브레이크",
                        "G80(RG3 F/L)",
                        "G80(RG3)",
                        "e-G80(RG3)",
                        "신형 G90(RS4)",
                        "GV60(JW)",
                        "GV70(JK F/L)",
                        "GV70(JK)",
                        "e-GV70(JK)",
                        "GV80(JX F/L)",
                        "GV80 쿠페(JX F/L)",
                        "GV80(JX)"],
            "기아": [
                        "더 뉴 모닝(JA PE)",
                        "더 뉴 기아 레이(PE)",
                        "레이 EV(PE)",
                        "더 뉴 K3",
                        "더 뉴 K3 GT",
                        "더 뉴 K5(DL3 F/L)",
                        "더 뉴 K5 HEV(DL3 F/L)",
                        "더 뉴 K8(GL3 F/L)",
                        "더 뉴 K8 HEV(GL3 F/L)",
                        "K8(GL3)",
                        "K8 HEV(GL3)",
                        "더 뉴 K9(RJ)",
                        "디 올 뉴 니로(SG2)",
                        "디 올 뉴 니로 EV(SG2)",
                        "니로 플러스(DE)",
                        "EV3",
                        "더 뉴 셀토스",
                        "디 올뉴스포티지(NQ5)",
                        "디 올뉴스포티지 HEV(NQ5)",
                        "더 뉴 쏘렌토(MQ4 F/L)",
                        "더 뉴 쏘렌토 HEV(MQ4 F/L)",
                        "더 뉴 EV6",
                        "EV6",
                        "EV6 GT",
                        "EV9",
                        "모하비 더 마스터",
                        "더 뉴 카니발(KA4 F/L)",
                        "더 뉴 카니발 HEV(KA4 F/L)",
                        "카니발 헤리티지",
                        "더 뉴봉고III(PU)",
                        "더 뉴봉고III 특장차",
                        "봉고III EV(PU)",
                        "봉고III EV 특장차"
                    ],
            "쉐보레": [
                "더 뉴 트레일블레이저",
                "트랙스 크로스오버",
                "더 뉴 트래버스",
                "타호(5세대)",
                "신형 콜로라도(3세대)",
            ],
            "KG모빌리티": ["더 뉴 티볼리",
                    "더 뉴 티볼리 에어",
                    "리스펙 코란도",
                    "코란도 EV",
                    "더 뉴 토레스",
                    "토레스(J100)",
                    "토레스 EVX(U100)",
                    "렉스턴 뉴 아레나",
                    "렉스턴 스포츠 쿨멘",
                    "렉스턴 스포츠 쿨멘 칸"],
            "르노": [
                "더 뉴 SM6",
                "아르카나",
                "아르카나 HEV",
                "XM3",
                "XM3 E-Tech HEV",
                "그랑 콜레오스",
                "그랑 콜레오스 HEV",
                "더 뉴 QM6(PE)",
                "더 뉴 QM6 퀘스트 (PE)",
                "뉴 마스터",
            ],
            "다피코": [
                "포트로",
                "포트로",
                ],
            "스마트 EV": [
                "EV Z",
                "D2C",
                "D2P",
                ],
            "마이브": [
                "M1",
                ],
            "벤츠": [
                        "A-Class(4세대)",
                        "CLA-Class(2세대 F/L)",
                        "The New C-Class(W206)",
                        "The New E-Class(W214)",
                        "EQE",
                        "EQE-SUV",
                        "S-Class(W223)",
                        "Maybach S-Class(W223)",
                        "EQS",
                        "EQS-SUV",
                        "CLE-Class",
                        "SL-Class(R232)",
                        "The New AMG GT 4DOOR",
                        "GLA-Class",
                        "The new EQA",
                        "EQA",
                        "GLB-Class",
                        "The new EQB",
                        "EQB",
                        "The New GLC-Class(2세대)",
                        "The New GLE-class(2세대 F/L)",
                        "The New GLS-Class(2세대 F/L)",
                        "The New Maybach GLS-Class",
                        "Maybach GLS-Class",
                        "G-Class(W463)",
                    ],
            "BMW": [
                "1 Series(3세대)",
                "2 Series GranCoupe(2세대)",
                "THE New 3 Series(G20/G)",
                "4 Series(2세대)",
                "i4",
                "5 Series(G60)",
                "i5 (G60)",
                "NEW 6 Series GT",
                "7 Series(G70)",
                "i7",
                "The New 8 Series(2세대 F/L)",
                "2 Series Coupe(2세대)",
                "M2(2세대)",
                "M3(6세대)",
                "M4(2세대)",
                "M5(6세대 F/L)",
                "The New M8",
                "The New Z4(3세대 F/L)",
                "X1(3세대)",
                "iX1",
                "X2(2세대)",
                "X3(3세대 F/L)",
                "iX3",
                "The New X3M",
                "X4(2세대)",
                "The New X4M",
                "iX",
                "The New X5(4세대 F/L)",
                "The New X5M(4세대 F/L)",
                "The New X6(3세대 F/L)",
                "The New X6M(3세대 F/L)",
                "The New X7(1세대 F/L)",
                "XM",
                "2 Series Active Tourer",
            ],
            "아우디": [
                "A3(8Y)",
                "S3(8Y)",
                "RS3(*Y)",
                "New A4(B9 F/L)",
                "New S4(B9 F/L)",
                "New A5(2세대 F/L)",
                "New S5(2세대 F/L)",
                "RS5(2세대 F/L)",
                "A6(C8)",
                "S6(C8)",
                "RS6 Avant(C8)",
                "A7(2세대)",
                "S7(2세대)",
                "RS7(2세대)",
                "The New A8(D5)",
                "The New S8(D5)",
                "e-tron GT",
                "RS e-tron GT",
                "The New Q2(1세대 F/L)",
                "Q3(2세대)",
                "Q4 E-tron",
                "New Q5(2세대 F/L)",
                "New SQ5(2세대 F/L)",
                "New Q7(2세대 F/L)",
                "SQ7(2세대 F/L)",
                "Q8",
                "RS Q8",
                "Q8 E-tron",
                "SQ8 E-tron",
                "e-tron",
                "e-tron S",
            ],
            "폭스바겐": [
                "Golf(8세대)",
                "Golf GTI(8세대)",
                "New Jetta(7세대)",
                "New Arteon(1세대 F/L)",
                "ID4",
                "New Tiguan(2세대 F/L)",
                "The New Touareg(3세대 F/L)",],
            "미니": [
                "Hatch(F65/66)",
                "New Hatch(F56 F/L)",
                "New cooper Convertible(3세대 F/L)",
                "Clubman(2세대 F/L)",
                "Countryman(3세대)",
                "Countryman(2세대 F/L)",
            ],
            "볼보": [
                "S60(3세대)",
                "V60 CrossCountry(2세대)",
                "New S90(2세대 F/L)",
                "S90 Recharge",
                "V90 CrossCountry(2세대)",
                "New XC40(1세대 F/L)",
                "New XC40 Recharge",
                "C40 Recharge",
                "EX30",
                "New XC60(2세대 F/L)",
                "XC60 Recharge",
                "New XC90(2세대 F/L)",
                "XC90 Recharge",],
            "폴스타": [
                "Polestar 2(F/L)",
                "Polestar 4",
                ],
            "랜드로버": [
                "Range Rover Evoque(2세대 F/L)",
                "New Discovery Sport(1세대 F/L)",
                "Range Rover Velar(1세대 F/L)",
                "Range Rover Sport(3세대)",
                "Discovery5(L462 F/L)",
                "Defender(2세대)",
                "Range Rover(5세대)",
            ],
            "포르쉐": [
                "718 Boxter(982)",
                "718 Cayman(982)",
                "911(992)",
                "Taycan(F/L)",
                "Taycan",
                "The New Panamera(3세대)",
                "Macan Electric(2세대)",
                "New Macan(95B F/L)",
                "New Cayenne(3세대 F/L)",],
            "람보르기니": [
                "Huracan EVO",
                "Urus",
                ],
            "벤틀리": [
                "Flying Spur(3세대)",
                "Continental GT(3세대)",
                "New Bentayga(1세대 F/L)",],
            "맥라렌": [
                "Artura",],
            "페라리": [
                "296 GTB",
                "SF90",
                "812 GTS",
                "Roma",
                "Purosangue",
                ],
            "에스턴마틴": [
                "Vantage(2세대)",
                "DBS",
                "DBX",],
            "로터스": [
                "Emira(1세대)",
                "Eletre"],
            "마세라티": [
                "GranTurismo(2세대)",
                "GranCabrio(2세대)",
                "MC20",
                "MC20 Cielo",
                "Grecale"],
            "롤스로이스": [
                "Ghost(2세대)",
                "Phantom SeriesⅡ(8세대 F/L)",
                "Spectre",
                "Cullinan"],
            "푸조": [
                "E-208",
                "308(3세대)",
                "E-2008",
                "408",
                "New 3008(2세대 F/L)",
                "New 5008(2세대 F/L)"],
            "이네오스": [
                "Grenadier"],
            "포드": [
                "All New Mustang(7세대)",
                "Bronco(6세대)",
                "Exploler(6세대)",
                "New Expedition(4세대 F/L)",
                "All New Ranger(4세대)"],
            "링컨": [
                "All New Nautilus",
                "Aviator(2세대)",
                "New Navigator(4세대 f/L)"],
            "지프": [
                "Renegade(BU F/L)",
                "Avenger",
                "Wrangler(JL F/L)",
                "All New Grand Cherokee(WL)",
                "Grand CherokeeL(WL)",
                "Gladiator"],
            "GMC": [
                "Sierra(5세대 F/L)"],
            "캐딜락": [
                "CT5-V",
                "The New XT4",
                "LYRIQ",
                "XT6",
                "Escalade(5세대)"],
            "테슬라": [
                "New Model 3",
                "New Model S",
                "Model Y",
                "New Model X"],
            "토요타": [
                "Prius(5세대)",
                "The New Camry(10세대 F/L)",
                "Crown Crossover",
                "GR86(2세대)",
                "GR Supra(3세대)",
                "The New RAV4(5세대 F/L)",
                "HighLander(4세대)",
                "Sienna(4세대)",
                "Alphard(4세대)"],
            "렉서스": [
                "THE New ES(7세대)",
                "THE New LS(5세대)",
                "LC(1세대)",
                "UX(1세대)",
                "NX(2세대)",
                "RZ",
                "RX(5세대)",
                "LM"],
            "혼다": [
                "Accord(11세대)",
                "All New CR-V(6세대)",
                "All New Pilot(4세대)",
                "The New Odyssey(5세대 F/L)"]
        }

        model_images = {
            "현대": [
                "https://file.cartner.kr/assets/images/model/20220616132134844.png",
                "https://file.cartner.kr/assets/images/model/20240709085800471.png",
                "https://file.cartner.kr/assets/images/model/20230313092821122.png",
                "https://file.cartner.kr/assets/images/model/20230726090545460.png",
                "https://file.cartner.kr/assets/images/model/20230313092855361.png",
                "https://file.cartner.kr/assets/images/model/20230420092324909.png",
                "https://file.cartner.kr/assets/images/model/20230420092400819.png",
                "https://file.cartner.kr/assets/images/model/20220726143317667.png",
                "https://file.cartner.kr/assets/images/model/20221116175303468.png",
                "https://file.cartner.kr/assets/images/model/20221116175309626.png",
                "https://file.cartner.kr/assets/images/model/20201029165258431.png",
                "https://file.cartner.kr/assets/images/model/20230118093755355.png",
                "https://file.cartner.kr/assets/images/model/20230118093830670.png",
                "https://file.cartner.kr/assets/images/model/20230413092418592.png",
                "https://file.cartner.kr/assets/images/model/20201029165019510.png",
                "https://file.cartner.kr/assets/images/model/20231121092123723.png",
                "https://file.cartner.kr/assets/images/model/20231121092149242.png",
                "https://file.cartner.kr/assets/images/model/20230814091809518.png",
                "https://file.cartner.kr/assets/images/model/20230814091823945.png",
                "https://file.cartner.kr/assets/images/model/20240305114215425.png",
                "https://file.cartner.kr/assets/images/model/20210420095045803.png",
                "https://file.cartner.kr/assets/images/model/20230904090554415.png",
                "https://file.cartner.kr/assets/images/model/20220518175451326.png",
                "https://file.cartner.kr/assets/images/model/20220618190826652.png",
                "https://file.cartner.kr/assets/images/model/20240228095405339.png",
                "https://file.cartner.kr/assets/images/model/20221108092319591.png",
                "https://file.cartner.kr/assets/images/model/20221108101956490.png",
                "https://file.cartner.kr/assets/images/model/20240423143723210.png",
                "https://file.cartner.kr/assets/images/model/20220608112634343.png",
                "https://file.cartner.kr/assets/images/model/20220727085153639.png",
                "https://file.cartner.kr/assets/images/model/20201029152347251.png",
                "https://file.cartner.kr/assets/images/model/20220725110432376.png",
                "https://file.cartner.kr/assets/images/model/20211103161832371.png",
                "https://file.cartner.kr/assets/images/model/20201029164820867.png"
            ],
            "제네시스": [
                "https://file.cartner.kr/assets/images/model/20220627141459924.png",
                "https://file.cartner.kr/assets/images/model/20220627092755700.png",
                "https://file.cartner.kr/assets/images/model/20231226090342885.png",
                "https://file.cartner.kr/assets/images/model/20220628094427347.png",
                "https://file.cartner.kr/assets/images/model/20210708130440843.png",
                "https://file.cartner.kr/assets/images/model/20211215100408649.png",
                "https://file.cartner.kr/assets/images/model/20221123175522104.png",
                "https://file.cartner.kr/assets/images/model/20240508090253799.png",
                "https://file.cartner.kr/assets/images/model/20201218171103266.png",
                "https://file.cartner.kr/assets/images/model/20220302141145129.png",
                "https://file.cartner.kr/assets/images/model/20230927101117812.png",
                "https://file.cartner.kr/assets/images/model/20230927101143106.png",
                "https://file.cartner.kr/assets/images/model/20220628094438747.png"
            ],
            "기아": [
                "https://file.cartner.kr/assets/images/model/20230705090803502.png",
                "https://file.cartner.kr/assets/images/model/20220810091940524.png",
                "https://file.cartner.kr/assets/images/model/20230823133938186.png",
                "https://file.cartner.kr/assets/images/model/20220524145800771.png",
                "https://file.cartner.kr/assets/images/model/20220623102317506.png",
                "https://file.cartner.kr/assets/images/model/20231025094031145.png",
                "https://file.cartner.kr/assets/images/model/20231025094107201.png",
                "https://file.cartner.kr/assets/images/model/20240809100916821.png",
                "https://file.cartner.kr/assets/images/model/20240809100939195.png",
                "https://file.cartner.kr/assets/images/model/20220519141847116.png",
                "https://file.cartner.kr/assets/images/model/20220519141951718.png",
                "https://file.cartner.kr/assets/images/model/20220627152508963.png",
                "https://file.cartner.kr/assets/images/model/20220228083827948.png",
                "https://file.cartner.kr/assets/images/model/20220524145429363.png",
                "https://file.cartner.kr/assets/images/model/20220524145435672.png",
                "https://file.cartner.kr/assets/images/model/20240604175602933.png",
                "https://file.cartner.kr/assets/images/model/20220630091118820.png",
                "https://file.cartner.kr/assets/images/model/20220524145557285.png",
                "https://file.cartner.kr/assets/images/model/20220524145605466.png",
                "https://file.cartner.kr/assets/images/model/20230821090408926.png",
                "https://file.cartner.kr/assets/images/model/20230821090514671.png",
                "https://file.cartner.kr/assets/images/model/20240514090207411.png",
                "https://file.cartner.kr/assets/images/model/20220519142048341.png",
                "https://file.cartner.kr/assets/images/model/20220929093923420.png",
                "https://file.cartner.kr/assets/images/model/20230503094733528.png",
                "https://file.cartner.kr/assets/images/model/20201029164219405.png",
                "https://file.cartner.kr/assets/images/model/20231108155751535.png",
                "https://file.cartner.kr/assets/images/model/20231108155806284.png",
                "https://file.cartner.kr/assets/images/model/20240805094627756.png",
                "https://file.cartner.kr/assets/images/model/20201029170524448.png",
                "https://file.cartner.kr/assets/images/model/20220725115022902.PNG",
                "https://file.cartner.kr/assets/images/model/20201029170534361.png",
                "https://file.cartner.kr/assets/images/model/20220725120118718.PNG"
            ],
            "쉐보레": [
                "https://file.cartner.kr/assets/images/model/20230719144358971.png",
                "https://file.cartner.kr/assets/images/model/20230322113751213.png",
                "https://file.cartner.kr/assets/images/model/20220127165428118.png",
                "https://file.cartner.kr/assets/images/model/20220126142528401.png",
                "https://file.cartner.kr/assets/images/model/20240715105513130.png"
            ],
            "KG모빌리티": [
                "https://file.cartner.kr/assets/images/model/20230601154910551.png",
                "https://file.cartner.kr/assets/images/model/20230601154934305.png",
                "https://file.cartner.kr/assets/images/model/20201029152008286.png",
                "https://file.cartner.kr/assets/images/model/20240604175746678.png",
                "https://file.cartner.kr/assets/images/model/20240509085718452.png",
                "https://file.cartner.kr/assets/images/model/20220612163421610.png",
                "https://file.cartner.kr/assets/images/model/20230331093756545.png",
                "https://file.cartner.kr/assets/images/model/20240812151639672.png",
                "https://file.cartner.kr/assets/images/model/20230503150744412.png",
                "https://file.cartner.kr/assets/images/model/20230503143928658.png",
                "https://file.cartner.kr/assets/images/model/20230503144001963.png"
            ],
            "르노": [
                   "https://chais.co.kr/assets/images//model/20201029151929476.png",
                   "https://chais.co.kr/assets/images//model/20240403103401755.png",
                   "https://chais.co.kr/assets/images//model/20240403103423512.png",
                   "https://chais.co.kr/assets/images//model/20220629091946646.png",
                   "https://chais.co.kr/assets/images//model/20220930171532248.png",
                   "https://chais.co.kr/assets/images//model/20220930171532248.png",
                   "https://chais.co.kr/assets/images//model/20220930171532248.png",
                   "https://chais.co.kr/assets/images//model/20220930171532248.png",
                   "https://chais.co.kr/assets/images//model/20220930171532248.png",
                   "https://chais.co.kr/assets/images//model/20201029151914401.png",
                   ],
            "다피코": [
                "https://chais.co.kr/assets/images//model/20231129145804219.png",
                "https://chais.co.kr/assets/images//model/20220921131736630.png"
            ],
            "스마트 EV": [
                "https://chais.co.kr/assets/images//model/20230314170922230.png",
                "https://chais.co.kr/assets/images//model/20230314170937976.png",
                "https://chais.co.kr/assets/images//model/20230314170952641.png"
            ],
            "마이브": [
                "https://chais.co.kr/assets/images//model/20230717100925410.png"
            ],
            "벤츠": [
                "https://file.cartner.kr/assets/images/model/20231030150224563.png",
                "https://file.cartner.kr/assets/images/model/20231226140825805.png",
                "https://file.cartner.kr/assets/images/model/20220630095239606.png",
                "https://file.cartner.kr/assets/images/model/20240122090155657.png",
                "https://file.cartner.kr/assets/images/model/20220923175910347.png",
                "https://file.cartner.kr/assets/images/model/20230712155309303.png",
                "https://file.cartner.kr/assets/images/model/20220630094204439.png",
                "https://file.cartner.kr/assets/images/model/20220714133635938.png",
                "https://file.cartner.kr/assets/images/model/20211122111150261.png",
                "https://file.cartner.kr/assets/images/model/20221006092721465.png",
                "https://file.cartner.kr/assets/images/model/20240802170426351.png",
                "https://file.cartner.kr/assets/images/model/20240219110436247.png",
                "https://file.cartner.kr/assets/images/model/20231031142723591.png",
                "https://file.cartner.kr/assets/images/model/20220613145211412.png",
                "https://file.cartner.kr/assets/images/model/20240131120335662.png",
                "https://file.cartner.kr/assets/images/model/20240527102921566.png",
                "https://file.cartner.kr/assets/images/model/20231221171110917.png",
                "https://file.cartner.kr/assets/images/model/20240527103055403.png",
                "https://file.cartner.kr/assets/images/model/20230608142815463.png",
                "https://file.cartner.kr/assets/images/model/20230829131521921.png",
                "https://file.cartner.kr/assets/images/model/20231113111440248.png",
                "https://file.cartner.kr/assets/images/model/20240131113508170.png",
                "https://file.cartner.kr/assets/images/model/20220616114521942.png"
            ],
            "BMW": [
                "https://file.cartner.kr/assets/images/model/20220629090517362.png",
                "https://file.cartner.kr/assets/images/model/20201029153620580.png",
                "https://file.cartner.kr/assets/images/model/20221026091208131.png",
                "https://file.cartner.kr/assets/images/model/20240729112546722.png",
                "https://file.cartner.kr/assets/images/model/20210208140640782.png",
                "https://file.cartner.kr/assets/images/model/20220324172344625.PNG",
                "https://file.cartner.kr/assets/images/model/20230906094007281.png",
                "https://file.cartner.kr/assets/images/model/20230906094048916.png",
                "https://file.cartner.kr/assets/images/model/20201029152712181.png",
                "https://file.cartner.kr/assets/images/model/20220926104526636.png",
                "https://file.cartner.kr/assets/images/model/20220926104327697.png",
                "https://file.cartner.kr/assets/images/model/20220705145120772.png",
                "https://file.cartner.kr/assets/images/model/20220612200800952.png",
                "https://file.cartner.kr/assets/images/model/20230704104548507.png",
                "https://file.cartner.kr/assets/images/model/20210416111049821.png",
                "https://file.cartner.kr/assets/images/model/20240805113400933.png",
                "https://file.cartner.kr/assets/images/model/20210416112208101.png",
                "https://file.cartner.kr/assets/images/model/20220629090636597.png",
                "https://file.cartner.kr/assets/images/model/20220914154700533.png",
                "https://file.cartner.kr/assets/images/model/20230313133238822.png",
                "https://file.cartner.kr/assets/images/model/20230329123631386.png",
                "https://file.cartner.kr/assets/images/model/20230329123733508.png",
                "https://file.cartner.kr/assets/images/model/20240404110356899.png",
                "https://file.cartner.kr/assets/images/model/20211103130615239.png",
                "https://file.cartner.kr/assets/images/model/20211123095828280.png",
                "https://file.cartner.kr/assets/images/model/20211111094336863.png",
                "https://file.cartner.kr/assets/images/model/20211103130712102.png",
                "https://file.cartner.kr/assets/images/model/20211111094249935.png",
                "https://file.cartner.kr/assets/images/model/20221206105016200.png",
                "https://file.cartner.kr/assets/images/model/20230707130116833.png",
                "https://file.cartner.kr/assets/images/model/20230725152650493.png",
                "https://file.cartner.kr/assets/images/model/20230707130151450.png",
                "https://file.cartner.kr/assets/images/model/20230725153031391.png",
                "https://file.cartner.kr/assets/images/model/20220824131920208.png",
                "https://file.cartner.kr/assets/images/model/20230329124922736.png",
                "https://file.cartner.kr/assets/images/model/20220804150247832.png"

            ],
            "아우디": [
                "https://chais.co.kr/assets/images//model/20220712174015838.png",
                "https://chais.co.kr/assets/images//model/20221220091525753.png",
                "https://chais.co.kr/assets/images//model/20230724090935737.png",
                "https://chais.co.kr/assets/images//model/20220617120121213.png",
                "https://chais.co.kr/assets/images//model/20220620140341859.png",
                "https://chais.co.kr/assets/images//model/20220527113834810.png",
                "https://chais.co.kr/assets/images//model/20220620135552872.png",
                "https://chais.co.kr/assets/images//model/20220616124627535.png",
                "https://chais.co.kr/assets/images//model/20220616130716628.PNG",
                "https://chais.co.kr/assets/images//model/20201029173838394.png",
                "https://chais.co.kr/assets/images//model/20220616112025768.PNG",
                "https://chais.co.kr/assets/images//model/20201029173801559.png",
                "https://chais.co.kr/assets/images//model/20201029173851643.png",
                "https://chais.co.kr/assets/images//model/20201029173851643.png",
                "https://chais.co.kr/assets/images//model/20221012102658642.png",
                "https://chais.co.kr/assets/images//model/20230704091128755.png",
                "https://chais.co.kr/assets/images//model/20211213173743483.png",
                "https://chais.co.kr/assets/images//model/20220506161013712.png",
                "https://chais.co.kr/assets/images//model/20220506161013712.png",
                "https://chais.co.kr/assets/images//model/20220629091713834.png",
                "https://chais.co.kr/assets/images//model/20220906130929120.png",
                "https://chais.co.kr/assets/images//model/20211109091631422.png",
                "https://chais.co.kr/assets/images//model/20220629091634146.png",
                "https://chais.co.kr/assets/images//model/20201029173704458.png",
                "https://chais.co.kr/assets/images//model/20240103090652931.png",
                "https://chais.co.kr/assets/images//model/20201029173809501.png",
                "https://chais.co.kr/assets/images//model/20220616104556664.png",
                "https://chais.co.kr/assets/images//model/20240610132600643.png",
                "https://chais.co.kr/assets/images//model/20240610132629214.png",
                "https://chais.co.kr/assets/images//model/20201029173857710.png",
                "https://chais.co.kr/assets/images//model/20220616125724275.png",
            ],
            "폭스바겐": [
                "https://file.cartner.kr/assets/images/model/20220106103033378.png",
                "https://file.cartner.kr/assets/images/model/20221201090415275.png",
                "https://file.cartner.kr/assets/images/model/20221014103443583.png",
                "https://file.cartner.kr/assets/images/model/20220106104220412.png",
                "https://file.cartner.kr/assets/images/model/20220906132207815.png",
                "https://file.cartner.kr/assets/images/model/20211109092450439.png",
                "https://file.cartner.kr/assets/images/model/20240806094727444.png"],
            "미니": [
                "https://file.cartner.kr/assets/images/model/20240703094130736.png",
                "https://file.cartner.kr/assets/images/model/20211112170104971.png",
                "https://file.cartner.kr/assets/images/model/20211112170141477.png",
                "https://file.cartner.kr/assets/images/model/20220628162649273.png",
                "https://file.cartner.kr/assets/images/model/20240614090548973.png",
                "https://file.cartner.kr/assets/images/model/20220628162637948.png"
            ],
            "볼보": [
                "https://file.cartner.kr/assets/images/model/20221006170303670.png",
                "https://file.cartner.kr/assets/images/model/20221006170315268.png",
                "https://file.cartner.kr/assets/images/model/20201029160330777.png",
                "https://file.cartner.kr/assets/images/model/20220418161254641.png",
                "https://file.cartner.kr/assets/images/model/20211230115728187.png",
                "https://file.cartner.kr/assets/images/model/20220817111128149.png",
                "https://file.cartner.kr/assets/images/model/20220817111011356.png",
                "https://file.cartner.kr/assets/images/model/20220216091401620.png",
                "https://file.cartner.kr/assets/images/model/20231114145326368.png",
                "https://file.cartner.kr/assets/images/model/20211230115651957.png",
                "https://file.cartner.kr/assets/images/model/20220418161853328.png",
                "https://file.cartner.kr/assets/images/model/20201029160307484.png",
                "https://file.cartner.kr/assets/images/model/20220418162114849.png",],
            "폴스타": [
                "https://file.cartner.kr/assets/images/model/20231026090556385.png",
                "https://file.cartner.kr/assets/images/model/20231026090556385.png"],
            "랜드로버": [
                "https://file.cartner.kr/assets/images//model/20240124105009520.png",
                "https://chais.co.kr/assets/images//model/20240124114901237.png",
                "https://chais.co.kr/assets/images//model/20240124105047104.png",
                "https://chais.co.kr/assets/images//model/20220921113658669.png",
                "https://chais.co.kr/assets/images//model/20220930175154600.png",
                "https://chais.co.kr/assets/images//model/20211109092555808.png",
                "https://chais.co.kr/assets/images//model/20211105090014444.png",
            ],
            "포르쉐": [
                "https://file.cartner.kr/assets/images/model/20201029161145557.png",
                "https://file.cartner.kr/assets/images/model/20210108131603946.png",
                "https://file.cartner.kr/assets/images/model/20201029161250186.png",
                "https://file.cartner.kr/assets/images/model/20240307152722162.png",
                "https://file.cartner.kr/assets/images/model/20220612180512667.png",
                "https://file.cartner.kr/assets/images/model/20231127091649818.png",
                "https://file.cartner.kr/assets/images/model/20240717111517393.png",
                "https://file.cartner.kr/assets/images/model/20211108112424904.png",
                "https://file.cartner.kr/assets/images/model/20230608142604753.png"],
            "람보르기니": [
                "https://file.cartner.kr/assets/images/model/20201029155232601.png",
                "https://file.cartner.kr/assets/images/model/20201029155214257.png"],
            "벤틀리": [
                "https://file.cartner.kr/assets/images/model/20210224180538186.png",
                "https://file.cartner.kr/assets/images/model/20220517165014709.png",
                "https://file.cartner.kr/assets/images/model/20220110170847878.png"],
            "맥라렌": [
                "https://file.cartner.kr/assets/images/model/20211008140204349.png"],
            "페라리": [
                "https://file.cartner.kr/assets/images/model/20220121103920451.png",
                "https://file.cartner.kr/assets/images/model/20210310181632860.png",
                "https://file.cartner.kr/assets/images/model/20211019100843184.png",
                "https://file.cartner.kr/assets/images/model/20211019101247965.png",
                "https://file.cartner.kr/assets/images/model/20221021144807263.png"],
            "에스턴마틴": [
                "https://file.cartner.kr/assets/images/model/20220628153638790.png",
                "https://file.cartner.kr/assets/images/model/20221207090838402.png",
                "https://file.cartner.kr/assets/images/model/20220629092135997.png"],
            "로터스": [
                "https://file.cartner.kr/assets/images/model/20230912104928644.png",
                "https://file.cartner.kr/assets/images/model/20230925111250869.png"],
            "마세라티": [
                "https://file.cartner.kr/assets/images/model/20240717092123853.png",
                "https://file.cartner.kr/assets/images/model/20240717092908199.png",
                "https://file.cartner.kr/assets/images/model/20211213173119452.png",
                "https://file.cartner.kr/assets/images/model/20230406093626771.png",
                "https://file.cartner.kr/assets/images/model/20221117105849575.png"],
            "롤스로이스": [
                "https://file.cartner.kr/assets/images/model/20201029155552222.png",
                "https://file.cartner.kr/assets/images/model/20221125105925539.png",
                "https://file.cartner.kr/assets/images/model/20230619110416595.png",
                "https://file.cartner.kr/assets/images/model/20210126114226518.png"],
            "푸조": [
                "https://file.cartner.kr/assets/images/model/20220620102810743.png",
                "https://file.cartner.kr/assets/images/model/20220914170202732.png",
                "https://file.cartner.kr/assets/images/model/20220523090736733.png",
                "https://file.cartner.kr/assets/images/model/20230523105424296.png",
                "https://file.cartner.kr/assets/images/model/20220616102007156.png",
                "https://file.cartner.kr/assets/images/model/20211115101448400.png"],
            "이네오스": [
                "https://file.cartner.kr/assets/images/model/20240419090154738.png"],
            "포드": [
                "https://file.cartner.kr/assets/images/model/20240116105148595.png",
                "https://file.cartner.kr/assets/images/model/20220623145523788.png",
                "https://file.cartner.kr/assets/images/model/20220629102241956.png",
                "https://file.cartner.kr/assets/images/model/20220729104302359.png",
                "https://file.cartner.kr/assets/images/model/20230116090935549.png"],
            "링컨": [
                "https://file.cartner.kr/assets/images/model/20231102141535545.png",
                "https://file.cartner.kr/assets/images/model/20230425170428783.png",
                "https://file.cartner.kr/assets/images/model/20220922090827242.png"],
            "지프": [
                "https://file.cartner.kr/assets/images/model/20220628163530994.png",
                "https://file.cartner.kr/assets/images/model/20240725085841886.png",
                "https://file.cartner.kr/assets/images/model/20240103131514477.png",
                "https://file.cartner.kr/assets/images/model/20221123094700920.png",
                "https://file.cartner.kr/assets/images/model/20211230115502596.png",
                "https://file.cartner.kr/assets/images/model/20201029160700496.png"],
            "GMC": [
                "https://file.cartner.kr/assets/images/model/20230207092502638.png"],
            "캐딜락": [
                "https://file.cartner.kr/assets/images/model/20220303165613954.png",
                "https://file.cartner.kr/assets/images/model/20240503171723650.png",
                "https://file.cartner.kr/assets/images/model/20240527102730107.png",
                "https://file.cartner.kr/assets/images/model/20220629101747485.png",
                "https://file.cartner.kr/assets/images/model/20211020092021498.png"],
            "테슬라": [
                "https://file.cartner.kr/assets/images/model/20240404113842827.png",
                "https://file.cartner.kr/assets/images/model/20220613160037200.png",
                "https://file.cartner.kr/assets/images/model/20210218093010980.png",
                "https://file.cartner.kr/assets/images/model/20220613160045562.png"],
            "토요타": [
                "https://file.cartner.kr/assets/images/model/20231213090743275.png",
                "https://file.cartner.kr/assets/images/model/20211230114518160.png",
                "https://file.cartner.kr/assets/images/model/20230605112739885.png",
                "https://file.cartner.kr/assets/images/model/20220517120654643.png",
                "https://file.cartner.kr/assets/images/model/20201029153745782.png",
                "https://file.cartner.kr/assets/images/model/20220613161122519.png",
                "https://file.cartner.kr/assets/images/model/20230725092306454.png",
                "https://file.cartner.kr/assets/images/model/20210407105905601.png",
                "https://file.cartner.kr/assets/images/model/20230918090029533.png"],
            "렉서스": [
                "https://file.cartner.kr/assets/images/model/20211230114709989.png",
                "https://file.cartner.kr/assets/images/model/20201029153925238.png",
                "https://file.cartner.kr/assets/images/model/20201029153917679.png",
                "https://file.cartner.kr/assets/images/model/20220629090736569.png",
                "https://file.cartner.kr/assets/images/model/20220629090821644.png",
                "https://file.cartner.kr/assets/images/model/20230621102531774.png",
                "https://file.cartner.kr/assets/images/model/20230621103704317.png",
                "https://file.cartner.kr/assets/images/model/20240611133518539.png"],
            "혼다": [
                "https://file.cartner.kr/assets/images/model/20231010135447436.png",
                "https://file.cartner.kr/assets/images/model/20230411101043752.png",
                "https://file.cartner.kr/assets/images/model/20230829105342788.png",
                "https://file.cartner.kr/assets/images/model/20211230114420456.png"]
        }
        
        cols = st.columns(3)
        for i, model in enumerate(models[st.session_state.manufacturer]):
            with cols[i % 3]:
                model_img_url = model_images[st.session_state.manufacturer][i]
                st.image(model_img_url, caption=model, use_column_width=True)
                st.write(f"<div style='text-align: center;'>", unsafe_allow_html=True)
                if st.button(model, key=model):
                    st.session_state.model = model
                    st.session_state.page = "model"
                    st.experimental_rerun()
                st.write("</div>", unsafe_allow_html=True)
        
        if st.button("이전", key="back_main"):
            st.session_state.page = "main"
            st.experimental_rerun()

    def model_page():
        st.header(f"{st.session_state.manufacturer} - {st.session_state.model} 세부모델 선택")
        st.write("추후 업데이트 예정")
        
        if st.button("이전", key="back_manufacturer"):
            st.session_state.page = "manufacturer"
            st.experimental_rerun()

    def submodel_page():
        st.header(f"{st.session_state.manufacturer} - {st.session_state.model} 세부모델")
        st.write("추후 업데이트 예정")
        
        if st.button("이전", key="back_model"):
            st.session_state.page = "model"
            st.experimental_rerun()

    if __name__ == "__main__":
        main()

        # 고객님 정보 이메일 발송 코드    
    # if current_state == "상담 신청하기":
    #         personal_consultation_form()
    # if current_state == "상담 신청하기1":
    #         personal_consultation_form1()
    #     if current_state == "상담 신청하기2":
    #         personal_consultation_form2()
    #     if current_state == "상담 신청하기3":
    #         personal_consultation_form3()
    #     if current_state == "상담 신청하기4":
    #         personal_consultation_form4()

    # def personal_consultation_form():
    #     with st.form("personal_consultation"):
    #         st.write("이름을 적어주세요.")
    #         name = st.text_input("이름")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("이메일을 적어주세요.")
    #         email = st.text_input("이메일")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("전화번호를 적어주세요.")
    #         phone = st.text_input("전화번호")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("성별과 나이대를 적어주세요.")
    #         gender_age = st.text_input("성별과 나이대")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("희망 차종과 브랜드를 적어주세요.")
    #         car_brand = st.text_input("희망 차종과 브랜드")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("희망 주행거리를 입력해주세요.")
    #         mileage = st.text_input("희망 주행거리")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("추가로 희망하는 사항을 적어주세요.")
    #         additional_info = st.text_input("추가로 희망하는 사항")
            
    #         submitted = st.form_submit_button("전송")

    #         if submitted:
    #             if send_email(name, email, phone, gender_age, car_brand, mileage, additional_info):
    #                 st.success("신청이 완료되었습니다!")
    #             else:
    #                 st.error("이메일 전송에 실패했습니다. 인터넷 연결을 다시 확인해보시거나, 다시 시도해주세요!")

    # def send_email(name, email, phone, gender_age, car_brand, mileage, additional_info):
    #     from_address = "AutoConnectChatBot@gmail.com"  # 보내는 사람 이메일 주소
    #     to_address = "nays43883@naver.com"
    #     subject = "(일반 상담 요청) 오토커넥트 챗봇에서 보낸 상담 요청 인적사항입니다"
        
    #     body = f"""
    #     요청자가 선택한 컨설팅은 일반 상담 요청입니다^^
        
    #     이름: {name}
    #     이메일: {email}
    #     전화번호: {phone}
    #     성별과 나이대: {gender_age}
    #     희망 차종과 브랜드: {car_brand}
    #     희망 주행거리: {mileage}
    #     추가로 희망하는 사항: {additional_info}
    #     """
        
    #     msg = MIMEText(body)
    #     msg["Subject"] = subject
    #     msg["From"] = from_address
    #     msg["To"] = to_address
        
    #     try:
    #         server = smtplib.SMTP("smtp.gmail.com", 587)  # SMTP 서버 및 포트 번호
    #         server.starttls()
    #         server.login("AutoConnectChatBot@gmail.com", "fwbzxrgzujmkcgua")  # 로그인 정보
    #         server.sendmail(from_address, to_address, msg.as_string())
    #         server.quit()
    #         return True
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return False

    # def personal_consultation_form1():
    #     with st.form("personal_consultation"):
    #         st.write("이름을 적어주세요.")
    #         name = st.text_input("이름")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("이메일을 적어주세요.")
    #         email = st.text_input("이메일")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("전화번호를 적어주세요.")
    #         phone = st.text_input("전화번호")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("성별과 나이대를 적어주세요.")
    #         gender_age = st.text_input("성별과 나이대")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("희망 차종과 브랜드를 적어주세요.")
    #         car_brand = st.text_input("희망 차종과 브랜드")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("희망 주행거리를 입력해주세요.")
    #         mileage = st.text_input("희망 주행거리")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("추가로 희망하는 사항을 적어주세요.")
    #         additional_info = st.text_input("추가로 희망하는 사항")
            
    #         submitted = st.form_submit_button("전송")

    #         if submitted:
    #             if send_email1(name, email, phone, gender_age, car_brand, mileage, additional_info):
    #                 st.success("신청이 완료되었습니다!")
    #             else:
    #                 st.error("이메일 전송에 실패했습니다. 인터넷 연결을 다시 확인해보시거나, 다시 시도해주세요!")

    # def send_email1(name, email, phone, gender_age, car_brand, mileage, additional_info):
    #     from_address = "AutoConnectChatBot@gmail.com"  # 보내는 사람 이메일 주소
    #     to_address = "nays43883@naver.com"
    #     subject = "(중고차구매) 오토커넥트 챗봇에서 보낸 상담 요청 인적사항입니다"
        
    #     body = f"""
    #     요청자가 선택한 컨설팅은 중고차구매입니다^^

    #     이름: {name}
    #     이메일: {email}
    #     전화번호: {phone}
    #     성별과 나이대: {gender_age}
    #     희망 차종과 브랜드: {car_brand}
    #     희망 주행거리: {mileage}
    #     추가로 희망하는 사항: {additional_info}
    #     """
        
    #     msg = MIMEText(body)
    #     msg["Subject"] = subject
    #     msg["From"] = from_address
    #     msg["To"] = to_address
        
    #     try:
    #         server = smtplib.SMTP("smtp.gmail.com", 587)  # SMTP 서버 및 포트 번호
    #         server.starttls()
    #         server.login("AutoConnectChatBot@gmail.com", "fwbzxrgzujmkcgua")  # 로그인 정보
    #         server.sendmail(from_address, to_address, msg.as_string())
    #         server.quit()
    #         return True
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return False

    # def personal_consultation_form2():
    #     with st.form("personal_consultation"):
    #         st.write("이름을 적어주세요.")
    #         name = st.text_input("이름")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("이메일을 적어주세요.")
    #         email = st.text_input("이메일")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("전화번호를 적어주세요.")
    #         phone = st.text_input("전화번호")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("성별과 나이대를 적어주세요.")
    #         gender_age = st.text_input("성별과 나이대")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("희망 차종과 브랜드를 적어주세요.")
    #         car_brand = st.text_input("희망 차종과 브랜드")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("희망 주행거리를 입력해주세요.")
    #         mileage = st.text_input("희망 주행거리")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("추가로 희망하는 사항을 적어주세요.")
    #         additional_info = st.text_input("추가로 희망하는 사항")
            
    #         submitted = st.form_submit_button("전송")

    #         if submitted:
    #             if send_email2(name, email, phone, gender_age, car_brand, mileage, additional_info):
    #                 st.success("신청이 완료되었습니다!")
    #             else:
    #                 st.error("이메일 전송에 실패했습니다. 인터넷 연결을 다시 확인해보시거나, 다시 시도해주세요!")

    # def send_email2(name, email, phone, gender_age, car_brand, mileage, additional_info):
    #     from_address = "AutoConnectChatBot@gmail.com"  # 보내는 사람 이메일 주소
    #     to_address = "nays43883@naver.com"
    #     subject = "(리스렌트 승계) 오토커넥트 챗봇에서 보낸 상담 요청 인적사항입니다"
        
    #     body = f"""
    #     요청자가 선택한 컨설팅은 리스렌트 승계입니다^^

    #     이름: {name}
    #     이메일: {email}
    #     전화번호: {phone}
    #     성별과 나이대: {gender_age}
    #     희망 차종과 브랜드: {car_brand}
    #     희망 주행거리: {mileage}
    #     추가로 희망하는 사항: {additional_info}
    #     """
        
    #     msg = MIMEText(body)
    #     msg["Subject"] = subject
    #     msg["From"] = from_address
    #     msg["To"] = to_address
        
    #     try:
    #         server = smtplib.SMTP("smtp.gmail.com", 587)  # SMTP 서버 및 포트 번호
    #         server.starttls()
    #         server.login("AutoConnectChatBot@gmail.com", "fwbzxrgzujmkcgua")  # 로그인 정보
    #         server.sendmail(from_address, to_address, msg.as_string())
    #         server.quit()
    #         return True
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return False

    # def personal_consultation_form3():
    #     with st.form("personal_consultation"):
    #         st.write("이름을 적어주세요.")
    #         name = st.text_input("이름")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("이메일을 적어주세요.")
    #         email = st.text_input("이메일")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("전화번호를 적어주세요.")
    #         phone = st.text_input("전화번호")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("성별과 나이대를 적어주세요.")
    #         gender_age = st.text_input("성별과 나이대")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("희망 차종과 브랜드를 적어주세요.")
    #         car_brand = st.text_input("희망 차종과 브랜드")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("희망 주행거리를 입력해주세요.")
    #         mileage = st.text_input("희망 주행거리")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("추가로 희망하는 사항을 적어주세요.")
    #         additional_info = st.text_input("추가로 희망하는 사항")
            
    #         submitted = st.form_submit_button("전송")

    #         if submitted:
    #             if send_email3(name, email, phone, gender_age, car_brand, mileage, additional_info):
    #                 st.success("신청이 완료되었습니다!")
    #             else:
    #                 st.error("이메일 전송에 실패했습니다. 인터넷 연결을 다시 확인해보시거나, 다시 시도해주세요!")

    # def send_email3(name, email, phone, gender_age, car_brand, mileage, additional_info):
    #     from_address = "AutoConnectChatBot@gmail.com"  # 보내는 사람 이메일 주소
    #     to_address = "nays43883@naver.com"
    #     subject = "(A/S 사후관리) 오토커넥트 챗봇에서 보낸 상담 요청 인적사항입니다"
        
    #     body = f"""
    #     요청자가 선택한 컨설팅은 A/S 사후관리입니다^^

    #     이름: {name}
    #     이메일: {email}
    #     전화번호: {phone}
    #     성별과 나이대: {gender_age}
    #     희망 차종과 브랜드: {car_brand}
    #     희망 주행거리: {mileage}
    #     추가로 희망하는 사항: {additional_info}
    #     """
        
    #     msg = MIMEText(body)
    #     msg["Subject"] = subject
    #     msg["From"] = from_address
    #     msg["To"] = to_address
        
    #     try:
    #         server = smtplib.SMTP("smtp.gmail.com", 587)  # SMTP 서버 및 포트 번호
    #         server.starttls()
    #         server.login("AutoConnectChatBot@gmail.com", "fwbzxrgzujmkcgua")  # 로그인 정보
    #         server.sendmail(from_address, to_address, msg.as_string())
    #         server.quit()
    #         return True
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return False

    # def personal_consultation_form4():
    #     with st.form("personal_consultation"):
    #         st.write("이름을 적어주세요.")
    #         name = st.text_input("이름")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("이메일을 적어주세요.")
    #         email = st.text_input("이메일")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("전화번호를 적어주세요.")
    #         phone = st.text_input("전화번호")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("성별과 나이대를 적어주세요.")
    #         gender_age = st.text_input("성별과 나이대")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("희망 차종과 브랜드를 적어주세요.")
    #         car_brand = st.text_input("희망 차종과 브랜드")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("희망 주행거리를 입력해주세요.")
    #         mileage = st.text_input("희망 주행거리")
    #         st.markdown("<hr>", unsafe_allow_html=True)
            
    #         st.write("추가로 희망하는 사항을 적어주세요.")
    #         additional_info = st.text_input("추가로 희망하는 사항")
            
    #         submitted = st.form_submit_button("전송")

    #         if submitted:
    #             if send_email4(name, email, phone, gender_age, car_brand, mileage, additional_info):
    #                 st.success("신청이 완료되었습니다!")
    #             else:
    #                 st.error("이메일 전송에 실패했습니다. 인터넷 연결을 다시 확인해보시거나, 다시 시도해주세요!")

    # def send_email4(name, email, phone, gender_age, car_brand, mileage, additional_info):
    #     from_address = "AutoConnectChatBot@gmail.com"  # 보내는 사람 이메일 주소
    #     to_address = "nays43883@naver.com"
    #     subject = "(법인 전문 컨설팅 의뢰) 오토커넥트 챗봇에서 보낸 상담 요청 인적사항입니다"
        
    #     body = f"""
    #     요청자가 선택한 컨설팅은 법인 전문입니다^^

    #     이름: {name}
    #     이메일: {email}
    #     전화번호: {phone}
    #     성별과 나이대: {gender_age}
    #     희망 차종과 브랜드: {car_brand}
    #     희망 주행거리: {mileage}
    #     추가로 희망하는 사항: {additional_info}
    #     """
        
    #     msg = MIMEText(body)
    #     msg["Subject"] = subject
    #     msg["From"] = from_address
    #     msg["To"] = to_address
        
    #     try:
    #         server = smtplib.SMTP("smtp.gmail.com", 587)  # SMTP 서버 및 포트 번호
    #         server.starttls()
    #         server.login("AutoConnectChatBot@gmail.com", "fwbzxrgzujmkcgua")  # 로그인 정보
    #         server.sendmail(from_address, to_address, msg.as_string())
    #         server.quit()
    #         return True
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return False


    # handle_buttons()

st.markdown("<hr>", unsafe_allow_html=True)

API_KEY = st.secrets['OPENAI_API_KEY']

# OpenAI 클라이언트 초기화
client = openai.OpenAI(api_key=API_KEY)

# 스레드 관리용 session_state 초기화
if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

thread_id = st.session_state.thread_id
assistant_id = "asst_GyHpEq4rKyMTSm05AbShypNc"  # 사용자 정의 어시스턴트 ID

if choice == "온라인 상담사와 함께하는 모빌리티 컨설팅":
    custom_header = """
        <style>
        /* Streamlit 기본 헤더와 푸터 숨기기 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .center-img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%; /* <- 여기가 이미지 사이즈 조절하는 곳입니다~ */
        }
        </style>
    """
    st.markdown(custom_header, unsafe_allow_html=True)

    # https://ifh.cc/g/P8K9BV.png <- 오토커넥트 로고 이미지 url입니다.

    image_url = "https://ifh.cc/g/P8K9BV.png"
    st.markdown(f"""
        <div style="text-align: center;">
            <img src="{image_url}" class="center-img" alt="Auto Connect Logo">
        </div>
    """, unsafe_allow_html=True)


    page_bg = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
    }
    </style>
    '''
    st.markdown(page_bg, unsafe_allow_html=True)

    st.title("AUTO CONNECT CHAT BOT")

    st.markdown("""
    안녕하세요. 환영합니다!<br><br>
    자동차 종합 모빌리티 플랫폼 오토커넥트입니다!<br><br>
    나만의 모빌리티를 찾기 위한 여정, 너무 어려우시죠?<br>
    오토커넥트 나만의 AI파트너, "AUTO CONNECT CHAT BOT"이 도와드리겠습니다^^<br><br>
    *언제든지 더 자세한 상담을 원하신다면 지금 바로 전화해주세요! 상담가능 시간(00:00~23:59)<br>
    -> 전화 상담 : 010 - 4433 - 1708
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # 새로운 메시지 입력
    prompt = st.chat_input("오토커넥트 챗봇에게 물어보세요!")
    if prompt:
        # 사용자의 메시지 스레드에 추가
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt,
        )
    
        # 어시스턴트 응답 실행
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
    
        while run.status != "completed":
            time.sleep(0.2)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
    
        # 어시스턴트의 응답 메시지 가져오기
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
        )
    
        # 어시스턴트의 응답 메시지 출력
        for msg in reversed(messages.data):
            role = "나" if msg.role == "user" else "오토커넥트 챗봇"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
            if msg.role == "user":
                st.markdown(
                    f'''
                    <div style="text-align: right; margin-bottom: 10px;">
                        <div style="display: inline-block; padding: 10px; border-radius: 10px; background-color: #F2F2F2; max-width: 70%;">
                            {msg.content[0].text.value}
                            <div style="font-size: 10px; text-align: left; margin-top: 5px;">
                                {timestamp}
                            </div>
                        </div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
            else:
                with st.spinner('오토커넥트 챗봇이 답변하는 중...'):
                    st.markdown(
                        f'''
                        <div style="text-align: left; margin-bottom: 10px;">
                            <div style="display: flex; align-items: flex-start;">
                                <div style="flex-shrink: 0; border-radius: 50%; width: 40px; height: 40px; background-color: #A0B4F2; display: flex; align-items: center; justify-content: center; margin-right: 10px;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" class="bi bi-car-front-fill" viewBox="0 0 16 16">
                                        <path d="M2.52 3.515A2.5 2.5 0 0 1 4.82 2h6.362c1 0 1.904.596 2.298 1.515l.792 1.848c.075.175.21.319.38.404.5.25.855.715.965 1.262l.335 1.679q.05.242.049.49v.413c0 .814-.39 1.543-1 1.997V13.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-1.338c-1.292.048-2.745.088-4 .088s-2.708-.04-4-.088V13.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-1.892c-.61-.454-1-1.183-1-1.997v-.413a2.5 2.5 0 0 1 .049-.49l.335-1.68c.11-.546.465-1.012.964-1.261a.8.8 0 0 0 .381-.404l.792-1.848ZM3 10a1 1 0 1 0 0-2 1 1 0 0 0 0 2m10 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2M6 8a1 1 0 0 0 0 2h4a1 1 0 1 0 0-2zM2.906 5.189a.51.51 0 0 0 .497.731c.91-.073 3.35-.17 4.597-.17s3.688.097 4.597.17a.51.51 0 0 0 .497-.731l-.956-1.913A.5.5 0 0 0 11.691 3H4.309a.5.5 0 0 0-.447.276L2.906 5.19Z"/>
                                    </svg>
                                </div>
                                <div style="display: flex; flex-direction: column; flex-grow: 1;">
                                    <strong>{role}</strong>
                                    <div style="display: inline-block; padding: 10px; border-radius: 10px; background-color: #A0B4F2; max-width: 100%; word-wrap: break-word;">
                                        {msg.content[0].text.value}
                                        <div style="font-size: 10px; text-align: right; margin-top: 5px;">
                                            {timestamp}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )
    
        print(run)
        print(message)

if choice == "상담사 바로 연결하기":
    custom_header = """
        <style>
        /* Streamlit 기본 헤더와 푸터 숨기기 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .center-img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%; /* <- 여기가 이미지 사이즈 조절하는 곳입니다~ */
        }
        </style>
    """
    st.markdown(custom_header, unsafe_allow_html=True)

    # https://ifh.cc/g/P8K9BV.png <- 오토커넥트 로고 이미지 url입니다.

    image_url = "https://ifh.cc/g/P8K9BV.png"
    st.markdown(f"""
        <div style="text-align: center;">
            <img src="{image_url}" class="center-img" alt="Auto Connect Logo">
        </div>
    """, unsafe_allow_html=True)


    page_bg = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
    }
    </style>
    '''
    st.markdown(page_bg, unsafe_allow_html=True)

    st.title("AUTO CONNECT CHAT BOT")

    def personal_consultation_form():
        with st.form("personal_consultation"):
            st.write("이름을 적어주세요.")
            name = st.text_input("ex) 홍길동")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("이메일을 적어주세요.")
            email = st.text_input("ex) KoreanP12345@naver.com")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("전화번호를 적어주세요.")
            phone = st.text_input("ex) 010-1234-5678")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("성별과 나이대를 적어주세요.")
            gender_age = st.text_input("ex) 남자, 20대 후반")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 차종과 브랜드를 적어주세요.")
            car_brand = st.text_input("ex) 현대 캐스퍼")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 주행거리를 입력해주세요.")
            mileage = st.text_input("ex) 2만km 이하")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("추가로 희망하는 사항을 적어주세요.")
            additional_info = st.text_input("ex) 중고차로 알아보고 있습니다. 주말 낮에 전화상담 가능할까요?")
            
            submitted = st.form_submit_button("전송")

            if submitted:
                if send_email(name, email, phone, gender_age, car_brand, mileage, additional_info):
                    st.success("신청이 완료되었습니다!")
                else:
                    st.error("이메일 전송에 실패했습니다. 인터넷 연결을 다시 확인해보시거나, 다시 시도해주세요!")

    def send_email(name, email, phone, gender_age, car_brand, mileage, additional_info):
        from_address = "AutoConnectChatBot@gmail.com"  # 보내는 사람 이메일 주소
        to_address = "nays43883@naver.com"
        subject = "(상담 요청) 오토커넥트 챗봇에서 보낸 상담 요청 인적사항입니다"
        
        body = f"""
        요청자가 선택한 컨설팅은 상담 요청입니다^^
        
        이름: {name}
        이메일: {email}
        전화번호: {phone}
        성별과 나이대: {gender_age}
        희망 차종과 브랜드: {car_brand}
        희망 주행거리: {mileage}
        추가로 희망하는 사항: {additional_info}
        """
        
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_address
        msg["To"] = to_address
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)  # SMTP 서버 및 포트 번호
            server.starttls()
            server.login("AutoConnectChatBot@gmail.com", "fwbzxrgzujmkcgua")  # 로그인 정보
            server.sendmail(from_address, to_address, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    personal_consultation_form()
