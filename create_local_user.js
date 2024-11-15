const localUser = process.env.DB_USERNAME;
const localPassword = process.env.DB_PASSWORD;
const localDb = process.env.DB_NAME;

db = db.getSiblingDB(localDb);
db.createUser({
  user: localUser,
  pwd: localPassword,
  roles: [
    { role: "readWrite", db: localDb }
  ]
});

db.users.insertOne({
  username: "User",
  hashed_password: "$2b$12$gTYpwFTkagvbEq69VpJ.6OOEqPM/P0Mazt3rrNtq5m3SipJgE92WO"
});