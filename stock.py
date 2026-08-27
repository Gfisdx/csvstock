from pathlib import Path
import pandas as pd
import csv


PATH_SOURCE = Path(__file__).parent
PATH_TRANS = PATH_SOURCE / 'invent_trans'
PATH_STOCK = PATH_SOURCE / 'stock'
SEPARATOR = ';'


def main() -> None:

    
    dfStock = pd.read_csv(PATH_STOCK / 'stock_2025_04_30.csv',
    sep=SEPARATOR)

    for csvPath in PATH_TRANS.glob('*.csv'):
        
        dfTrans = pd.read_csv(csvPath, parse_dates=['trans_date'],sep=SEPARATOR)

        for date, group in dfTrans.groupby('trans_date'):

            date_str = date.strftime('%Y-%m-%d')

            changes = (
                group
                .groupby('item_id')[['qty', 'cost_amount']]
                .sum()
            )

            dfStock['qty'] += (
                dfStock['item_id']
                .map(changes['qty'])
                .fillna(0)
            )

            dfStock['cost_amount'] += (
                dfStock['item_id']
                .map(changes['cost_amount'])
                .fillna(0)
            )

            dfStock['trans_date'] = date

            dfStock.to_csv(
                PATH_STOCK / f'stock_{date_str}.csv',
                sep=';',
                index=False,
                quoting=csv.QUOTE_ALL
            )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print('Oops... Something wrong!')
