const localUser = process.env.DB_USERNAME;
const localPassword = process.env.DB_PASSWORD;
const localDb = process.env.DB_NAME;

db = db.getSiblingDB(localDb); // Переключение на указанную базу данных
db.createUser({
  user: localUser,
  pwd: localPassword,
  roles: [
    { role: "readWrite", db: localDb } // Назначаем права readWrite для базы данных
  ]
});