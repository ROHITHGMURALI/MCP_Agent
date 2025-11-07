import { OpenAPI } from 'openapi-types';
interface IrTypeRef {
    typeId: string;
    nullable?: boolean;
}
interface IrType {
    id: string;
    name: string;
    kind: 'object' | 'array' | 'string' | 'number' | 'integer' | 'boolean' | 'null' | 'union' | 'intersection' | 'enum' | 'map' | 'ref';
    description?: string;
    properties?: {
        [key: string]: IrTypeRef;
    };
    required?: string[];
    items?: IrTypeRef;
    enum?: (string | number)[];
}
interface IrOperation {
    id: string;
    name: string;
    summary?: string;
    description?: string;
    transport: 'http';
    method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' | 'OPTIONS' | 'HEAD';
    pathTemplate: string;
    tags?: string[];
    inputs: any;
    outputs: any;
}
interface Ir {
    meta: any;
    service: {
        id: string;
        title: string;
        description?: string;
        version: string;
    };
    servers?: {
        url: string;
        variables?: object;
    }[];
    types: IrType[];
    operations: IrOperation[];
}
export declare function transformOpenApiToIr(spec: OpenAPI.Document): Ir;
export {};
