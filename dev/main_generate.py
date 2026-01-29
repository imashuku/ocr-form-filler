from pdf_utils import embed_text_to_pdf
from ocr_fields import get_vehicle_registration_data, get_chassis_data, get_owner_code_data, get_model_data, get_class_data, get_owner_name_data, get_owner_address_data, get_user_name_data, get_user_address_data, get_section_data, get_single_char_data

def main():
    input_pdf = "OCR_第１号様式_記入済み.pdf"
    output_pdf = "OCR_Final_Product.pdf"
    
    # 1. 自動車登録番号
    reg_fields = get_vehicle_registration_data("尾張小牧", "330", "さ", "1234")
    
    # 2. 車台番号
    chassis_fields = get_chassis_data("2H81846")

    # 3. 所有者コード 
    owner_fields = get_owner_code_data("47774")

    # 4. 型式指定・類別区分
    model_fields = get_model_data("18923")
    class_fields = get_class_data("0001")

    # 5. 新所有者 氏名
    owner_name_fields = get_owner_name_data("株式会社アットカーズ\n代表取締役　上田和治")

    # 6. 新所有者 住所
    owner_address_fields = get_owner_address_data("滋賀県守山市赤野井町761-2")

    # 7. 使用者 氏名 (新所有者と同じ)
    user_name_fields = get_user_name_data("株式会社アットカーズ\n代表取締役　上田和治")

    # 8. 使用者 住所 (新所有者と同じ)
    user_address_fields = get_user_address_data("滋賀県守山市赤野井町761-2")

    # 9. 旧所有者
    old_owner_fields = get_section_data(
        "株式会社旧オーナー代表取締役 旧田太郎", # 1行テスト
        "旧県旧市旧町1-1",
        "old_owner_name", "old_owner_address"
    )

    # 10. 申請代理人
    agent_fields = get_section_data(
        "日本自動車販売協会連合会滋賀県支部長", # 1行テスト
        "滋賀県守山市木浜町2298-4",
        "agent_name", "agent_address"
    )

    # 11. 受検者
    examinee_fields = get_section_data(
        "受検 太郎", 
        "受検県受検市受検町3-3",
        "examinee_name", "examinee_address"
    )

    # 12. フラグ (Flags)
    # 所有権解除 "1"
    flag_release = get_single_char_data("1", "owner_ownership_release_flag")
    
    # 使用者 氏名 同上 "1"
    flag_user_name = get_single_char_data("1", "user_name_same_flag")
    
    # 使用者 住所 同上 "1"
    flag_user_address = get_single_char_data("1", "user_address_same_flag")
    
    # 使用の本拠 同上 "1"
    flag_principal_place = get_single_char_data("1", "principal_place_same_flag")
    
    # 全データを結合
    all_fields = (reg_fields + chassis_fields + owner_fields + model_fields + class_fields + 
                 owner_name_fields + owner_address_fields + user_name_fields + user_address_fields +
                 old_owner_fields + agent_fields + examinee_fields +
                 flag_release + flag_user_name + flag_user_address + flag_principal_place)
    
    print("Generating PDF...")
    # 用紙サイズ (595, 836) は必須
    embed_text_to_pdf(input_pdf, output_pdf, all_fields, pagesize=(595, 836))
    print(f"Done: {output_pdf}")

if __name__ == "__main__":
    main()
