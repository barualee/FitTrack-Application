// DatabaseService.js
import * as SQLite from 'expo-sqlite';

const db = SQLite.openDatabase('accelerometer.db');

const initDatabase = () => {
  db.transaction((tx) => {
    tx.executeSql(
      'CREATE TABLE IF NOT EXISTS accelerometer_data (id INTEGER PRIMARY KEY AUTOINCREMENT, x REAL, y REAL, z REAL, timestamp INTEGER);',
      [],
      () => console.log('Database initialized'),
      (_, error) => console.error('Error initializing database', error)
    );
  });
};

const insertData = (data) => {
  
  const { x, y, z, timestamp =Date.now() } = data;
  db.transaction(tx => {
    tx.executeSql(
      'INSERT INTO accelerometer_data (x, y, z, timestamp) VALUES (?, ?, ?, ?)',
      [x, y, z, timestamp],
      (_, { rowsAffected }) => {
        console.log(`Inserted ${rowsAffected} rows`);
      },
      (_, error) => {
        console.error('Error inserting data:', error);
      }
    );
  });
};

const queryDataFromDatabase = () => {
  return new Promise((resolve, reject) => {
    db.transaction(tx => {
      tx.executeSql(
        'SELECT * FROM accelerometer_data;',
        [],
        (_, { rows }) => resolve(rows._array), // Resolve with the retrieved data
        (_, error) => reject(error) // Reject with the error if any
      );
    });
  });
};

const clearDatabase = () => {
  db.transaction((tx) => {
    tx.executeSql(
      'DELETE FROM accelerometer_data;',
      [],
      () => {
        console.log('Database cleared successfully');
        // You can also add additional logic here if needed
      },
      (_, error) => console.error('Error clearing database', error)
    );
  });
};

export { initDatabase, insertData, queryDataFromDatabase,clearDatabase };
