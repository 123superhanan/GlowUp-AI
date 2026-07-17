import jwt from "jsonwebtoken";
import { env } from "../config/env.js";
import { logger } from "../config/logger.js";

// Main authentication middleware
export const authenticate = async (req, res, next) => {
  try {
    // 1. Get token from Authorization header
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(401).json({ error: "Access token required" });
    }

    const accessToken = authHeader.split(" ")[1];

    // 2. Verify token
    const decoded = jwt.verify(accessToken, env.accessTokenSecret);

    // 3. Attach user info to request object
    req.user = {
      id: decoded.sub,
      role: decoded.role,
      tokenVersion: decoded.tokenVersion,
    };

    next(); // Proceed to controller
  } catch (err) {
    if (err.name === "TokenExpiredError") {
      return res.status(401).json({ error: "Access token expired" });
    }
    if (err.name === "JsonWebTokenError") {
      return res.status(401).json({ error: "Invalid access token" });
    }

    logger.error("Auth middleware error:", err);
    res.status(401).json({ error: "Authentication failed" });
  }
};

// Optional: Role-based authorization
export const authorize = (...allowedRoles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: "Authentication required" });
    }

    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({
        error: "Access denied. Insufficient permissions",
      });
    }

    next();
  };
};

// Optional: Refresh token middleware (for /refresh route later)
export const verifyRefreshToken = (req, res, next) => {
  const refreshToken = req.cookies.refreshToken;

  if (!refreshToken) {
    return res.status(401).json({ error: "Refresh token required" });
  }

  try {
    const decoded = jwt.verify(refreshToken, env.refreshTokenSecret);
    req.refreshToken = refreshToken;
    req.userId = decoded.sub;
    req.tokenVersion = decoded.tokenVersion;
    next();
  } catch (err) {
    return res.status(401).json({ error: "Invalid refresh token" });
  }
};
