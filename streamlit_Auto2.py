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
            "쉐보레": ["더 뉴 티볼리",
                    "더 뉴 티볼리 에어",
                    "리스펙 코란도",
                    "코란도 EV",
                    "더 뉴 토레스",
                    "토레스(J100)",
                    "토레스 EVX(U100)",
                    "렉스턴 뉴 아레나",
                    "렉스턴 스포츠 쿨멘",
                    "렉스턴 스포츠 쿨멘 칸"],

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

            "르노": ["클리오", "캡처", "트윙고", "메간", "탈리스만", "에스파스", "카자르", "콜레오스", "마스터", "조에"],
            "다피코": ["다피코1", "다피코2", "다피코3", "다피코4", "다피코5", "다피코6", "다피코7", "다피코8", "다피코9", "다피코10"],
            "스마트 EV": ["스마트EV1", "스마트EV2", "스마트EV3", "스마트EV4", "스마트EV5", "스마트EV6", "스마트EV7", "스마트EV8", "스마트EV9", "스마트EV10"],
            "마이브": ["마이브1", "마이브2", "마이브3", "마이브4", "마이브5", "마이브6", "마이브7", "마이브8", "마이브9", "마이브10"],
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
            "BMW": ["3 Series", "5 Series", "7 Series", "X1", "X3", "X5", "X7", "Z4", "i3", "i8"],
            "아우디": ["A4", "A6", "A8", "Q2", "Q3", "Q5", "Q7", "Q8", "TT", "R8"],
            "폭스바겐": ["Golf", "Passat", "Polo", "Tiguan", "Touareg", "Jetta", "Arteon", "T-Roc", "ID.3", "ID.4"],
            "미니": ["Mini Cooper", "Mini Countryman", "Mini Clubman", "Mini Convertible", "Mini Electric", "Mini JCW", "Mini Roadster", "Mini Paceman", "Mini Coupé", "Mini Rocketman"],
            "볼보": ["XC60", "XC90", "S60", "S90", "V60", "V90", "XC40", "C40", "V40", "S80"],
            "폴스타": ["Polestar 1", "Polestar 2", "Polestar 3", "Polestar 4", "Polestar 5", "Polestar 6", "Polestar 7", "Polestar 8", "Polestar 9", "Polestar 10"],
            "랜드로버": ["Range Rover", "Discovery", "Evoque", "Defender", "Velar", "Sport", "Freelander", "Series", "County", "Santana"],
            "포르쉐": ["911", "Cayenne", "Macan", "Panamera", "Taycan", "Boxster", "Cayman", "Carrera", "Targa", "Spyder"],
            "람보르기니": ["Aventador", "Huracan", "Urus", "Gallardo", "Murciélago", "Diablo", "Reventón", "Veneno", "Sian", "Centenario"],
            "벤틀리": ["Continental", "Bentayga", "Flying Spur", "Mulsanne", "Arnage", "Azure", "Brooklands", "Turbo R", "Hunaudières", "Mark VI"],
            "맥라렌": ["720S", "GT", "P1", "600LT", "650S", "675LT", "MP4-12C", "Senna", "Elva", "Artura"],
            "페라리": ["488", "Portofino", "812 Superfast", "Roma", "F8 Tributo", "SF90 Stradale", "GTC4Lusso", "California", "LaFerrari", "Enzo"],
            "에스턴마틴": ["DB11", "Vantage", "DBS", "Rapide", "Vanquish", "Valkyrie", "One-77", "Virage", "Lagonda", "Cygnet"],
            "로터스": ["Evora", "Elise", "Exige", "Emira", "Evija", "Esprit", "Europa", "Elite", "Eclat", "Seven"],
            "마세라티": ["Ghibli", "Levante", "Quattroporte", "GranTurismo", "GranCabrio", "MC20", "Biturbo", "Bora", "Merak", "MC12"],
            "롤스로이스": ["Phantom", "Ghost", "Wraith", "Dawn", "Cullinan", "Silver Shadow", "Corniche", "Park Ward", "Seraph", "Cloud"],
            "푸조": ["208", "3008", "508", "2008", "5008", "308", "4008", "1007", "607", "RCZ"],
            "이네오스": ["Grenadier", "Defender", "Pathfinder", "Shogun", "Patriot", "Trooper", "Tracker", "Vanguard", "Warrior", "Pioneer"],
            "포드": ["Mustang", "Explorer", "Fiesta", "Focus", "Escape", "Edge", "Ranger", "Everest", "F-150", "Bronco"],
            "링컨": ["Navigator", "Corsair", "Aviator", "MKC", "MKT", "MKX", "MKZ", "Town Car", "Continental", "Blackwood"],
            "지프": ["Wrangler", "Grand Cherokee", "Renegade", "Compass", "Cherokee", "Patriot", "Commander", "Liberty", "Gladiator", "Scrambler"],
            "GMC": ["Sierra", "Yukon", "Canyon", "Acadia", "Terrain", "Savana", "Envoy", "Jimmy", "Safari", "Sonoma"],
            "캐딜락": ["Escalade", "XT5", "XT4", "XT6", "CT4", "CT5", "ATS", "CTS", "XTS", "DTS"],
            "테슬라": ["Model S", "Model 3", "Model X", "Model Y", "Cybertruck", "Roadster", "Semi", "Solar Roof", "Powerwall", "Autopilot"],
            "토요타": ["Camry", "Corolla", "Prius", "Highlander", "RAV4", "Supra", "Land Cruiser", "4Runner", "Tacoma", "Tundra"],
            "렉서스": ["ES", "RX", "LS", "NX", "GX", "UX", "IS", "RC", "LC", "LFA"],
            "혼다": ["Accord", "Civic", "CR-V", "HR-V", "Pilot", "Passport", "Ridgeline", "Odyssey", "Insight", "Clarity"]
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
            "쉐보레": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
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

            "르노": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "다피코": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "스마트 EV": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "마이브": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
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
            "BMW": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "아우디": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "폭스바겐": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "미니": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "볼보": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "폴스타": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "랜드로버": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "포르쉐": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "람보르기니": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "벤틀리": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "맥라렌": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "페라리": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "에스턴마틴": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "로터스": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "마세라티": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "롤스로이스": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "푸조": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "이네오스": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "포드": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "링컨": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "지프": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "GMC": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "캐딜락": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "테슬라": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "토요타": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "렉서스": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"],
            "혼다": ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png", "img9.png", "img10.png"]
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
