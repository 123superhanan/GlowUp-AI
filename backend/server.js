import cors from "cors";
import dotenv from "dotenv";
import express from "express";
import { query } from "./config/db.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

//  health check to verify active database connectivity
app.get("/health", async (req, res) => {
  try {
    // basic query to check the DB connection
    const dbCheck = await query("SELECT NOW()");

    res.json({
      status: "ok",
      service: "backend",
      database: "connected",
      timestamp: dbCheck.rows[0].now,
    });
  } catch (err) {
    res.status(500).json({
      status: "error",
      service: "backend",
      database: "disconnected",
      error: err.message,
    });
  }
});

app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
