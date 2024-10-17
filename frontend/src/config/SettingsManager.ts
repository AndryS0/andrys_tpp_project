import dotenv from 'dotenv';
import Joi from 'joi';  // Optional: Use Joi for validation

// Load environment variables from .env file
dotenv.config();

class SettingsManager {
    private readonly config: { backendUrl: string | null; someApiKey: string | null };
    constructor() {
        // Initialize all required settings here
        this.config = {
            backendUrl: process.env.REACT_APP_BACKEND_URL || null,
            someApiKey: process.env.REACT_APP_API_KEY || null,
        };

        // Validate the configuration to ensure everything is properly set
        this.validateConfig();
    }

    // Function to validate the configuration using Joi (optional but recommended)
    validateConfig() {
        const schema = Joi.object({
            backendUrl: Joi.string().uri().required().messages({
                'string.base': `"REACT_APP_BACKEND_URL" must be a string`,
                'string.uri': `"REACT_APP_BACKEND_URL" must be a valid URL`,
                'any.required': `"REACT_APP_BACKEND_URL" is required`,
            }),
            someApiKey: Joi.string().min(10).required().messages({
                'string.base': `"REACT_APP_API_KEY" must be a string`,
                'string.min': `"REACT_APP_API_KEY" must be at least 10 characters`,
                'any.required': `"REACT_APP_API_KEY" is required`,
            }),
        });

        const { error } = schema.validate(this.config, { abortEarly: false });
        if (error) {
            throw new Error(`Environment configuration error: ${error.message}`);
        }
    }

    // Getter methods to safely access the environment variables
    get backendUrl() {
        return this.config.backendUrl;
    }

    get someApiKey() {
        return this.config.someApiKey;
    }
}

export default new SettingsManager();  // Singleton pattern for easy access
