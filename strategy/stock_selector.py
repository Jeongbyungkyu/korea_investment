import pandas as pd
from typing import List, Dict
from analysis.technical import StockAnalyzer

class TopStockSelector:
    def __init__(self):
        self.analyzer = StockAnalyzer()
        
    async def get_top_stocks(self, stock_data_dict: Dict[str, Dict]) -> List[str]:
        """상위 종목 선정"""
        stock_scores = {}
        
        for code, data in stock_data_dict.items():
            try:
                score = self.analyzer.get_stock_score(data)
                stock_scores[code] = score
            except Exception as e:
                print(f"Error analyzing stock {code}: {e}")
                continue
        
        # 점수 기준 상위 10개 종목 선정
        top_stocks = sorted(stock_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return [code for code, score in top_stocks]
    
    def print_analysis(self, stock_code: str, stock_data: Dict):
        """종목 분석 결과 출력"""
        try:
            trend_scores = self.analyzer.analyze_trend(stock_data['prices'], stock_data['volumes'])
            volume_trend = self.analyzer.analyze_volume_trend(stock_data['volumes'])
            fi_scores = self.analyzer.analyze_foreign_institutional(
                stock_data['foreign_trading'],
                stock_data['institutional_trading']
            )
            breakout = self.analyzer.analyze_box_breakout(stock_data['prices'], stock_data['volumes'])
            candle = self.analyzer.analyze_candle_pattern(
                stock_data['opens'],
                stock_data['highs'],
                stock_data['lows'],
                stock_data['closes']
            )
            
            print(f"\n=== {stock_code} 분석 결과 ===")
            print(f"추세 점수: {trend_scores}")
            print(f"거래량 증가율: {volume_trend:.2f}")
            print(f"외국인/기관 수급: {fi_scores}")
            print(f"박스권 돌파: {breakout}")
            print(f"캔들 패턴: {candle}")
            print("=" * 30)
            
        except Exception as e:
            print(f"Error printing analysis for {stock_code}: {e}")