import express from "express";

// Import Controllers
import {
  loginUser,
  logoutAllDevices,
  logoutUser,
  registerUser,
} from "../modules/auth/auth.controller.js";

// Import Middleware
import { authenticate } from "../middleware/auth.js";

const router = express.Router();

// ====================== PUBLIC ROUTES ======================
router.post("/register", registerUser);
router.post("/login", loginUser);

// ====================== PROTECTED ROUTES ======================
router.post("/logout", authenticate, logoutUser); // Logout current session
router.post("/logout-all", authenticate, logoutAllDevices); // Logout from all devices

// Example of future protected routes:
// router.get("/profile", authenticate, getProfile);
// router.put("/profile", authenticate, updateProfile);

export default router;
