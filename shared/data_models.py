# -*- coding: utf-8 -*-
"""
共通データモデル

車検証や印鑑証明から読み取ったデータを保持する共通フォーマット。
普通車・軽自動車どちらのフォームにも流し込める。
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import date


@dataclass
class VehicleData:
    """車両情報（車検証から読み取る項目）"""
    
    # 登録番号・車両番号
    office: str = ""           # 運輸支局等（例: 尾張小牧、一宮）
    class_number: str = ""     # 分類番号（例: 330、580）
    kana: str = ""             # かな（例: さ、と）
    serial_number: str = ""    # 一連番号（例: 1234、6528）
    
    # 車両詳細
    chassis_number: str = ""   # 車台番号
    model_code: str = ""       # 型式
    maker: str = ""            # 車名（メーカー）
    body_type: str = ""        # 車体の形状
    
    # 諸元
    category: str = ""         # 種別（普通=3, 軽=4）
    usage: str = ""            # 用途（乗用=01, 貨物=02）
    private: str = ""          # 自家用/事業用（家庭用=2, 営業用=1）
    capacity: str = ""         # 乗車定員
    weight: str = ""           # 車両重量
    total_weight: str = ""     # 車両総重量
    length: str = ""           # 長さ
    width: str = ""            # 幅
    height: str = ""           # 高さ
    displacement: str = ""     # 総排気量
    fuel_type: str = ""        # 燃料の種類（ガソリン=1, 軽油=2）
    
    # 型式指定・類別
    model_designation: str = ""    # 型式指定番号
    category_code: str = ""        # 類別区分番号
    engine_model: str = ""         # 原動機型式
    
    # 初度登録
    first_registration_era: str = ""   # 年号（令和=5, 平成=4）
    first_registration_year: str = ""  # 年
    first_registration_month: str = "" # 月


@dataclass
class OwnerData:
    """所有者・使用者情報"""
    
    # 納税義務者 / 新所有者
    name: str = ""
    zip_code: str = ""         # 郵便番号（ハイフン付き可）
    address: str = ""
    phone: str = ""            # 電話番号
    
    # フラグ
    is_owner_same: bool = False    # 所有者同上
    is_user_same: bool = False     # 使用者同上
    ownership_type: str = "1"      # 所有形態（自己所有=1, リース=2）
    
    @property
    def zip_upper(self) -> str:
        """郵便番号上3桁"""
        clean = self.zip_code.replace("-", "")
        return clean[:3] if len(clean) >= 3 else clean
    
    @property
    def zip_lower(self) -> str:
        """郵便番号下4桁"""
        clean = self.zip_code.replace("-", "")
        return clean[3:7] if len(clean) >= 4 else ""
    
    @property
    def phone_clean(self) -> str:
        """ハイフンなし電話番号"""
        return self.phone.replace("-", "")


@dataclass
class FormerOwnerData:
    """旧所有者・旧使用者情報"""
    
    former_owner_name: str = ""
    former_owner_address: str = ""
    former_user_name: str = ""
    former_user_address: str = ""


@dataclass 
class ApplicantData:
    """申告者・代理人情報"""
    
    name: str = ""
    address: str = ""
    phone_area: str = ""       # 市外局番
    phone_local: str = ""      # 局番
    phone_number: str = ""     # 番号


@dataclass
class FormData:
    """
    申請書フォーム全体のデータ
    
    車検証OCR → このクラスにデータを格納 → 各フォームに流し込み
    """
    
    vehicle: VehicleData = field(default_factory=VehicleData)
    owner: OwnerData = field(default_factory=OwnerData)
    former: FormerOwnerData = field(default_factory=FormerOwnerData)
    applicant: ApplicantData = field(default_factory=ApplicantData)
    
    # メタデータ
    form_type: str = ""        # "普通乗用車" or "軽自動車"
    created_at: Optional[date] = None
