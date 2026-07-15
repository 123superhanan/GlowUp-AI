import { createClient } from "redis";
import { logger } from "./logger.js";

// Initialize  Redis client
const redisClient = createClient({
  url: process.env.REDIS_URL || "redis://localhost:6379",
});

// Setup event listeners for monitoring connection health
redisClient.on("connect", () => logger.info("Connecting to Redis..."));
redisClient.on("ready", () =>
  logger.info(" Redis client connected and ready!"),
);
redisClient.on("error", (err) => logger.error(" Redis Client Error", err));

await redisClient.connect();

export default redisClient;
