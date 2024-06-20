import json
from datetime import date, timedelta

def create_calendar_json(json_file_path):
    # 十干と十二支
    jukkan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    junishi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    # 開始年と終了年
    start_year = 2024
    end_year = 2030

    calendar = []

    for year in range(start_year, end_year + 1):
        year_day_count = 0  # 年初からの経過日数
        for month in range(1, 13):
            days_in_month = (date(year if month < 12 else year + 1, month % 12 + 1, 1) - timedelta(days=1)).day
            for day in range(1, days_in_month + 1):
                # 月の十干と十二支の計算を、年初からの経過月数を基に行います
                elapsed_months_jukkan = (month - 10) + (year - start_year) * 12
                elapsed_months_junishi = (month - 12) + (year - start_year) * 12
                # 日の十干と十二支の計算も、年初からの経過日数を基に行います
                calendar.append({
                    "year": {
                        "value": year,
                        "jukkan": jukkan[(year - 4) % 10],
                        "junishi": junishi[(year - 4) % 12]
                    },
                    "month": {
                        "value": month,
                        "jukkan": jukkan[elapsed_months_jukkan % 10],
                        "junishi": junishi[elapsed_months_junishi % 12]
                    },
                    "day": {
                        "value": day,
                        "jukkan": jukkan[year_day_count % 10],
                        "junishi": junishi[year_day_count % 12]
                    }
                })
                year_day_count += 1  # 経過日数をインクリメント

    final_data = {
        "user": "admin",
        "koyomi": calendar
    }

    # JSONファイルに書き込み
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(final_data, json_file, ensure_ascii=False, indent=4)

# JSONファイルのパス
json_file_path = '/workspaces/hakke/sample/daneki/app/data/koyomi/koyomi_daneki.json'
create_calendar_json(json_file_path)
