import axios from "axios";
import FormData from "form-data";
import { pool } from "../../config/db.js";
import { aiService } from "../../services/ai.service.js";

export const predictFaceShape = async (req, res) => {
  try {
    if (!req.file) {
      return res
        .status(400)
        .json({ success: false, message: "No image file uploaded" });
    }

    const userId = req.user.id;

    // Forward image file stream to FastAPI for computer vision inference
    const form = new FormData();
    form.append("file", req.file.buffer, {
      filename: req.file.originalname,
      contentType: req.file.mimetype,
    });

    const fastapiResponse = await axios.post(
      "http://localhost:8000/face-shape/predict",
      form,
      {
        headers: { ...form.getHeaders() },
      },
    );

    const { success, prediction } = fastapiResponse.data;
    if (!success) {
      return res
        .status(400)
        .json({ success: false, message: "FastAPI prediction failed" });
    }

    const faceShape =
      typeof prediction === "object" ? prediction.class || "Oval" : prediction;

    //  NEW: Call your fresh AI service to fetch RAG LLM data!
    const recommendation =
      await aiService.getFaceShapeRecommendations(faceShape);

    const skinTone = null;
    const bodyType = null;
    const skinCondition = null;
    const imageUrl = `/uploads/${Date.now()}_${req.file.originalname}`;

    // Store tracking data securely inside PostgreSQL table
    const insertQuery = `
      INSERT INTO prediction_history (
        user_id, skin_tone, face_shape, body_type, skin_condition, recommendation, image_url
      ) VALUES ($1, $2, $3, $4, $5, $6, $7)
      RETURNING *;
    `;

    const values = [
      userId,
      skinTone,
      faceShape,
      bodyType,
      skinCondition,
      recommendation,
      imageUrl,
    ];
    const dbResult = await pool.query(insertQuery, values);

    return res.status(200).json({
      success: true,
      message: "Prediction processed and stored securely",
      data: dbResult.rows[0], // Return the single row instead of the array wrapper
    });
  } catch (error) {
    return res.status(500).json({
      success: false,
      message: "Internal Server Error in secure node gateway",
      error: error.message,
    });
  }
};
