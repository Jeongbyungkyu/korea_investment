import numpy as np
import pandas as pd
from typing import List, Dict, Optional

class StockAnalyzer:
    def __init__(self):
        self.MA_PERIODS = [5, 20, 60, 120]  # 이동평균선 기간
        self.VOLUME_WINDOW = 20  # 거래량 분석 기간
        
    def analyze_trend(self, prices: pd.Series, volumes: pd.Series) -> Dict:
        """상승/하락 추세 분석"""
        ma_data = {}
        for period in self.MA_PERIODS:
            ma_data[f'MA{period}'] = prices.rolling(window=period).mean()
        
        # 추세 판단 (단기/중기/장기)
        trend_scores = {
            'short_trend': 0,  # 5일선 vs 20일선
            'mid_trend': 0,    # 20일선 vs 60일선
            'long_trend': 0    # 60일선 vs 120일선
        }
        
        # 단기 추세
        if ma_data['MA5'][-1] > ma_data['MA20'][-1]:
            trend_scores['short_trend'] = 1
            
        # 중기 추세
        if ma_data['MA20'][-1] > ma_data['MA60'][-1]:
            trend_scores['mid_trend'] = 1
            
        # 장기 추세
        if ma_data['MA60'][-1] > ma_data['MA120'][-1]:
            trend_scores['long_trend'] = 1
            
        return trend_scores
    
    def analyze_volume_trend(self, volumes: pd.Series) -> float:
        """거래량 추세 분석"""
        avg_volume = volumes.rolling(window=self.VOLUME_WINDOW).mean()
        recent_volume = volumes[-1]
        
        volume_ratio = recent_volume / avg_volume[-1] if not avg_volume.empty else 0
        return volume_ratio
    
    def analyze_foreign_institutional(self, foreign_data: pd.Series, inst_data: pd.Series) -> Dict:
        """외국인/기관 수급 분석"""
        WINDOW = 20  # 20일 기준
        
        foreign_sum = foreign_data.rolling(window=WINDOW).sum()
        inst_sum = inst_data.rolling(window=WINDOW).sum()
        
        return {
            'foreign_score': 1 if foreign_sum[-1] > 0 else 0,
            'inst_score': 1 if inst_sum[-1] > 0 else 0
        }
    
    def analyze_box_breakout(self, prices: pd.Series, volumes: pd.Series) -> Dict:
        """박스권 돌파 분석"""
        WINDOW = 20
        
        upper = prices.rolling(window=WINDOW).max()
        lower = prices.rolling(window=WINDOW).min()
        
        # 박스권 돌파 여부
        current_price = prices[-1]
        prev_upper = upper[-2]  # 직전 고점
        
        volume_avg = volumes.rolling(window=WINDOW).mean()
        current_volume = volumes[-1]
        
        breakout = {
            'is_breakout': current_price > prev_upper,
            'volume_confirm': current_volume > volume_avg[-1] * 1.5  # 거래량 1.5배 이상
        }
        
        return breakout
    
    def analyze_candle_pattern(self, opens: pd.Series, highs: pd.Series, 
                             lows: pd.Series, closes: pd.Series) -> Dict:
        """캔들 패턴 분석 (양봉 판단 등)"""
        current_open = opens[-1]
        current_close = closes[-1]
        current_high = highs[-1]
        current_low = lows[-1]
        
        body_size = abs(current_close - current_open)
        upper_shadow = current_high - max(current_open, current_close)
        lower_shadow = min(current_open, current_close) - current_low
        
        return {
            'is_bullish': current_close > current_open,
            'body_strength': body_size / (current_high - current_low),
            'shadow_ratio': (upper_shadow + lower_shadow) / body_size if body_size > 0 else 0
        }

    def calculate_elasticity(self, stock_returns: pd.Series, market_returns: pd.Series) -> float:
        """시장 대비 탄력성 계산"""
        WINDOW = 60  # 60일 기준
        
        # 베타 계산
        cov = stock_returns.rolling(window=WINDOW).cov(market_returns)
        market_var = market_returns.rolling(window=WINDOW).var()
        
        beta = cov / market_var
        return beta[-1]
    
    def get_stock_score(self, stock_data: Dict) -> float:
        """종합 점수 계산"""
        scores = []
        
        # 1. 추세 분석 (30%)
        trend_scores = self.analyze_trend(stock_data['prices'], stock_data['volumes'])
        trend_total = (trend_scores['short_trend'] * 0.4 + 
                      trend_scores['mid_trend'] * 0.3 + 
                      trend_scores['long_trend'] * 0.3)
        scores.append(trend_total * 0.3)
        
        # 2. 거래량 분석 (20%)
        volume_score = min(self.analyze_volume_trend(stock_data['volumes']), 2) / 2
        scores.append(volume_score * 0.2)
        
        # 3. 외국인/기관 수급 (20%)
        fi_scores = self.analyze_foreign_institutional(
            stock_data['foreign_trading'], 
            stock_data['institutional_trading']
        )
        fi_total = (fi_scores['foreign_score'] + fi_scores['inst_score']) / 2
        scores.append(fi_total * 0.2)
        
        # 4. 박스권 돌파 (15%)
        breakout = self.analyze_box_breakout(stock_data['prices'], stock_data['volumes'])
        breakout_score = (1 if breakout['is_breakout'] else 0) * \
                        (1 if breakout['volume_confirm'] else 0.5)
        scores.append(breakout_score * 0.15)
        
        # 5. 캔들패턴 (15%)
        candle = self.analyze_candle_pattern(
            stock_data['opens'],
            stock_data['highs'],
            stock_data['lows'],
            stock_data['closes']
        )
        candle_score = (1 if candle['is_bullish'] else 0) * \
                      min(candle['body_strength'] * 2, 1)
        scores.append(candle_score * 0.15)
        
        return sum(scores)