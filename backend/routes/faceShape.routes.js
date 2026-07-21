import { Router } from "express";
import multer from "multer";
import { authenticate } from "../middleware/auth.js";
import { predictFaceShape } from "../modules/prediction/prediction.controller.js";

const router = Router();
const upload = multer({ storage: multer.memoryStorage() });

router.post("/predict", authenticate, upload.single("image"), predictFaceShape);

export default router;
