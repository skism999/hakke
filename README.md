# HAKKE 占術アプリケーション

## 概要
HAKKE占術アプリケーションは、旧暦を元に複数の東洋占術（奇門遁甲、断易など）を利用することができるWebアプリケーションです。FastAPIを使用して、ユーザーからの入力を基に占術結果を表示するAPIを提供します。

## ディレクトリ構造

```text
hakke_senjutsu/
├── app/
│ ├── init.py
│ ├── main.py
│ ├── api/
│ │ ├── init.py
│ │ ├── divinations/
│ │ │ ├── init.py
│ │ │ ├── kimontonko.py
│ │ │ └── daneki.py
│ │ └── calendar/
│ │ ├── init.py
│ │ └── eto_calendar.py
│ ├── core/
│ │ ├── init.py
│ │ └── config.py
│ ├── routers/
│ │ ├── init.py
│ │ └── schemas.py
│ │ └── view.py
│ ├── services/
│ ├── init.py
│ ├── eto_service.py
│ ├── kimon_service.py
│ └── daneki_service.py
├── tests/
│ ├── init.py
│ ├── test_kimontonko.py
│ └── test_daneki.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```


## 各ファイルの処理内容

### `app/__init__.py`
パッケージとして認識させるためのファイル。

### `app/main.py`
FastAPIアプリケーションのエントリーポイント。各APIルータをインクルードし、アプリケーションを起動する設定。

例：
```python
from fastapi import FastAPI
from app.api.divinations import kimontonko, daneki
from app.api.calendar import eto_calendar

app = FastAPI()

app.include_router(kimontonko.router, prefix="/api/kimontonko")
app.include_router(daneki.router, prefix="/api/daneki")
app.include_router(eto_calendar.router, prefix="/api/eto_calendar")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Divination API"}
```

### `app/api/__init__.py`
APIモジュールの初期化。

### `app/api/divinations/__init__.py`
占術APIのモジュール初期化。

### `app/api/divinations/kimontonko.py`
奇門遁甲のAPIエンドポイント。ユーザーからの日付入力を受け取り、干支暦に変換し、盤を作成する処理。

例：
```python
from fastapi import APIRouter
from app.services.kimon_service import create_kimon_chart

router = APIRouter()

@router.post("/generate")
def generate_kimon_chart(date: str):
    return create_kimon_chart(date)
```

### `app/api/divinations/daneki.py`
断易のAPIエンドポイント。ユーザーからの入力データを受け取り、干支暦を計算し、六爻を生成する処理。

例：
```python
from fastapi import APIRouter
from app.services.daneki_service import generate_daneki_chart

router = APIRouter()

@router.post("/generate")
def generate_daneki_chart(data: dict):
    return generate_daneki_chart(data)
```

### `app/api/calendar/__init__.py`
暦APIのモジュール初期化。

### `app/api/calendar/eto_calendar.py`
旧暦の計算を行うAPIエンドポイント。日付を干支暦に変換する処理。

例：
```python
from fastapi import APIRouter
from app.services.eto_service import convert_to_eto_calendar

router = APIRouter()

@router.get("/convert")
def convert_date_to_eto(date: str):
    return convert_to_eto_calendar(date)
```

### `app/core/__init__.py`
コアモジュールの初期化。

### `app/core/config.py`
環境設定や設定値を管理。

例：
```python
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Divination API"
    environment: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
```

### `app/routers/__init__.py`
モデルモジュールの初期化。

### `app/models/schemas.py`
Pydanticを使用してデータスキーマを定義。

例：
```python
from pydantic import BaseModel

class DateInput(BaseModel):
    date: str

class KimonChart(BaseModel):
    year: str
    month: str
    day: str
    hour: str
    elements: dict

class DanekiChart(BaseModel):
    elements: list
    result: str
```

### `app/services/__init__.py`
サービスモジュールの初期化。

### `app/services/eto_service.py`
旧暦の計算を行うサービス。

例：
```python
jukkan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
junishi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

def convert_to_eto_calendar(date: str):
    # 日付を干支暦に変換するロジックを実装
    pass
```


### `app/services/kimon_service.py`
奇門遁甲の盤を作成するサービス。

例：
```python
def create_kimon_chart(date: str):
    # 日付を元に干支暦を計算し、盤を作成するロジックを実装
    pass
```

### `app/services/daneki_service.py`
断易の盤を作成するサービス。

例：
```python
def generate_daneki_chart(data: dict):
    # 入力データを元に干支暦を計算し、六爻を生成するロジックを実装
    pass
```
