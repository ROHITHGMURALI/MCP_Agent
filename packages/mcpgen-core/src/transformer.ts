import { OpenAPI, OpenAPIV2 } from 'openapi-types';

// A simplified IR for now.
interface Ir {
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
}

function toCamelCase(str: string): string {
    return str.replace(/[^a-zA-Z0-9]+(.)?/g, (match, chr) => chr ? chr.toUpperCase() : '').replace(/^./, str[0].toLowerCase());
}

export function transformOpenApiToIr(spec: OpenAPI.Document): Ir {
  const ir: Partial<Ir> = {};

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
  } else {
    const specV2 = spec as OpenAPIV2.Document;
    const host = specV2.host;
    const basePath = specV2.basePath;
    const schemes = specV2.schemes || ['http'];
    if (host) {
      ir.servers = schemes.map((scheme: string) => ({
        url: `${scheme}://${host}${basePath || ''}`
      }));
    }
  }

  return ir as Ir;
}
