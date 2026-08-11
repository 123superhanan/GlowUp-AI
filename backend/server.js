import cookieParser from "cookie-parser";
import cors from "cors";
import dotenv from "dotenv";
import express from "express";

import { query } from "./config/db.js";
import { logger } from "./config/logger.js";

import authRoutes from "./routes/auth.routes.js";
// import chatRoutes from "./routes/chat.routes.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(
  cors({
    origin: true,
    credentials: true,
  }),
);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

// Routes
app.use("/api/auth", authRoutes);
// app.use("/api/chats", chatRoutes);

// Health check
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
    logger.error("Health check failed", err);

    res.status(500).json({
      status: "error",
      service: "backend",
      database: "disconnected",
    });
  }
});

// Global error handler
app.use((err, req, res, next) => {
  logger.error("Unhandled server error", err);

  res.status(500).json({
    error: "Something went wrong!",
    message: process.env.NODE_ENV === "development" ? err.message : undefined,
  });
});

app.listen(PORT, () => {
  logger.info(`Server running on http://localhost:${PORT}`);
  logger.info(`Health check: http://localhost:${PORT}/health`);
});
