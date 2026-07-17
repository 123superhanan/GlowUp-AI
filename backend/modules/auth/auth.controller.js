import bcrypt from "bcrypt";
import crypto from "crypto";
import jwt from "jsonwebtoken";
import { pool, query } from "../../config/db.js";
import { env } from "../../config/env.js";
import { logger } from "../../config/logger.js";
import { loginSchema, registerSchema } from "./auth.validation.js";

// Helper function to hash a token string via SHA-256
const hashToken = (token) => {
  return crypto.createHash("sha256").update(token).digest("hex");
};

// 1. REGISTRATION WITH TRANSACTION SAFETY
export const registerUser = async (req, res) => {
  // Parse and validate incoming structure using Zod
  const validation = registerSchema.safeParse(req.body);
  if (!validation.success) {
    return res.status(400).json({ errors: validation.error.format() });
  }

  const { name, email, password, gender, avatar } = validation.data;

  // Acquire an isolated pool client to safely handle the multi-step transaction blocks
  const client = await pool.connect();

  try {
    await client.query("BEGIN");

    // Email availability check
    const userCheck = await client.query(
      "SELECT id FROM users WHERE email = $1",
      [email],
    );
    if (userCheck.rows.length > 0) {
      await client.query("ROLLBACK");
      return res.status(409).json({ error: "Email is already registered" });
    }

    const hashedPassword = await bcrypt.hash(password, 12);

    // Main insertion
    const newUserResult = await client.query(
      `INSERT INTO users (name, email, password, gender, avatar)   
   VALUES ($1, $2, $3, $4, $5) RETURNING id, name, email, role, created_at`,
      [name, email, hashedPassword, gender || null, avatar || null],
    );

    const user = newUserResult.rows[0];

    /*   
  NOTE: If you scale up with supplementary profiles or settings tables later:  
  await client.query("INSERT INTO profiles (user_id) VALUES ($1)", [user.id]);  
*/

    await client.query("COMMIT");
    logger.info(`Transaction successful: User registered (${email})`);

    res.status(201).json({
      message: "User registered successfully",
      user,
    });
  } catch (err) {
    await client.query("ROLLBACK");
    logger.error("Registration transaction rolled back due to error:", err);
    res.status(500).json({ error: "Internal server error" });
  } finally {
    client.release();
  }
};

// 2. LOGIN WITH SECURE COOKIES & TOKEN HASHING
export const loginUser = async (req, res) => {
  const validation = loginSchema.safeParse(req.body);
  if (!validation.success) {
    return res.status(400).json({ errors: validation.error.format() });
  }

  const { email, password } = validation.data;

  try {
    const userResult = await query("SELECT * FROM users WHERE email = $1", [
      email,
    ]);
    if (userResult.rows.length === 0) {
      return res.status(401).json({ error: "Invalid email or password" });
    }

    const user = userResult.rows[0];

    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({ error: "Invalid email or password" });
    }

    // Generate tokens with standardized claims and distinct signing secrets
    const accessToken = jwt.sign(
      { sub: user.id, role: user.role, tokenVersion: user.token_version },
      env.accessTokenSecret,
      { expiresIn: "15m" },
    );

    const refreshToken = jwt.sign(
      { sub: user.id, tokenVersion: user.token_version },
      env.refreshTokenSecret,
      { expiresIn: "7d" },
    );

    // Cryptographically obscure token before saving to Neon DB
    const tokenHash = hashToken(refreshToken);
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 7);

    // Capture requester analytics data
    const ipAddress = req.ip || req.headers["x-forwarded-for"] || "127.0.0.1";
    const userAgent = req.headers["user-agent"] || "unknown";

    await query(
      `INSERT INTO refresh_tokens (user_id, token_hash, ip_address, user_agent, expires_at)   
   VALUES ($1, $2, $3, $4, $5)`,
      [user.id, tokenHash, ipAddress, userAgent, expiresAt],
    );

    logger.info(
      `Session created: User ${user.email} logged in from IP ${ipAddress}`,
    );

    // Deliver long-lived refresh token via strict httpOnly cookie mechanism
    res.cookie("refreshToken", refreshToken, {
      httpOnly: true,
      secure: env.nodeEnv === "production", // strict secure flag matching environment state
      sameSite: "strict",
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days matching token lifespan
    });

    // Return access token and clean payload to front-end app state
    res.json({
      accessToken,
      user: {
        id: user.id,
        name: user.name,
        email: user.email,
        role: user.role,
        avatar: user.avatar,
        createdAt: user.created_at,
      },
    });
  } catch (err) {
    logger.error("Login route failure:", err);
    res.status(500).json({ error: "Internal server error" });
  }
};

// Logout - Single Device
// Logout - Single Device
export const logoutUser = async (req, res) => {
  try {
    const refreshToken = req.cookies.refreshToken;

    console.log("Logout attempt - Refresh Token exists:", !!refreshToken);

    if (refreshToken) {
      const tokenHash = hashToken(refreshToken);

      const result = await query(
        `DELETE FROM refresh_tokens WHERE token_hash = $1`,
        [tokenHash],
      );

      console.log("Deleted refresh tokens:", result.rowCount);
    }

    // Clear cookie
    res.clearCookie("refreshToken", {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
    });

    res.json({ message: "Logged out successfully" });
  } catch (err) {
    logger.error("Logout error details:", err);
    console.error("Full logout error:", err);
    res.status(500).json({
      error: "Logout failed",
      message: err.message,
    });
  }
};

// Logout from all devices
export const logoutAllDevices = async (req, res) => {
  try {
    const userId = req.user?.id;

    if (!userId) {
      return res.status(401).json({ error: "Authentication required" });
    }

    // Delete all refresh tokens for this user
    await query(`DELETE FROM refresh_tokens WHERE user_id = $1`, [userId]);

    // Increment token version to invalidate all existing access tokens
    await query(
      `UPDATE users SET token_version = token_version + 1 WHERE id = $1`,
      [userId],
    );

    res.clearCookie("refreshToken", {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
    });

    res.json({ message: "Logged out from all devices successfully" });
  } catch (err) {
    logger.error("Logout all devices error:", err);
    res.status(500).json({ error: "Logout failed" });
  }
};
