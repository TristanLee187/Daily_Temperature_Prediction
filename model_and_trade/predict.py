import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from datetime import date, timedelta

def predict():
    ret = {}
    for loc in ['austin', 'chicago', 'miami', 'ny']:
        # load the model
        model = load_model(f'{loc}_model.keras')

        data = pd.read_csv(f'../data/{loc}/{loc}_all_data.csv')

        # keep just the most recent 30 to use as input
        latest_data = data.tail(30)

        # normalize
        scaler = np.load(f'{loc}_scaler.npy', allow_pickle=True).item()
        input_data_scaled = scaler.fit_transform(latest_data.drop(columns=['date']))
        input_data_reshaped = np.reshape(input_data_scaled, (1, 30, 5))

        # predict!
        predictions_scaled = model.predict(input_data_reshaped)
        predictions = scaler.inverse_transform(predictions_scaled)

        ret[loc] = predictions[0][0]

        # print(loc, (date.fromisoformat(list(latest_data['date'])[-1]) + timedelta(days=1)))
        # prediction_df = pd.DataFrame(columns = ['tmax', 'prec', 'pres', 'cloud', 'rhum'])
        # prediction_df.loc[0] = predictions[0]
        # print(prediction_df)
    return ret

if __name__ == '__main__':
    print(predict())