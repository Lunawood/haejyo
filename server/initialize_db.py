import json
from models import rag_model
from config import VECTOR_DB_PATH
import faiss


def load_terms_and_conditions():
    # 이용약관 및 개인정보 동의 내용을 로드하는 함수
    # 실제 구현에서는 파일이나 데이터베이스에서 데이터를 로드해야 합니다
    return [
        "1. Terms of Service: These terms govern the conditions and procedures for using all services provided by [Company Name] ('the Company'), and stipulate the rights, obligations, and responsibilities between the Company and its members.",
        "2. Consent to Personal Information Collection: The Company collects the minimum amount of personal information necessary to provide its services. This may include names, email addresses, phone numbers, and other relevant details.",
        "3. Purpose of Personal Information Use: Collected personal information may be used for service provision, customer support, new service development, and marketing purposes.",
        "4. Retention and Destruction of Personal Information: Personal information is immediately destroyed upon membership withdrawal. However, information required to be kept for a certain period according to relevant laws will be retained for that duration.",
        "5. Third-party Information Provision: The Company does not provide personal information to external parties without the member's consent. However, it may be provided exceptionally if required by law or requested by investigative agencies following legally prescribed procedures and methods for investigation purposes.",
        "6. Member Obligations: Members must securely manage their account information and must not share it with others. Members must not use or allow others to use information obtained through the service for commercial purposes without prior consent from the Company, including reproduction, transmission, publication, distribution, or broadcasting.",
        "7. Service Changes and Termination: The Company may change the services provided based on operational or technical needs. When changes occur, the Company will notify members of the changes and their effective dates within the service.",
        "8. Intellectual Property Rights: All copyrights and other intellectual property rights for content provided through the service belong to the Company.",
        "9. Limitation of Liability: The Company is exempt from responsibility for providing services in cases of force majeure, including natural disasters or similar uncontrollable circumstances.",
        "10. Dispute Resolution: In the event of a dispute related to service use, the member and the Company will sincerely negotiate to resolve the dispute. If an agreement cannot be reached, the dispute will be resolved according to relevant laws.",
    ]


if __name__ == "__main__":
    texts = load_terms_and_conditions()
    rag_model.create_index(texts)
    faiss.write_index(rag_model.index, VECTOR_DB_PATH)

    # text_chunks도 함께 저장
    with open(VECTOR_DB_PATH + "_chunks.json", "w") as f:
        json.dump(rag_model.text_chunks, f)

    print(f"Vector database initialized and saved to {VECTOR_DB_PATH}")
