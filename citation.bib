import numpy as np
import pandas as pd
import pytest
from sp500_research.features import build_supervised_frame, model_features
from sp500_research.evaluation import chronological_split, regression_metrics, train_and_compare
from sp500_research.strategies import illustrative_sma_strategy
from sp500_research.market import clean_ohlcv


def prices(n=510):
    times=pd.bdate_range("2020-01-01",periods=n)
    close=100+np.arange(n)*0.12+2*np.sin(np.arange(n)/15)
    return pd.DataFrame({"Open":close-0.4,"High":close+1.1,
      "Low":close-1.2,"Close":close,"Volume":np.full(n,150000)},index=times)


def test_target_is_one_day_ahead_and_lags_are_past_values():
    p=prices(); f=build_supervised_frame(p)
    day=f.index[10]; loc=p.index.get_loc(day)
    assert f.loc[day,"target_next_close"]==pytest.approx(p.iloc[loc+1]["Close"])
    assert f.loc[day,"lag_7"]==pytest.approx(p.iloc[loc-7]["Close"])
    assert f.loc[day,"target_date"]==p.index[loc+1]
    assert "target_next_close" not in model_features(f)
    assert "target_date" not in model_features(f)


def test_split_keeps_target_dates_strictly_ordered():
    f=build_supervised_frame(prices())
    t=chronological_split(f)
    assert t.train.target_date.max()<t.valid.target_date.min()
    assert t.valid.target_date.max()<t.test.target_date.min()
    assert len(t.train)+len(t.valid)+len(t.test)==len(f)


def test_model_evaluation_runs_offline():
    t=chronological_split(build_supervised_frame(prices()))
    result,best,_=train_and_compare(t)
    assert set(result.split)=={"valid","test"}
    assert "Naive last close" in set(result.model)
    assert (result.MAE>=0).all()
    assert isinstance(best,str)


def test_sma_uses_prior_signal_and_includes_turnover_cost():
    p=prices(350)
    st=illustrative_sma_strategy(p.Close,short=10,long=50,cost_per_turnover=.001)
    assert st.iloc[0].next_bar_exposure==0
    assert np.allclose(st.next_bar_exposure.iloc[1:].to_numpy(), st.signal_after_close.iloc[:-1].to_numpy())
    assert st.iloc[-1].sma_cumulative>0


def test_no_volume_yields_no_obv():
    p=prices().drop(columns="Volume"); c=clean_ohlcv(p)
    assert "obv" not in build_supervised_frame(c).columns
