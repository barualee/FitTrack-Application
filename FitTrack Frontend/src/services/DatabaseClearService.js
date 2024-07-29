import * as SQLite from 'expo-sqlite';

const db = SQLite.openDatabase('accelerometer.db');

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

export default clearDatabase;
