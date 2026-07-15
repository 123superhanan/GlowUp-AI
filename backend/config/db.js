import { Pool } from "@neondatabase/serverless";
import { env } from "./env.js";

export const pool = new Pool({
  connectionString: env.dbUrl,
});

export const query = (text, params) => pool.query(text, params);
