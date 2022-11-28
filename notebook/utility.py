from pathlib import Path
from typing import Optional, List
import pandas as pd
from who_member_states import WHO_MEMBER_STATES

__all__=['select_df']
def select_df(df: pd.DataFrame,
              column_drop:Optional[List[str]] = None,
              year: int=2000,
              save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    define a function named select_df
    預設沒有要drop掉column, 所以=None
    因為Our World in Data collected since 2000, so year must greater than 2000
    """
    df = df.copy()
    """
    The copy() method returns a copy of the DataFrame.
    By default, the copy is a "deep copy" meaning that any changes 
    made in the original DataFrame will NOT be reflected in the copy.
    新跑出來的df不會影響最原始的df
    """
    if column_drop is not None:
        df = df.drop(columns=column_drop)
    """
    if we want to drop specific column,
    df need to drop the option
    """


    year_mask: pd.Series[bool] = df['Year'] > year
    # type is list of bool; 比較df["year"]有沒有> default 的year
    entity_mask:List[bool]= [country in WHO_MEMBER_STATES for country in df['Entity']]
    # 在df裡Entity 裡的country有沒有也在who member states 裡，有的就True.
    _df: pd.DataFrame = df[year_mask & entity_mask].reset_index(drop=True)
    # 使用新的索引 df.reset_index; 把drop掉的也不要加進去新df裡(drop=True), ret=return

    if drop_na is not None:
        try:
            _df.dropna(subset=drop_na, inplace=True)
    # inplace = True, 是在執行完 _df.dropna()之後，會返回到 _dr.dropna 裡; 如果是inplace = false, 執行完_df.dropna 後
    # df 還是原本的樣子. subset = dop_na 是指定在要drop掉的位置上
        except KeyError as e:
            raise ValueError(f'{e} not in the dataframe, should be one of the {_df.columns.tolist()}')
    # 如果輸入錯誤，就把其實沒有NA 的地方抓出並列表 f'' f-string 不用一直打 '''' 

    if save_path is not None:
        _df.to_csv(save_path)

    return _df