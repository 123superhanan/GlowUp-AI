import express from "express";
import { loginUser, registerUser } from "../modules/auth/auth.controller.js";
// Import middleware (we'll use it later)

const router = express.Router();

// ====================== PUBLIC ROUTES ======================
router.post("/register", registerUser);
router.post("/login", loginUser);

// ====================== PROTECTED ROUTES (Example) ======================
// router.get("/profile", authenticate, getProfile);
// router.put("/profile", authenticate, updateProfile);

// ====================== FUTURE ENDPOINTS ======================
/*
router.post("/refresh", refreshSessionTokens);
router.post("/logout", logoutUser);
router.post("/logout-all", logoutAllDevices);
*/

export default router;
