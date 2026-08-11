// createChat()
// getChats()
// getChat()
// deleteChat()
// sendMessage()
// getMessages()

// Request
//    ↓
// Controller
//    ↓
// Validate
//    ↓
// Database / Redis
//    ↓
// AI service
//    ↓
// Response

import { query } from "../../config/db.js";
import { logger } from "../../config/logger.js";
import { createChatSchema } from "./chat.validation.js";

export const createChat = async (req, res) => {
  const validation = createChatSchema.safeParse(req.body);
  if (!validation.success) {
    return res.status(400).json({ errors: validation.error.format() });
  }

  const { title } = validation.data;
  const userId = req.user.id;

  try {
    const result = await query(
      `INSERT INTO chats (user_id, title) VALUES ($1, $2) RETURNING id, title, created_at`,
      [userId, title || null],
    );

    logger.info(`Chat created: ${result.rows[0].id}`);

    return res.status(201).json({
      chat: result.rows[0],
    });
  } catch (err) {
    logger.error("Create chat error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
};

export const getChats = async (req, res) => {
  const userId = req.user.id;

  try {
    const result = await query(
      `SELECT id, title, created_at, updated_at
       FROM chats
       WHERE user_id = $1
       ORDER BY updated_at DESC`,
      [userId],
    );

    return res.status(200).json({
      chats: result.rows,
    });
  } catch (err) {
    logger.error("Get chats error:", err);

    return res.status(500).json({
      error: "Internal server error",
    });
  }
};

export const getChat = async (req, res) => {
  const userId = req.user.id;
  const chatId = req.params.chatId;

  try {
    const result = await query(
      `SELECT id, title, created_at, updated_at
       FROM chats
       WHERE id = $1 AND user_id = $2`,
      [chatId, userId],
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: "Chat not found" });
    }

    return res.status(200).json({
      chat: result.rows[0],
    });
  } catch (err) {
    logger.error("Get chat error:", err);

    return res.status(500).json({
      error: "Internal server error",
    });
  }
};
// ==================== DELETE CHAT ====================

export const deleteChat = async (req, res) => {
  const validation = chatIdSchema.safeParse(req.params);

  if (!validation.success) {
    return res.status(400).json({
      errors: validation.error.format(),
    });
  }

  const chatId = validation.data.chatId;
  const userId = req.user.id;

  try {
    const result = await query(
      `DELETE FROM chats
       WHERE id = $1 AND user_id = $2
       RETURNING id`,
      [chatId, userId],
    );

    if (result.rows.length === 0) {
      return res.status(404).json({
        error: "Chat not found",
      });
    }

    logger.info(`Chat deleted: ${chatId}`);

    return res.status(200).json({
      message: "Chat deleted successfully",
    });
  } catch (err) {
    logger.error("Delete chat error:", err);

    return res.status(500).json({
      error: "Internal server error",
    });
  }
};

// ==================== GET MESSAGES ====================

export const getMessages = async (req, res) => {
  const validation = chatIdSchema.safeParse(req.params);

  if (!validation.success) {
    return res.status(400).json({
      errors: validation.error.format(),
    });
  }

  const chatId = validation.data.chatId;
  const userId = req.user.id;

  try {
    // Make sure the chat belongs to this user
    const chatResult = await query(
      `SELECT id
       FROM chats
       WHERE id = $1 AND user_id = $2`,
      [chatId, userId],
    );

    if (chatResult.rows.length === 0) {
      return res.status(404).json({
        error: "Chat not found",
      });
    }

    const result = await query(
      `SELECT id, role, content, created_at
       FROM messages
       WHERE chat_id = $1
       ORDER BY created_at ASC`,
      [chatId],
    );

    return res.status(200).json({
      messages: result.rows,
    });
  } catch (err) {
    logger.error("Get messages error:", err);

    return res.status(500).json({
      error: "Internal server error",
    });
  }
};

// ==================== SEND MESSAGE ====================

export const sendMessage = async (req, res) => {
  const chatValidation = chatIdSchema.safeParse(req.params);

  if (!chatValidation.success) {
    return res.status(400).json({
      errors: chatValidation.error.format(),
    });
  }

  const messageValidation = sendMessageSchema.safeParse(req.body);

  if (!messageValidation.success) {
    return res.status(400).json({
      errors: messageValidation.error.format(),
    });
  }

  const chatId = chatValidation.data.chatId;
  const userId = req.user.id;
  const { content } = messageValidation.data;

  try {
    // Check chat ownership
    const chatResult = await query(
      `SELECT id
       FROM chats
       WHERE id = $1 AND user_id = $2`,
      [chatId, userId],
    );

    if (chatResult.rows.length === 0) {
      return res.status(404).json({
        error: "Chat not found",
      });
    }

    // Save user message
    const result = await query(
      `INSERT INTO messages (chat_id, role, content)
       VALUES ($1, $2, $3)
       RETURNING id, chat_id, role, content, created_at`,
      [chatId, "user", content],
    );

    // Update chat timestamp
    await query(
      `UPDATE chats
       SET updated_at = CURRENT_TIMESTAMP
       WHERE id = $1`,
      [chatId],
    );

    logger.info(`Message created in chat: ${chatId}`);

    return res.status(201).json({
      message: result.rows[0],
    });
  } catch (err) {
    logger.error("Send message error:", err);

    return res.status(500).json({
      error: "Internal server error",
    });
  }
};
