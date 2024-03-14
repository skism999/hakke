import streamlit as st
import json

def render_nakkohyo(nakkohyo, selected_ids):
    for item in nakkohyo:
        if item['id'] in selected_ids:
            st.write(item)

def main():
    st.title("納甲データ表示")

    # ドロップダウンでの選択肢
    choices = ['陽', '陰']

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
        # 陰陽を数値に変換（陽: 1, 陰: 0）
        yin_yang_values = [1 if value == '陽' else 0 for value in selections.values()]

        # JSONファイルを読み込み
        with open('/workspaces/unken/app/data/nakko/nakko_kajurin.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            nakkohyo = data["nakkohyo"]

        for item in nakkohyo:
            if "6th" not in item:
                print(f'Key "6th" not found in item with id {item["id"]}')

        # 条件に合致するIDを探索（"1st"から"6th"の順に値を比較）
        matched_ids = []
        for item in nakkohyo:

            # 各キーの存在を確認
            for key in ["6th", "5th", "4th", "3rd", "2nd", "1st"]:
                if key not in item:
                    st.error(f"{key} not found in item with id {item['id']}")
                    break
            else:  # すべてのキーが存在する場合、条件をチェック
                if (item["6th"]['nega_posi'] == yin_yang_values[5] and
                    item["5th"]['nega_posi'] == yin_yang_values[4] and
                    item["4th"]['nega_posi'] == yin_yang_values[3] and
                    item["3rd"]['nega_posi'] == yin_yang_values[2] and
                    item["2nd"]['nega_posi'] == yin_yang_values[1] and
                    item["1st"]['nega_posi'] == yin_yang_values[0]):
                    matched_ids.append(item['id'])

        # 該当するデータを表示
        render_nakkohyo(nakkohyo, matched_ids)

if __name__ == '__main__':
    main()