// POST   /api/chats
// GET    /api/chats
// GET    /api/chats/:chatId
// DELETE /api/chats/:chatId

// GET    /api/chats/:chatId/messages
// POST   /api/chats/:chatId/messages
import {
  createChat,
  deleteChat,
  getChat,
  getChats,
  getMessages,
  sendMessage,
} from "./chat.controller.js";

import express from "express";
import { authenticate } from "../../middleware/auth.middleware.js";

const router = express.Router();

router.post("/", authenticate, createChat);
router.get("/", authenticate, getChats);
router.get("/:chatId", authenticate, getChat);
router.delete("/:chatId", authenticate, deleteChat);

router.get("/:chatId/messages", authenticate, getMessages);
router.post("/:chatId/messages", authenticate, sendMessage);

export default router;
