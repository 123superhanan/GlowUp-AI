import "dotenv/config";

// Fail early if critical environment variables are missing
const requiredEnv = ["DATABASE_URL", "JWT_SECRET"];
for (const envName of requiredEnv) {
  if (!process.env[envName]) {
    throw new Error(` Missing required environment variable: ${envName}`);
  }
}

// Export a clean config object with clean fallback values
export const env = {
  port: parseInt(process.env.PORT || "5000", 10),
  dbUrl: process.env.DATABASE_URL,
  accessTokenSecret: process.env.ACCESS_TOKEN_SECRET,
  refreshTokenSecret: process.env.REFRESH_TOKEN_SECRET,
  nodeEnv: process.env.NODE_ENV || "development",
};
