import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input
from keras.callbacks import EarlyStopping

for loc in ['austin', 'chicago', 'miami', 'ny']:
    data = pd.read_csv(f'../data/{loc}/{loc}_all_data.csv')

    # ensure the data only includes up to 3/4/2024, to make predictions for 3/5 and on
    data = data[data['date'] <= '2024-03-04']

    # normalize
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data[['tmax', 'prec', 'pres', 'cloud', 'rhum']])

    # the input to the LSTM will be a sequence of 30 days' conditions,
    # and the output will be the following day's conditions
    sequence_length = 30
    num_features = 5

    X, y = [], []
    for i in range(len(scaled_data) - sequence_length):
        X.append(scaled_data[i:i+sequence_length])
        y.append(scaled_data[i+sequence_length])

    X = np.array(X)
    y = np.array(y)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the LSTM model
    model = Sequential([
        Input(shape=(sequence_length, num_features)),
        LSTM(units=50, return_sequences=True),
        LSTM(units=50),
        Dense(units=num_features)
    ])

    model.compile(optimizer='adam', loss='mse')
    early_stopping = EarlyStopping(patience=5, restore_best_weights=True)

    # train! (with validation data)
    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_val, y_val), callbacks=[early_stopping])

    # save
    model.save(f'{loc}_model.keras')
    np.save(f'{loc}_scaler.npy', scaler)
