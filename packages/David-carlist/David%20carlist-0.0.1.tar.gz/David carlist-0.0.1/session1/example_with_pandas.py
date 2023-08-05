import pandas as pd


def average_price_in(df, neighbourhood):
    df_private_rooms_in_brooklyn = df.loc[
        (df['neighbourhood_group'] == neighbourhood) & (df['room_type'] == 'Private room')]
    avg_price = df_private_rooms_in_brooklyn['price'].mean()
    return avg_price


if __name__ == "__main__":
    df = pd.read_csv('AB_NYC_2019.csv')
    print(df['room_type'].head())
    print(df.columns)

    print(f' The avg price is ${average_price_in(df,"Brooklyn")}')
