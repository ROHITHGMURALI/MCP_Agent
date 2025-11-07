"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.transformOpenApiToIr = transformOpenApiToIr;
const crypto_1 = __importDefault(require("crypto"));
// --- Utility Functions ---
function toCamelCase(str) {
    return str.replace(/[^a-zA-Z0-9]+(.)?/g, (match, chr) => chr ? chr.toUpperCase() : '').replace(/^./, str[0].toLowerCase());
}
function stableId(parts) {
    const hash = crypto_1.default.createHash('sha256');
    for (const part of parts) {
        hash.update(part || '');
    }
    return hash.digest('hex');
}
// --- Transformation Logic ---
function getSchemas(spec) {
    if ('components' in spec && spec.components && spec.components.schemas) {
        return spec.components.schemas;
    }
    if ('definitions' in spec && spec.definitions) {
        return spec.definitions;
    }
    return {};
}
function resolveRef(ref) {
    const prefix = '#/definitions/';
    const componentsPrefix = '#/components/schemas/';
    if (ref.startsWith(prefix)) {
        return ref.substring(prefix.length);
    }
    if (ref.startsWith(componentsPrefix)) {
        return ref.substring(componentsPrefix.length);
    }
    throw new Error(`Unsupported reference format: ${ref}`);
}
function transformSchemaObject(name, schema) {
    const typeId = stableId([name]);
    let kind = 'object';
    if (schema.type === 'string')
        kind = 'string';
    if (schema.type === 'integer')
        kind = 'integer';
    if (schema.type === 'number')
        kind = 'number';
    if (schema.type === 'boolean')
        kind = 'boolean';
    if (schema.type === 'array')
        kind = 'array';
    const irType = {
        id: typeId,
        name: name,
        kind: kind,
        description: schema.description,
    };
    if (schema.properties) {
        irType.properties = {};
        for (const [propName, propSchema] of Object.entries(schema.properties)) {
            if ('$ref' in propSchema) {
                const refName = resolveRef(propSchema.$ref);
                irType.properties[propName] = { typeId: stableId([refName]) };
            }
            else {
                const propSchemaTyped = propSchema;
                const inlineTypeId = stableId([name, propName, propSchemaTyped.type]);
                irType.properties[propName] = { typeId: inlineTypeId };
            }
        }
    }
    if (schema.required) {
        irType.required = schema.required;
    }
    if (schema.type === 'array' && schema.items) {
        const items = schema.items;
        if ('$ref' in items) {
            const refName = resolveRef(items.$ref);
            irType.items = { typeId: stableId([refName]) };
        }
    }
    return irType;
}
function transformOpenApiToIr(spec) {
    const schemas = getSchemas(spec);
    // --- Transform Types ---
    const types = Object.entries(schemas).map(([name, schema]) => {
        return transformSchemaObject(name, schema);
    });
    // --- Transform Operations ---
    const operations = [];
    if (spec.paths) {
        for (const [path, pathItemObject] of Object.entries(spec.paths)) {
            if (!pathItemObject)
                continue;
            for (const key of Object.keys(pathItemObject)) {
                const method = key.toUpperCase();
                if (['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'].includes(method)) {
                    const opObject = pathItemObject[key];
                    if (!opObject.operationId)
                        continue;
                    const operation = {
                        id: stableId([opObject.operationId]),
                        name: opObject.operationId,
                        summary: opObject.summary,
                        description: opObject.description,
                        transport: 'http',
                        method: method,
                        pathTemplate: path,
                        inputs: {}, // Placeholder
                        outputs: {}, // Placeholder
                    };
                    if (opObject.tags) {
                        operation.tags = opObject.tags;
                    }
                    operations.push(operation);
                }
            }
        }
    }
    // --- Construct Final IR ---
    const ir = { types, operations };
    const info = spec.info;
    ir.service = {
        id: toCamelCase(info.title),
        title: info.title,
        version: info.version,
        description: info.description,
    };
    if ('servers' in spec && spec.servers) {
        ir.servers = spec.servers.map(server => ({
            url: server.url,
            variables: server.variables,
        }));
    }
    else {
        const specV2 = spec;
        const host = specV2.host;
        const basePath = specV2.basePath;
        const schemes = specV2.schemes || ['http'];
        if (host) {
            ir.servers = schemes.map((scheme) => ({
                url: `${scheme}://${host}${basePath || ''}`
            }));
        }
    }
    return ir;
}
