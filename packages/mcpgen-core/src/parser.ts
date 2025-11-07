import SwaggerParser from "@apidevtools/swagger-parser";
import { OpenAPI } from "openapi-types";

export async function parseOpenApiSpec(filePath: string): Promise<OpenAPI.Document> {
  try {
    const api = await SwaggerParser.validate(filePath);
    return api as OpenAPI.Document;
  } catch (err) {
    console.error(`Error parsing OpenAPI spec: ${err}`);
    throw err;
  }
}
