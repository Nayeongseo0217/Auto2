import openai
import streamlit as st
import smtplib
from email.mime.text import MIMEText
import time
from streamlit_option_menu import option_menu

with st.sidebar:
    choice = option_menu("Menu", ["버튼으로 차량 고르기", "채팅으로 차량 상담하기"],
                         icons=['bi bi-hand-index-thumb', 'bi bi-chat-right-dots'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#0D6FBA"},
    }
    )

if choice == "버튼으로 차량 고르기":
    # 페이지 구성을 설정합니다.
    st.set_page_config(page_title="Auto Connect Chat Bot",  page_icon="https://ifh.cc/g/P8K9BV.png", layout="centered", initial_sidebar_state="expanded")

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

    if "button_state" not in st.session_state:
        st.session_state.button_state = "main"
        st.markdown("<hr>", unsafe_allow_html=True)

    def create_buttons(options, current_state, back_state=None, home_state="main"):
        for option, state in options.items():
            if st.button(option):
                st.session_state.button_state = state
        if current_state != "main":
            if back_state and st.button("이전으로 돌아가기"):
                st.session_state.button_state = back_state
            if st.button("처음으로 돌아가기"):
                st.session_state.button_state = home_state

    #    "버튼 상태(함수호출 느낌)": {
    #        "버튼 이름(실제로 보이는 것)": "클릭하면 변하게 되는 버튼의 상태(상태가 변함으로 '버튼 상태(함수호출 느낌)'를 실행하게 됨)"
    #   }

    buttons_data = {
        "main": {
            "신차구매 컨설팅": "신차구매 컨설팅",
            "중고차구매 컨설팅": "중고차구매 컨설팅",
            "리스렌트 승계 컨설팅": "리스렌트 승계 컨설팅",
            "A/S 사후관리 컨설팅": "사후관리 컨설팅",
            "법인 전문 컨설팅 의뢰": "법인 전문 컨설팅 의뢰",
            "상담 신청하기":"상담 신청하기",
        },
        "신차구매 컨설팅": {
            "국산차": "국산차",
            "수입차": "수입차",
            "최신 인기차량 추천받기": "최신 인기차량 추천받기",
            "나만의 모빌리티 선택하기": "나만의 모빌리티 선택하기",
            "이전으로 돌아가기": "main",
        },
        "중고차구매 컨설팅": {
            "국산차": "국산차",
            "수입차": "수입차",
            "상담 신청하기": "상담 신청하기1",
            "이전으로 돌아가기": "main",
        },
        "리스렌트 승계 컨설팅 컨설팅": {
            "국산차": "국산차",
            "수입차": "수입차",
            "상담 신청하기": "상담 신청하기2",
            "이전으로 돌아가기": "main",
        },
        "사후관리 컨설팅": {
            "상담 신청하기": "상담 신청하기3",
            "이전으로 돌아가기": "main",
        },
        "법인 전문 컨설팅 의뢰": {
            "상담 신청하기": "상담 신청하기4",
            "이전으로 돌아가기": "main",
        },
        "국산차": {
            "현대": "현대",
            "제네시스": "제네시스",
            "기아": "기아",
            "쉐보레": "쉐보레",
            "KG모빌리티": "KG모빌리티",
            "르노": "르노",
            "다피코": "다피코",
            "스마트 EV": "스마트 EV",
            "마이브": "마이브",
            "이전으로 돌아가기": "신차구매 컨설팅",
        },
        "수입차": {
            "유럽": "유럽",
            "미국": "미국",
            "일본": "일본",
            "이전으로 돌아가기": "신차구매 컨설팅",
        },
        "최신 인기차량 추천받기": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "신차구매 컨설팅",
        },
        "나만의 모빌리티 선택하기": {
            "미구현(main)": "미구현",
            "이전으로 돌아가기": "신차구매 컨설팅",
        },
        "유럽": {
            "벤츠": "벤츠",
            "BMW": "BMW",
            "아우디": "아우디",
            "폭스바겐": "폭스바겐",
            "미니": "미니",
            "볼보": "볼보",
            "폴스타": "폴스타",
            "랜드로버": "랜드로버",
            "포르쉐": "포르쉐",
            "람보르기니": "람보르기니",
            "벤틀리": "벤틀리",
            "맥라렌": "맥라렌",
            "페라리": "페라리",
            "애스턴마틴": "애스턴마틴",
            "로터스": "로터스",
            "마세라티": "마세라티",
            "롤스로이스": "롤스로이스",
            "푸조": "푸조",
            "이네오스": "이네오스",
            "이전으로 돌아가기": "수입차",
        },
        "미국": {
            "포드": "포드",
            "링컨": "링컨",
            "지프": "지프",
            "GMC": "GMC",
            "캐딜락": "캐딜락",
            "테슬라": "테슬라",
            "이전으로 돌아가기": "수입차",
        },
        "일본": {
            "토요타": "토요타",
            "렉서스": "렉서스",
            "혼다": "혼다",
            "이전으로 돌아가기": "수입차",
        },
        "현대": {
            "캐스퍼": "현대_1",
            "더 뉴 아반떼(CN7 F/L)": "현대_2",
            "더 뉴 아반떼N(CN7 F/L)": "현대_3",
            "더 뉴 아반떼HEV(CN7 F/L)": "현대_4",
            "쏘나타 디 엣지(DN8 F/L)": "현대_5",
            "쏘나타 디 엣지HEV(DN8 F/L)": "현대_6",
            "아이오닉6": "현대_7",
            "디 올-뉴 그랜저(GN7)": "현대_8",
            "디 올-뉴 그랜저HEV(GN7)": "현대_9",
            "베뉴": "현대_10",
            "디 올 뉴 코나(SX2)": "현대_11",
            "디 올 뉴 코나HEV(SX2)": "현대_12",
            "디 올 뉴 코나EV(SX2)": "현대_13",
            "넥쏘": "현대_14",
            "더 뉴 투싼(NX4 F/L)": "현대_15",
            "더 뉴 투싼HEV(NX4 F/L)": "현대_16",
            "디 올-뉴 산타페(MX5)": "현대_17",
            "디 올-뉴 산타페HEV(MX5)": "현대_18",
            "더 뉴 아이오닉5": "현대_19",
            "아이오닉5": "현대_20",
            "아이오닉5N": "현대_21",
            "더 뉴 팰리세이드": "현대_22",
            "스타리아": "현대_23",
            "스타리아HEV": "현대_24",
            "스타리아 아클란": "현대_25",
            "스타리아 아클란S": "현대_26",
            "ST1": "현대_27",
            "더 뉴 포터II": "현대_28",
            "더 뉴 포터II 특장차": "현대_29",
            "포터II EV": "현대_30",
            "포터II EV 특장차": "현대_31",
            "올 뉴마이티": "현대_32",
            "쏠라티": "현대_33",
            "이전으로 돌아가기": "국산차",
        },
        "제네시스": {
            "미구현": "제네시스_1",
            "미구현": "제네시스_2",
            "[준대형] G80(RG3 F/L)": "제네시스_3",
            "[준대형] G80(RG3)": "제네시스_4",
            "[준대형] e-G80(RG3)": "제네시스_5",
            "[대형] 신형 G90(RS4)": "제네시스_6",
            "미구현": "제네시스_7",
            "미구현": "제네시스_8",
            "[중형SUV] GV70(JK)": "제네시스_9",
            "미구현": "제네시스_10",
            "미구현": "제네시스_11",
            "미구현": "제네시스_12",
            "[대형SUV] GV80(JX)": "제네시스_13",
            "이전으로 돌아가기": "국산차",
        },
        "기아": {
            "더 뉴 모닝(JA PE)": "기아_1",
            "더 뉴 기아 레이(PE)": "기아_2",
            "레이 EV(PE)": "기아_3",
            "더 뉴 K3": "기아_4",
            "더 뉴 K3 GT": "기아_5",
            "더 뉴 K5(DL3 F/L)": "기아_6",
            "더 뉴 K5 HEV(DL3 F/L)": "기아_7",
            "K8(GL3)": "기아_8",
            "K8 HEV(GL3)": "기아_9",
            "더 뉴 K9(RJ)": "기아_10",
            "디 올 뉴 니로(SG2)": "기아_11",
            "디 올 뉴 니로EV(SG2)": "기아_12",
            "니로 플러스(DE)": "기아_13",
            "EV3": "기아_14",
            "더 뉴 셀토스": "기아_15",
            "디 올 뉴 스포티지(NQ5)": "기아_16",
            "디 올 뉴 스포티지 HEV(NQ5)": "기아_17",
            "더 뉴 쏘렌토(MQ4 F/L)": "기아_18",
            "더 뉴 쏘렌토 HEV(MQ4 F/L)": "기아_19",
            "더 뉴 EV6": "기아_20",
            "EV6": "기아_21",
            "EV6 GT": "기아_22",
            "EV9": "기아_23",
            "모하비 더 마스터": "기아_24",
            "더 뉴 카니발(KA4 F/L)": "기아_25",
            "더 뉴 카니발 HEV(KA4 F/L)": "기아_26",
            "카니발 헤리티지": "기아_27",
            "카니발 LM": "기아_28",
            "더 뉴봉고III(PU)": "기아_29",
            "더 뉴봉고III 특장차": "기아_30",
            "봉고III EV(PU)": "기아_31",
            "봉고III EV 특장차": "기아_32",
            "이전으로 돌아가기": "국산차",
        },
        "쉐보레": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "국산차",
        },
        "KG모빌리티": {
            "더 뉴 티볼리": "KG모빌리티_1",
            "더 뉴 티볼리 에어": "KG모빌리티_2",
            "리스펙 코란도": "KG모빌리티_3",
            "코란도 EV": "KG모빌리티_4",
            "더 뉴 토레스": "KG모빌리티_5",
            "토레스(J100)": "KG모빌리티_6",
            "토레스 EVX(U100)": "KG모빌리티_7",
            "렉스턴 뉴 아레나": "KG모빌리티_8",
            "렉스턴 스포츠 쿨멘": "KG모빌리티_9",
            "렉스턴 스포츠 쿨멘 칸": "KG모빌리티_10",
            "이전으로 돌아가기": "국산차",
        },
        "르노": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "국산차",
        },
        "다피코": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "국산차",
        },
        "스마트 EV": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "국산차",
        },
        "마이브": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "국산차",
        },
        "벤츠": {
            "A-Class(4세대)": "벤츠_1",
            "CLA-Class(2세대 F/L)": "벤츠_2",
            "The New C-Class(W206)": "벤츠_3",
            "The New E-Class(W214)": "벤츠_4",
            "EQE": "벤츠_5",
            "EQE-SUV": "벤츠_6",
            "S-Class(W223)": "벤츠_7",
            "Maybach S-Class(W223)": "벤츠_8",
            "EQS": "벤츠_9",
            "EQS-SUV": "벤츠_10",
            "CLE-Class": "벤츠_11",
            "SL-Class(R232)": "벤츠_12",
            "The New AMG GT 4DOOR": "벤츠_13",
            "GLA-Class": "벤츠_14",
            "The new EQA": "벤츠_15",
            "EQA": "벤츠_16",
            "GLB-Class": "벤츠_17",
            "The new EQB": "벤츠_18",
            "EQB": "벤츠_19",
            "The New GLC-Class(2세대)": "벤츠_20",
            "The New GLE-class(2세대 F/L)": "벤츠_21",
            "The New GLS-Class(2세대 F/L)": "벤츠_22",
            "The New Maybach GLS-Class": "벤츠_23",
            "Maybach GLS-Class": "벤츠_24",
            "G-Class(W463)": "벤츠_25",
            "이전으로 돌아가기": "유럽",
        },
        "벤츠_1": {
            "2024년형 가솔린 2.0 2WD 세단 : A220 Sedan(자동)": "벤츠_1_1_1",
            "2024년형 가솔린 2.0 2WD 해치백 : A220 Hatchback(자동)": "벤츠_1_2_2",
            "2024년형 가솔린 2.0 4WD 세단 : A35 Sedan AMG 4Matic(자동)": "벤츠_1_3_3",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_2": {
            "2024년형 가솔린 2.0 4WD : CLA 250 4Matic(자동)": "벤츠_2_1_1",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_3": {
            "2024년형 가솔린 2.0 AWD : C300 4Matic Avantgarde(자동)": "벤츠_3_1_1",
            "2024년형 가솔린 2.0 AWD : C300 4Matic AMG Line(자동)": "벤츠_3_1_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_4": {
            "2024년형 가솔린 2.0 2WD : E200 Avantgarde(자동)": "벤츠_4_1_1",
            "2024년형 가솔린 2.0 AWD : E300 4Matic Exclusive(자동)": "벤츠_4_2_1",
            "2024년형 가솔린 2.0 AWD : E300 4Matic AMG Line(자동)": "벤츠_4_2_2",
            "2024년형 가솔린 3.0 AWD : E450 4Matic Exclusive(자동)": "벤츠_4_3_1",
            "2024년형 디젤 2.0 AWD : E220d 4Matic Exclusive(자동)": "벤츠_4_4_1",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_5": {
            "2024년형 전기 2WD : EQE 350+(자동)": "벤츠_5_1_1",
            "2024년형 전기 AWD : EQE 350+ 4Matic(자동)": "벤츠_5_2_1",
            "2023년형 전기 2WD : EQE 300(자동)": "벤츠_5_3_1",
            "2023년형 전기 2WD : EQE 350+(자동)": "벤츠_5_3_2",
            "2023년형 전기 AWD : EQE 350+ 4Matic(자동)": "벤츠_5_4_1",
            "2023년형 전기 AWD : EQE 53 AMG 4Matic+(자동)": "벤츠_5_4_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_6": {
            "2024년형 전기 AWD : EQE 350 4Matic(자동)": "벤츠_6_1_1",
            "2023년형 전기 AWD : EQE 350 4Matic(자동)": "벤츠_6_2_1",
            "2023년형 전기 AWD : EQE 500 4Matic(자동)": "벤츠_6_2_2",
            "2023년형 전기 AWD : EQE 500 4Matic Launch Edition(자동)": "벤츠_6_2_3",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_7": {
            "2024년형 가솔린 3.0 4WD : S450 4Matic L(자동)": "벤츠_7_1_1",
            "2024년형 가솔린 3.0 4WD : S500 4Matic L(자동)": "벤츠_7_1_2",
            "2024년형 가솔린 4.0 4WD : S580 4Matic L(자동)": "벤츠_7_2_1",
            "2024년형 가솔린 3.0 플러그인 하이브리드 4WD : S580e 4Matic L(자동)": "벤츠_7_3_1",
            "2024년형 가솔린 4.0 플러그인 하이브리드 4WD : S63 AMG E Performance(자동)": "벤츠_7_4_1",
            "2024년형 디젤 3.0  4WD : S450d 4Matic(자동)": "벤츠_7_5_1",
            "2024년형 디젤 3.0  4WD : S450d 4Matic AMG Line(자동)": "벤츠_7_5_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_8": {
            "2024년형 가솔린 4.0 4WD : Maybach S580 4Matic L(자동)": "벤츠_8_1_1",
            "2024년형 가솔린 6.0 4WD : Maybach S680 4Matic L(자동)": "벤츠_8_2_1",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_9": {
            "2023년형 전기 2WD : EQS 450+(자동)": "벤츠_9_1_1",
            "2023년형 전기 AWD : EQS 450 4Matic(자동)": "벤츠_9_2_1",
            "2023년형 전기 AWD : EQS 53 AMG 4Matic+(자동)": "벤츠_9_2_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_10": {
            "2023년형 전기 AWD : EQS 450 4Matic(자동)": "벤츠_10_1_1",
            "2023년형 전기 AWD : EQS 580 4Matic(자동)": "벤츠_10_1_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_11": {
            "2024년형 가솔린 2.0 2WD 쿠페 : CLE 200(자동)": "벤츠_11_1_1",
            "2024년형 가솔린 3.0 AWD 쿠페 : CLE 450 4Matic(자동)": "벤츠_11_2_1",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_12": {
            "2024년형 가솔린 4.0 터보 AWD : SL63 AMG 4Matic+(자동)": "벤츠_12_1_1",
            "2024년형 가솔린 4.0 터보 AWD : SL63 AMG 4Matic+Performence(자동)": "벤츠_12_1_2",
            "2023년형 가솔린 4.0 터보 AWD : SL63 AMG 4Matic+(자동)": "벤츠_12_2_1",
            "2023년형 가솔린 4.0 터보 AWD : SL63 AMG 4Matic+Performence(자동)": "벤츠_12_2_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_13": {
            "2024년형 가솔린 3.0 4WD : 43 4Matic+(자동)": "벤츠_13_1_1",
            "2023년형 가솔린 3.0 4WD : 43 4Matic+(자동)": "벤츠_13_2_1",
            "2023년형 가솔린 3.0 4WD : 43 4Matic+Dynamic(자동)": "벤츠_13_2_2",
            "2023년형 가솔린 4.0 4WD : 63 S 4Matic+(자동)": "벤츠_13_3_1",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_14": {
            "2024년형 가솔린 2.0 4WD : GLA 250 4Matic(자동)": "벤츠_14_1_1",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_15": {
            "2024년형 전기 2WD : EQA 250 Electric Art(자동)": "벤츠_15_1_1",
            "2024년형 전기 2WD : EQA 250 AMG Line(자동)": "벤츠_15_1_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_16": {
            "2024년형 전기 2WD : EQA 250 Electric Art(자동)": "벤츠_16_1_1",
            "2024년형 전기 2WD : EQA 250 AMG Line(자동)": "벤츠_16_1_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_17": {
            "2024년형 가솔린 2.0 4WD : GLB 250 4Matic(자동)": "벤츠_17_1_1",
            "2024년형 가솔린 2.0 4WD : GLB 35 AMG 4Matic(자동)": "벤츠_17_1_2",
            "2024년형 디젤 2.0 2WD : GLB 200d(자동)": "벤츠_17_2_1",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_18": {
            "2024년형 전기 AWD : EQB 300 4Matic Electric Art(자동)": "벤츠_18_1_1",
            "2024년형 전기 AWD : EQB 300 4Matic AMG Line(자동)": "벤츠_18_1_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_19": {
            "2024년형 전기 AWD : EQB 300 4Matic Electric Art(자동)": "벤츠_19_1_1",
            "2024년형 전기 AWD : EQB 300 4Matic AMG Line(자동)": "벤츠_19_1_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_20": {
            "2024년형 가솔린 2.0 4WD : GLC 300 4Matic(자동)": "벤츠_20_1_1",
            "2024년형 가솔린 2.0 4WD : GLC 43 AMG 4Matic(자동)": "벤츠_20_1_2",
            "2024년형 가솔린 2.0 4WD 쿠페 : GLC 300 4Matic(자동)": "벤츠_20_2_1",
            "2024년형 가솔린 2.0 4WD 쿠페 : GLC 43 AMG 4Matic(자동)": "벤츠_20_2_2",
            "2024년형 디젤 2.0 4WD : GLC 220d 4Matic(자동)": "벤츠_20_3_1",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_21": {
            "2024년형 가솔린 3.0 4WD : GLC 450 4Matic(자동)": "벤츠_21_1_1",
            "2024년형 가솔린 3.0 4WD : GLC 53 AMG 4Matic +(자동)": "벤츠_21_1_2",
            "2024년형 가솔린 3.0 4WD 쿠페 : GLC 53 Coupe AMG 4Matic +(자동)": "벤츠_21_2_1",
            "2024년형 가솔린 2.0 플러그인 하이브리드 4WD 쿠페 : GLC 400e Coupe 4Matic(자동)": "벤츠_21_3_1",
            "2024년형 디젤 2.0 4WD : GLC 300d 4Matic(자동)": "벤츠_21_4_1",
            "2024년형 디젤 3.0 4WD 쿠페 : GLC 450d Coupe 4Matic(자동)": "벤츠_21_5_1",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_22": {
            "2024년형 가솔린 4.0 4WD : GLS 580 4Matic(자동)": "벤츠_22_1_1",
            "2024년형 디젤 3.0 4WD : GLS 450d 4Matic(자동)": "벤츠_22_2_1",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_23": {
            "2024년형 가솔린 4.0 4WD : Maybach GLS 600 4Matic(자동)": "벤츠_23_1_1",
            "2024년형 가솔린 4.0 4WD : Maybach GLS 600 4Matic Manufaktur(자동)": "벤츠_23_1_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_24": {
            "2024년형 가솔린 4.0 4WD : Maybach GLS 600 4Matic(자동)": "벤츠_24_1_1",
            "2024년형 가솔린 4.0 4WD : Maybach GLS 600 4Matic Manufaktur(자동)": "벤츠_24_1_2",
            "이전으로 돌아가기": "벤츠",
        },
        "벤츠_25": {
            "2024년형 가솔린 4.0 4WD : G63 AMG(자동)": "벤츠_25_1_1",
            "2024년형 가솔린 4.0 4WD : G63 AMG Manufaktur(자동)": "벤츠_25_1_2",
            "2024년형 디젤 3.0 4WD : G400d (자동)": "벤츠_25_2_1",
            "이전으로 돌아가기": "벤츠",
        },
        "BMW": {
            "1 Series(3세대)": "BMW_1",
            "2 Series GranCoupe(2세대)": "BMW_2",
            "THE New 3 Series(G20/G)": "BMW_3",
            "4 Series(2세대)": "BMW_4",
            "i4": "BMW_5",
            "5 Series(G60)": "BMW_6",
            "i5 (G60)": "BMW_7",
            "NEW 6 Series GT": "BMW_8",
            "7 Series(G70)": "BMW_9",
            "i7": "BMW_10",
            "The New 8 Series(2세대 F/L)": "BMW_11",
            "2 Series Coupe(2세대)": "BMW_12",
            "M2(2세대)": "BMW_13",
            "M3(6세대)": "BMW_14",
            "M4(2세대)": "BMW_15",
            "M5(6세대 F/L)": "BMW_16",
            "The New M8": "BMW_17",
            "The New Z4(3세대 F/L)": "BMW_18",
            "X1(3세대)": "BMW_19",
            "iX1": "BMW_20",
            "X2(2세대)": "BMW_21",
            "X3(3세대 F/L)": "BMW_22",
            "iX3": "BMW_23",
            "The New X3M": "BMW_24",
            "X4(2세대)": "BMW_25",
            "The New X4M": "BMW_26",
            "iX": "BMW_27",
            "The New X5(4세대 F/L)": "BMW_28",
            "The New X5M(4세대 F/L)": "BMW_29",
            "The New X6(3세대 F/L)": "BMW_30",
            "The New X6M(3세대 F/L)": "BMW_31",
            "The New X7(1세대 F/L)": "BMW_32",
            "XM": "BMW_33",
            "2 Series Active Tourer": "BMW_34",
            "이전으로 돌아가기": "유럽",
        },
        "BMW_1": {
            "2024년형 가솔린 2.0 2WD : 120i Sport(자동)": "BMW_1_1_1",
            "2024년형 가솔린 2.0 2WD : 120i Sport_p1(자동)": "BMW_1_1_2",
            "2024년형 가솔린 2.0 2WD : 120i M Sport Package(자동)": "BMW_1_1_3",
            "2024년형 가솔린 2.0 2WD : 120i M Sport Package_P0-0(자동)": "BMW_1_1_4",
            "2024년형 가솔린 2.0 2WD : 120i M Sport Package_P1(자동)": "BMW_1_1_5",
            "2024년형 가솔린 2.0 2WD : 120i M Sport Package_P1-0(자동)": "BMW_1_1_6",
            "2024년형 가솔린 2.0 4WD : M135i xDrive(자동)": "BMW_1_2_1",
            "2024년형 가솔린 2.0 4WD : M135i xDrive_P1(자동)": "BMW_1_2_2",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_2": {
            "2024년형 가솔린 2.0 2WD : Gran Coupe 220i Spt(자동)": "BMW_2_1_1",
            "2024년형 가솔린 2.0 2WD : Gran Coupe 220i Spt_P1(자동)": "BMW_2_1_2",
            "2024년형 가솔린 2.0 2WD : Gran Coupe 220i M Spt(자동)": "BMW_2_1_3",
            "2024년형 가솔린 2.0 2WD : Gran Coupe 220i M Spt P1(자동)": "BMW_2_1_4",
            "2024년형 가솔린 2.0 4WD : Gran Coupe M235i xDrive(자동)": "BMW_2_2_1",
            "2024년형 가솔린 2.0 4WD : Gran Coupe M235i xDrive_P1(자동)": "BMW_2_2_2",
            "2024년형 가솔린 2.0 4WD : Gran Coupe M235i xDrive_P1-0(자동)": "BMW_2_2_3",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_3": {
            "2024년형 가솔린 2.0 2WD 세단 : 320i LCI(자동)": "BMW_3_1_1",
            "2024년형 가솔린 2.0 2WD 세단 : 320i P1(자동)": "BMW_3_1_2",
            "2024년형 가솔린 2.0 2WD 세단 : 320i M Sport LCI(자동)": "BMW_3_1_3",
            "2024년형 가솔린 2.0 2WD 세단 : 320i M Sport P1(자동)": "BMW_3_1_4",
            "2024년형 가솔린 2.0 2WD 세단 : 320i M Sport P2(자동)": "BMW_3_1_5",
            "2024년형 가솔린 3.0 2WD 세단 : M340i LCI(자동)": "BMW_3_2_1",
            "2024년형 가솔린 3.0 2WD 세단 : M340i P1(자동)": "BMW_3_2_2",
            "2024년형 가솔린 3.0 2WD 세단 : M340i P1-0(자동)": "BMW_3_2_3",
            "2024년형 가솔린 3.0 2WD 세단 : M340i P2(자동)": "BMW_3_2_4",
            "2024년형 디젤 2.0 2WD 세단 : 320d_P1(자동)": "BMW_3_3_1",
            "2024년형 디젤 2.0 2WD 세단 : 320d P2(자동)": "BMW_3_3_2",
            "2024년형 디젤 2.0 2WD 세단 : 320d M Sport LCI(자동)": "BMW_3_3_3",
            "2024년형 디젤 2.0 2WD 세단 : 320d M Sport P1(자동)": "BMW_3_3_4",
            "2024년형 디젤 2.0 2WD 세단 : 320d M Sport P2(자동)": "BMW_3_3_5",
            "2024년형 디젤 2.0 AWD 세단 : 320d xDrive LCI_P1(자동)": "BMW_3_4_1",
            "2024년형 디젤 2.0 AWD 세단 : 320d xDrive LCI_P2(자동)": "BMW_3_4_2",
            "2024년형 디젤 2.0 AWD 세단 : 320d xDrive M Sport LCI(자동)": "BMW_3_4_3",
            "2024년형 디젤 2.0 AWD 세단 : 320d xDrive M Sport P1(자동)": "BMW_3_4_4",
            "2024년형 디젤 2.0 AWD 세단 : 320d xDrive M Sport P2(자동)": "BMW_3_4_5",
            "2024년형 가솔린 2.0 2WD 투어링 : 320i Touring LCI(자동)": "BMW_3_5_1",
            "2024년형 가솔린 2.0 2WD 투어링 : 320i Touring P1(자동)": "BMW_3_5_2",
            "2024년형 가솔린 2.0 2WD 투어링 : 320i Touring M Sport LCI(자동)": "BMW_3_5_3",
            "2024년형 가솔린 2.0 2WD 투어링 : 320i Touring M Sport P1(자동)": "BMW_3_5_4",
            "2024년형 가솔린 2.0 2WD 투어링 : 320i Touring M Sport P2(자동)": "BMW_3_5_5",
            "2024년형 가솔린 3.0 AWD 투어링 : M340i xDrive Touring LCI(자동)": "BMW_3_6_1",
            "2024년형 가솔린 3.0 AWD 투어링 : M340i xDrive Touring P1(자동)": "BMW_3_6_2",
            "2024년형 가솔린 3.0 AWD 투어링 : M340i xDrive Touring P1-1(자동)": "BMW_3_6_3",
            "2024년형 가솔린 3.0 AWD 투어링 : M340i xDrive Touring P2(자동)": "BMW_3_6_4",
            "2024년형 디젤 2.0 2WD 투어링 : 320d Touring LCI(자동)": "BMW_3_7_1",
            "2024년형 디젤 2.0 2WD 투어링 : 320d Touring LCI P1(자동)": "BMW_3_7_2",
            "2024년형 디젤 2.0 2WD 투어링 : 320d Touring LCI P2(자동)": "BMW_3_7_3",
            "2024년형 디젤 2.0 2WD 투어링 : 320d Touring M Sport LCI(자동)": "BMW_3_7_4",
            "2024년형 디젤 2.0 2WD 투어링 : 320d Touring M Sport P1(자동)": "BMW_3_7_5",
            "2024년형 디젤 2.0 2WD 투어링 : 320d Touring M Sport P2(자동)": "BMW_3_7_6",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_4": {
            "2024년형 가솔린 2.0 2WD 쿠페 : Coupe 420i M Sport(자동)": "BMW_4_1_1",
            "2024년형 가솔린 2.0 2WD 쿠페 : Coupe 420i M Sport_P0-1(자동)": "BMW_4_1_2",
            "2024년형 가솔린 2.0 2WD 쿠페 : Coupe 420i M Sport_P1(자동)": "BMW_4_1_3",
            "2024년형 가솔린 2.0 2WD 쿠페 : Coupe 420i M Sport_P2(자동)": "BMW_4_1_4",
            "2024년형 가솔린 2.0 2WD 그란쿠페 : Gran Coupe 420i M Sport(자동)": "BMW_4_2_1",
            "2024년형 가솔린 2.0 2WD 그란쿠페 : Gran Coupe 420i M Sport_P1(자동)": "BMW_4_2_2",
            "2024년형 가솔린 2.0 2WD 그란쿠페 : Gran Coupe 420i M Sport_P2(자동)": "BMW_4_2_3",
            "2024년형 가솔린 2.0 2WD 그란쿠페 : Gran Coupe 420i M Sport_P3(자동)": "BMW_4_2_4",
            "2024년형 가솔린 2.0 2WD 그란쿠페 : Gran Coupe 420i M Spt Perf(자동)": "BMW_4_2_5",
            "2024년형 가솔린 2.0 2WD 컨버터블 : Convertible 420i M Sport(자동)": "BMW_4_3_1",
            "2024년형 가솔린 2.0 2WD 컨버터블 : Convertible 420i M Sport_P0-0(자동)": "BMW_4_3_2",
            "2024년형 가솔린 2.0 2WD 컨버터블 : Convertible 420i M Sport_P0-1(자동)": "BMW_4_3_3",
            "2024년형 가솔린 2.0 2WD 컨버터블 : Convertible 420i M Sport_P1(자동)": "BMW_4_3_4",
            "2024년형 가솔린 2.0 2WD 컨버터블 : Convertible 420i M Sport_P1-0(자동)": "BMW_4_3_5",
            "2024년형 가솔린 2.0 2WD 컨버터블 : Convertible 420i M Sport_P2(자동)": "BMW_4_3_6",
            "2024년형 가솔린 2.0 2WD 컨버터블 : Convertible 420i M Sport_P2-0(자동)": "BMW_4_3_7",
            "2024년형 가솔린 3.0 4WD 쿠페 : Coupe M440i xDrive_OS(자동)": "BMW_4_4_1",
            "2024년형 가솔린 3.0 4WD 쿠페 : Coupe M440i xDrive OS_P0-1(자동)": "BMW_4_4_2",
            "2024년형 가솔린 3.0 4WD 쿠페 : Coupe M440i xDrive OS_P1(자동)": "BMW_4_4_3",
            "2024년형 가솔린 3.0 4WD 쿠페 : Coupe M440i xDrive OS_P2(자동)": "BMW_4_4_4",
            "2024년형 가솔린 3.0 4WD 컨버터블 : Convertible M440i xDrive OS(자동)": "BMW_4_5_1",
            "2024년형 가솔린 3.0 4WD 컨버터블 : Convertible M440i xDrive OS_P0-1(자동)": "BMW_4_5_2",
            "2024년형 가솔린 3.0 4WD 컨버터블 : Convertible M440i xDrive OS_P1(자동)": "BMW_4_5_3",
            "2024년형 가솔린 3.0 4WD 컨버터블 : Convertible M440i xDrive OS_P2(자동)": "BMW_4_5_4",
            "2024년형 디젤 2.0 2WD 그란쿠페 : Gran Coupe 420d M Sport(자동)": "BMW_4_6_1",
            "2024년형 디젤 2.0 2WD 그란쿠페 : Gran Coupe 420d M Sport_P1(자동)": "BMW_4_6_1",
            "2024년형 디젤 2.0 2WD 그란쿠페 : Gran Coupe 420d M Sport_P2(자동)": "BMW_4_6_1",
            "2024년형 디젤 2.0 2WD 그란쿠페 : Gran Coupe 420d M Spt Perf(자동)": "BMW_4_6_1",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_5": {
            "2024년형 그란쿠페 전기 2WD : eDrive Gran Coupe 40 M Sport Pro(자동)": "BMW_5_1_1",
            "2024년형 그란쿠페 전기 2WD : eDrive Gran Coupe 40 M Sport Pro_P0-1(자동)": "BMW_5_1_2",
            "2024년형 그란쿠페 전기 2WD : eDrive Gran Coupe 40 M Sport Pro_P0(자동)": "BMW_5_1_3",
            "2024년형 그란쿠페 전기 2WD : eDrive Gran Coupe 40 M Sport Pro_P2(자동)": "BMW_5_1_4",
            "2024년형 그란쿠페 전기 2WD : eDrive Gran Coupe 40 M Sport Pro_P3(자동)": "BMW_5_1_5",
            "2024년형 그란쿠페 전기 AWD : M50 Gran Coupe(자동)": "BMW_5_2_1",
            "2024년형 그란쿠페 전기 AWD : M50 Gran Coupe P0-1(자동)": "BMW_5_2_2",
            "2024년형 그란쿠페 전기 AWD : M50 Gran Coupe P1(자동)": "BMW_5_2_3",
            "2024년형 그란쿠페 전기 AWD : M50 Gran Coupe P3(자동)": "BMW_5_2_4",
            "2024년형 그란쿠페 전기 AWD : M50 Gran Coupe Pro(자동)": "BMW_5_2_5",
            "2024년형 그란쿠페 전기 AWD : M50 Gran Coupe Pro_P0-1(자동)": "BMW_5_2_6",
            "2024년형 그란쿠페 전기 AWD : M50 Gran Coupe Pro_P0(자동)": "BMW_5_2_7",
            "2024년형 그란쿠페 전기 AWD : M50 Gran Coupe Pro_P2(자동)": "BMW_5_2_8",
            "2024년형 그란쿠페 전기 AWD : M50 Gran Coupe Pro_P3(자동)": "BMW_5_2_9",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_6": {
            "2024년형 가솔린 2.0 2WD : 520i(자동)": "BMW_6_1_1",
            "2024년형 가솔린 2.0 2WD : 520i P1(자동)": "BMW_6_1_2",
            "2024년형 가솔린 2.0 2WD : 520i P2(자동)": "BMW_6_1_3",
            "2024년형 가솔린 2.0 2WD : 520i M Sport(자동)": "BMW_6_1_4",
            "2024년형 가솔린 2.0 2WD : 520i M Sport P1(자동)": "BMW_6_1_5",
            "2024년형 가솔린 2.0 2WD : 520i M Sport P1-1(자동)": "BMW_6_1_6",
            "2024년형 가솔린 2.0 2WD : 520i M Sport P2(자동)": "BMW_6_1_7",
            "2024년형 가솔린 2.0 2WD : 520i M Sport Pro Special Edition(자동)": "BMW_6_1_8",
            "2024년형 가솔린 2.0 2WD : 520i M Sport Pro Special Edition P1(자동)": "BMW_6_1_9",
            "2024년형 가솔린 2.0 AWD : 530i xDrive(자동)": "BMW_6_2_1",
            "2024년형 가솔린 2.0 AWD : 530i xDrive P1(자동)": "BMW_6_2_2",
            "2024년형 가솔린 2.0 AWD : 530i xDrive P2(자동)": "BMW_6_2_3",
            "2024년형 가솔린 2.0 AWD : 530i xDrive M Sport(자동)": "BMW_6_2_4",
            "2024년형 가솔린 2.0 AWD : 530i xDrive M Sport P1(자동)": "BMW_6_2_5",
            "2024년형 가솔린 2.0 AWD : 530i xDrive M Sport P1-1(자동)": "BMW_6_2_6",
            "2024년형 가솔린 2.0 AWD : 530i xDrive M Sport P2(자동)": "BMW_6_2_7",
            "2024년형 디젤 2.0 2WD : 523d(자동)": "BMW_6_3_1",
            "2024년형 디젤 2.0 2WD : 523d P1(자동)": "BMW_6_3_2",
            "2024년형 디젤 2.0 2WD : 523d P2(자동)": "BMW_6_3_3",
            "2024년형 디젤 2.0 2WD : 523d M Sport(자동)": "BMW_6_3_4",
            "2024년형 디젤 2.0 2WD : 523d M Sport P0(자동)": "BMW_6_3_5",
            "2024년형 디젤 2.0 2WD : 523d M Sport P1(자동)": "BMW_6_3_6",
            "2024년형 디젤 2.0 2WD : 523d M Sport P1-1(자동)": "BMW_6_3_7",
            "2024년형 디젤 2.0 2WD : 523d M Sport P2(자동)": "BMW_6_3_8",
            "2024년형 디젤 2.0 AWD : 523d xDrive(자동)": "BMW_6_4_1",
            "2024년형 디젤 2.0 AWD : 523d xDrive P1(자동)": "BMW_6_4_2",
            "2024년형 디젤 2.0 AWD : 523d xDrive P2(자동)": "BMW_6_4_3",
            "2024년형 디젤 2.0 AWD : 523d xDrive M Sport(자동)": "BMW_6_4_4",
            "2024년형 디젤 2.0 AWD : 523d xDrive M Sport P1(자동)": "BMW_6_4_5",
            "2024년형 디젤 2.0 AWD : 523d xDrive M Sport P1-1(자동)": "BMW_6_4_6",
            "2024년형 디젤 2.0 AWD : 523d xDrive M Sport P2(자동)": "BMW_6_4_7",
            "2024년형 가솔린 2.0 플러그인 하이브리드 2WD : 530e(자동)": "BMW_6_5_1",
            "2024년형 가솔린 2.0 플러그인 하이브리드 2WD : 530e_P0-1(자동)": "BMW_6_5_2",
            "2024년형 가솔린 2.0 플러그인 하이브리드 2WD : 530e M Sport(자동)": "BMW_6_5_3",
            "2024년형 가솔린 2.0 플러그인 하이브리드 2WD : 530e M Sport_P0-1(자동)": "BMW_6_5_4",
            "2024년형 가솔린 2.0 플러그인 하이브리드 2WD : 530e M Sport_P1(자동)": "BMW_6_5_5",
            "2024년형 가솔린 2.0 플러그인 하이브리드 2WD : 530e M Sport Pro_P1(자동)": "BMW_6_5_6",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_7": {
            "2024년형 전기 2WD : eDrive 40(자동)": "BMW_7_1_1",
            "2024년형 전기 2WD : eDrive 40 P1(자동)": "BMW_7_1_2",
            "2024년형 전기 2WD : eDrive 40 M Sport(자동)": "BMW_7_1_3",
            "2024년형 전기 2WD : eDrive 40 M Sport P1(자동)": "BMW_7_1_4",
            "2024년형 전기 2WD : eDrive 40 M Sport Pro(자동)": "BMW_7_1_5",
            "2024년형 전기 2WD : eDrive 40 M Sport Pro P1(자동)": "BMW_7_1_6",
            "2024년형 전기 AWD : M60 xDrive Pro(자동)": "BMW_7_2_1",
            "2024년형 전기 AWD : M60 xDrive Pro P0-1(자동)": "BMW_7_2_2",
            "2024년형 전기 AWD : M60 xDrive Pro P1(자동)": "BMW_7_2_3",
            "2024년형 전기 AWD : M60 xDrive Pro P1-1(자동)": "BMW_7_2_4",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_8": {
            "2024년형 가솔린 3.0 4WD : 630i xDrive GT Luxury(자동)": "BMW_8_1_1",
            "2024년형 가솔린 3.0 4WD : 630i xDrive GT Luxury P1(자동)": "BMW_8_1_2",
            "2024년형 가솔린 3.0 4WD : 630i xDrive GT Luxury P2(자동)": "BMW_8_1_3",
            "2024년형 가솔린 3.0 4WD : 630i xDrive GT M Sport(자동)": "BMW_8_1_4",
            "2024년형 가솔린 3.0 4WD : 630i xDrive GT M Sport_P0-0(자동)": "BMW_8_1_5",
            "2024년형 가솔린 3.0 4WD : 630i xDrive GT M Sport P1(자동)": "BMW_8_1_6",
            "2024년형 가솔린 3.0 4WD : 630i xDrive GT M Sport_P1-0(자동)": "BMW_8_1_7",
            "2024년형 가솔린 3.0 4WD : 630i xDrive GT M Sport P2(자동)": "BMW_8_1_8",
            "2024년형 가솔린 3.0 4WD : 640i xDrive GT Luxury(자동)": "BMW_8_1_9",
            "2024년형 가솔린 3.0 4WD : 640i xDrive GT Luxury P1(자동)": "BMW_8_1_10",
            "2024년형 가솔린 3.0 4WD : 640i xDrive GT M Sport(자동)": "BMW_8_1_11",
            "2024년형 가솔린 3.0 4WD : 640i xDrive GT M Sport Pro P1(자동)": "BMW_8_1_12",
            "2024년형 가솔린 3.0 4WD : 640i xDrive GT M Sport Pro P2(자동)": "BMW_8_1_13",
            "2024년형 디젤 2.0 2WD : 620d GT Luxury(자동)": "BMW_8_2_1",
            "2024년형 디젤 2.0 2WD : 620d GT Luxury P1(자동)": "BMW_8_2_2",
            "2024년형 디젤 2.0 2WD : 620d GT Luxury P2(자동)": "BMW_8_2_3",
            "2024년형 디젤 2.0 2WD : 620d GT M Sprot(자동)": "BMW_8_2_4",
            "2024년형 디젤 2.0 2WD : 620d GT M Sprot P1(자동)": "BMW_8_2_5",
            "2024년형 디젤 2.0 2WD : 620d GT M Sprot P2(자동)": "BMW_8_2_6",
            "2024년형 디젤 2.0 4WD : 620d xDrive GT Luxury(자동)": "BMW_8_3_1",
            "2024년형 디젤 2.0 4WD : 620d xDrive GT Luxury P1(자동)": "BMW_8_3_2",
            "2024년형 디젤 2.0 4WD : 620d xDrive GT Luxury P2(자동)": "BMW_8_3_3",
            "2024년형 디젤 2.0 4WD : 620d xDrive GT M Sport(자동)": "BMW_8_3_4",
            "2024년형 디젤 2.0 4WD : 620d xDrive GT M Sport_P0-0(자동)": "BMW_8_3_5",
            "2024년형 디젤 2.0 4WD : 620d xDrive GT M Sport P1(자동)": "BMW_8_3_6",
            "2024년형 디젤 2.0 4WD : 620d xDrive GT M Sport P1-0(자동)": "BMW_8_3_7",
            "2024년형 디젤 2.0 4WD : 620d xDrive GT M Sport P2(자동)": "BMW_8_3_8",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_9": {
            "2024년형 가솔린 3.0 AWD : 740i xDrive M Sport(자동)": "BMW_9_1_1",
            "2024년형 가솔린 3.0 AWD : 740i xDrive M Sport Limited Edition(자동)": "BMW_9_1_2",
            "2024년형 가솔린 3.0 AWD : 740i xDrive M Sport Limited Edition P1(자동)": "BMW_9_1_3",
            "2024년형 가솔린 3.0 AWD : 740i xDrive M Sport Limited Edition P2(자동)": "BMW_9_1_4",
            "2024년형 가솔린 3.0 AWD : 740i xDrive M Sport P0-0(자동)": "BMW_9_1_5",
            "2024년형 가솔린 3.0 AWD : 740i xDrive M Sport P1(자동)": "BMW_9_1_6",
            "2024년형 가솔린 3.0 AWD : 740i xDrive M Sport P1-0(자동)": "BMW_9_1_7",
            "2024년형 가솔린 3.0 AWD : 740i xDrive M Sport P2(자동)": "BMW_9_1_8",
            "2024년형 가솔린 3.0 플러그인 하이브리드 AWD : 750e xDrive DPE(자동)": "BMW_9_2_1",
            "2024년형 가솔린 3.0 플러그인 하이브리드 AWD : 750e xDrive DPE P1(자동)": "BMW_9_2_2",
            "2024년형 가솔린 3.0 플러그인 하이브리드 AWD : 750e xDrive M Sport(자동)": "BMW_9_2_3",
            "2024년형 가솔린 3.0 플러그인 하이브리드 AWD : 750e xDrive M Sport P0-0(자동)": "BMW_9_2_4",
            "2024년형 가솔린 3.0 플러그인 하이브리드 AWD : 750e xDrive M Sport P1(자동)": "BMW_9_2_5",
            "2024년형 가솔린 3.0 플러그인 하이브리드 AWD : 750e xDrive M Sport P1-0(자동)": "BMW_9_2_6",
            "2024년형 가솔린 3.0 플러그인 하이브리드 AWD : 750e xDrive M Sport P2(자동)": "BMW_9_2_7",
            "2024년형 디젤 3.0 AWD : 740d xDrive M Sport LCI(자동)": "BMW_9_3_1",
            "2024년형 디젤 3.0 AWD : 740d xDrive M Sport P1(자동)": "BMW_9_3_2",
            "2024년형 디젤 3.0 AWD : 740d xDrive M Sport P1-0(자동)": "BMW_9_3_3",
            "2024년형 디젤 3.0 AWD : 740d xDrive M Sport P2(자동)": "BMW_9_3_4",
            "2024년형 디젤 3.0 AWD : 740d xDrive M Sport P2-0(자동)": "BMW_9_3_5",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_10": {
            "2024년형 전기 2WD : eDrive 50M Spt Limited(자동)": "BMW_10_1_1",
            "2024년형 전기 2WD : eDrive 50M Spt Limited P1(자동)": "BMW_10_1_2",
            "2024년형 전기 2WD : eDrive 50M Spt Limited P2(자동)": "BMW_10_1_3",
            "2024년형 전기 2WD : eDrive 50M Sport(자동)": "BMW_10_1_4",
            "2024년형 전기 2WD : eDrive 50M Sport P1(자동)": "BMW_10_1_5",
            "2024년형 전기 2WD : eDrive 50M Sport P2(자동)": "BMW_10_1_6",
            "2024년형 전기 AWD : xDrive 60 DPE LCI(자동)": "BMW_10_2_1",
            "2024년형 전기 AWD : xDrive 60 DPE P1(자동)": "BMW_10_2_2",
            "2024년형 전기 AWD : xDrive 60M Sport(자동)": "BMW_10_2_3",
            "2024년형 전기 AWD : xDrive 60M Sport P1(자동)": "BMW_10_2_4",
            "2024년형 전기 AWD : xDrive 60M Sport P2(자동)": "BMW_10_2_5",
            "2024년형 전기 AWD : M70 xDrive(자동)": "BMW_10_2_6",
            "2024년형 전기 AWD : M70 xDrive M Perf(자동)": "BMW_10_2_7",
            "2024년형 전기 AWD : M70 xDrive M Perf P1(자동)": "BMW_10_2_8",
            "2024년형 전기 AWD : M70 xDrive First Edition(자동)": "BMW_10_2_9",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_11": {
            "2024년형 가솔린 4.4 AWD 그란쿠페 : Gran Coupe M850i xDrive(자동)": "BMW_11_1_1",
            "2024년형 가솔린 4.4 AWD 그란쿠페 : Gran Coupe M850i xDrive P0-0(자동)": "BMW_11_1_2",
            "2024년형 가솔린 4.4 AWD 그란쿠페 : Gran Coupe M850i xDrive P1(자동)": "BMW_11_1_3",
            "2024년형 가솔린 4.4 AWD 그란쿠페 : Gran Coupe M850i xDrive P1-0(자동)": "BMW_11_1_4",
            "2024년형 가솔린 4.4 AWD 쿠페 : Coupe M850i xDrive(자동)": "BMW_11_2_1",
            "2024년형 가솔린 4.4 AWD 쿠페 : Coupe M850i xDrive P1(자동)": "BMW_11_2_2",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_12": {
            "2024년형 가솔린 3.0 4WD : Coupe M240i xDrive_OS(자동)": "BMW_12_1_1",
            "2024년형 가솔린 3.0 4WD : Coupe M240i xDrive_OS_P1(자동)": "BMW_12_1_2",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_13": {
            "2024년형 가솔린 3.0 2WD : Coupe(자동)": "BMW_13_1_1",
            "2024년형 가솔린 3.0 2WD : Coupe Special Edition(자동)": "BMW_13_1_2",
            "2024년형 가솔린 3.0 2WD : Coupe P1(자동)": "BMW_13_1_3",
            "2024년형 가솔린 3.0 2WD : Coupe P2(자동)": "BMW_13_1_4",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_14": {
            "2024년형 가솔린 3.0 터보 4WD : Sedan Competition M xDrive(자동)": "BMW_14_1_1",
            "2024년형 가솔린 3.0 터보 4WD : Sedan Competition M xDrive_P1(자동)": "BMW_14_1_2",
            "2024년형 가솔린 3.0 터보 4WD : Sedan Competition M xDrive_P2(자동)": "BMW_14_1_3",
            "2024년형 가솔린 3.0 터보 4WD : Sedan Competition M xDrive_P3(자동)": "BMW_14_1_4",
            "2024년형 가솔린 3.0 터보 투어링 4WD : Touring Competition M xDrive(자동)": "BMW_14_2_1",
            "2024년형 가솔린 3.0 터보 투어링 4WD : Touring Competition M xDrive_P1(자동)": "BMW_14_2_2",
            "2024년형 가솔린 3.0 터보 투어링 4WD : Touring Competition M xDrive_P2(자동)": "BMW_14_2_3",
            "2024년형 가솔린 3.0 터보 투어링 4WD : Touring Competition M xDrive_P3(자동)": "BMW_14_2_4",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_15": {
            "2024년형 가솔린 3.0 4WD 구페 : Coupe Competition M xDrive(자동)": "BMW_15_1_1",
            "2024년형 가솔린 3.0 4WD 구페 : Coupe Competition M xDrive_P1(자동)": "BMW_15_1_2",
            "2024년형 가솔린 3.0 4WD 구페 : Coupe Competition M xDrive_P2(자동)": "BMW_15_1_3",
            "2024년형 가솔린 3.0 4WD 컨버터블 : Convertible Competition M xDrive(자동)": "BMW_15_2_1",
            "2024년형 가솔린 3.0 4WD 컨버터블 : Convertible Competition M xDrive_P1(자동)": "BMW_15_2_2",
            "2024년형 가솔린 3.0 4WD 컨버터블 : Convertible Competition M xDrive_P1-1(자동)": "BMW_15_2_3",
            "2024년형 가솔린 3.0 4WD 컨버터블 : Convertible Competition M xDrive_P2(자동)": "BMW_15_2_4",
            "2024년형 가솔린 3.0 4WD 컨버터블 : Convertible Competition M xDrive_P2-0(자동)": "BMW_15_2_5",
            "2024년형 가솔린 3.0 4WD 컨버터블 : Convertible Competition M xDrive_P2-1(자동)": "BMW_15_2_6",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_16": {
            "2024년형 가솔린 4.4 4WD : Sedan Competition_P1(자동)": "BMW_16_1_1",
            "2024년형 가솔린 4.4 4WD : Sedan Competition_P2(자동)": "BMW_16_1_2",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_17": {
            "2024년형 가솔린 4.4 4WD 그란쿠페 : Gran Coupe Competition(자동)": "BMW_17_1_1",
            "2024년형 가솔린 4.4 4WD 그란쿠페 : Gran Coupe Competition P2(자동)": "BMW_17_1_2",
            "2024년형 가솔린 4.4 4WD 쿠페 : Coupe Competition(자동)": "BMW_17_2_1",
            "2024년형 가솔린 4.4 4WD 쿠페 : Coupe Competition P2(자동)": "BMW_17_2_2",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_18": {
            "2024년형 가솔린 2.0 2WD : 20i sDrive M Sport(자동)": "BMW_18_1_1",
            "2024년형 가솔린 2.0 2WD : 20i sDrive M Sport_P0-0(자동)": "BMW_18_1_2",
            "2024년형 가솔린 2.0 2WD : 20i sDrive M Sport P1(자동)": "BMW_18_1_3",
            "2024년형 가솔린 2.0 2WD : 20i sDrive M Sport_P1-0(자동)": "BMW_18_1_4",
            "2024년형 가솔린 3.0 2WD : M40i(자동)": "BMW_18_2_1",
            "2024년형 가솔린 3.0 2WD : M40i P1(자동)": "BMW_18_2_2",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_19": {
            "2024년형 가솔린 2.0 2WD : 20i sDrive xLine(자동)": "BMW_19_1_1",
            "2024년형 가솔린 2.0 2WD : 20i sDrive xLine_P0-0(자동)": "BMW_19_1_2",
            "2024년형 가솔린 2.0 2WD : 20i sDrive xLine_P1(자동)": "BMW_19_1_3",
            "2024년형 가솔린 2.0 2WD : 20i sDrive M Sport(자동)": "BMW_19_1_4",
            "2024년형 가솔린 2.0 2WD : 20i sDrive M Sport_P0-1(자동)": "BMW_19_1_5",
            "2024년형 가솔린 2.0 2WD : 20i sDrive M Sport_P1(자동)": "BMW_19_1_6",
            "2024년형 가솔린 2.0 AWD : 20i xDrive xLine(자동)": "BMW_19_2_1",
            "2024년형 가솔린 2.0 AWD : 20i xDrive xLine_P1(자동)": "BMW_19_2_2",
            "2024년형 가솔린 2.0 AWD : 20i xDrive xLine_P1-1(자동)": "BMW_19_2_3",
            "2024년형 가솔린 2.0 AWD : 20i xDrive xLine_P2(자동)": "BMW_19_2_4",
            "2024년형 가솔린 2.0 AWD : 20i xDrive M Sport(자동)": "BMW_19_2_5",
            "2024년형 가솔린 2.0 AWD : 20i xDrive M Sport_P0-1(자동)": "BMW_19_2_6",
            "2024년형 가솔린 2.0 AWD : 20i xDrive M Sport_P1(자동)": "BMW_19_2_7",
            "2024년형 가솔린 2.0 AWD : 20i xDrive M Sport_P2(자동)": "BMW_19_2_8",
            "2024년형 가솔린 2.0 AWD : M35i xDrive(자동)": "BMW_19_2_9",
            "2024년형 디젤 2.0 2WD : 18d sDrive xLine(자동)": "BMW_19_3_1",
            "2024년형 디젤 2.0 2WD : 18d sDrive xLine_P1(자동)": "BMW_19_3_2",
            "2024년형 디젤 2.0 2WD : 18d sDrive M Sport(자동)": "BMW_19_3_3",
            "2024년형 디젤 2.0 2WD : 18d sDrive M Sport_P0-1(자동)": "BMW_19_3_4",
            "2024년형 디젤 2.0 2WD : 18d sDrive M Sport_P1(자동)": "BMW_19_3_5",
            "2024년형 디젤 2.0 2WD : 18d sDrive M Sport_P2(자동)": "BMW_19_3_6",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_20": {
            "2024년형 전기 AWD : 30 xDrive xLine(자동)": "BMW_20_1_1",
            "2024년형 전기 AWD : 30 xDrive xLine P1(자동)": "BMW_20_1_2",
            "2024년형 전기 AWD : 30 xDrive M Sport(자동)": "BMW_20_1_3",
            "2024년형 전기 AWD : 30 xDrive M Sport P0-1(자동)": "BMW_20_1_4",
            "2024년형 전기 AWD : 30 xDrive M Sport P1(자동)": "BMW_20_1_5",
            "2024년형 전기 AWD : 30 xDrive M Sport_P2(자동)": "BMW_20_1_6",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_21": {
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Sport(자동)": "BMW_21_1_1",
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Sport P1(자동)": "BMW_21_1_2",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_22": {
            "2024년형 가솔린 2.0 4WD : 20i xDrive xLine(자동)": "BMW_22_1_1",
            "2024년형 가솔린 2.0 4WD : 20i xDrive xLine_P0-0(자동)": "BMW_22_1_2",
            "2024년형 가솔린 2.0 4WD : 20i xDrive xLine_P1(자동)": "BMW_22_1_3",
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Spt(자동)": "BMW_22_1_4",
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Spt_P1(자동)": "BMW_22_1_5",
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Spt_P2(자동)": "BMW_22_1_6",
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Sport Pro(자동)": "BMW_22_1_7",
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Sport Pro_P1(자동)": "BMW_22_1_8",
            "2024년형 가솔린 3.0 4WD : M40i(자동)": "BMW_22_2_1",
            "2024년형 가솔린 3.0 4WD : M40i P1(자동)": "BMW_22_2_2",
            "2024년형 가솔린 2.0 플러그인 하이브리드 4WD : 30e xDrive xLine(자동)": "BMW_22_3_1",
            "2024년형 가솔린 2.0 플러그인 하이브리드 4WD : 30e xDrive xLine_P1(자동)": "BMW_22_3_2",
            "2024년형 가솔린 2.0 플러그인 하이브리드 4WD : 30e xDrive M Spt(자동)": "BMW_22_3_3",
            "2024년형 가솔린 2.0 플러그인 하이브리드 4WD : 30e xDrive M Spt P1(자동)": "BMW_22_3_4",
            "2024년형 가솔린 2.0 플러그인 하이브리드 4WD : 30e xDrive M Spt P1-0(자동)": "BMW_22_3_5",
            "2024년형 가솔린 2.0 플러그인 하이브리드 4WD : 30e xDrive M Spt P2(자동)": "BMW_22_3_6",
            "2024년형 가솔린 2.0 플러그인 하이브리드 4WD : 30e xDrive M Sport Pro(자동)": "BMW_22_3_7",
            "2024년형 가솔린 2.0 플러그인 하이브리드 4WD : 30e xDrive M Sport Pro_P1(자동)": "BMW_22_3_8",
            "2024년형 디젤 2.0 4WD : 20d xDrive xLine(자동)": "BMW_22_4_1",
            "2024년형 디젤 2.0 4WD : 20d xDrive xLine P1(자동)": "BMW_22_4_2",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport(자동)": "BMW_22_4_3",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport P1(자동)": "BMW_22_4_4",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport P1-0(자동)": "BMW_22_4_5",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport P2(자동)": "BMW_22_4_6",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport Pro(자동)": "BMW_22_4_7",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport Pro_P1(자동)": "BMW_22_4_8",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport Pro_P2(자동)": "BMW_22_4_9",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_23": {
            "2024년형 전기 2WD : M Sport Package(자동)": "BMW_23_1_1",
            "2024년형 전기 2WD : M Sport Package_P1(자동)": "BMW_23_1_2",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_24": {
            "2024년형 가솔린 3.0 4WD : Competition(자동)": "BMW_24_1_1",
            "2024년형 가솔린 3.0 4WD : Competition_P1(자동)": "BMW_24_1_2",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_25": {
            "2024년형 가솔린 2.0 4WD : 20i xDrive xLine(자동)": "BMW_19_1_1",
            "2024년형 가솔린 2.0 4WD : 20i xDrive xLine_P1(자동)": "BMW_19_1_2",
            "2024년형 가솔린 2.0 4WD : 20i xDrive xLine_P1-0(자동)": "BMW_19_1_3",
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Spt(자동)": "BMW_19_1_4",
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Spt_P1(자동)": "BMW_19_1_5",
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Spt_P2(자동)": "BMW_19_1_6",
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Sport Pro(자동)": "BMW_19_1_7",
            "2024년형 가솔린 2.0 4WD : 20i xDrive M Sport Pro_P1(자동)": "BMW_19_1_8",
            "2024년형 가솔린 3.0 4WD : M40i(자동)": "BMW_19_2_1",
            "2024년형 가솔린 3.0 4WD : M40i P1(자동)": "BMW_19_2_2",
            "2024년형 디젤 2.0 4WD : 20d xDrive xLine(자동)": "BMW_19_3_1",
            "2024년형 디젤 2.0 4WD : 20d xDrive xLine_P1(자동)": "BMW_19_3_2",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport(자동)": "BMW_19_3_3",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport_P1(자동)": "BMW_19_3_4",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport_P2(자동)": "BMW_19_3_5",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport Pro(자동)": "BMW_19_3_6",
            "2024년형 디젤 2.0 4WD : 20d xDrive M Sport Pro_P1(자동)": "BMW_19_3_7",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_26": {
            "2024년형 가솔린 3.0 4WD : Competition(자동)": "BMW_20_1_1",
            "2024년형 가솔린 3.0 4WD : Competition_P1(자동)": "BMW_20_1_2",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_27": {
            "2024년형 전기 AWD : xDrive50 Sport Plus(자동)": "BMW_21_1_1",
            "2024년형 전기 AWD : xDrive50 Sport Plus P1(자동)": "BMW_21_1_2",
            "2024년형 전기 AWD : xDrive50 Sport Plus P2(자동)": "BMW_21_1_3",
            "2024년형 전기 AWD : M60(자동)": "BMW_21_1_4",
            "2024년형 전기 AWD : M60_P1-0(자동)": "BMW_21_1_5",
            "2024년형 전기 AWD : M60_P1(자동)": "BMW_21_1_6",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_28": {
            "2024년형 가솔린 3.0 4WD : 40i xDrive xLine 7Seater(자동)": "BMW_22_1_1",
            "2024년형 가솔린 3.0 4WD : 40i xDrive xLine 7Seater P1(자동)": "BMW_22_1_2",
            "2024년형 가솔린 3.0 4WD : 40i xDrive xLine 7Seater P2(자동)": "BMW_22_1_3",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport(자동)": "BMW_22_1_4",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport P1(자동)": "BMW_22_1_5",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport P2(자동)": "BMW_22_1_6",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport P2-0(자동)": "BMW_22_1_7",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport 7Seater(자동)": "BMW_22_1_8",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport 7Seater P1(자동)": "BMW_22_1_9",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport 7Seater P2(자동)": "BMW_22_1_10",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport Pro 7Seater_P0-0(자동)": "BMW_22_1_11",
            "2024년형 가솔린 4.4 4WD : M60i xDrive Pro(자동)": "BMW_22_2_1",
            "2024년형 가솔린 4.4 4WD : M60i xDrive Pro P1(자동)": "BMW_22_2_2",
            "2024년형 가솔린 4.4 4WD : M60i xDrive Pro P2(자동)": "BMW_22_2_3",
            "2024년형 가솔린 3.0 플러그인 하이브리드 4WD : 50e xDrive xLine(자동)": "BMW_22_3_1",
            "2024년형 가솔린 3.0 플러그인 하이브리드 4WD : 50e xDrive xLine P1(자동)": "BMW_22_3_2",
            "2024년형 가솔린 3.0 플러그인 하이브리드 4WD : 50e xDrive xLine P2(자동)": "BMW_22_3_3",
            "2024년형 가솔린 3.0 플러그인 하이브리드 4WD : 50e xDrive M Sport Pro(자동)": "BMW_22_3_4",
            "2024년형 가솔린 3.0 플러그인 하이브리드 4WD : 50e xDrive M Sport Pro P1(자동)": "BMW_22_3_5",
            "2024년형 가솔린 3.0 플러그인 하이브리드 4WD : 50e xDrive M Sport Pro P2(자동)": "BMW_22_3_6",
            "2024년형 가솔린 3.0 플러그인 하이브리드 4WD : 50e xDrive M Sport Pro Special Edition(자동)": "BMW_22_3_7",
            "2024년형 가솔린 3.0 플러그인 하이브리드 4WD : 50e xDrive M Sport Pro P3(자동)": "BMW_22_3_8",
            "2024년형 디젤 3.0 4WD : 30d xDrive xLine 7Seater(자동)": "BMW_22_4_1",
            "2024년형 디젤 3.0 4WD : 30d xDrive xLine 7Seater P1(자동)": "BMW_22_4_2",
            "2024년형 디젤 3.0 4WD : 30d xDrive xLine 7Seater P2(자동)": "BMW_22_4_3",
            "2024년형 디젤 3.0 4WD : 30d xDrive M Sport(자동)": "BMW_22_4_4",
            "2024년형 디젤 3.0 4WD : 30d xDrive M Sport P1(자동)": "BMW_22_4_5",
            "2024년형 디젤 3.0 4WD : 30d xDrive M Sport P2(자동)": "BMW_22_4_6",
            "2024년형 디젤 3.0 4WD : 30d xDrive M Sport P2-0(자동)": "BMW_22_4_7",
            "2024년형 디젤 3.0 4WD : 30d xDrive M Sport 7Seater(자동)": "BMW_22_4_8",
            "2024년형 디젤 3.0 4WD : 30d xDrive M Sport 7Seater P1(자동)": "BMW_22_4_9",
            "2024년형 디젤 3.0 4WD : 30d xDrive M Sport 7Seater P2(자동)": "BMW_22_4_10",
            "2024년형 디젤 3.0 4WD : 30d xDrive M Sport Pro 7Seater_P0-0(자동)": "BMW_22_4_11",
            "2024년형 디젤 3.0 4WD : 30d xDrive M Sport Pro(자동)": "BMW_22_4_12",
            "2024년형 디젤 3.0 4WD : 30d xDrive M Sport Pro P1(자동)": "BMW_22_4_13",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_29": {
            "2024년형 가솔린 4.4 4WD : Conpetition(자동)": "BMW_23_1_1",
            "2024년형 가솔린 4.4 4WD : Conpetition P0-0(자동)": "BMW_23_1_2",
            "2024년형 가솔린 4.4 4WD : Conpetition P1(자동)": "BMW_23_1_3",
            "2024년형 가솔린 4.4 4WD : Conpetition P1-1(자동)": "BMW_23_1_4",
            "2024년형 가솔린 4.4 4WD : Conpetition P2(자동)": "BMW_23_1_5",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_30": {
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport(자동)": "BMW_24_1_1",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport P1(자동)": "BMW_24_1_2",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport P2(자동)": "BMW_24_1_3",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport P2-0(자동)": "BMW_24_1_1",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport P3(자동)": "BMW_24_1_1",
            "2024년형 가솔린 4.4 4WD : M60i xDrive Pro(자동)": "BMW_24_2_1",
            "2024년형 가솔린 4.4 4WD : M60i xDrive Pro P1(자동)": "BMW_24_2_2",
            "2024년형 가솔린 4.4 4WD : M60i xDrive Pro P2(자동)": "BMW_24_2_3",
            "2024년형 디젤 3.0 4WD : 30d xDrive M sport(자동)": "BMW_24_3_1",
            "2024년형 디젤 3.0 4WD : 30d xDrive M sport P1(자동)": "BMW_24_3_2",
            "2024년형 디젤 3.0 4WD : 30d xDrive M sport P2(자동)": "BMW_24_3_3",
            "2024년형 디젤 3.0 4WD : 30d xDrive M sport P2-0(자동)": "BMW_24_3_4",
            "2024년형 디젤 3.0 4WD : 30d xDrive M sport Pro(자동)": "BMW_24_3_5",
            "2024년형 디젤 3.0 4WD : 30d xDrive M sport Pro_P0-0(자동)": "BMW_24_3_6",
            "2024년형 디젤 3.0 4WD : 40d xDrive M sport Pro(자동)": "BMW_24_3_7",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_31": {
            "2024년형 가솔린 4.4 4WD : Competition(자동)": "BMW_31_1_1",
            "2024년형 가솔린 4.4 4WD : Competition P0-0(자동)": "BMW_31_1_2",
            "2024년형 가솔린 4.4 4WD : Competition P1(자동)": "BMW_31_1_3",
            "2024년형 가솔린 4.4 4WD : Competition P1-1(자동)": "BMW_31_1_4",
            "2024년형 가솔린 4.4 4WD : Competition P2(자동)": "BMW_31_1_5",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_32": {
            "2024년형 가솔린 3.0 4WD : 40i xDrive DPE 6seater(자동)": "BMW_32_1_1",
            "2024년형 가솔린 3.0 4WD : 40i xDrive DPE 6seater_P1(자동)": "BMW_32_1_2",
            "2024년형 가솔린 3.0 4WD : 40i xDrive DPE 6seater_P2(자동)": "BMW_32_1_3",
            "2024년형 가솔린 3.0 4WD : 40i xDrive DPE 7seater(자동)": "BMW_32_1_4",
            "2024년형 가솔린 3.0 4WD : 40i xDrive DPE 7seater_P1(자동)": "BMW_32_1_5",
            "2024년형 가솔린 3.0 4WD : 40i xDrive DPE 7seater_P2(자동)": "BMW_32_1_6",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport 6seater(자동)": "BMW_32_1_7",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport 6seater_P0-1(자동)": "BMW_32_1_8",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport 6seater_P1(자동)": "BMW_32_1_9",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport 6seater_P2(자동)": "BMW_32_1_10",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport 6seater_P3(자동)": "BMW_32_1_11",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport 7seater(자동)": "BMW_32_1_12",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport 7seater_P1(자동)": "BMW_32_1_13",
            "2024년형 가솔린 3.0 4WD : 40i xDrive M Sport 7seater_P2(자동)": "BMW_32_1_14",
            "2024년형 가솔린 4.4 4WD : M60i M Sport Pro(자동)": "BMW_32_2_1",
            "2024년형 가솔린 4.4 4WD : M60i M Sport Pro_P0-1(자동)": "BMW_32_2_2",
            "2024년형 가솔린 4.4 4WD : M60i M Sport Pro P1(자동)": "BMW_32_2_3",
            "2024년형 가솔린 4.4 4WD : M60i M Sport Pro P2(자동)": "BMW_32_2_4",
            "2024년형 가솔린 4.4 4WD : M60i M Sport Pro P2-0(자동)": "BMW_32_2_5",
            "2024년형 디젤 3.0 4WD : 40d xDrive DPE 6seater(자동)": "BMW_32_3_1",
            "2024년형 디젤 3.0 4WD : 40d xDrive DPE 6seater_P1(자동)": "BMW_32_3_2",
            "2024년형 디젤 3.0 4WD : 40d xDrive DPE 6seater_P2(자동)": "BMW_32_3_3",
            "2024년형 디젤 3.0 4WD : 40d xDrive DPE 7seater(자동)": "BMW_32_3_4",
            "2024년형 디젤 3.0 4WD : 40d xDrive DPE 7seater_P1(자동)": "BMW_32_3_5",
            "2024년형 디젤 3.0 4WD : 40d xDrive DPE 7seater_P2(자동)": "BMW_32_3_6",
            "2024년형 디젤 3.0 4WD : 40d xDrive M Sport 6seater(자동)": "BMW_32_3_7",
            "2024년형 디젤 3.0 4WD : 40d xDrive M Sport 6seater_P1(자동)": "BMW_32_3_8",
            "2024년형 디젤 3.0 4WD : 40d xDrive M Sport 6seater_P2(자동)": "BMW_32_3_9",
            "2024년형 디젤 3.0 4WD : 40d xDrive M Sport 6seater_P3(자동)": "BMW_32_3_10",
            "2024년형 디젤 3.0 4WD : 40d xDrive M Sport 7seater(자동)": "BMW_32_3_11",
            "2024년형 디젤 3.0 4WD : 40d xDrive M Sport 7seater_P1(자동)": "BMW_32_3_12",
            "2024년형 디젤 3.0 4WD : 40d xDrive M Sport 7seater_P1-0(자동)": "BMW_32_3_13",
            "2024년형 디젤 3.0 4WD : 40d xDrive M Sport 7seater_P2(자동)": "BMW_32_3_14",
            "2024년형 디젤 3.0 4WD : 40d xDrive M Sport 7seater_P3(자동)": "BMW_32_3_15",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_33": {
            "2024년형 가솔린 4.4 터보 플러그인 하이브리드 4WD : V8 PHEV Night Gold(자동)": "BMW_33_1_1",
            "2024년형 가솔린 4.4 터보 플러그인 하이브리드 4WD : V8 PHEV High Gloss Shadow Line(자동)": "BMW_33_1_2",
            "2024년형 가솔린 4.4 터보 플러그인 하이브리드 4WD : V8 PHEV High Gloss Shadow Line P0-0(자동)": "BMW_33_1_3",
            "2024년형 가솔린 4.4 터보 플러그인 하이브리드 4WD : V8 PHEV Label Red Limited Edition(자동)": "BMW_33_1_4",
            "이전으로 돌아가기": "BMW",
        },
        "BMW_34": {
            "2024년형 가솔린 2.0 2WD : 220i Advantage(자동)": "BMW_34_1_1",
            "2024년형 가솔린 2.0 2WD : 220i Advantage P1(자동)": "BMW_34_1_2",
            "2024년형 가솔린 2.0 2WD : 220i Advantage P2(자동)": "BMW_34_1_3",
            "2024년형 가솔린 2.0 2WD : 220i Luxury(자동)": "BMW_34_1_4",
            "2024년형 가솔린 2.0 2WD : 220i Luxury P1(자동)": "BMW_34_1_5",
            "2024년형 가솔린 2.0 2WD : 220i Luxury P2(자동)": "BMW_34_1_6",
            "2024년형 디젤 2.0 2WD : 218d Advantage(자동)": "BMW_34_2_1",
            "2024년형 디젤 2.0 2WD : 218d Advantage P1(자동)": "BMW_34_2_2",
            "2024년형 디젤 2.0 2WD : 218d Advantage P2(자동)": "BMW_34_2_3",
            "2024년형 디젤 2.0 2WD : 218d Luxury(자동)": "BMW_34_2_4",
            "2024년형 디젤 2.0 2WD : 218d Luxury P1(자동)": "BMW_34_2_5",
            "2024년형 디젤 2.0 2WD : 218d Luxury P2(자동)": "BMW_34_2_6",
            "이전으로 돌아가기": "BMW",
        },
        "아우디": {
            "A3(8Y)": "아우디_1",
            "S3(8Y)": "아우디_2",
            "RS3(*Y)": "아우디_3",
            "New A4(B9 F/L)": "아우디_4",
            "New S4(B9 F/L)": "아우디_5",
            "New A5(2세대 F/L)": "아우디_6",
            "New S5(2세대 F/L)": "아우디_7",
            "RS5(2세대 F/L)": "아우디_8",
            "A6(C8)": "아우디_9",
            "S6(C8)": "아우디_10",
            "RS6 Avant(C8)": "아우디_11",
            "A7(2세대)": "아우디_12",
            "S7(2세대)": "아우디_13",
            "RS7(2세대)": "아우디_14",
            "The New A8(D5)": "아우디_15",
            "The New S8(D5)": "아우디_16",
            "e-tron GT": "아우디_17",
            "RS e-tron GT": "아우디_18",
            "The New Q2(1세대 F/L)": "아우디_19",
            "Q3(2세대)": "아우디_20",
            "Q4 E-tron": "아우디_21",
            "New Q5(2세대 F/L)": "아우디_22",
            "New SQ5(2세대 F/L)": "아우디_23",
            "New Q7(2세대 F/L)": "아우디_24",
            "SQ7(2세대 F/L)": "아우디_25",
            "Q8": "아우디_26",
            "RS Q8": "아우디_27",
            "Q8 E-tron": "아우디_28",
            "SQ8 E-tron": "아우디_29",
            "e-tron": "아우디_30",
            "e-tron S": "아우디_31",
            "이전으로 돌아가기": "유럽",
        },
        "아우디_1": {
            "2023년형 가솔린 2.0 2WD : 40 TFSI(자동)": "아우디_1_1_1",
            "2023년형 가솔린 2.0 2WD : 40 TFSI Premium(자동)": "아우디_1_1_2",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_2": {
            "2023년형 가솔린 2.0 터보 AWD : TFSI(자동)": "아우디_2_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_3": {
            "2024년형 가솔린 2.5 터보 AWD : TFSI(자동)": "아우디_3_1_1",
            "이전으로 돌아가기": "아우디",
        },
        # 0618 작업 여기까지이ㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣㅣ
        "아우디_4": {
            "2023년형 가솔린 2.0 2WD : (자동)": "아우디_4_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_5": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_5_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_6": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_6_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_7": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_7_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_8": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_8_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_9": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_9_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_10": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_10_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_11": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_11_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_12": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_12_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_13": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_13_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_14": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_14_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_15": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_15_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_16": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_16_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_17": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_17_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_18": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_18_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_19": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_19_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_20": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_20_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_21": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_21_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_22": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_22_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_23": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_23_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_24": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_24_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_25": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_25_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_26": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_26_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_27": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_27_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_28": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_28_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_29": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_29_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_30": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_30_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "아우디_31": {
            "2024년형 가솔린 2.0 2WD : (자동)": "아우디_31_1_1",
            "이전으로 돌아가기": "아우디",
        },
        "폭스바겐": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "미니": {
            "New Hatch(F56 F/L)": "미니_1",
            "New cooper Convertible(3세대 F/L)": "미니_2",
            "Clubman(2세대 F/L)": "미니_3",
            "Countryman(3세대)": "미니_4",
            "Countryman(2세대 F/L)": "미니_5",
            "이전으로 돌아가기": "유럽",
        },
        "미니_1": {
            "2024년형 가솔린 1.5 터보 2WD 3도어 : 3-Door Cooper Classic(자동)": "미니_1_1_1",
            "2024년형 가솔린 1.5 터보 2WD 3도어 : 3-Door Cooper Classic Plus(자동)": "미니_1_1_2",
            "2024년형 가솔린 1.5 터보 2WD 3도어 : 3-Door Cooper Classic Plus T1(자동)": "미니_1_1_3",
            "2024년형 가솔린 2.0 터보 2WD 3도어 : 3-Door Cooper S Classic(자동)": "미니_1_2_1",
            "2024년형 가솔린 2.0 터보 2WD 3도어 : 3-Door Cooper S Classic T1(자동)": "미니_1_2_2",
            "2024년형 가솔린 2.0 터보 2WD 3도어 : 3-Door Cooper JCW(자동)": "미니_1_2_3",
            "2024년형 가솔린 1.5 터보 2WD 5도어 : 5-Door Cooper Classic": "미니_1_3_1",
            "2024년형 가솔린 2.0 터보 2WD 5도어 : 5-Door Cooper S Classic": "미니_1_4_1",
            "이전으로 돌아가기": "미니",
        },
        "미니_2": {
            "2024년형 가솔린 1.5 터보 2WD : Cooper Classic(자동)": "미니_2_1_1",
            "2024년형 가솔린 2.0 터보 2WD : Cooper S Classic(자동)": "미니_2_2_1",
            "2024년형 가솔린 2.0 터보 2WD : JCW(자동)": "미니_2_2_2",
            "이전으로 돌아가기": "미니",
        },
        "미니_3": {
            "2024년형 가솔린 1.5 터보 2WD : Cooper Classic(자동)": "미니_3_1_1",
            "2024년형 가솔린 2.0 터보 2WD : Cooper S Classic(자동)": "미니_3_2_1",
            "2024년형 가솔린 2.0 터보 4WD : JCW ALL 4(자동)": "미니_3_3_1",
            "이전으로 돌아가기": "미니",
        },
        "미니_4": {
            "2024년형 가솔린 2.0 터보 AWD : Cooper S ALL 4 Classic(자동)": "미니_4_1_1",
            "2024년형 가솔린 2.0 터보 AWD : Cooper S ALL 4 Favoured(자동)": "미니_4_1_2",
            "2024년형 가솔린 2.0 터보 AWD : JCW ALL 4(자동)": "미니_4_1_3",
            "이전으로 돌아가기": "미니",
        },
        "미니_5": {
            "2024년형 가솔린 1.5 터보 2WD : Cooper Classic(자동)": "미니_5_1_1",
            "2024년형 가솔린 1.5 터보 2WD : Cooper Classic T1(자동)": "미니_5_1_2",
            "2024년형 가솔린 2.0 터보 4WD : Cooper S ALL 4 Classic(자동)": "미니_5_2_1",
            "2024년형 가솔린 2.0 터보 4WD : Cooper S ALL 4 Classic T1(자동)": "미니_5_2_2",
            "2024년형 가솔린 2.0 터보 4WD : JCW ALL 4(자동)": "미니_5_2_3",
            "이전으로 돌아가기": "미니",
        },
        "볼보": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "폴스타": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "랜드로버": {
            "Range Rover Evoque(2세대 F/L)": "랜드로버_1",
            "New Discovery Sport(1세대 F/L)": "랜드로버_2",
            "Range Rover Velar(1세대 F/L)": "랜드로버_3",
            "Range Rover Sport(3세대)": "랜드로버_4",
            "Discovery5(L462 F/L)": "랜드로버_5",
            "Defender(2세대)": "랜드로버_6",
            "Range Rover(5세대)": "랜드로버_7",
            "이전으로 돌아가기": "유럽",
        },
        "랜드로버_1": {
            "2024년형 가솔린 2.0 터보 4WD : P250 S(자동)": "랜드로버_1_1_1",
            "2024년형 가솔린 2.0 터보 4WD : P250 Dynamic SE(자동)": "랜드로버_1_1_2",
            "이전으로 돌아가기": "랜드로버",
        },
        "랜드로버_2": {
            "2024년형 가솔린 2.0 터보 4WD : P250 S(자동)": "랜드로버_2_1_1",
            "2024년형 가솔린 2.0 터보 4WD : P250 Dynamic SE(자동)": "랜드로버_2_1_2",
            "이전으로 돌아가기": "랜드로버",
        },
        "랜드로버_3": {
            "2025년형 가솔린 2.0 4WD : P250 Dynamic SE(자동)": "랜드로버_3_1_1",
            "2025년형 가솔린 3.0 4WD : P400 Dynamic HSE(자동)": "랜드로버_3_2_1",
            "2025년형 가솔린 2.0 플러그인 하이브리드 4WD : P400e Dynamic SE(자동)": "랜드로버_3_3_1",
            "이전으로 돌아가기": "랜드로버",
        },
        "랜드로버_4": {
            "2024년형 가솔린 3.0 4WD : P360 SE Dynamic(자동)": "랜드로버_4_1_1",
            "2024년형 가솔린 3.0 4WD : P360 HSE Dynamic(자동)": "랜드로버_4_1_2",
            "2024년형 가솔린 3.0 4WD : P360 Autobiography(자동)": "랜드로버_4_1_3",
            "2024년형 가솔린 4.4 4WD : P635 SV Edition One Carbon Bronze(자동)": "랜드로버_4_2_1",
            "2024년형 가솔린 4.4 4WD : P635 SV Edition One Obsidian Black(자동)": "랜드로버_4_2_2",
            "2024년형 가솔린 4.4 4WD : P635 SV Edition One Flux Silver(자동)": "랜드로버_4_2_3",
            "2024년형 가솔린 3.0 플러그인 하이브리드 4WD : P550e HSE Dynamic(자동)": "랜드로버_4_3_1",
            "2024년형 디젤 3.0 4WD : D300 HSE Dynamic(자동)": "랜드로버_4_4_1",
            "이전으로 돌아가기": "랜드로버",
        },
        "랜드로버_5": {
            "2024년형 가솔린 2.0 터보 4WD : P300 S(자동)": "랜드로버_5_1_1",
            "2024년형 가솔린 3.0 터보 4WD : P360 Dynamic SE(자동)": "랜드로버_5_2_1",
            "2024년형 디젤 3.0 4WD : D250 S(자동)": "랜드로버_5_3_1",
            "2024년형 디젤 3.0 4WD : D300 Dynamic HSE(자동)": "랜드로버_5_3_2",
            "2023.5년형 가솔린 2.0 터보 4WD : P300 SE(자동)": "랜드로버_5_4_1",
            "2023.5년형 가솔린 3.0 터보 4WD : P360 R-Dynamic SE(자동)": "랜드로버_5_5_1",
            "2023.5년형 디젤 3.0 4WD : D250 S(자동)": "랜드로버_5_6_1",
            "2023.5년형 디젤 3.0 4WD : D250 SE(자동)": "랜드로버_5_6_2",
            "2023.5년형 디젤 3.0 4WD : D300 R-Dynamic HSE(자동)": "랜드로버_5_6_3",
            "이전으로 돌아가기": "랜드로버",
        },
        "랜드로버_6": {
            "2024년형 가솔린 2.0 4WD 4도어 : 110 P300 X-Dynamic SE(자동)": "랜드로버_6_1_1",
            "2024년형 가솔린 3.0 4WD 2도어 : 90 P400 X(자동)": "랜드로버_6_2_1",
            "2024년형 가솔린 3.0 4WD 4도어 : 110 P400 X (자동)": "랜드로버_6_3_1",
            "2024년형 가솔린 3.0 4WD 4도어 8인승 : 130 P400 X-Dynamic HSE(자동)": "랜드로버_6_4_1",
            "2024년형 가솔린 3.0 4WD 4도어 8인승 : 130 P400 OutBound(자동)": "랜드로버_6_4_2",
            "2024년형 디젤 3.0 4WD 2도어 : 90 D250 XS(자동)": "랜드로버_6_5_1",
            "2024년형 디젤 3.0 4WD 4도어 : 110 D250 SE(자동)": "랜드로버_6_6_1",
            "2024년형 디젤 3.0 4WD 4도어 : 110 D250 SE County Edition(자동)": "랜드로버_6_6_2",
            "2024년형 디젤 3.0 4WD 4도어 : 110 D300 X-Dynamic HSE(자동)": "랜드로버_6_6_3",
            "2024년형 디젤 3.0 4WD 4도어 8인승 : 130 D300 X-Dynamic HSE(자동)": "랜드로버_6_7_1",
            "이전으로 돌아가기": "랜드로버",
        },
        "랜드로버_7": {
            "2024년형 가솔린 4.4 4WD : P530 Autobiography SWB(자동)": "랜드로버_7_1_1",
            "2024년형 가솔린 4.4 4WD : P530 Autobiography LWB 5Seater(자동)": "랜드로버_7_1_2",
            "2024년형 가솔린 4.4 4WD : P530 Autobiography LWB 7Seater(자동)": "랜드로버_7_1_3",
            "2024년형 가솔린 4.4 4WD : P615 SV LWB(자동)": "랜드로버_7_1_4",
            "2024년형 디젤 3.0 4WD : D350 Autobiography SWB(자동)": "랜드로버_7_2_1",
            "2024년형 가솔린 3.0 플러그인 하이브리드 4WD : P550e Autobiography SWB(자동)": "랜드로버_7_3_1",
            "이전으로 돌아가기": "랜드로버",
        },
        "포르쉐": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "람보르기니": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "벤틀리": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "맥라렌": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "페라리": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "애스턴마틴": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "로터스": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "마세라티": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "롤스로이스": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "푸조": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "이네오스": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "유럽",
        },
        "포드": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "미국",
        },
        "링컨": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "미국",
        },
        "지프": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "미국",
        },
        "GMC": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "미국",
        },
        "캐딜락": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "미국",
        },
        "테슬라": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "미국",
        },
        "토요타": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "일본",
        },
        "렉서스": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "일본",
        },
        "혼다": {
            "미구현(main)": "main",
            "이전으로 돌아가기": "일본",
        },
        "현대_1": { #캐스퍼 세부모델
            "2023년형 가솔린1.0 2WD : 스마트(자동)": "현대_1_1_1",
            "2023년형 가솔린1.0 2WD : 디 에센셜 라이트(자동)": "현대_1_1_2",
            "2023년형 가솔린1.0 2WD : 디 에센셜(자동)": "현대_1_1_3",
            "2023년형 가솔린1.0 2WD : 인스퍼레이션(자동)": "현대_1_1_4",
            "2023년형 가솔린1.0 2WD밴 : 스마트(자동)": "현대_1_2_1",
            "2023년형 가솔린1.0 2WD밴 : 스마트초이스(자동)": "현대_1_2_2",
            "2023년형 가솔린1.0터보 액티브 I 2WD : 스마트(자동)": "현대_1_3_1",
            "2023년형 가솔린1.0터보 액티브 I 2WD : 디 에센셜 라이트(자동)": "현대_1_3_2",
            "2023년형 가솔린1.0터보 액티브 II 2WD : 디 에센셜(자동)": "현대_1_4_1",
            "2023년형 가솔린1.0터보 액티브 II 2WD : 인스퍼레이션(자동)": "현대_1_4_2",
            "2023년형 가솔린1.0터보 액티브 I 2WD밴 : 스마트(자동)": "현대_1_5_1",
            "2023년형 가솔린1.0터보 액티브 I 2WD밴 : 스마트초이스(자동)": "현대_1_5_2",
            "이전으로 돌아가기": "현대",
        },
        "현대_1_1_1": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "현대_1_1_2": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "현대_1_1_3": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "현대_1_1_4": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "현대_1_2_1": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "현대_1_2_2": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "현대_1_3_1": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "현대_1_3_2": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "현대_1_4_1": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "현대_1_4_2": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "현대_1_5_1": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "현대_1_5_2": { #캐스퍼 색상
            "NES-언블리치드 아이보리": "현대_1_1_1",
            "R4G-티탄 그레이 메탈릭": "현대_1_1_2",
            "SAW-아틀라스 화이트": "현대_1_1_3",
            "SOP-소울트로닉 오렌지 펄": "현대_1_1_4",
            "TKS-톰보이 카키": "현대_1_2_1",
            "YP5-인텐스블루 펄": "현대_1_2_2",
            "TKM-비자림 카키 매트": "현대_1_3_1",
            "이전으로 돌아가기": "현대_1",
        },
        "제네시스_3": { #G80 (RG3 F/L) 세부모델
            "2024년형 가솔린2.5 터보 2WD : 기본형(자동)": "제네시스_3_1_1",
            "2024년형 가솔린2.5 터보 2WD : 스포츠패키지(자동)": "제네시스_3_1_2",
            "2024년형 가솔린2.5 터보 AWD : 기본형(자동)": "제네시스_3_2_1",
            "2024년형 가솔린2.5 터보 AWD : 스포츠패키지자동)": "제네시스_3_2_2",
            "2024년형 가솔린3.5 터보 2WD : 기본형(자동)": "제네시스_3_3_1",
            "2024년형 가솔린3.5 터보 2WD : 스포츠패키지(자동)": "제네시스_3_3_2",
            "2024년형 가솔린3.5 터보 AWD : 기본형(자동)": "제네시스_3_4_1",
            "2024년형 가솔린3.5 터보 AWD : 스포츠패키지(자동)": "제네시스_3_4_2",
            "이전으로 돌아가기": "제네시스",
        },
        # 다른 상태들에 대한 데이터 추가...
    }


    #    아래 코드 설명..
    #    "[1]": "[2]"
    #
    #    다음과 같이 출력됩니다..
    #
    #    ->  오토커넥트 챗봇 : [2]
    #        [1]

    messages_data = {
        "신차구매 컨설팅": "어떤 종류에 관심이 있으신가요?",
        "바로 상담하기": "상담 요청을 위해 정보를 입력해주세요!",
        "국산차": "원하시는 제조사는 어디인가요?",
        "수입차": "원하시는 제조사의 국가는 어디인가요?",
        "최신 인기차량 추천받기": "최신 인기차량을 추천해드리겠습니다!",
        "나만의 모빌리티 선택하기": "구체적인 정보를 입력해주세요!",
        "유럽": "원하시는 제조사는 어디인가요?",
        "미국": "원하시는 제조사는 어디인가요?",
        "일본": "원하시는 제조사는 어디인가요?",
        "현대": "어떤 차종을 원하시나요?",
        "제네시스": "어떤 차종을 원하시나요?",
        "기아": "어떤 차종을 원하시나요?",
        "쉐보레": "어떤 차종을 원하시나요?",
        "KG 모빌리티": "어떤 차종을 원하시나요?",
        "르노": "어떤 차종을 원하시나요?",
        "다피코": "어떤 차종을 원하시나요?",
        "스마트 EV": "어떤 차종을 원하시나요?",
        "마이브": "어떤 차종을 원하시나요?",
        "벤츠": "어떤 차종을 원하시나요?",
        "BMW": "어떤 차종을 원하시나요?",
        "아우디": "어떤 차종을 원하시나요?",
        "폭스바겐": "어떤 차종을 원하시나요?",
        "미니": "어떤 차종을 원하시나요?",
        "볼보": "어떤 차종을 원하시나요?",
        "폴스타": "어떤 차종을 원하시나요?",
        "랜드로버": "어떤 차종을 원하시나요?",
        "포르쉐": "어떤 차종을 원하시나요?",
        "람보르기니": "어떤 차종을 원하시나요?",
        "벤틀리": "어떤 차종을 원하시나요?",
        "맥라렌": "어떤 차종을 원하시나요?",
        "페라리": "어떤 차종을 원하시나요?",
        "애스턴마틴": "어떤 차종을 원하시나요?",
        "로터스": "어떤 차종을 원하시나요?",
        "마세라티": "어떤 차종을 원하시나요?",
        "롤스로이스": "어떤 차종을 원하시나요?",
        "푸조": "어떤 차종을 원하시나요?",
        "이네오스": "어떤 차종을 원하시나요?",
        "포드": "어떤 차종을 원하시나요?",
        "링컨": "어떤 차종을 원하시나요?",
        "지프": "어떤 차종을 원하시나요?",
        "GMC": "어떤 차종을 원하시나요?",
        "캐딜락": "어떤 차종을 원하시나요?",
        "테슬라": "어떤 차종을 원하시나요?",
        "토요타": "어떤 차종을 원하시나요?",
        "렉서스": "어떤 차종을 원하시나요?",
        "혼다": "어떤 차종을 원하시나요?",
        "현대_1": "세부모델을 골라주세요!",
        "현대_1_1_1": "색상을 골라주세요!",
        "현대_1_1_2": "색상을 골라주세요!",
        "현대_1_1_3": "색상을 골라주세요!",
        "현대_1_1_4": "색상을 골라주세요!",
        "현대_1_2_1": "색상을 골라주세요!",
        "현대_1_2_2": "색상을 골라주세요!",
        "현대_1_3_1": "색상을 골라주세요!",
        "현대_1_3_2": "색상을 골라주세요!",
        "현대_1_4_1": "색상을 골라주세요!",
        "현대_1_4_2": "색상을 골라주세요!",
        "현대_1_5_1": "색상을 골라주세요!",
        "현대_1_5_2": "색상을 골라주세요!",
        # 다른 상태들에 대한 메시지 추가...
    }

    def handle_buttons():
        current_state = st.session_state.get("button_state", "main")
        options = buttons_data.get(current_state, {})
        back_state = options.pop("이전으로 돌아가기", None)
        create_buttons(options, current_state, back_state)
        
        # 상태에 맞는 메시지 표시
        if current_state in messages_data:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f"<div style='display: flex; justify-content: flex-start;'><strong>오토커넥트 챗봇 : {messages_data[current_state]}</strong></div>", unsafe_allow_html=True)
            #st.markdown(f"<div style='display: flex; justify-content: flex-start;'><strong>{current_state}</strong></div>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)

        # 고객님 정보 이메일 발송 코드    
        if current_state == "상담 신청하기":
            personal_consultation_form()
        if current_state == "상담 신청하기1":
            personal_consultation_form1()
        if current_state == "상담 신청하기2":
            personal_consultation_form2()
        if current_state == "상담 신청하기3":
            personal_consultation_form3()
        if current_state == "상담 신청하기4":
            personal_consultation_form4()

    def personal_consultation_form():
        with st.form("personal_consultation"):
            st.write("이름을 적어주세요.")
            name = st.text_input("이름")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("이메일을 적어주세요.")
            email = st.text_input("이메일")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("전화번호를 적어주세요.")
            phone = st.text_input("전화번호")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("성별과 나이대를 적어주세요.")
            gender_age = st.text_input("성별과 나이대")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 차종과 브랜드를 적어주세요.")
            car_brand = st.text_input("희망 차종과 브랜드")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 주행거리를 입력해주세요.")
            mileage = st.text_input("희망 주행거리")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("추가로 희망하는 사항을 적어주세요.")
            additional_info = st.text_input("추가로 희망하는 사항")
            
            submitted = st.form_submit_button("전송")

            if submitted:
                if send_email(name, email, phone, gender_age, car_brand, mileage, additional_info):
                    st.success("신청이 완료되었습니다!")
                else:
                    st.error("이메일 전송에 실패했습니다. 인터넷 연결을 다시 확인해보시거나, 다시 시도해주세요!")

    def send_email(name, email, phone, gender_age, car_brand, mileage, additional_info):
        from_address = "AutoConnectChatBot@gmail.com"  # 보내는 사람 이메일 주소
        to_address = "nays43883@naver.com"
        subject = "(일반 상담 요청) 오토커넥트 챗봇에서 보낸 상담 요청 인적사항입니다"
        
        body = f"""
        요청자가 선택한 컨설팅은 일반 상담 요청입니다^^
        
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

    def personal_consultation_form1():
        with st.form("personal_consultation"):
            st.write("이름을 적어주세요.")
            name = st.text_input("이름")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("이메일을 적어주세요.")
            email = st.text_input("이메일")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("전화번호를 적어주세요.")
            phone = st.text_input("전화번호")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("성별과 나이대를 적어주세요.")
            gender_age = st.text_input("성별과 나이대")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 차종과 브랜드를 적어주세요.")
            car_brand = st.text_input("희망 차종과 브랜드")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 주행거리를 입력해주세요.")
            mileage = st.text_input("희망 주행거리")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("추가로 희망하는 사항을 적어주세요.")
            additional_info = st.text_input("추가로 희망하는 사항")
            
            submitted = st.form_submit_button("전송")

            if submitted:
                if send_email1(name, email, phone, gender_age, car_brand, mileage, additional_info):
                    st.success("신청이 완료되었습니다!")
                else:
                    st.error("이메일 전송에 실패했습니다. 인터넷 연결을 다시 확인해보시거나, 다시 시도해주세요!")

    def send_email1(name, email, phone, gender_age, car_brand, mileage, additional_info):
        from_address = "AutoConnectChatBot@gmail.com"  # 보내는 사람 이메일 주소
        to_address = "nays43883@naver.com"
        subject = "(중고차구매) 오토커넥트 챗봇에서 보낸 상담 요청 인적사항입니다"
        
        body = f"""
        요청자가 선택한 컨설팅은 중고차구매입니다^^

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

    def personal_consultation_form2():
        with st.form("personal_consultation"):
            st.write("이름을 적어주세요.")
            name = st.text_input("이름")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("이메일을 적어주세요.")
            email = st.text_input("이메일")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("전화번호를 적어주세요.")
            phone = st.text_input("전화번호")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("성별과 나이대를 적어주세요.")
            gender_age = st.text_input("성별과 나이대")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 차종과 브랜드를 적어주세요.")
            car_brand = st.text_input("희망 차종과 브랜드")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 주행거리를 입력해주세요.")
            mileage = st.text_input("희망 주행거리")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("추가로 희망하는 사항을 적어주세요.")
            additional_info = st.text_input("추가로 희망하는 사항")
            
            submitted = st.form_submit_button("전송")

            if submitted:
                if send_email2(name, email, phone, gender_age, car_brand, mileage, additional_info):
                    st.success("신청이 완료되었습니다!")
                else:
                    st.error("이메일 전송에 실패했습니다. 인터넷 연결을 다시 확인해보시거나, 다시 시도해주세요!")

    def send_email2(name, email, phone, gender_age, car_brand, mileage, additional_info):
        from_address = "AutoConnectChatBot@gmail.com"  # 보내는 사람 이메일 주소
        to_address = "nays43883@naver.com"
        subject = "(리스렌트 승계) 오토커넥트 챗봇에서 보낸 상담 요청 인적사항입니다"
        
        body = f"""
        요청자가 선택한 컨설팅은 리스렌트 승계입니다^^

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

    def personal_consultation_form3():
        with st.form("personal_consultation"):
            st.write("이름을 적어주세요.")
            name = st.text_input("이름")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("이메일을 적어주세요.")
            email = st.text_input("이메일")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("전화번호를 적어주세요.")
            phone = st.text_input("전화번호")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("성별과 나이대를 적어주세요.")
            gender_age = st.text_input("성별과 나이대")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 차종과 브랜드를 적어주세요.")
            car_brand = st.text_input("희망 차종과 브랜드")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 주행거리를 입력해주세요.")
            mileage = st.text_input("희망 주행거리")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("추가로 희망하는 사항을 적어주세요.")
            additional_info = st.text_input("추가로 희망하는 사항")
            
            submitted = st.form_submit_button("전송")

            if submitted:
                if send_email3(name, email, phone, gender_age, car_brand, mileage, additional_info):
                    st.success("신청이 완료되었습니다!")
                else:
                    st.error("이메일 전송에 실패했습니다. 인터넷 연결을 다시 확인해보시거나, 다시 시도해주세요!")

    def send_email3(name, email, phone, gender_age, car_brand, mileage, additional_info):
        from_address = "AutoConnectChatBot@gmail.com"  # 보내는 사람 이메일 주소
        to_address = "nays43883@naver.com"
        subject = "(A/S 사후관리) 오토커넥트 챗봇에서 보낸 상담 요청 인적사항입니다"
        
        body = f"""
        요청자가 선택한 컨설팅은 A/S 사후관리입니다^^

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

    def personal_consultation_form4():
        with st.form("personal_consultation"):
            st.write("이름을 적어주세요.")
            name = st.text_input("이름")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("이메일을 적어주세요.")
            email = st.text_input("이메일")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("전화번호를 적어주세요.")
            phone = st.text_input("전화번호")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("성별과 나이대를 적어주세요.")
            gender_age = st.text_input("성별과 나이대")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 차종과 브랜드를 적어주세요.")
            car_brand = st.text_input("희망 차종과 브랜드")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("희망 주행거리를 입력해주세요.")
            mileage = st.text_input("희망 주행거리")
            st.markdown("<hr>", unsafe_allow_html=True)
            
            st.write("추가로 희망하는 사항을 적어주세요.")
            additional_info = st.text_input("추가로 희망하는 사항")
            
            submitted = st.form_submit_button("전송")

            if submitted:
                if send_email4(name, email, phone, gender_age, car_brand, mileage, additional_info):
                    st.success("신청이 완료되었습니다!")
                else:
                    st.error("이메일 전송에 실패했습니다. 인터넷 연결을 다시 확인해보시거나, 다시 시도해주세요!")

    def send_email4(name, email, phone, gender_age, car_brand, mileage, additional_info):
        from_address = "AutoConnectChatBot@gmail.com"  # 보내는 사람 이메일 주소
        to_address = "nays43883@naver.com"
        subject = "(법인 전문 컨설팅 의뢰) 오토커넥트 챗봇에서 보낸 상담 요청 인적사항입니다"
        
        body = f"""
        요청자가 선택한 컨설팅은 법인 전문입니다^^

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


    handle_buttons()

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

if choice == "채팅으로 차량 상담하기":
    st.set_page_config(page_title="Auto Connect Chat Bot",  page_icon="https://ifh.cc/g/P8K9BV.png", layout="centered", initial_sidebar_state="expanded")

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
            if msg.role == "user":
                st.markdown(
                    f'<div style="text-align: right; margin-bottom: 10px;">'
                    f'<div style="display: inline-block; padding: 10px; border-radius: 10px; background-color: #F2F2F2; max-width: 70%;">'
                    f'{msg.content[0].text.value}</div></div>',
                    unsafe_allow_html=True
                )
            else:
                with st.spinner('오토커넥트 챗봇이 답변하는 중...'):
                    st.markdown(
                        f'<div style="text-align: left; margin-bottom: 10px;">'
                        f'<div style="display: inline-block; padding: 10px; border-radius: 10px; background-color: #A0B4F2; max-width: 70%;">'
                        f'<strong>{role}<br>:</strong> {msg.content[0].text.value}</div></div>',
                        unsafe_allow_html=True
                    )

        print(run)
        print(message)
