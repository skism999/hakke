import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta, date

def render_nakkohyo(nakkohyo, result_placeholder, selected_ids, today_koyomi):
    with result_placeholder.container():
        for item in nakkohyo:
            if item['id'] in selected_ids:

                # ID、本卦、八宮をデータフレームに含める
                df_info = {
                    "情報": ["ID", "本卦", "八宮"],
                    "詳細": [str(item['id']), item['name_ke'], item['name_hachigu']]
                }
                st.table(df_info)

                today_info_df = pd.DataFrame({
                    "情報": ["年", "月", "日"],
                    "値": [str(today_koyomi['year']['value']), str(today_koyomi['month']['value']), str(today_koyomi['day']['value'])],
                    "十干": [today_koyomi['year']['jukkan'], today_koyomi['month']['jukkan'], today_koyomi['day']['jukkan']],
                    "十二支": [today_koyomi['year']['junishi'], today_koyomi['month']['junishi'], today_koyomi['day']['junishi']],
                })
                st.table(today_info_df.T)  # .T で転置

                # データフレームを用いてテーブル形式でデータを整形
                data = {
                    "爻": ["上爻", "五爻", "四爻", "三爻", "二爻", "初爻"],
                    "陰陽": [],
                    "五類": [],
                    "十二支": []
                }
                
                # 各爻についてデータを追加
                for k in ["6th", "5th", "4th", "3rd", "2nd", "1st"]:
                    k_data = item[k]
                    yin_yang_str = "ーーー" if k_data['nega_posi'] == 1 else "ー　ー"
                    # "seko_oko" の値が存在する場合は、陰陽の文字列に追加
                    if k_data.get('seko_oko'):
                        yin_yang_str += f" {k_data['seko_oko']}"
                    data["陰陽"].append(yin_yang_str)
                    data["五類"].append(k_data['gorui'])
                    data["十二支"].append(k_data['junishi'])
                
                df = pd.DataFrame(data)
                st.table(df)

def get_today_koyomi():
    # 今日の日付を取得
    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day

    # JSONファイルを読み込む
    with open('/workspaces/unken/app/data/koyomi/koyomi_daneki.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data["koyomi"]:
            if item["year"]["value"] == year and item["month"]["value"] == month and item["day"]["value"] == day:
                return item
    return None

def handle_nakkohyo_search(selections, result_placeholder):
    # 陰陽を数値に変換（陽: 1, 陰: 0）
    yin_yang_values = [1 if value == '陽' else 0 for value in selections.values()]

    # 今日の暦のデータを取得
    today_koyomi = get_today_koyomi()
    if today_koyomi is None:
        st.error("今日の暦のデータが見つかりません。")
        return

    # JSONファイルを読み込み
    with open('/workspaces/unken/app/data/nakko/nakko_kajurin.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        nakkohyo = data["nakkohyo"]

    # 条件に合致するIDを探索（"1st"から"6th"の順に値を比較）
    matched_ids = []
    for item in nakkohyo:

        # 各キーの存在を確認
        for key in ["6th", "5th", "4th", "3rd", "2nd", "1st"]:
            if key not in item:
                st.error(f"{key} not found in item with id {item['id']}")
                break
        else:  # すべてのキーが存在する場合、条件をチェック
            if (item["6th"]['nega_posi'] == yin_yang_values[0] and
                item["5th"]['nega_posi'] == yin_yang_values[1] and
                item["4th"]['nega_posi'] == yin_yang_values[2] and
                item["3rd"]['nega_posi'] == yin_yang_values[3] and
                item["2nd"]['nega_posi'] == yin_yang_values[4] and
                item["1st"]['nega_posi'] == yin_yang_values[5]):
                matched_ids.append(item['id'])
        
    if matched_ids:
        render_nakkohyo(nakkohyo, result_placeholder, matched_ids, today_koyomi)
    else:
        st.write("該当するデータがありません。")    


def main():
    st.title("納甲データ表示")

    # 結果表示用のプレースホルダー
    result_placeholder = st.empty()

    # ドロップダウンでの選択肢
    choices = ['陽', '陰']

    # 結果を表示するためのプレースホルダー
    result_placeholder = st.empty()

    # 各段の陰陽の選択肢を受け取る（"6th"から"1st"の順）
    selections = {
        "6th": st.selectbox('6th', choices, key=6),
        "5th": st.selectbox('5th', choices, key=5),
        "4th": st.selectbox('4th', choices, key=4),
        "3rd": st.selectbox('3rd', choices, key=3),
        "2nd": st.selectbox('2nd', choices, key=2),
        "1st": st.selectbox('1st', choices, key=1),
    }

    # "納甲"ボタンを作成
    if st.button('納甲'):
        handle_nakkohyo_search(selections, result_placeholder)


if __name__ == '__main__':
    main()