// POST /api/chats
//         ↓
// createChatSchema

// POST /api/chats/:chatId/messages
//         ↓
// sendMessageSchema + chatIdSchema

import { z } from "zod";

export const createChatSchema = z.object({
  title: z
    .string()
    .trim()
    .min(1, "Chat title is required")
    .max(100, "Chat title must be 100 characters or less")
    .optional(),
});

export const sendMessageSchema = z.object({
  content: z
    .string()
    .trim()
    .min(1, "Message cannot be empty")
    .max(5000, "Message is too long"),
});

export const chatIdSchema = z.object({
  chatId: z.string().regex(/^\d+$/, "Invalid chat ID"),
});
