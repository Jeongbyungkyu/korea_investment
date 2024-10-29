from datetime import datetime, timedelta
import pandas as pd
import requests
from kis_client import KISClient


class StockDailyData:
    def __init__(self):
        self.client = KISClient()
        self.base_url = self.client.base_url
        self.headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.client.get_access_token()}",
            "appkey": self.client.app_key,
            "appsecret": self.client.app_secret,
            "tr_id": "FHKST03010100",
        }

    def _get_daily_chunk(self, stock_code, start_date, end_date):
        """특정 기간의 일봉 데이터 조회"""
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": stock_code,
            "FID_INPUT_DATE_1": start_date.strftime("%Y%m%d"),
            "FID_INPUT_DATE_2": end_date.strftime("%Y%m%d"),
            "FID_PERIOD_DIV_CODE": "D",
            "FID_ORG_ADJ_PRC": "1",
        }

        try:
            print(
                f"데이터 요청: {start_date.strftime('%Y%m%d')} ~ {end_date.strftime('%Y%m%d')}"
            )
            response = requests.get(
                f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice",
                headers=self.headers,
                params=params,
            )
            data = response.json()

            if data.get("rt_cd") == "0":
                daily_data = []
                for item in data.get("output2", []):
                    daily_data.append(
                        {
                            "date": item.get("stck_bsop_date"),
                            "close": float(item.get("stck_clpr", 0)),
                            "open": float(item.get("stck_oprc", 0)),
                            "high": float(item.get("stck_hgpr", 0)),
                            "low": float(item.get("stck_lwpr", 0)),
                            "volume": float(item.get("acml_vol", 0)),
                            "amount": float(item.get("acml_tr_pbmn", 0)),
                        }
                    )
                return daily_data, data.get("output1", {}).get("hts_kor_isnm", "")
            else:
                print(f"API 오류 응답: {data}")
                return None, None
        except Exception as e:
            print(f"데이터 조회 중 예외 발생: {str(e)}")
            return None, None

    def get_daily_stock_data(self, stock_code, required_days=120):
        """여러 번의 호출로 필요한 기간의 데이터 수집"""
        print(f"\n{stock_code} 종목의 일봉 데이터를 조회합니다...")

        all_data = []
        stock_name = ""
        end_date = datetime.now()

        # 100일씩 끊어서 데이터 조회
        while len(all_data) < required_days:
            start_date = end_date - timedelta(days=100)

            # API 호출 전 대기
            print("API 호출 대기 중...")
            import time

            time.sleep(1.0)  # 1초로 증가

            chunk_data, name = self._get_daily_chunk(stock_code, start_date, end_date)

            if chunk_data is None:
                print(f"{stock_code} 데이터 조회 실패")
                return None

            if not stock_name and name:
                stock_name = name

            all_data.extend(chunk_data)
            print(f"현재까지 수집된 데이터: {len(all_data)}일")

            if len(chunk_data) == 0:  # 더 이상 데이터가 없음
                break

            end_date = start_date - timedelta(days=1)

        print(f"\n종목명: {stock_name}")
        print(f"최종 수집된 데이터 수: {len(all_data)}일")

        if len(all_data) < required_days:
            print(
                f"충분한 데이터를 가져오지 못했습니다. (필요: {required_days}일, 수집: {len(all_data)}일)"
            )
            return None

        # DataFrame 생성 및 기술적 지표 계산
        df = pd.DataFrame(all_data)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        # 120일 이동평균선
        df["MA120"] = df["close"].rolling(window=120).mean()
        df["MA120_slope"] = df["MA120"].diff(5) / 5
        df["volume_ratio"] = df["volume"] / df["volume"].rolling(window=20).mean()

        return df

    def analyze_stock(self, stock_code):
        """종목 분석"""
        df = self.get_daily_stock_data(stock_code)
        if df is None:
            return None

        latest = df.iloc[-1]

        analysis = {
            "code": stock_code,
            "price": latest["close"],
            "above_ma120": latest["close"] > latest["MA120"],
            "ma120_trend": latest["MA120_slope"] > 0,
            "volume_increase": latest["volume_ratio"] > 2.0,
            "recent_high": df["high"].tail(20).max(),
            "recent_low": df["low"].tail(20).min(),
        }

        analysis["suitable"] = (
            analysis["above_ma120"]
            and analysis["ma120_trend"]
            and analysis["volume_increase"]
        )

        return analysis


def main():
    print("주식 데이터 분석을 시작합니다...")
    analyzer = StockDailyData()

    test_stocks = [
        ("005930", "삼성전자"),
        ("000660", "SK하이닉스"),
        ("035720", "카카오"),
    ]

    print("\n=== 종목 분석 시작 ===")
    for code, name in test_stocks:
        print(f"\n{name}({code}) 분석 중...")
        result = analyzer.analyze_stock(code)

        if result:
            print(f"\n[{name}({code}) 분석 결과]")
            print(f"현재가: {result['price']:,}원")
            print(f"120일선 위: {'예' if result['above_ma120'] else '아니오'}")
            print(f"상승추세: {'예' if result['ma120_trend'] else '아니오'}")
            print(f"거래량 증가: {'예' if result['volume_increase'] else '아니오'}")
            print(f"매매적합: {'예' if result['suitable'] else '아니오'}")
            print(f"최근 고가: {result['recent_high']:,}원")
            print(f"최근 저가: {result['recent_low']:,}원")


if __name__ == "__main__":
    main()
