import json
from models import rag_model
from config import VECTOR_DB_PATH
import faiss


def load_terms_and_conditions():

    return [
        "1. 서비스 이용 약관: 본 약관은 [회사명]('회사')이 제공하는 모든 서비스의 이용 조건과 절차, 회사와 회원 간의 권리, 의무 및 책임사항 등을 규정합니다. 회원은 본 약관을 숙지하고 동의한 것으로 간주되며, 본 약관에 동의하지 않을 경우 서비스 이용이 제한될 수 있습니다.",
        "2. 개인정보 수집 동의: 회사는 서비스 제공을 위해 필요한 최소한의 개인정보를 수집합니다. 수집하는 개인정보는 이름, 이메일 주소, 전화번호, 생년월일, 성별, 주소 등이 포함될 수 있습니다. 회원은 개인정보 수집 및 이용에 대한 동의를 거부할 권리가 있으나, 이 경우 서비스 이용이 제한될 수 있습니다.",
        "3. 개인정보 이용 목적: 수집된 개인정보는 다음과 같은 목적으로 활용됩니다. a) 서비스 제공 및 운영, b) 회원 관리 및 본인 확인, c) 고객 지원 및 민원 처리, d) 신규 서비스 개발 및 맞춤 서비스 제공, e) 이벤트 및 광고성 정보 제공 및 참여기회 제공, f) 서비스 이용 통계 분석. 회사는 수집한 개인정보를 본 이용 목적 이외의 용도로 사용하지 않으며, 이용 목적이 변경될 시에는 사전에 회원의 동의를 구하도록 하겠습니다.",
        "4. 개인정보 보유 및 파기: 회원의 개인정보는 원칙적으로 개인정보의 수집 및 이용목적이 달성되면 지체 없이 파기됩니다. 회원 탈퇴 시 개인정보는 즉시 파기됩니다. 단, 관계 법령의 규정에 의하여 보존할 필요가 있는 경우 회사는 아래와 같이 관계 법령에서 정한 일정한 기간 동안 회원정보를 보관합니다. a) 계약 또는 청약철회 등에 관한 기록: 5년, b) 대금결제 및 재화 등의 공급에 관한 기록: 5년, c) 소비자의 불만 또는 분쟁처리에 관한 기록: 3년, d) 표시/광고에 관한 기록: 6개월, e) 세법이 규정하는 모든 거래에 관한 장부 및 증빙서류: 5년, f) 전자금융 거래에 관한 기록: 5년, g) 서비스 방문 기록: 3개월",
        "5. 제3자 정보 제공: 회사는 회원의 개인정보를 원칙적으로 외부에 제공하지 않습니다. 다만, 아래의 경우에는 예외로 합니다. a) 회원이 사전에 동의한 경우, b) 법령의 규정에 의거하거나, 수사 목적으로 법령에 정해진 절차와 방법에 따라 수사기관의 요구가 있는 경우, c) 통계작성, 학술연구 또는 시장조사를 위하여 필요한 경우로서 특정 개인을 식별할 수 없는 형태로 제공하는 경우. 회사는 제3자에게 개인정보를 제공하는 경우에도 제공받는 자, 제공목적, 제공정보의 항목, 보유 및 이용기간 등을 회원에게 고지하고 동의를 받습니다.",
        "6. 회원의 의무: 회원은 자신의 계정 정보를 안전하게 관리해야 하며, 타인에게 공유해서는 안 됩니다. 회원은 자신의 계정과 관련된 모든 활동에 대해 책임을 집니다. 회원은 서비스를 이용하면서 취득한 정보를 회사의 사전 승낙 없이 복제, 송신, 출판, 배포, 방송 등 기타 방법에 의하여 영리목적으로 이용하거나 제3자에게 이용하게 하여서는 안 됩니다. 또한 회원은 서비스 이용과 관련하여 다음과 같은 행위를 하여서는 안 됩니다. a) 다른 회원의 계정을 부정하게 사용하는 행위, b) 서비스를 이용하여 법령 또는 이 약관이 금지하거나 공서양속에 반하는 행위를 하는 경우, c) 회사의 서비스를 방해하거나 그 정보를 도용하는 등 서비스에 지장을 주는 행위, d) 다른 회원이나 제3자를 비방하거나 명예를 손상시키는 행위, e) 회사의 지적재산권, 제3자의 지적재산권 등 기타 권리를 침해하는 행위, f) 음란물을 게시하거나 음란사이트를 연결하는 행위, g) 회사의 동의 없이 영리를 목적으로 서비스를 사용하는 행위",
        "7. 서비스 변경 및 중단: 회사는 운영상, 기술상의 필요에 따라 제공하고 있는 서비스를 변경할 수 있습니다. 서비스의 내용, 이용방법, 이용시간에 대하여 변경이 있는 경우에는 변경사유, 변경될 서비스의 내용 및 제공일자 등을 그 변경 전 7일 이상 해당 서비스 초기화면에 게시하여야 합니다. 다만, 버그 및 오류 등의 수정을 위하여 긴급하게 변경이 필요한 경우 사후에 고지할 수 있습니다. 회사는 무료로 제공되는 서비스의 일부 또는 전부를 회사의 정책 및 운영의 필요상 수정, 중단, 변경할 수 있으며, 이에 대하여 관련법에 특별한 규정이 없는 한 회원에게 별도의 보상을 하지 않습니다.",
        "8. 지적재산권: 회사가 제공하는 서비스 및 관련 제반 콘텐츠에 대한 지적재산권은 회사에 귀속됩니다. 회원은 회사가 제공하는 서비스를 이용함으로써 얻은 정보 중 회사에게 지적재산권이 귀속된 정보를 회사의 사전 승낙 없이 복제, 송신, 출판, 배포, 방송 등 기타 방법에 의하여 영리목적으로 이용하거나 제3자에게 이용하게 하여서는 안됩니다. 회사는 회원이 게시하거나 등록하는 서비스 내의 내용물, 게시 내용에 대해 제3자의 지적재산권을 침해하거나 기타 원인으로 문제가 될 소지가 있는 경우 이를 삭제하거나 등록 거부할 수 있습니다.",
        "9. 책임제한: 회사는 천재지변, 전쟁 및 기타 이에 준하는 불가항력으로 인하여 서비스를 제공할 수 없는 경우에는 서비스 제공에 대한 책임을 지지 않습니다. 회사는 기간통신 사업자가 전기통신 서비스를 중지하거나 정상적으로 제공하지 아니하여 손해가 발생한 경우 책임이 면제됩니다. 회사는 서비스용 설비의 보수, 교체, 정기점검, 공사 등 부득이한 사유로 발생한 손해에 대한 책임이 면제됩니다. 회사는 회원의 귀책사유로 인한 서비스 이용의 장애에 대하여 책임을 지지 않습니다. 회사는 회원이 서비스와 관련하여 게재한 정보, 자료, 사실의 신뢰도, 정확성 등의 내용에 관하여는 책임을 지지 않습니다. 회사는 회원 간 또는 회원과 제3자 상호간에 서비스를 매개로 하여 거래 등을 한 경우에는 책임이 면제됩니다. 회사는 무료로 제공되는 서비스 이용과 관련하여 관련법에 특별한 규정이 없는 한 책임을 지지 않습니다.",
        "10. 분쟁해결: 서비스 이용과 관련하여 회사와 회원 사이에 분쟁이 발생한 경우, 회사와 회원은 분쟁의 해결을 위해 성실히 협의합니다. 회사는 분쟁 해결을 위한 기구를 설치·운영할 수 있습니다. 협의가 이루어지지 않을 경우 양 당사자는 민사소송법상의 관할법원에 소를 제기할 수 있습니다. 회사와 회원 간 제기된 전자상거래 소송에는 한국 법을 적용합니다. 본 약관은 한국어를 정본으로 합니다. 본 약관 또는 서비스와 관련된 여러 언어로 작성된 번역본이 있는 경우 한국어 버전과 해석상의 차이가 있는 경우 한국어 버전이 우선합니다.",
    ]


if __name__ == "__main__":
    texts = load_terms_and_conditions()
    rag_model.create_index(texts)
    faiss.write_index(rag_model.index, VECTOR_DB_PATH)

    # text_chunks도 함께 저장
    with open(VECTOR_DB_PATH + "_chunks.json", "w") as f:
        json.dump(rag_model.text_chunks, f)

    print(f"Vector database initialized and saved to {VECTOR_DB_PATH}")
