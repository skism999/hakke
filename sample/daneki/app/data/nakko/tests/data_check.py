import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pytest

expected_gorui = ["父母", "兄弟", "官⿁", "妻財", "子孫"]
expected_junishi = ["子水", "丑土", "寅木", "卯木", "辰土", "巳火", "午火", "未土", "申金", "酉金", "戌土", "亥水"]
expected_seko_oko = ["世", "応", None]

# データファイルを読み込みます。
@pytest.fixture
def nakkohyo_data():
    file_path = '/workspaces/hakke/sample/daneki/app/data/nakko/nakko_kajurin.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["nakkohyo"]

# 各セクションが正確に必要なキーを持っているか確認するテスト
@pytest.mark.parametrize("section", ["6th", "5th", "4th", "3rd", "2nd", "1st"])
def test_section_keys(nakkohyo_data, section):
    for index, item in enumerate(nakkohyo_data, start=1):
        data = item.get(section, {})
        assert set(data.keys()) >= {"nega_posi", "gorui", "junishi", "seko_oko", "fukushin"}, f'Error in item {index} section {section}: Missing keys'
        fukushin = data.get("fukushin", {})
        assert set(fukushin.keys()) >= {"gorui_fukushin", "junishi_fukushin"}, f'Error in item {index} section {section}: Missing fukushin keys'


# nega_posi が 0 または 1 であることを確認するテスト
@pytest.mark.parametrize("section", ["6th", "5th", "4th", "3rd", "2nd", "1st"])
def test_nega_posi(nakkohyo_data, section):
    for index, item in enumerate(nakkohyo_data, start=1):
        data = item.get(section, {})
        nega_posi = data.get("nega_posi")
        assert nega_posi in [0, 1], f'Error in item {index} section {section}: Invalid nega_posi {nega_posi}'

# gorui が期待される値の一つであることを確認するテスト
@pytest.mark.parametrize("section", ["6th", "5th", "4th", "3rd", "2nd", "1st"])
def test_gorui(nakkohyo_data, section):
    for index, item in enumerate(nakkohyo_data, start=1):
        data = item.get(section, {})
        gorui = data.get("gorui")
        assert gorui in expected_gorui, f'Error in item {index} section {section}: Invalid gorui {gorui}'

# junishi が期待される値の一つであることを確認するテスト
@pytest.mark.parametrize("section", ["6th", "5th", "4th", "3rd", "2nd", "1st"])
def test_junishi(nakkohyo_data, section):
    for index, item in enumerate(nakkohyo_data, start=1):
        data = item.get(section, {})
        junishi = data.get("junishi")
        assert junishi in expected_junishi, f'Error in item {index} section {section}: Invalid junishi {junishi}'

# seko_oko が期待される値の一つまたはNoneであることを確認するテスト
@pytest.mark.parametrize("section", ["6th", "5th", "4th", "3rd", "2nd", "1st"])
def test_seko_oko(nakkohyo_data, section):
    for index, item in enumerate(nakkohyo_data, start=1):
        data = item.get(section, {})
        seko_oko = data.get("seko_oko")
        assert seko_oko in expected_seko_oko, f'Error in item {index} section {section}: Invalid seko_oko {seko_oko}'

# fukushin の gorui_fukushin が期待される値の一つまたはNoneであることを確認するテスト
@pytest.mark.parametrize("section", ["6th", "5th", "4th", "3rd", "2nd", "1st"])
def test_fukushin_gorui_fukushin(nakkohyo_data, section):
    for index, item in enumerate(nakkohyo_data, start=1):
        fukushin = item.get(section, {}).get("fukushin", {})
        gorui_fukushin = fukushin.get("gorui_fukushin")
        assert gorui_fukushin in expected_gorui or gorui_fukushin is None, f'Error in item {index} section {section}: Invalid fukushin_gorui_fukushin {gorui_fukushin}'

# fukushin の junishi_fukushin が期待される値の一つまたはNoneであることを確認するテスト
@pytest.mark.parametrize("section", ["6th", "5th", "4th", "3rd", "2nd", "1st"])
def test_fukushin_junishi_fukushin(nakkohyo_data, section):
    for index, item in enumerate(nakkohyo_data, start=1):
        fukushin = item.get(section, {}).get("fukushin", {})
        junishi_fukushin = fukushin.get("junishi_fukushin")
        assert junishi_fukushin in expected_junishi or junishi_fukushin is None, f'Error in item {index} section {section}: Invalid fukushin_junishi_fukushin {junishi_fukushin}'

print("チェック完了")