import axios from "axios";
import { logger } from "../config/logger.js"; // Adapts to your existing logger layout

class AIService {
  constructor() {
    // Falls back to localhost if the environ
    // ment variable is missing
    this.fastApiBaseUrl = process.env.AI_SERVICE_URL || "http://localhost:8000";
  }

  /**
   * Contacts the FastAPI RAG engine to query local LLM recommendations
   * @param {string} faceShape - Clean string label (e.g., "Oval", "Square")
   * @returns {Promise<string>} Markdown text or string containing AI recommendations
   */
  async getFaceShapeRecommendations(faceShape) {
    try {
      // 1. Send the clean label to your FastAPI RAG router configuration
      // Adjust the URL endpoint if your Python RAG endpoint maps differently
      const response = await axios.post(
        `${this.fastApiBaseUrl}/face-shape/recommend`,
        {
          face_shape: faceShape,
          model_name: "llama3.2:3b", // Matches your exact Python comment configuration
          top_k: 2,
        },
      );

      // 2. Return data safely if the engine responds correctly
      if (response.data && response.data.success) {
        return response.data.recommendations;
      }

      throw new Error("RAG payload returned success: false");
    } catch (error) {
      // 3. Centralized error tracking using your system logger
      logger.error(`AI Service RAG Connection Failure: ${error.message}`);

      // 4. Graceful Fallback: Return structured generic advice so your database write doesn't break
      return `Standard dynamic profile matches a ${faceShape} classification profile. Keep clean geometric frames or balances according to proportions.`;
    }
  }
}

export const aiService = new AIService();
