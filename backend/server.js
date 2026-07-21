import cors from "cors";
import dotenv from "dotenv";
import express from "express";

import cookieParser from "cookie-parser";
import { query } from "./config/db.js";
import authRoutes from "./routes/auth.routes.js";
import predictRoute from "./routes/faceShape.routes.js";
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// ====================== MIDDLEWARE ======================
app.use(
  cors({
    origin: true, // Allow all origins for now (change in production)
    credentials: true, // Important for cookies (refresh token)
  }),
);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

// ====================== ROUTES ======================
app.use("/api/auth", authRoutes);
app.use("/api/predict", predictRoute);

// Health Check Route
app.get("/health", async (req, res) => {
  try {
    const dbCheck = await query("SELECT NOW()");

    res.json({
      status: "ok",
      service: "backend",
      database: "connected",
      timestamp: dbCheck.rows[0].now,
      environment: process.env.NODE_ENV || "development",
    });
  } catch (err) {
    console.error("Health check failed:", err.message);
    res.status(500).json({
      status: "error",
      service: "backend",
      database: "disconnected",
      error: err.message,
    });
  }
});

// Global Error Handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: "Something went wrong!",
    message: process.env.NODE_ENV === "development" ? err.message : undefined,
  });
});

// ====================== START SERVER ======================
app.listen(PORT, () => {
  console.log(` Server running on http://localhost:${PORT}`);
  console.log(` Health check: http://localhost:${PORT}/health`);
});
