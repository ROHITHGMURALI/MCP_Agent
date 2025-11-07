"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseOpenApiSpec = parseOpenApiSpec;
const swagger_parser_1 = __importDefault(require("@apidevtools/swagger-parser"));
async function parseOpenApiSpec(filePath) {
    try {
        const api = await swagger_parser_1.default.validate(filePath);
        return api;
    }
    catch (err) {
        console.error(`Error parsing OpenAPI spec: ${err}`);
        throw err;
    }
}
