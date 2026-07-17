import { query } from "./config/db.js";

async function initializeDatabase() {
  console.log(" Initializing Database...");

  // ==================== USERS TABLE ====================
  const createUsersTable = `
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      email VARCHAR(255) UNIQUE NOT NULL,
      password VARCHAR(255) NOT NULL,
      role VARCHAR(50) DEFAULT 'user',
      avatar TEXT,
      gender VARCHAR(50),
      token_version INT DEFAULT 1,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `;

  // ==================== REFRESH TOKENS TABLE ====================
  const createRefreshTokensTable = `
    CREATE TABLE IF NOT EXISTS refresh_tokens (
      id SERIAL PRIMARY KEY,
      user_id INT REFERENCES users(id) ON DELETE CASCADE,
      token_hash TEXT UNIQUE NOT NULL,
      ip_address VARCHAR(50),
      user_agent TEXT,
      expires_at TIMESTAMP NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `;

  // ==================== PREDICTION HISTORY TABLE ====================
  const createPredictionHistoryTable = `
    CREATE TABLE IF NOT EXISTS prediction_history (
      id SERIAL PRIMARY KEY,
      user_id INT REFERENCES users(id) ON DELETE CASCADE,
      skin_tone VARCHAR(100),
      face_shape VARCHAR(100),
      body_type VARCHAR(100),
      skin_condition TEXT,
      recommendation TEXT,
      image_url TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `;

  // ==================== NOTIFICATIONS TABLE ====================
  const createNotificationsTable = `
    CREATE TABLE IF NOT EXISTS notifications (
      id SERIAL PRIMARY KEY,
      user_id INT REFERENCES users(id) ON DELETE CASCADE,
      title VARCHAR(255) NOT NULL,
      message TEXT NOT NULL,
      is_read BOOLEAN DEFAULT FALSE,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `;

  try {
    await query(createUsersTable);
    console.log(" 'users' table ready.");

    await query(createRefreshTokensTable);
    console.log(" 'refresh_tokens' table ready.");

    await query(createPredictionHistoryTable);
    console.log(" 'prediction_history' table ready.");

    await query(createNotificationsTable);
    console.log(" 'notifications' table ready.");

    console.log(" All database tables initialized successfully!");
  } catch (err) {
    console.error(" Error initializing database:", err);
  }
}

initializeDatabase();
