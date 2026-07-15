// Simple, clean logger wrapper. (Can be upgraded later to use 'winston' or 'pino')
export const logger = {
  info: (message, meta = "") => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [INFO]: ${message}`, meta);
  },
  error: (message, error = "") => {
    const timestamp = new Date().toISOString();
    console.error(`[${timestamp}] [ERROR]: ${message}`, error?.stack || error);
  },
  warn: (message, meta = "") => {
    const timestamp = new Date().toISOString();
    console.warn(`[${timestamp}] [WARN]: ${message}`, meta);
  },
};
