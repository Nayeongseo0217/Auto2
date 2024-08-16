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
            
            # Add spacing between rows
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
            "현대": ["https://www.hyundai.com/contents/repn-car/side-45/casper-23my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/casper-23my-45side.png", 
                    "https://www.hyundai.com/contents/repn-car/side-45/avante-25my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/avante-n-25my-45side.png", 
                    "https://www.hyundai.com/contents/repn-car/side-45/avante-hybrid-25my-45side.png", 
                    "https://www.hyundai.com/contents/repn-car/side-45/sonata-the-edge-45side.png", 
                    "https://www.hyundai.com/contents/repn-car/side-45/sonata-the-edge-hybrid-45side.png", 
                    "https://www.hyundai.com/contents/repn-car/side-45/ioniq6-24my-45side.png", 
                    "https://www.hyundai.com/contents/repn-car/side-45/grandeur-25my-45side.png", 
                    "https://www.hyundai.com/contents/repn-car/side-45/grandeur-hybrid-25my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/venue-23my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/kona-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/kona-hybrid-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/kona-electric-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/nexo-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/nexo-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/the-new-tucson-hybrid-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/the-all-new-santafe-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/the-all-new-santafe-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/the-new-ioniq5-24pe-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/the-new-ioniq5-24pe-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/the-new-ioniq5-24pe-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/palisade-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/staria-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/staria-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/staria-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/staria-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/staria-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/porter2-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/porter2-built-in-truck-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/porter2-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/porter2-built-in-truck-24my-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/mighty-45side.png",
                    "https://www.hyundai.com/contents/repn-car/side-45/solati-45side.png"],
            "제네시스": ["https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/G70/list-thumbnail/2024-07-03/11-29-48/genesis-kr-admin-model-list-thumbnail-g70-desktop-630x240-kr.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/G70/list-thumbnail/2024-07-03/11-31-18/genesis-kr-admin-model-list-thumbnail-g70-shooting-brake-desktop-630x240-kr.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV80/list-thumbnail/2023-09-25/20-34-15/gv80_24fl_gnb_thumbnail.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV80/list-thumbnail/2023-09-25/20-34-15/gv80_24fl_gnb_thumbnail.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/G80/list-thumbnail/2023-08-29/15-34-14/electrified_g80_24my_gnb_thumbnail.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/G90%20BLACK/list-thumbnail/2024-03-21/07-55-08/genesis-kr-admin-model-list-thumbnail-g90-black-desktop-630x240-ko.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV60/list-thumbnail/2024-03-08/15-33-30/genesis-kr-admin-model-list-thumbnail-gv60-desktop-630x240-ko.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV70/list-thumbnail/2024-05-08/08-50-44/genesis-kr-admin-model-list-thumbnail-gv70-desktop-630x240-ko.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV70/list-thumbnail/2024-05-08/08-50-44/genesis-kr-admin-model-list-thumbnail-gv70-desktop-630x240-ko.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV70/list-thumbnail/2023-07-21/17-09-45/egv70_GNB_Thumbnail.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV80/list-thumbnail/2023-09-25/20-34-15/gv80_24fl_gnb_thumbnail.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV80%20COUPE/list-thumbnail/2023-09-25/20-42-12/gv80-coupe-gnb-thumbnail.png",
                        "https://www.genesis.com/content/dam/genesis-p2/kr/admin/model-information/GV80/list-thumbnail/2023-09-25/20-34-15/gv80_24fl_gnb_thumbnail.png"
                        ],
            "기아": [
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krja181/morning_q_a2g.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krtm148/ray_q_m9y.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krtm138/ray-ev_q_eu3.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krdb132/k3_q_m4b.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krdb133/k3-gt_q_cr5.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krdl145/k5_q_c7s.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krdl145/k5_q_c7s.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krgl185/k8_q_byg.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krgl185/k8_q_byg.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krgl185/k8_q_byg.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krgl185/k8_q_byg.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krjr174/k9_q_d9b.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krsg077/niro-hybrid_q_cge.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krsg078/niro-ev_q_swp.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krdp079/niro-plus_q_m7g.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krsv178/ev3_q_ag3.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krsu182/seltos_q_swp.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krnq131/sportage_q_swp.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krnq131/sportage_q_swp.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krmq135/sorento_q_bn4.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krmq135/sorento_q_bn4.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krcv177/ev6_q_glb.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krcv177/ev6_q_glb.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krcv173/ev6-gt_q_klm.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krmv107/ev9_q_ism.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krjs129/mohave_q_abp.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krkp175/carnival_q_isg.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krkp175/carnival_q_isg.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krkp176/carnival-hi-limousine_q_abp.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krb1183/bongo3_q_ud.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krb1153/bongo3-frozen-standard-king_q_ud.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krb1167/bongo3-ev_q_ud.png",
                        "https://www.kia.com/content/dam/kwp/kr/ko/vehicles/represent/krb1081/bongo3-ev-frozen-s_q_ud.png",
                    ],
            "쉐보레": [
                    "https://chais.co.kr/assets/images//model/20230719144358971.png",
                    "https://chais.co.kr/assets/images//model/20230322113751213.png",
                    "https://chais.co.kr/assets/images//model/20230322113751213.png",
                    "https://chais.co.kr/assets/images//model/20230322113751213.png",
                    "https://chais.co.kr/assets/images//model/20230322113751213.png",
                    ],
            "KG모빌리티": ["https://www.kg-mobility.com/kr/images/20160624/160624_common/car_tivoli_off.jpg",
                    "https://www.kg-mobility.com/kr/images/20160624/160624_common/car_tivoliair_off.jpg",
                    "https://www.kg-mobility.com/kr/images/20160624/160624_common/car_korandoC_off.jpg",
                    "https://www.kg-mobility.com/kr/images/20160624/160624_common/car_korandoev_off.jpg",
                    "https://www.kg-mobility.com/kr/images/20160624/160624_common/car_torres_off.jpg",
                    "https://www.kg-mobility.com/kr/images/20160624/160624_common/car_torres_off.jpg",
                    "https://www.kg-mobility.com/kr/images/20160624/160624_common/car_torresevx_off.jpg",
                    "https://www.kg-mobility.com/kr/images/20160624/160624_common/car_g4rexton_off.jpg",
                    "https://www.kg-mobility.com/kr/images/20160624/160624_common/car_Q200_off.jpg",
                    "https://www.kg-mobility.com/kr/images/20160624/160624_common/car_Q201_off.jpg"],
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
            "다피코": ["https://chais.co.kr/assets/images//model/20231129145804219.png", "https://chais.co.kr/assets/images//model/20220921131736630.png"],
            "스마트 EV": ["https://chais.co.kr/assets/images//model/20230314170922230.png", "https://chais.co.kr/assets/images//model/20230314170937976.png", "https://chais.co.kr/assets/images//model/20230314170952641.png"],
            "마이브": ["https://chais.co.kr/assets/images//model/20230717100925410.png"],
            "벤츠": [
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXqaWFqtyO67PobzIr3eWsrrCsdRRzwQZg9pZbMw3SGtGyWtsd2sDcUfp8fXGEuiRJ0l3ItOB2NQObApjTXI5uVcZQC31SrkzNBTwm7jAymhKV5XN%25vq4t9yLRgLFYaxP0VrH1endn8wsbfoiZrb1M4FnKrTg95bn6PDakDSeWHnStsd8oxcUfiXyXGE45wJ0lCrnOIJtR1q%25SoiZeIQM6o2xgTSMCi36PDKLrSeWgXhtsdPY%25cUfx8kXGE0GSJ0lBHtOB2AMnbAp5dXI5gZ8lXhRjwQZgV4zN8uoQ3pE77V9hDNt3DkSW9wUwopoL24PvEa2zq7DJ3D&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://search.pstatic.net/common?quality=75&direct=true&src=https%3A%2F%2Fimgauto-phinf.pstatic.net%2F20240703_36%2Fauto_17199726348975c02G_PNG%2F20240703111020_BoDjIsIU.png",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXqaSFqtyO67PobzIr3eWsrrCsdRRzwQZgk4ZbMw3SGtGyWtsd2HtcUfp8qXGEubmJ0l3ItOB2NQnbApjdCI5uVcZQC3qkWkzNRLkm7jxaShKVFSR%25vq9v9yLRDLVYaxW0SrH1dItn8wvOcoiZLioM4FaSMTg9Ht96PD81DSeWAmutsd5hQcUfCUuXGEzJjJ0l7OZOB2aMRbApHtXI5u8KZQC3UM3kzNGtkm7j023hKVB%25M%25vqAycyLR5i6YaxC4prH1gObnMr%25E2fchI5uKMTQmIwlzkhQg5Km7jG2jhKVUXd%25vq7UcyLRKA6Yax27frH18B%25n8wiA2oiZ45gM4FgCQTg9Pv96PKNCZnX2f3SNsF6hdeDkSW9wUUEVXqdYWqtyRV3H3k9kBF7v0wAFslUqoWq&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXqrWFqtyO67PobzIr3eWsrrCsdRRzwQZgk4ZbMw3SGtxKFtsd2s%25cUfp8cXGEu9BJ0l36xOB2NzObApj7pI5ux52QC31gFkzNBTnm7jA7mhKV5YV%25vqCJTyLRgc6YaxPa9rH1entn8wsb4oiZrqNM4FAm2Tg95Yp6PDakDSeWHeutsd8Z3cUfiFWXGE4TSJ0lg6fOB2Pb%25bApeIoI5usKYQC3vT6khQOZ9wnJSeW0h%25tXSNFUcJtvekXGEHaVJ0lUHtOB2G8ObApFUiI5uC5JQC3zCTkzN7P9m7jKGjhKUWP3IrZxD%25WLkzcHZVS%25qjuaa1frEROqEyJlfDADSjSiNsG8u4NLwaEQqE&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXq0WFqtyO67PobzIr3eWsrrCsdRRzwQZ6TfZbMw3SGtlaStsd2HVcUfpOkXGEubSJ0l3IrOB2NS1bApj7pI5uVKMQC31MTkzNwPnm7jZGohKVFXM%25vqCtTyLRzLyYax758rH1KMrn8wvVwoiZUbEM4FGIJTg90gw6PDBPlSeWAtRtsd5%25QcUfKM6XGEvhSJ0lgYlOB2PMObApedlI5uscJQC3UXpkzNGmnm7j0hShKVBHM%25vqA8lyLRiO6Yax4JOroYhfldtmbAp7oMIkb1ECQmI4A3kzNeUJm7jCcmhKVfz3%25vqLvkyLRaGmYaxH0ErHAlGqhTWFEnlioUiYW1JnwxV449pTuZkwuoQ3pE7EJxJeRB5PVsRiD4u%25wu&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://search.pstatic.net/common?quality=75&direct=true&src=https%3A%2F%2Fimgauto-phinf.pstatic.net%2F20240711_41%2Fauto_1720670291586zbggH_PNG%2F20240711125800_1wnuMiBc.png",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXq0WFqtyO67PobzIr3eWsrrCsdRRzwQZgk4ZbMw3SGtle2tsd2HtcUfpOyXGEuTRJ0l3OtOB2NzObApj79I5ux52QC31grkzNwP9m7jZcohKV5SM%25vqCv%25yLRzAHYax75qrH1KItn8wsOcoiZUidM4FGSlTg90tT6PDBSoSeWAtRtsd7vGcUfi%25qXGE49dJ0lg6lOB2Pb%25bApeIoI5usKYQC3Uv7kzNp%25bm7ja7mhKVHtc%25YhQDd9TIXGE5YrJbXqWBOIJHGcbApPnXI5ug1J0nrvwOBX3wZbA4sLFI5QI19QCkQNDkzm6gWm7hXPdhce6CF2iaPfeyjPRW7KVfv75YYHU2GLwvGE10UPbPV7VoztXn5Mzy8YG9vG&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXqbSFqtyO67PobzIr3eWsrrCsdRRzwQZgk4ZbMw3SGtle2tsd2vtcUfp8cXGEuiBJ0l3IrOB2NS1bApjtCI5uVQJQC3qvQkzNRLdm7jZ6IhKVFSL%25vq9vjyLRDG6YaxW0ErH1dItn8wvOcoiZLbYM4Fa4MTg9Hvn6PD8LmSeWiXRtsd4YTcUfgrcXGEzymJ0l7YJOB2KQqbApvkbI5uLfYQC3aEOkzNHmbm7j8hfhKVk%259%25vqetoyLRsLFYaxU08rH1GBun8w0AEoiZB7pM4FAy2Tg956p6PDakNSeWHeutsd8YdcUfiFWXGE4TEJ0lgOhOB2PbnbApe7yI5usKzQC3UvpkzNp%25bm7ja6DhKVHtc%25YhQDd9TIXGE5YrJbXqWBOIJHG1bApLTRI5ua6YQC3sspkzNeZbAMoaFI5OMl9QCbV9DkzmNsWm7hm7dhK%25hqf%25vycsEyLYbUlYarzV2rb0XvdNe4Gp0oxGSz0H1p8aKMMgAN5iD85u9CAGmG1a1SLOI6KtLoPM5f85&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://search.pstatic.net/common?quality=75&direct=true&src=https%3A%2F%2Fimgauto-phinf.pstatic.net%2F20221123_175%2Fauto_1669188441720vyAm0_PNG%2F20221123162709_pPcRP9DR.png",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXqrWFqtyO67PobzIr3eWsrrCsdRRzwQZgk4ZbMw3SGtGnFtsd1HpcUfwOuXGEZ93J0lF6NOB2Nr%25bApjnVI5uV5ZQC3qsQkzNRU9m7jxyohKV1YQ%25vqwr%25yLRZOmYaxFNhrH19jin8wDhyoiZW%25pM4FdyfTg9fU26PDEGoSeWl0Stsd2BdcUfpAyXGEjyYJ0lV0fOB2q8%25bApRipI5ux4ZQC31g7kzNwtnm7jZcDhKVFpW%25vq9ulyLRDiXYax7XSrH1KHrn8wvzcoiZL7gM4FaKjTg9HtT6PD8cNSeWiXRtsd4oVcUfgXyXGEzyjJ0l7YhOB2KrObApvn9I5uL5IQC3aCRkzNHU9m7j8ymhKVipE%25vq4yTyLRgY2YaxP48rH1eOtn8wsXwoiZr51M4FnKFTg9o6k6PDC76SeWzK3tsd7oTcUfKMjXGEv5VJ0lL%25tOB2Pr2bApeARI5use1QC3Uh7kzNGtNm7j02ZhKVBbM%25vqAIkyLR5QHYaxCkqrH1znrn8w7oboiZKeEM4FvsJTg9LUV6PDaGFSeWFmMtsd9JtcUfArkXGE5nXJ0lCorOB2znobQOcxwRytM4FsQkTSMp1P6tTz4oSeW5yStsdLvNcUfe%25WXGEsGEJ0lU0ZOB2G8qbAp0iyI5uBeYQC3AhTkzN5tkm7jCt6hKVzcZ%25vq7X4yLRKX9YaxvJVrH1LO6n8waeIoiZ3bXM4FNcyTg9PQO6PDePpSeWseMtsdUs%25cUfGLqXGHRvW6INpqJRBOXW2vEyJlfDAAu1Iw2MlwOoZ1qgqyfyzda8CD7dB3AwSlw&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXqrWeqtyO67PobzIr3eWsrrCsdRRzwQZgk4ZbMw3SGtlaStsd2HVcUfpOkXGEubSJ0l3IrOB2NS1bApj7oI5ux5xQC31CpkzNwPnm7jZeDhKVFHt%25vqCtTyLRzLyYax7oYrH1KM1n8wvVwoiZUbXM4FG4fTg90626PDCroSeWzn3tsd7BVcUfi%25fXGE4GjJ0lgDfOB2Pb%25bApeIoI5usKYQC3Uv3kzNGLdm7jacShKVHtc%25YhQDd9TIXGE5YrJbXqWBOIJHG%25bApPnpI5ug6FQC3AgrkzN5P6m7jdA7hKVvsW%25vqLUayLRaARYaxH4ErHAlGqhTWFEnlibr7gW1JnwxV449pTuZkwuoQ3pE7EJxJeRB5PVsRiD4u%25wu&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.jpg?COSY-EU-100-1713d0VXqrWeqtyO67PobzIr3eWsrrCsdRRzwQZ6ZGZbMw3SGtxX2tsd1ZpcUfwMuXGEuymJ0l34JOB2Ng1bApjkbI5uVmMQC3qS7kzNRlKm7jxODhKV1Ht%25vq9tcyLRDLVYaxW0SrH1dCOn8wfQcoiZEqpM4FlRjTg9HQO6PD8k6SeWimhtsd4vQcUfg8WXGEPbXJ0leDlOB2sWFbApUtRI5uGcZQC30XTkzNHTwm7j86ohKViSE%25vq4v%25yLRgARYaxP5prH1eItn8wsQ2oiZUMXM4FGTwTg9ogE6PDM7FSeWTaWtsd7vNcUfKONXGEvTXJ0lL6qOB2azRbApenpI5us5xQC3USOkzNGlum7j0OohKVBbV%25vqAyTyLR5Y2YaxCrJrH1zgtn8w7P3oiZx6YM4F1SMTg9UQV6PDG7FSeW0yItsdB%25ycJtTjqNkMYax4JOroYfV8nMrBawoiZ7%25oM4F5KrTg9CvT6PDzLDSeWvwxtsdPv3cUfeOyXGEsnXJ0lUDlOB2GS%25bAp0oEI5u9LRQC3zMrkzN7zwm7jK7ShKVv0W%25vqLrdyLRa3DYaxHrqrHAlGqhTWFEnlibW61W1JnwxV449pTuZkwuoQ3pE7EJxJeRB5PVsRiD4u%25wu&imgt=P27&bkgnd=9&pov=BE040,DZO&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXqrWFqtyO67PobzIr3eWsrrCsdRRzwQZg9pZbMw3SGtGyWtsd2HdcUfpOyXGEuTRJ0l3CJOB2qrubApRARI5uxfJQC30MrkzNBzNm7jAymhKV5YL%25vqCu%25yLRgcDYaxPXSrH1eHDn8wsVxoiZBkEM4FvIFTg9Lg26PDa1FSeWHnMtsd8c%25cUfiANXGE45wJ0lCrnOIJtR1q%25SoiZeIQM6o2xgTSMCiZ6PDLLoSeWvw5tsdPJ%25cUfxg7XGE0aBJ0lBIxOB2ASqbAp5tlI5uCQ2QCPFi2J%25xVZkF7mL2DF3MkNulKKqD%25WjcNWmtdDZGZMuMapgeLlHp7RKWONW&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXqNEFqtyO67PobzIr3eWsrrCsdRRzwQZg9pZbMw3SGtle9tsd2HdcUfp8qXGEuiYJ0l3ItOB2NQObApjTXI5uVcZQC31C1kzNwtnm7jA6ZhKV5Kh%25vqCr%25yLRzOVYaxPXWrH1eHrn8ws8WoiZUqNM4FGR1Tg906O6PDMkFSeWTaMtsd7vVcUfKM6XGEvhEJ0lgYxOB2PSObApet9I5usQMQC3Uv1kzNGLdm7jucZhKVHtc%25YhQDd9TIXGE5YrJbXqWBOIJHGEbAp4xXGrpa1J08glwOBbnRZbAIoQFI5QMB9QCkVNDkzm0ZWmtPT5Zl8LgdP%25sSFvh7jdKzAyyaslUv1KUfxGsgOgjzjnCScrAoC%25HyUFKU&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXq5JFqtyO67PobzIr3eWsrrCsdRRzwQZg9BZbMw3SGtGyWtsd2HdcUfp8qXGEuiYJ0l3ItOB2NQObApjTXI5uVfzQC3qXFkzNwUnm7jZcohKV5Kh%25vqCr%25yLRzOVYaxPXWrH1eJtn8ws8noiZUidM4FGR1Tg906O6PDBSsSeWTm9tsd7vVcUfKm6XGE4yEJ0lg4qOB2PMObApetbI5uscDQC3UkTkzNGLwm7j0afhKV3YQ%25vqNIoyLRiLyYax4JOroYhfldtmbAp7oMIkb1ECQmI4ArkzNetDm7jCyShKVz2c%25vqLvkyLRaLXYaxH0hrH18Mln8wiQboiZ4qYM4zuA1YtEWpTuPNprpEFIT9ZxeedNtjD%259j6hVNpLpIZIGwC7Ux0wPfejr9j&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXq5JFqtyO67PobzIr3eWsrrCsdRRzwQZg9BZbMw3SGtGyWtsd2HdcUfp8qXGEuiYJ0l3ItOB2NQObApjTXI5uVfzQC3qXFkzNwUnm7jZcohKV5Kh%25vqCr%25yLRzOVYaxPXWrH1eJtn8ws8noiZUidM4FGR1Tg906O6PDBSsSeWTm9tsd7vVcUfKm6XGE4yEJ0lg4qOB2PMObApetbI5uscDQC3UkTkzNGLwm7j0afhKV3YQ%25vqNIoyLRiLyYax4JOroYhfldtmbAp7oMIkb1ECQmI4ArkzNetDm7jCyShKVz2c%25vqLvkyLRaLXYaxH0hrH18Mln8wiQboiZ4qYM4zuA1YtEWpTuPNprpEFIT9ZxeedNtjD%259j6hVNpLpIZIGwC7Ux0wPfejr9j&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXqaWFqtyO67PobzIr3eWsrrCsdRRzwQZg9pZbMw3SGtGeOtsd0YdcUfpUWXGEuiEJ0l34xOB2NgnbApjkXI5uVmIQC3qSOkzNRJ9m7jZ7ZhKVFXM%25vqCt9yLRzLyYax7oYrH1KIRn8wsOfoiZUioM4FG4fTg90xV6PDB1ZSeWAtItsd6hDcUfS86XGEvaRJ0lL%25tOB2Pr2bApetbI5uscDQC3UkTkzNGLwm7j0afhKVHtc%25YhQDd9TIXGE5YrJbXqWBOIJHG5bAp4xXGroN1J0cu2wOBbORZbAIoxFI5Qj39QCkGwDkSgMAwEHv4Wghe6A3BzNW7CB%25%25LeEsKx7sdRUe4J4NCNr56tYBn5ha%25sZ7s&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXq5JFqtyO67PobzIr3eWsrrCsdRRzwQZg9BZbMw3SGtGyWtsd2HdcUfp8qXGEuiYJ0l3ItOB2NQObApjTXI5uVfzQC3qXFkzNwUnm7jZcohKV5Kh%25vqCr%25yLRzOVYaxPXWrH1eJtn8ws8noiZUidM4FGRjTg90xw6PDBSbSeWTm9tsd7vVcUfKm6XGE4yEJ0lg4qOB2PMObApetbI5uscDQC3UkTkzNGLwm7j0afhKV3YQ%25vqNIoyLRiXJYnymdEWSkOB2znobQOxf5IkbiBYQC3PS9kzN5%256m7jClthKVvKQ%25vqLvcyLRaGmYaxHoErH18IOn8wiVyoiCpBxySfD2Mpg32x2GZbMFwRPPW3SN9hFNTmj32v2bwbU15zsRG1gdPNYFN&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXq5JFqtyO67PobzIr3eWsrrCsdRRzwQZg9BZbMw3SGtGyWtsd2HdcUfp8qXGEuiYJ0l3ItOB2NQObApjTXI5uVfzQC3qXFkzNwUnm7jZcohKV5Kh%25vqCr%25yLRzOVYaxPXWrH1eJtn8ws8noiZUidM4FGRjTg90xw6PDBSbSeWTm9tsd7vVcUfKm6XGE4yEJ0lg4qOB2PMObApetbI5uscDQC3UkTkzNGLwm7j0afhKV3YQ%25vqNIoyLRiXJYnymdEWSkOB2znobQOxf5IkbiBYQC3PS9kzN5%256m7jClthKVvKQ%25vqLvcyLRaGmYaxHoErH18IOn8wiVyoiCpBxySfD2Mpg32x2GZbMFwRPPW3SN9hFNTmj32v2bwbU15zsRG1gdPNYFN&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXq0WFqtyO67PobzIr3eWsrrCsdRRzwQZQ9vZbMw3SGtGyWtsd2HtcUfp8qXGEubSJ0l3otOB2NW5bApjtwI5ux5YQC30MrkzNBzkm7jAymhKV5ph%25vqCycyLRgcDYaxPXSrH1eHrn8wsV3oiZUMXM4FGTjTg906E6PDM7FSeWTXMtsd7vtcUfKLjXGEvTSJ0lgYlOB2PBqbApekCI5uscJQC3UX7kzNGm6m7j0aZhKVBHE%25vqNtTyLRjnyYax4JOroYhfldtmbAp7oMIkb1ECQmI4A7kzNUUnm7jseFhKVzKE%25vq7U9yLRKG6Yaxv5SrH1Lj1n8wusloiZ4bXM4FgIQTg9Pgn6PDe7oSeWsK9tsdUcTcUaqKDTb32VXqa8L0xqf%25XEd9BBpxb1loE1JnwxV4V%25d%25CWLH59zW0uB16E1&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXq0WFqtyO67PobzIr3eWsrrCsdRRzwQZQ9vZbMw3SGtGyWtsd2HtcUfp8qXGEubSJ0l3otOB2NW5bApjtwI5ux5YQC30MrkzNBzkm7jAymhKV5ph%25vqCycyLRgcDYaxPXSrH1eHrn8wsV3oiZUMXM4FGTjTg906E6PDM7FSeWTXMtsd7vtcUfKLjXGEvTSJ0lgYlOB2PBqbApekCI5uscJQC3UX7kzNGm6m7j0aZhKVBHE%25vqNtTyLRjnyYax4JOroYhfldtmbAp7oMIkb1ECQmI4A7kzNUUnm7jseFhKVzKE%25vq7U9yLRKG6Yaxv5SrH1Lj1n8wusloiZ4bXM4FgIQTg9Pgn6PDe7oSeWsK9tsdUcTcUaqKDTb32VXqa8L0xqf%25XEd9BBpxb1loE1JnwxV4V%25d%25CWLH59zW0uB16E1&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXq4EFqtyO67PobzIr3eWsrrCsdRRzwQZgk4ZbMw3SGtGyWtsd2vGcUfp8cXGEuiRJ0l3ItOB2NMcbApjdCI5uVcZQC3qvWkzNwznm7jZaShKV5SM%25vqCtkyLRzLyYax758rH1KCun8wvTnoiZL6NM4FaRMTg9H6k6PDBkpSeWAmItsd5stcUfCUuXGEzbXJ0l7OhOB2KbcbApvI9I5uO42QC3bhOkzNImbm7jgemhKVPs9%25vqeIkyLRsQWYaxCXxrH1zHdn8w7T2oiZK6gM4FvmFTg9LY96PDarsSeWHtUtsd8c%25cUfiANXGE45wJ0lgCfOB2fr%25bApEnXI5ulmIQC3vC7kzNL6Sm%25kbFDZoOtsdB%25ycJtj9GXOcLsmJ0lKoJOB2gg%25bAp4iMI5uBo2QC3ACWkzN5Pwm7jCeohKVz0M%25vq7uqyLRlMGYaxHXSrH18JOn8wiA4oiZ451M4FgTrTg735wrcldu637vz09i9Q6DF1ssfjcVWyDVS%25qjuauQFQ0ZzKG1BZeEsVnDV&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXqbSFqtyO67PobzIr3eWsrrCsdRR%25wQZhkHZbMMlSGtGXutsLSy89i9COiZbmji4FIhVog9Q%25s8PDkyvieWmYOfsdhriSUf%25npJGEy6LO0lYSlKB2rtN8Apnf8L5uoEi0C3Ml3CzNT2fV7j6pE%25KVSuaKvqt3HYLRcNB7axXjAaH1JV6H8wOqiAiZbRWy4FIE5Yg9QlCBPDk2DPeWmpGesdhuUCUf%253GPGEyN0O0lYU1%25B2rGCUApn1pS5uowFJC3MZdIzNTEgT7j6ljiKVS2GSvqtp5tLRcuC1axX3H0H1JN9h8wOjDMiZbVWJ4FIJ50g9QOC8PDkbzPeWmIGesdh2dEUf%25pLaGBUPSc67gH1J9BA84HytZig8p1T4FIl3Yg9Q2KgPDkRDAeWmqVvsdhDdXUf%25WRTGEydx70lYfkYB2rE8eApnIgA5uo3iaC3MN3MzNTjfo7j6VriKVSqvCvqEhWTC8IJmLhE2fFtRtsLcSM11Oy8YXAcYaBrymumsSsF6flZM96xb1YzcY&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://assets.oneweb.mercedes-benz.com/iris/iris.png?COSY-EU-100-1713d0VXqbSFqtyO67PobzIr3eWsrrCsdRR%25wQZhkHZbMMlSGtGXutsLSy89i9COiZbmji4FIhVog9Q%25s8PDkyvieWmYOfsdhriSUf%25npJGEy6LO0lYSlKB2rtN8Apnf8L5uoEi0C3Ml3CzNT2fV7j6pE%25KVSuaKvqt3HYLRcNB7axXjAaH1JV6H8wOqiAiZbRWy4FIE5Yg9QlCBPDk2DPeWmpGesdhuUCUf%253GPGEyN0O0lYU1%25B2rGCUApn1pS5uowFJC3MZdIzNTEgT7j6ljiKVS2GSvqtp5tLRcuC1axX3H0H1JN9h8wOjDMiZbVWJ4FIJ50g9QOC8PDkbzPeWmIGesdh2dEUf%25pLaGBUPSc67gH1J9BA84HytZig8p1T4FIl3Yg9Q2KgPDkRDAeWmqVvsdhDdXUf%25WRTGEydx70lYfkYB2rE8eApnIgA5uo3iaC3MN3MzNTjfo7j6VriKVSqvCvqEhWTC8IJmLhE2fFtRtsLcSM11Oy8YXAcYaBrymumsSsF6flZM96xb1YzcY&imgt=P27&bkgnd=9&pov=BE040&uni=cs&im=Crop,rect=(0,0,1450,750),gravity=Center;Resize,width=250",
                        "https://search.pstatic.net/common?quality=75&direct=true&src=https%3A%2F%2Fimgauto-phinf.pstatic.net%2F20240329_203%2Fauto_1711688218070QjADp_PNG%2F20240329135656_bxPQL5h0.png",
                    ],
            "BMW": [
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBguf4Jl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSRnqoQh47wMvcYi9NGUVMb3islBglUb90cRScH8g7MbnMdoPayJGy53LSrQ%25r9Y3FW8zWuERRqogqaGH8l3ilU%2580cRScHzo7MbnMdgBoyJGy5i8KrQ%25r9SuUW8zWunYEqogqaG47l3ilU%25egcRScHzqjMbnMdemRyJGy5m8ErQ%25r9sRnW8zWuKbMqogqaDnal3ilUCGwcRScHb8gMbnMdJoHyJGy5Q3grQ%25r98SFW8zWuuRbqogqaYM1l3ilUb%259cRScHzRUMbnMdeo7yJGy57ubrQ%25r90oaW8zWuBbuqogqaYSDl3ilUE0mcRScHFrBMbnMdjIdyJGy57kSrQ%25r90vSW8zWuu5VqogqaFQ8l3ilU%2575cRScHzesMbnMdeBSyJGy5QoarQ%25r98QwW8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBg3RJ6l384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSRrqoQh47wMvcYi9NGUVMb3islBglUb90cRScH8g7MbnMdoPayJGy53LSrQ%25r9Y3FW8zWunUQqogqaGQ7l3ilU%258jcRScHz08MbnMdg5uyJGy5i0BrQ%25r9SDFW8zWunC%25qogqaGrEl3ilUC4ocRScH4JBMbnMdeoiyJGy5m3lrQ%25r9si9W8zWuKSkqogqa3EFl3ilURQzcRScHb8UMbnMdJozyJGy5QiErQ%25r993RW8zWu3ndqogqaGoul3ilUCQFcRScH4%25WMbnMdj9RyJGy578urQ%25r90R9W8zWuBiKqogqaY7el3ilUEy0cRScHFr2MbnMdjIdyJGy57kSrQ%25r90vSW8zWuu5VqogqaFQ8l3ilU%2575cRScHzesMbnMdeBSyJGy5QoarQ%25r98QwW8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgoRuyl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSGNqoQh47wMvcYi9SDGgMb3islBglUb%259cRScHJzYMbnMdQYSyJGy53SBrQ%25r9RKYW8zWub8KqogqaJ25l3ilUQT9cRScH8ZAMbnMd088yJGy5BRbrQ%25r9YEaW8zWuEiJqogqaGH7l3ilU%258jcRScHz09MbnMdgBoyJGy5isDrQ%25r9SoDW8zWunYbqogqaGEFl3ilU%25e0cRScHzmiMbnMdgAJyJGy5iJdrQ%25r9SeUW8zWunm7qogqaDjzl3ilUCzjcRScH4e3MbnMdeoiyJGy5m3trQ%25r9sRmW8zWuKbhqogqaDnQl3ilUCGzcRScH4%25VMbnMdezqyJGy5Q0BrQ%25r98RnW8zWuob9qogqa3Jnl3ilUR%250cRScHbR2MbnMdJ13yJGy5Q4ErQ%25r98XHW8zWuuU%25qogqaabdl3ilUUJecRScHHJ9MbnMdd5syJGy55ODrQ%25r90aJW8zWuB3UqogqaYJal3ilUEuGcRScHFG4MbnMdjYKyJGy57qErQ%25r90lIW8zWuBAuqogqaY20l3ilUEOzcRScHFpVMbnMdjf6yJGy5sRKrQ%25r9KDFW8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgKRK5l384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSD5qoQh47wMvcYi9kQRAMb3islBglUbDqcRScHz1bMbnMdoi0yJGy53LtrQ%25r9Y33W8zWuEJQqogqaGH7l3ilU%258jcRScHzesMbnMdg70yJGy5iKnrQ%25r9SQwW8zWunmHqogqaDC8l3ilUCQzcRScH48AMbnMdeo4yJGy5mgRrQ%25r9si8W8zWuobGqogqa3Jul3ilURQGcRScHbzBMbnMdJbtyJGy5QARrQ%25r98eFW8zWuuRbqogqaYM1l3ilUEtBcRScHFpVMbnMdQgayJGy53sBrQ%25r9RXHW8zWuKbhqogqaDnyl3ilUEdocRScHFJ5MbnMdjodyJGy57HgrQ%25r90gsW8zWuBj4qogqaYM7l3ilUEtUcRScHFpgMbnMdjfgyJGy5BYurQ%25r9RX9W8zWuuRHqogqaab4l3ilUUHecRScH70uMbnMdoIayJGy5BObrQ%25r9Yp9W8zWunyYqogqa3EFl3ilUU4gcRScHHwsMb37ur1MESxgYXMb3dnqbgyFntBoJltJ0ab6",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBguRJOl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uEUHqoQh47wMvcYi9kQC5Mb3islBglUb%259cRScH8g7MbnMdobeyJGy53LUrQ%25r9RXnW8zWubxuqogqaJh6l3ilUj8ocRScH705MbnMd0zHyJGy5Bd2rQ%25r9SaFW8zWunJEqogqaGjdl3ilU%257QcRScHzj7MbnMdgsYyJGy5idmrQ%25r9SmbW8zWunNoqogqaG27l3ilU%25K5cRScHzDsMbnMdgCEyJGy5iL3rQ%25r9sEGW8zWuKGEqogqaDJ%25l3ilUCQ1cRScH48CMbnMdeoLyJGy5m3ArQ%25r9sibW8zWuKSkqogqaDnyl3ilURFjcRScHb8gMbnMdJoHyJGy5Q3grQ%25r98SFW8zWuo86qogqa3NQl3ilURK0cRScHbZuMbnMdd8uyJGy55oKrQ%25r99KGW8zWuu3HqogqaaU4l3ilUUvmcRScHF53MbnMdjQ9yJGy5735rQ%25r90UiW8zWuBj4qogqaYM1l3ilUEtUcRScHFNYMbnMdjfJyJGy5sRKrQ%25r9KDFW8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgbRuYl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSFtqoQh47wMvcYi9SyrfMb3islBglUb%259cRScHJzUMbnMdQgEyJGy58glrQ%25r9R3JW8zWubGEqogqaJ2ul3ilUQT9cRScH8ZgMbnMd088yJGy5BRbrQ%25r9YEaW8zWuESNqogqaFr%25l3ilUjvQcRScHz53MbnMdg30yJGy5iYFrQ%25r9SKFW8zWunD4qogqaGEFl3ilU%25a1cRScHzCoMbnMdgbEyJGy5mSBrQ%25r9sKJW8zWuKbsqogqaDn3l3ilUCGrcRScHbdiMbnMdJoiyJGy5Q3drQ%25r98RiW8zWuonjqogqa3o1l3ilURI8cRScHbDBMbnMdJC9yJGy55unrQ%25r993UW8zWuu3HqogqaaU4l3ilUUupcRScHF53MbnMdjQ9yJGy5735rQ%25r90gsW8zWuBj4qogqaYM1l3ilUEtUcRScHFpgMbnMdmIoyJGy56SprQbBUq2rjGTSFhrQb9%25cQSW7%25IER8MI8YHQA",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgERunl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSGNqoQh47wMvcYi9SyUCMb3islBglUQJocRScH8g7MbnMdoPayJGy53LSrQ%25r9RXxW8zWuERRqogqaFQ8l3ilUj7dcRScH70uMbnMd0zAyJGy5Bc0rQ%25r9YpJW8zWuEfuqogqaGH8l3ilU%25JJcRScHzo7MbnMdgBAyJGy5isErQ%25r9SK3W8zWunbQqogqaGu6l3ilU%25WFcRScHzCoMbnMdgbayJGy5iJFrQ%25r9S1FW8zWunm4qogqaGs0l3ilU%25TQcRScH4g7MbnMdemRyJGy5m3erQ%25r9sicW8zWuKSVqogqa3J%25l3ilURQacRScHb8%25MbnMdJgYyJGy5QdnrQ%25r98QIW8zWuotJqogqa3s7l3ilURKdcRScHHQ9MbnMddmSyJGy558arQ%25r99uDW8zWuu5Vqogqaakel3ilUEdocRScHFJ5MbnMdjodyJGy57agrQ%25r90FCW8zWuBc6qogqaY2al3ilUEORcRScHeN8Mb37ur1MESxgYXMb3dnqbgyFntBoJltJ0ab6",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgoRdIl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251unaCqoQh47wMvcYi9INRJMb3islBglUb%25BcRScH8g7MbnMdom0yJGy536UrQ%25r9RXHW8zWuEJQqogqaFQ7l3ilUjGrcRScHz53MbnMdg88yJGy5iRErQ%25r9SbYW8zWunDjqogqaGCbl3ilU%25D8cRScHz14MbnMdgbayJGy5i6urQ%25r9S1YW8zWunmHqogqaDJ6l3ilUCQDcRScH486MbnMdezJyJGy5mgXrQ%25r983UW8zWuobGqogqa3Jul3ilURQGcRScHbzBMbnMdJHoyJGy5QJXrQ%25r98eYW8zWu3ndqogqaJb8l3ilU%253acRScH48PMbnMdezqyJGy5QKDrQ%25r90aJW8zWuB3UqogqaYJal3ilUEnCcRScHFBsMbnMdjWYyJGy57qNrQ%25r9019W8zWuBA7qogqaaM8l3ilUQeRcRScH7gQMbnMdgQoyJGy5i3vrQ%25r9SejW8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgER9Dl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uS3%25qoQh47wMvcYi9h%25U3Mb3islBglUb%259cRScHJzUMbnMdQgEyJGy58gFrQ%25r9o5CW8zWubRQqogqaJ25l3ilUQT9cRScH8ZgMbnMdoPeyJGy5BYurQ%25r9Yn3W8zWuEDRqogqaFGGl3ilUjGwcRScH7%25bMbnMdg88yJGy5iRBrQ%25r9SESW8zWunDjqogqaGCzl3ilU%25becRScHzJoMbnMdgoRyJGy5idnrQ%25r9S5DW8zWun9IqogqaGuvl3ilU%25DzcRScHzRYMbnMdgI8yJGy5i6urQ%25r9SeCW8zWuKGEqogqaDJKl3ilUCGrcRScH4%25fMbnMdJoiyJGy5Q3drQ%25r98RiW8zWuonjqogqa3u0l3ilUR3AcRScHb6oMbnMdJCYyJGy5Q4urQ%25r993UW8zWuuaCqogqaakHl3ilUEdocRScHFJ5MbnMdjodyJGy57zmrQ%25r90FCW8zWuBc6qogqaY2al38F5MIlBgL%250Pl38Uir3%25cYiA7QRWARj93N",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgKR9Yl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSGJqoQh47wMvcYi9h%25U3Mb3islBglUbazcRScH8Q3MbnMdoPayJGy53LSrQ%25r9RXsW8zWubxMqogqaFH8l3ilUj7dcRScH7gQMbnMd0ggyJGy5BgprQ%25r9Yi8W8zWunUUqogqaGbbl3ilU%258jcRScHz0uMbnMdgmYyJGy5isnrQ%25r9SoDW8zWun3JqogqaGJ8l3ilU%25agcRScHzUmMbnMdgH2yJGy5idprQ%25r9SmnW8zWun87qogqaG27l3ilU%25tJcRScHzN5MbnMdgCKyJGy5iL3rQ%25r9snYW8zWuKbsqogqaDnyl3ilUCGpcRScHb8gMbnMdJoHyJGy5Q3grQ%25r98SFW8zWuo9bqogqa3u0l3ilUR3AcRScHb6oMbnMdJCYyJGy5Q4urQ%25r993UW8zWuuaRqogqaakHl3ilUEdocRScHFJ5MbnMdjodyJGy57agrQ%25r90FCW8zWuBc6qogqaY2al3ilU48ecRScHemBMbnMdmIoyJGy5s6brQbBUq2rjGTSFhrQb9%25cQSW7%25IER8MI8YHQA",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgUn%25Jl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSFbqoQh47wMvcYi9hQa2Mb3islBglUb%25BcRScHJaBMbnMdobeyJGy536nrQ%25r9RXHW8zWubxGqogqaJhDl3ilUjdocRScH7o3MbnMd03YyJGy5BY1rQ%25r9Yn3W8zWuESMqogqaGQFl3ilU%2540cRScHz83MbnMdgHOyJGy5ieUrQ%25r9SpNW8zWuKGEqogqaDJ%25l3ilUCQDcRScH486MbnMdezJyJGy5mglrQ%25r98RnW8zWuob9qogqa3Jnl3ilUR%250cRScHbU8MbnMdJbLyJGy5Q4ErQ%25r993UW8zWuuRCqogqaaCzl3ilUUHJcRScHHzlMbnMdj9RyJGy578urQ%25r90R9W8zWuBiKqogqaY7el3ilUEy0cRScHFr2MbnMdjIdyJGy576trQ%25r901jW8zWuBw2qogqaCQ4l3ilU4e0cRoj9y6cYiXzBLcRoHSWRzMES208bq2b7uRI",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBg3RJ6l384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSRrqoQh47wMvcYi9NGUVMb3islBglUb90cRScH8g7MbnMdoPayJGy53LSrQ%25r9Y3FW8zWunUQqogqaGQ7l3ilU%258jcRScHz08MbnMdg5uyJGy5i0BrQ%25r9SDFW8zWunC%25qogqaGrEl3ilUC4ocRScH4JBMbnMdeoiyJGy5m3lrQ%25r9si9W8zWuKSkqogqa3EFl3ilURQzcRScHb8UMbnMdJozyJGy5QiErQ%25r993RW8zWu3ndqogqaGoul3ilUCQFcRScH4%25WMbnMdj9RyJGy578urQ%25r90R9W8zWuBiKqogqaY7el3ilUEy0cRScHFr2MbnMdjIdyJGy57kSrQ%25r90vSW8zWuu5VqogqaFQ8l3ilU%2575cRScHzesMbnMdeBSyJGy5QoarQ%25r98QwW8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBg3Rnvl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uS39qoQh47wMvcYi9kQ6jMb3islBglUb%25BcRScHJa5MbnMdQVayJGy53SBrQ%25r9R1GW8zWubAdqogqaJh5l3ilUQTzcRScH8ZHMbnMd03RyJGy5iuSrQ%25r9SbYW8zWunFHqogqaGjJl3ilU%2578cRScHzesMbnMdg70yJGy5iKErQ%25r9SDGW8zWunyYqogqaGk%25l3ilU%253acRScHzDYMbnMdeBSyJGy5mSBrQ%25r9sKJW8zWuKbGqogqaDJyl3ilUCQZcRScH4%25oMbnMdeziyJGy5mg5rQ%25r9sifW8zWuKSMqogqa3EFl3ilURQzcRScHb8UMbnMdJozyJGy5QiErQ%25r98StW8zWuo86qogqa3NQl3ilURK0cRScHbZuMbnMdd8RyJGy558arQ%25r99uDW8zWuBUQqogqaYRHl3ilUEQUcRScHFG4MbnMdjYKyJGy57qNrQ%25r9019W8zWuBwnqoQEdcNq0zPG7ZqoQagyoGlBg1jJ3r13F5ot",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgnRJ9l384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSGrqoQh47wMvcYi967G2Mb3islBglUb%259cRScHJzYMbnMdQVayJGy586orQ%25r9RnYW8zWubA%25qogqaJh5l3ilUQTzcRScH8ZHMbnMd088yJGy5BRbrQ%25r9YgbW8zWunJEqogqaGjdl3ilU%257QcRScHzeBMbnMdgmKyJGy5i0BrQ%25r9SDFW8zWunC%25qogqaGrEl3ilU%25vzcRScHzRUMbnMdgCuyJGy5mYnrQ%25r9snYW8zWuKbGqogqaDJ6l3ilUCQDcRScH48PMbnMdeo1yJGy5mgRrQ%25r9sinW8zWuKSoqogqaDnyl3ilURFjcRScHb8gMbnMdJoHyJGy5Q3grQ%25r98SFW8zWuotJqogqa3s7l3ilURT9cRScHHQ3MbnMddQuyJGy559KrQ%25r99pCW8zWuBUQqogqaYRHl3ilUEQUcRScHFa%25MbnMdj%25eyJGy57EDrQ%25r90lFW8zWuBc6qogqaY2al3ilUEtBcRScHFpVMbnMdm3syJGy5sKErQbBUq2rjGTSFhrQb9%25cQSW7%25IER8MI8YHQA",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgERJNl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSRSqoQh47wMvcYi967qmMb3islBglU%25vzcRScHJD9MbnMdobzyJGy558arQ%25r993nW8zWuEfuqogqaDJNl3ilU%25FzcRScHzqjMbnMd09RyJGy5BoorQ%25r9YbJW8zWunFHqogqaG47l3ilURJ5cRScHbeiMbnMdJ70yJGy58OUrQ%25r9R2bW8zWubxdqogqaFnyl3ilUCGRcRScHbziMbnMdJgAyJGy5Q4BrQ%25r99p5W8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgBRunl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSGrqoQh47wMvcYi9InGlMb3islBglUbv9cRScH8g7MbnMdobzyJGy53LSrQ%25r9YaJW8zWuEJQqogqaFnIl3ilU%258jcRScHzeBMbnMdgH2yJGy5ic0rQ%25r9SmbW8zWun87qogqaG27l3ilUCQDcRScH4%25fMbnMdea3yJGy5Q3SrQ%25r98R5W8zWuobSqogqa3JKl3ilUR%250cRScHbR2MbnMdJ13yJGy55oSrQ%25r99u3W8zWuuf9qogqaRnIl3ilUQT9cRScH4%25WMbnMdj9RyJGy578urQ%25r90R9W8zWuBHSqogqaYSDl3ilUE0mcRScHFr2MbnMdjIdyJGy5iY2rQ%25r9oMbW8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgMxHJl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uEUHqoQh47wMvcYi9KGEJMb3islBglUb%25BcRScHJwoMbnMdQIeyJGy53JgrQ%25r9R1GW8zWubxdqogqaJh%25l3ilUjdocRScH7o3MbnMd03YyJGy5BsBrQ%25r9YicW8zWuEfuqogqaGb4l3ilU%25JJcRScHzo7MbnMdgmYyJGy5i0BrQ%25r9SMBW8zWunsJqogqaGK5l3ilU%25vzcRScHzRuMbnMdei0yJGy5m3SrQ%25r9sRmW8zWuKbtqogqaDn3l3ilUCGrcRScHb8gMbnMdJoHyJGy5Q3grQ%25r98SFW8zWuo9bqogqa3oTl3ilURK0cRScHHQ3MbnMddQuyJGy559orQ%25r99SyW8zWuuf4qogqaakQl3ilUUvacRScHHwbMbnMdj9RyJGy578urQ%25r90R9W8zWuBiKqogqaY7el3ilUEy0cRScHFr2MbnMdjIdyJGy576FrQ%25r90vAW8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgm94Jl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSFbqoQh47wMvcYi9kQGbMb3islBglUb%25BcRScHJ6mMbnMdoi0yJGy536nrQ%25r9R1HW8zWubxdqogqaJh%25l3ilUQTUcRScH7o3MbnMd079yJGy5BObrQ%25r9YpBW8zWuEdJqogqaGQFl3ilU%2575cRScHz08MbnMdgmKyJGy5i8KrQ%25r9SuUW8zWunYEqogqaG47l3ilU%25egcRScHz8fMbnMdgl7yJGy5izgrQ%25r9SQ5W8zWunm7qogqaDjzl3ilUCzjcRScH4e3MbnMdeQYyJGy5m3SrQ%25r9sRcW8zWuKSuqogqaDnvl3ilUCGrcRScHbQ9MbnMdJ70yJGy5Q3SrQ%25r98R5W8zWuobSqogqa3G7l3ilUR3ZcRScHbDBMbnMdd8uyJGy55o3rQ%25r993DW8zWuu3Hqogqaakel3ilUEdocRScHFJ5MbnMdjodyJGy57zmrQ%25r90FCW8zWuBcjqogqaYM1l3ilUEtUcRScHeomMbnMdmsYyJR0aWAyFnhiExyJR5GlJirjGNY3QcNQBUJ1",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgnR9ul384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uS3RqoQh47wMvcYi9SKz2Mb3islBglUbQqcRScHJzuMbnMdQzqyJGy58HgrQ%25r9R3JW8zWubGEqogqaJ2ul3ilUQT9cRScH8ZgMbnMdoPdyJGy5BRbrQ%25r9YEaW8zWuEfGqogqaGH8l3ilU%25J0cRScHzo7MbnMdgBuyJGy5iY3rQ%25r9SKDW8zWunD4qogqaGUdl3ilU%25FQcRScHzmiMbnMdgUkyJGy5iJvrQ%25r9snYW8zWuKDQqogqaDJ%25l3ilUCQDcRScH4%25bMbnMdJ8uyJGy5Q9nrQ%25r98RnW8zWuob9qogqa3Jnl3ilUR%250cRScHbR2MbnMdJ13yJGy5Q4ErQ%25r993UW8zWuu3HqogqaaU4l3ilUUupcRScHF53MbnMdjQ9yJGy5735rQ%25r90gsW8zWuBj4qogqaYM1l3ilUEtUcRScHFpgMbnMdm3syJGy5sKErQ%25r9K0AW8zWuDAbqogqaC28l3ilU4t8cRoj9y6cYiXzBLcRoHSWRzMES208bq2b7uRI",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgoR9al384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uEUHqoQh47wMvcYi9SDrfMb3islBglUbuGcRScH8Q3MbnMdoi0yJGy53LUrQ%25r9RXnW8zWubxuqogqaFQ8l3ilUj7dcRScH7wgMbnMdg9RyJGy5ioErQ%25r9SbYW8zWunFHqogqaGjJl3ilU%254ecRScHzesMbnMdg5uyJGy5i03rQ%25r9SDGW8zWunsQqogqaGoOl3ilU%25t0cRScHzDsMbnMdgPoyJGy5mSBrQ%25r9sKJW8zWuKbGqogqaDJKl3ilUCGRcRScHbQ9MbnMdJ5SyJGy5Q3SrQ%25r98R5W8zWuobSqogqa3G7l3ilUR3AcRScHb6oMbnMdJCYyJGy55oarQ%25r99oUW8zWuuaCqogqaa9Ol3ilUEdocRScHFJ5MbnMdjodyJGy57agrQ%25r90FCW8zWuBc6qogqaY2al3ilUEORcRScHeomMbnMdmsYyJGy5s71rQ%25r9K1RW8zWuDAQqoQEdcNq0zPG7ZqoQagyoGlBg1jJ3r13F5ot",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgKRrvl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSD5qoQh47wMvcYi9SKGHMb3islBglUQzjcRScH8ZgMbnMdg9RyJGy5iRBrQ%25r9SKCW8zWunaHqogqaG4zl3ilU%25t0cRScHzZ8MbnMdeoiyJGy5m3erQ%25r98uGW8zWuobGqogqa3Jul3ilURQGcRScHb6oMbnMdjWtyJGy53obrQ%25r9RXHW8zWuKSMqogqaYH8l3ilUEbdcRScHF8HMbnMdjuzyJGy57EDrQ%25r9019W8zWuBwoqogqaFjHl3ilUQTUcRScHzj8MbnMdgbkyJGy55oarQ%25r99oUW8zWuuaCqogqaaInl3ilUjJ0cRScH7o3MbnMd0%253yJGy5iYarQ%25r9SERW8zWuKDQqogqaDn3l3ilURJ5cRScHbR2MbnMdJCYyJGqo9qaR9nl38F5MIlBgL%250Pl38Uir3%25cYiA7QRWARj93N",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgnRnKl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uRCHqoQh47wMvcYi9kQRAMb3islBglUbTFcRScH8oBMbnMdoi0yJGy53ARrQ%25r9RXHW8zWubxGqogqaFQ8l3ilUjGacRScH7GoMbnMd0ViyJGy5ioErQ%25r9SbFW8zWunFHqogqaGjJl3ilU%25FQcRScHzj7MbnMdgsoyJGy5iKnrQ%25r9SgyW8zWunAjqogqaGsdl3ilU%25KmcRScHzDYMbnMdgPoyJGy5mYnrQ%25r9snYW8zWuKbGqogqaDJ6l3ilUCQDcRScH48PMbnMdeo1yJGy5mgRrQ%25r9si8W8zWuoRHqogqa3EFl3ilURQzcRScHb8UMbnMdJozyJGy5QiErQ%25r98QxW8zWuomjqogqa3sFl3ilUUJ5cRScHHQmMbnMddQuyJGy559KrQ%25r99d2W8zWuBUQqogqaYRHl3ilUEQUcRScHF9%25MbnMdjYKyJGy57qErQ%25r90lIW8zWuBAuqogqaY20l3ilU48ecRScHemBMb37ur1MESxgYXMb3dnqbgyFntBoJltJ0ab6",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgnRnKl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uRCHqoQh47wMvcYi9kQRAMb3islBglUbTFcRScH8oBMbnMdoi0yJGy53ARrQ%25r9RXHW8zWubxGqogqaFQ8l3ilUjGacRScH7GoMbnMd0ViyJGy5ioErQ%25r9SbFW8zWunFHqogqaGjJl3ilU%25FQcRScHzj7MbnMdgsoyJGy5iKnrQ%25r9SgyW8zWunAjqogqaGsdl3ilU%25KmcRScHzDYMbnMdgPoyJGy5mYnrQ%25r9snYW8zWuKbGqogqaDJ6l3ilUCQDcRScH48PMbnMdeo1yJGy5mgRrQ%25r9si8W8zWuoRHqogqa3EFl3ilURQzcRScHb8UMbnMdJozyJGy5QiErQ%25r98QxW8zWuomjqogqa3sFl3ilUUJ5cRScHHQmMbnMddQuyJGy559KrQ%25r99d2W8zWuBUQqogqaYRHl3ilUEQUcRScHF9%25MbnMdjYKyJGy57qErQ%25r90lIW8zWuBAuqogqaY20l3ilU48ecRScHemBMb37ur1MESxgYXMb3dnqbgyFntBoJltJ0ab6",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgERrIl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSDJqoQh47wMvcYi9StrfMb3islBglU%257AcRScJHZuMbnMddUkyJGy5BYurQ%25rosSbW8zWuEs7qogqaFQdl3ilUjG6cRScJtrfMbnMdgBtyJGy5BO3rQ%25r9RbFW8zWuKb2qogqaDn3l3ilU%258jcRScH8ZuMbnMdJ13yJGy5Q0BrQ%25r98KGW8zWuEUQqogqaG4zl3ilU%25D8cRScHzUAMbnMdg8YyJGy53SBrQ%25r9sKJW8zWunm7qogqaGbHl3ilUC7gcRScHJzYMbnMdg9RyJGy87u3rQ%25r9oSHW8zWu3n9qogqaRnal3ilUQtacRScH8ZAMbnMdgbEyJGy5mSBrQ%25r9sRwW8zWuobuqogqa3o1l3ilUUb5cRScHHdmMbnMdjUayJGy57zRrQ%25r90FFW8zWuBj4qogqaCJGl3ilU4tQcRScHeN3MbnMdmI3yJGy5s6UrQ%25r9YbJW8zWuBAuqogqaGEJl3ilUEHmcRScHe58MbnMdmsoyJGy53YarQ%25r98R5W8zWuomjqogqaYCJl3ilU48ecRScHe8zMbnMdd8uyJGy5iYvrQ%25r9S5NW8zWunYEqogqaYV%25l3ilUUdgcRoj9y6cYiXzBLcRoHSWRzMES208bq2b7uRI",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgbRntl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSGNqoQh47wMvcYi9kQC5Mb3islBglUb%259cRScHJzYMbnMdQ2syJGy53obrQ%25r9RbDW8zWubGEqogqaJCFl3ilUQtacRScH8ZuMbnMd03RyJGy5BzRrQ%25r9SaJW8zWunJjqogqaGQFl3ilU%2575cRScHz08MbnMdg70yJGy5iKErQ%25r9SRwW8zWun9KqogqaGKQl3ilU%256DcRScHzRUMbnMdgCuyJGy5i4FrQ%25r9sEGW8zWuKGEqogqaDC8l3ilUCQzcRScH48AMbnMdeo4yJGy5m3XrQ%25r9sibW8zWuKSoqogqa3bdl3ilURHJcRScHbmsMbnMdJoiyJGy5Q3drQ%25r98RiW8zWuonjqogqa3oTl3ilURK0cRScHF53MbnMdjQ9yJGy5735rQ%25r90gsW8zWuBj4qogqaYM7l3ilUEyAcRScHFNHMbnMdjIEyJGy57kSrQ%25r90vSW8zWuDJCqogqaC47l38F5MIlBgL%250Pl38Uir3%25cYiA7QRWARj93N)",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgbR9%25l384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSGKqoQh47wMvcYi9In%25oMb3islBglUb%25BcRScHJwoMbnMdQVAyJGy58E0rQ%25r9RnYW8zWubxdqogqaJh%25l3ilUj8ocRScH7GoMbnMdg9RyJGy5iRErQ%25r9SbYW8zWunYEqogqaG47l3ilU%25aCcRScHzqjMbnMdg43yJGy5iOSrQ%25r9SQ5W8zWuKGEqogqaDJ6l3ilUCQDcRScH48PMbnMdeo1yJGy5mgRrQ%25r9si8W8zWuoRHqogqa3EFl3ilURemcRScHb8gMbnMdJoHyJGy5Q3grQ%25r98SFW8zWuonNqogqa3oTl3ilURK0cRScHbD7MbnMdd8RyJGy55ODrQ%25r99pbW8zWuufoqogqaYH8l3ilUEbdcRScHF8HMbnMdj%25eyJGy57EDrQ%25r90lFW8zWuBc6qogqaY2al3ilUEtBcRScHFpIMbnMdm3syJGy5sKErQbBUq2rjGTSFhrQb9%25cQSW7%25IER8MI8YHQA",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpua8rQbhSIqppglBgbRGal384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSDUqoQh47wMvcYi9M%25CoMb3islBglUb6%25cRScH8ZuMbnMdoPiyJGy53LFrQ%25r9YbJW8zWuEJjqogqaFjdl3ilU%25ddcRScHzo7MbnMdg33yJGy5isErQ%25r9SRbW8zWun9rqogqaGuvl3ilU%25DzcRScHzRuMbnMdgbEyJGy5i6ErQ%25r9SeCW8zWunxbqogqaD%25Fl3ilUCQzcRScH48jMbnMdeo4yJGy5m3ArQ%25r9sicW8zWuKSVqogqa3J%25l3ilURQacRScHb8%25MbnMdJgYyJGy5Qd3rQ%25r98QIW8zWuotJqogqa3s7l3ilURKdcRScHF53MbnMdjQ9yJGy5735rQ%25r90UiW8zWuBj4qogqaYM1l3ilUEtUcRScHeomMbnMdmsYyJGy5s6BrQbBUq2rjGTSFhrQb9%25cQSW7%25IER8MI8YHQA",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgbR9Kl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSGVqoQh47wMvcYi9hQrfMb3islBglUb%259cRScHJzUMbnMdQgEyJGy58gFrQ%25r9oNSW8zWubRQqogqaJC4l3ilUQ4jcRScH8NuMbnMdoPayJGy53LFrQ%25r9YaJW8zWuEJQqogqaFQ7l3ilUj8jcRScH78IMbnMd0zJyJGy5BOUrQ%25r9SaJW8zWunRUqogqaGbFl3ilU%258QcRScHzoBMbnMdg30yJGy5iSRrQ%25r9SKFW8zWunDRqogqaGJ8l3ilU%25a1cRScHzCoMbnMdg4ayJGy5iz1rQ%25r9SQHW8zWunAEqogqaGsel3ilU%25K9cRScHzDYMbnMdei0yJGy5msbrQ%25r9sRnW8zWuKbIqogqaDJKl3ilUCGpcRScHbj7MbnMdJsKyJGy5Q3SrQ%25r98R5W8zWuobSqogqa3G7l3ilUR3AcRScHb6oMbnMdJCYyJGy5Q4BrQ%25r99FaW8zWuujMqogqaYH8l3ilUEbdcRScHF8HMbnMdj%25eyJGy57EDrQ%25r90lFW8zWuBc6qogqaY2al38F5MIlBgL%250Pl38Uir3%25cYiA7QRWARj93N",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBg3R9tl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSGrqoQh47wMvcYi967rfMb3islBglUb%25acRScHJzYMbnMdQzAyJGy58ORrQ%25r9o19W8zWubxdqogqaJh%25l3ilUjdocRScH7o3MbnMd03YyJGy5BOSrQ%25r9SaaW8zWunRUqogqaGbFl3ilU%2580cRScHzo7MbnMdgi3yJGy5isErQ%25r9SKCW8zWun9IqogqaGrEl3ilU%25D8cRScHzCuMbnMdgV3yJGy5iOSrQ%25r9SQHW8zWunAUqogqaD%25Fl3ilUC4ocRScH48gMbnMdeo2yJGy5m3erQ%25r9siwW8zWuoC4qogqa3J%25l3ilURQacRScHb8%25MbnMdJgYyJGy5Qd3rQ%25r98QIW8zWuotJqogqa3s7l3ilURKjcRScHHdQMbnMddVKyJGy55ElrQ%25r90aJW8zWuB3UqogqaYJal3ilUEnCcRScHFBsMbnMdjWYyJGy57qNrQ%25r9019W8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBg3R99l384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uEC4qoQh47wMvcYi9hQrfMb3islBglUb%259cRScHJzUMbnMdQzdyJGy58tQrQ%25r9R3JW8zWubDEqogqaJoDl3ilUQT9cRScH8ZYMbnMd09RyJGy5BRbrQ%25r9YbFW8zWuESoqogqaFk%25l3ilU%25docRScHzQ5MbnMdg80yJGy5iRErQ%25r9SbYW8zWunGJqogqaGC7l3ilU%254JcRScHz83MbnMdgH2yJGy5ieRrQ%25r9SmHW8zWunNkqogqaGo5l3ilU%25tjcRScHzDYMbnMdei0yJGy5msbrQ%25r9sRnW8zWuKbIqogqaDJKl3ilUCGpcRScHbj7MbnMdJsKyJGy5Q3SrQ%25r98R5W8zWuobSqogqa3G7l3ilUR3AcRScHb6oMbnMdJCYyJGy5Q4BrQ%25r993UW8zWuuRCqogqaaRdl3ilUUHecRScHHBWMbnMdj9RyJGy578urQ%25r90R9W8zWuBiKqogqaY7el3ilUEy0cRScHFr2MbnMdjIdyJR0aWAyFnhiExyJR5GlJirjGNY3QcNQBUJ1",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgbR9tl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSDJqoQh47wMvcYi967%25oMb3islBglUb%25acRScHJzYMbnMdQzAyJGy58ORrQ%25r9o19W8zWubxdqogqaJh%25l3ilUjdocRScH7o3MbnMd03YyJGy5BOSrQ%25r9SaaW8zWunRUqogqaGbFl3ilU%2580cRScHzo7MbnMdgi3yJGy5isErQ%25r9SKCW8zWun9IqogqaGrEl3ilU%25D8cRScHzCuMbnMdgV3yJGy5iOSrQ%25r9SQHW8zWunAUqogqaD%25Fl3ilUC4ocRScH48gMbnMdeo2yJGy5m3erQ%25r9siwW8zWuoC4qogqa3J%25l3ilURQacRScHb8%25MbnMdJgYyJGy5Qd3rQ%25r98QIW8zWuotJqogqa3s7l3ilURKjcRScHHdQMbnMddVKyJGy55ElrQ%25r90aJW8zWuB3UqogqaYJal3ilUEnCcRScHFBsMbnMdjWYyJGy57qNrQ%25r9019W8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgbR9vl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSDCqoQh47wMvcYi9hQrfMb3islBglUb%259cRScHJzUMbnMdQgEyJGy58gFrQ%25r9oHnW8zWubRQqogqaJC4l3ilUQ4jcRScH8NuMbnMdoPayJGy53LmrQ%25r9RXcW8zWuEUQqogqaFQ8l3ilUj80cRScH7o7MbnMd0o6yJGy5BgQrQ%25r9YpHW8zWunUUqogqaGbHl3ilU%25JjcRScHzo8MbnMdg3YyJGy5iRBrQ%25r9SnbW8zWunDjqogqaGCbl3ilU%25QocRScHzUAMbnMdg43yJGy5ieUrQ%25r9SpDW8zWun8kqogqaGo3l3ilU%25tdcRScHzDsMbnMdgCEyJGy5ikvrQ%25r9snYW8zWuKbGqogqaDJ6l3ilUCQDcRScH4%25fMbnMdJ70yJGy5QKDrQ%25r98RnW8zWuob9qogqa3Jnl3ilUR%250cRScHbR2MbnMdJ13yJGy5Q4ErQ%25r98eYW8zWuuaRqogqaa7yl3ilUEdocRScHFJ5MbnMdjodyJGy57zmrQ%25r90FCW8zWuBcjqogqaYM1l3ilUtzacRoj9y6cYiXzBLcRoHSWRzMES208bq2b7uRI",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgbRGyl384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uSD5qoQh47wMvcYi9h%25rfMb3islBglUbGBcRScHJUCMbnMdoISyJGy536UrQ%25r9RXHW8zWubxGqogqaJhOl3ilUjdocRScH7o3MbnMd03YyJGy5BgQrQ%25r9YpRW8zWunJjqogqaGQFl3ilU%25z8cRScHzeBMbnMdgH2yJGy5ieRrQ%25r9SmHW8zWunfJqogqaGk%25l3ilU%25t0cRScHzN5MbnMdgCKyJGy5i4FrQ%25r9SXRW8zWuKGEqogqaDJ%25l3ilUCQ1cRScH48CMbnMdezJyJGy5Q3SrQ%25r98R5W8zWuobSqogqa3G7l3ilURaQcRScHbR2MbnMdJ13yJGy5Q4ErQ%25r98eYW8zWuujMqogqaYH8l3ilUEbdcRScHF8HMbnMdjuzyJGy57zmrQ%25r90FCW8zWuBcjqogqaYM1l3ilU48ecRScHemBMb37ur1MESxgYXMb3dnqbgyFntBoJltJ0ab6",
                "https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-2545xM4RIyFnbm9Mb3AgyyIJrjG0suyJRBODlsrjGpuaprQbhSIqppglBgBRd1l384MlficYiGHqoQxYLW7%25f3tiJ0PCJirQbLDWcQW7%251uEUHqoQh47wMvcYi9SDrfMb3islBglUbQqcRScHJzuMbnMdQzqyJGy582lrQ%25r9R3JW8zWubGEqogqaJ2al3ilUQT9cRScH8ZgMbnMd03RyJGy5iubrQ%25r9SbYW8zWunFHqogqaGjJl3ilU%254mcRScHzd9MbnMdg7oyJGy5iKnrQ%25r9S5SW8zWunyoqogqaGoOl3ilUCzjcRScH4e3MbnMdeoiyJGy5m3lrQ%25r9sRAW8zWuKSoqogqa3bdl3ilURHgcRScHb8gMbnMdJoHyJGy5Q3grQ%25r98QIW8zWuotJqogqa3s7l3ilUUupcRScHF53MbnMdjQ9yJGy5735rQ%25r90gsW8zWuBj4qogqaYM1l3ilUEtUcRScHFpgMbnMdm3syJGy5sKErQ%25r91nNW8JYHltW7%25ZnjTW8JuzM8nq0z6Fboy6oEd82",
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
                "https://prod.cosy.bmw.cloud/miniweb/cosySec?COSY-EU-100-7331L%25LayVd4Ws46Iq5gmvhmN2VUyXqiGtySE5CpLjFt3aJqZvjDlwXYuN4WD9%25UsDOPit2VZ8XiDESHWp3mlDWLfV91KVZ0pEuTQLjKvQFQ%25d4b2Ydw6ZuQLqptQ%25wc3ZylifZu%25KXcCYHSc3uBrBNCJdKX324NFlTQBrXpFkIclZ24riInY3scpF4Hv5AQ0KiIFJG8WxABHvIT9PGhO2JGvloVqjgpT9GsLzjQUilo90yaAwbHsLoACROkhJ0yLOExZlqTACygNWK3mlOECUkeRs7sgNEbn%25hL10UkNh5uqiVAbnkq83mazOh5nmPX5Eagq857Mr8fRUmP81D4Jkxb7MPVYFvnWh1DMztIG0eqVYDafv0ZjmztYRSGBO67aftxd92hw1RSfWQo4Y%25VxdSeZLs3uzWQdjcy9T3aeZQ6KCnSXRjcZwBQv4rx6Kc%252ZuJ4WwBKupcBQFe%252B3iK2RIjup2XHBJsv63iprJ2T9GwXHi4TpzB9%25rJHFliafou4TJIsHpWL3FlTv0JnHyXIslGAT5MCrv0s9Ol%25kE4GA0ogsmLNF9OALUP6XkIogOybMcrnvLUgChDYC5GybUEqYtY89ChbNmtfkPoEqhk7fSpMLNmqn1SdfDyk7m5VdQPYCn178zQZStE5V1PaZ3dfN8zVMRcWQSkPazDxKFcdnMRaYWBIqQ5DxRte2vFZ8YWxfjpT2cPteWS6i1UKMfjedwSEBBDFjTgH%25ekxh0mzXRTZhOIBQmSwpsB%25yzDuP%25ABNSi4cFLURAWVxEa7sgNp0UoPBDSUjea5EE4Gd0sHuusjdzOh5JDyejhw8UqIbxC2yv4cPrUtV5lkmbO7fNwyzMpBzcM6p0lZyQVo7Xau8jmBLViuADOPJEFg1qTMUw8jSK9QFe0SRnm2KVZEYA89RJBzc62O%25lZyQjKrPXYu3PCzOSM5Z7pRix2uzt",
                "https://prod.cosy.bmw.cloud/miniweb/cosySec?COSY-EU-100-7331L%25LayVd4Ws46Iq5gmvhmK0bdyXqiGtySE5CpLjFt3aJqZvjDlwXYu34WX9%25UsDOPit2VZ8XrevZ1RCzQFe0LwzXy2osfNw273QqdvQFnozlE47ivb4g4TrOD9%25rJHFl47pou4TJIsF1NL3FlTv0IV%25yXIslGAGEtCrv0s9Oao6E4GA0ogRUkNF9OALUxbvkIogOybWUMnvLUgChe%2585GybUEqjXO89ChbNm6ipPoEqhk7ZfHMLNmqn1cHFDyk7m5VKJ9YCn178zBPltE5V1Pa2IkfN8zVMRpG9SkPazDxi9jdnMRaYWHYtQ5DxRteJp8Z8YWxfjTk4cPteWS6AdEKMfjedwOQ2BDS6jQ%25g6x2Ydw6ZuUw4ptQ%25wc3bkeifZu%25KXhmjHSc3uBrq7PJdKX324mPGTQBrXpF7LDlZ24riI1ySscpF4HvV5B0KiIFJGz7kABHvIT9ae4O2JGvloIqUgpT9GsLv0NUilo90yGoIbHsLoAC9L2hJ0yLOEoN5qTACygNLk7mlOECUkyKo7sgNEbnCBr10UkNh5EyiVAbnkq8NeEzOh5nmPkj%25agq857MnsWRUmP81D5dVxb7MPVYwTOWh1DMzt%25GgeqVYDafu3ajmztYRS3X367aftxdXrWw1RSfWQr4y%25VxdSeZ4FruzWQdjcFIw3aeZQ6KIv4XRjcZwBvAFrx6Kc%252GiI4WwBKup9bGFe%252B3iohSIjup2XHLqbv63iprJykLGwXHi4TCZY9%25rJHFl4RooubJkDEsHWpf8dKO2kvfMhoId4ly5oszKu0wsPox4CUGbVY2PicpRBQ5Dxy8Y1wou4YJHBj7HdP3wu7BcVxb7MsfNw%2573Dq19mjkHNov2YIqdRMA8VmbzQ53NxtJix2tuJgABNKRCzFWrD%25ViERTrUfbYsnGBI10tq3D%25ZpyKGwgZePVHpRBnSUDyesix2uHbXABNK%25pIYFSr4YkxbZtMBzJeTjHrxd",
                "https://prod.cosy.bmw.cloud/miniweb/cosySec?COSY-EU-100-7331L%25LayVd4Ws46Iq5gmvhmTAVUyXqiGtySE5CpLjFt3aJqZvjDlwXYuGFDA9%25UsDOPit2VZ8XrevZ1RCzQFe0LwzXy2osfNw273QqdvQFnozlE47ivb4g4Tret9%25rJHFlFeIou4TJIsIVGL3FlTv0VGayXIslGAzOECrv0s9OagFE4GA0ogRwlNF9OALUxnLkIogOybWBKnvLUgChe2G5GybUEqjhY89ChbNm63MPoEqhk7ZfHMLNmqn1cHFDyk7m5VK8TYCn178zBFNtE5V1Pa2vGfN8zVMRpKkSkPazDxi3AdnMRaYWlBOQ5DxRtesOyZ8YWxfj0SzcPteWS6AdEKMfjedwOQ2BDS6jQ%25g6x2Ydw6ZuUw4ptQ%25wc3bXFifZu%25KXhndHSc3uBrq6JJdKX324m1wTQBrXpF7VDlZ24riI1U3scpF4HvVxX0KiIFJGztyABHvIT9aNSO2JGvloRkcgpT9GsLxkkUilo90yWwJbHsLoAC91qhJ0yLOEog5qTACygNLCimlOECUkynP7sgNEbnC5V10UkNh5E2yVAbnkq8NpFzOh5nmPkEJagq857Mn6fRUmP81D5wnxb7MPVY8%25XWh1DMztPO6eqVYDafusUjmztYRS3ob67aftxdXrxw1RSfWQr4r%25VxdSeZ4FjuzWQdjcFIE3aeZQ6KIvFXRjcZwBvGurx6Kc%252G9I4WwBKup9gvFe%252B3ioJGIjup2XHLqdv63iprJymhGwXHi4TCny9%25rJHFl4RooubJkDEsHWpf8dKO2kvfMhoId4ly5oszKu0wsPox4CUGbVY2PicpRBQ5Dxy8Y1wou4YJHBj74WuGqsO2JGdyXqmJ19iTjHbrYX6WPoxiEAGZIlH2sNF1XOLtDOPL7tKZ8X5AusRgz9mlD3AfzBy2od4eXDTQLi19mkM%255eqKkUvlYMA84CB9%25UdDOP7Y2VZ8X5mMxoRCzaorO2kLG8stUfbYzOE",
                "https://prod.cosy.bmw.cloud/miniweb/cosySec?COSY-EU-100-7331L%25LayVd4Ws46Iq5gmvhmKMyyyXqiGtySE5CpLjFt3aJqZvjDlwXYuq4O29%25UsDOPit2VZ8XrevZ1RCzQFe0LwzXy2osfNw273QqdvQFnozlE47ivb4g4TiCA9%25rJHFl47you4TJIsI7fL3FlTv0v6%25yXIslGAzsHCrv0s9OaN3E4GA0ogRO2NF9OALUtyKkIogOybfD4nvLUgChZB35GybUEqcNP89ChbNmKhzPoEqhk7BSUMLNmqn12z8Dyk7m5VqztYCn178zmZBtE5V1Pa7omfN8zVMR16cSkPazDxK9QdnMRaYWB2tQ5DxRte2vCZ8YWxfjxLucPteWS6WfRKMfjedwe7YBDS6jQ%25mt42Ydw6ZuQLTptQ%25wc3csfifZu%25KXKyBHSc3uBrBKkJdKX324NFlTQBrXpFkazlZ24riIqgRscpF4HvmYP0KiIFJGzbWABHvIT9alrO2JGvloRG4gpT9GsLxnKUilo90yWE7bHsLoACe%25phJ0yLOEozpqTACygNLafmlOECUkyih7sgNEbnRBJ10UkNh5xWxVAbnkq8WeszOh5nmPe%253agq857M5FbRUmP81D8Llxb7MPVYPegWh1DMztLj5eqKD3v%25fMA8o4ykQ53RoIBeayVt6refTkqSbfFe0VwcxKJG5FPN8snCrv064GHbeqVGDMngiMAKob27d8Dyk7IagdQkc1EnTNfUXglH%25ViExM7Gq7xua2Il6gXUi5Bo0aVo70nawjmBq9cvDLPlkIVK9RP%25AusWpf5TFe0X5lkb1ZqfNwbyJIz19mpO%25lZyWVo7nzu8jmBqk1YsDOP5I2oub0TmvayRCzTfr",
                "https://prod.cosy.bmw.cloud/miniweb/cosySec?COSY-EU-100-7331L%25LayVd4Ws46Iq5gmvhmNAjKyXqiGtySE5CpLetUi5Zo1srPAb4g6qqdzOSMrt3kME2oubhl1oBHWp9mlDRApbxEaMIjAEKU9ZG19mwapPeqKk1dqfq8hlFzOh5nmPmjgagq857MBjRRUmP81D2Vlxb7MPVYpteWh1DMztifmeqVYDafHtujmztYRSJ0w67aftxdTL3w1RSfWQlUY%25VxdSeZsNEuzWQdjc0ka3aeZQ6KoInXRjcZwBL%25mrx6Kc%252y574WwBKupC8hFe%252B3iEXMIjup2XHNrwv63iprJkV%25GwXHi4TnaR9%25rJHFl5RVou4TJIs8k3L3FlTv0P1HyXIslGAM7QCrv0s9Of5ZE4GA0ogSZwNF9OALUdylkIogOybQCunvLUgChZE85GybUEqcbV89ChbNmK7zPoEqhk7BXyMLNmqn12iUDyk7m5VpHIYCn178ziIWtE5V1PaH6GfN8zVMRJwySkPazDxT%25jdnMRaYWl2VQ5DxRtes6GZ8YWxfj0wpcPteWS6A%250KMfjedwOukBDS6jQ%25gqt2Ydw6ZuUmeptQ%25wc36lHifZu%25KXwuDHSc3uBr%254vJdKX324uFlTQBrXpF3PalZ24riIXuYscpF4HvrbL0KiIFJG4hrABHvIT9Fq1O2JGvloIZbgpT9GsLmSKUilo90y7jBbHsLoAC1VAhJ0yLOEVzVqTACygNzaUmlOECUkaRu7sgNEbnRxa10UkNh5xWmVAbnkq8WeRzOh5nmPecxagq857MjYWRUmP81D6pjxb7MPVYwiEWh1DMzt%25HpeqVYDafu4%25jmztYRS3nL67aftxdt%25qw1RSfWQxg%25%25ViSFLrZfbYEGkPBDFjEoH%25ekxQ3v%25ZAPVc7Z9%25UxXp6i0yD9t8YgMnvLU3Gys7%25VxySfMqlfbiE7JaKYSkPaoeqKBPpR5MA8ZmIqOsrxl56fayVD8kYw1pqSWvFSrW2vEyXq3fbYTWHRBDFhfGHNekxo701EMLW5pRB%25rU30KE%25QzDI4fX7jNRUQoFSr2YkiyXq3B4lxTjH1cmSk%25WaXYvQGZIH0Z",
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
