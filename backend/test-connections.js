import { pool, query } from "./config/db.js";
import { logger } from "./config/logger.js";
import redisClient from "./config/redis.js";

async function runTests() {
  logger.info("⚡ Starting system connectivity checks...");

  try {
    // ---- Test 1: Neon DB Check ----
    logger.info("Testing Neon DB Connection...");
    const dbResult = await query("SELECT NOW()");
    logger.info(`✅ Neon DB Connected! Server time: ${dbResult.rows[0].now}`);

    // ---- Test 2: Upstash Redis Check ----
    logger.info("Testing Upstash Redis Connection...");

    // Set a temporary test value that expires in 10 seconds
    await redisClient.set("test_key", "Neon+Redis_Is_Working", { EX: 10 });
    const cachedValue = await redisClient.get("test_key");

    if (cachedValue === "Neon+Redis_Is_Working") {
      logger.info(
        `✅ Redis Connected! Successfully cached and retrieved: "${cachedValue}"`,
      );
    } else {
      throw new Error("Redis retrieved data does not match what was stored.");
    }

    logger.info("🎉 All systems are operational and connected successfully!");
  } catch (error) {
    logger.error("❌ Connectivity Test Failed!", error);
  } finally {
    // Clean up open connections so the script finishes executing in terminal
    await pool.end();
    await redisClient.disconnect();
    logger.info("Connections closed cleanly.");
  }
}

runTests();
